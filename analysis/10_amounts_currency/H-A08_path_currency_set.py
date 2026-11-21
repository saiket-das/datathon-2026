"""Explore whether payment currency belongs to a visible-path country mode.

Run: uv run python analysis/10_amounts_currency/H-A08_path_currency_set.py
Both-account bit-0 development only; no confirmation outcomes or identities exported.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys
import subprocess

import duckdb
import numpy as np

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("currency_endpoint", HERE / "H-A06_currency_endpoint.py")
endpoint = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(endpoint)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', choices=['explore','validate'], default='explore')
    parser.add_argument('--freeze')
    args = parser.parse_args()
    if args.phase == 'explore' and datetime.now(timezone.utc) >= datetime(2026,11,18,12,tzinfo=timezone.utc):
        return 1
    try:
        if args.phase == 'validate':
            if not args.freeze:
                raise ValueError('Freeze required')
            root = HERE.parents[1]
            subprocess.run(['git','merge-base','--is-ancestor',args.freeze,'HEAD'],cwd=root,check=True,capture_output=True)
            for path in [Path(__file__).resolve(),Path(endpoint.__file__),Path(endpoint.foundation.__file__)]:
                frozen = subprocess.check_output(['git','show',f'{args.freeze}:{path.relative_to(root).as_posix()}'],cwd=root)
                if frozen.replace(b'\r\n',b'\n') != path.read_bytes().replace(b'\r\n',b'\n'):
                    raise ValueError('Frozen source mismatch')
        with duckdb.connect() as con:
            con.execute("SET memory_limit='512MB'; SET threads=1; SET temp_directory=''; SET preserve_insertion_order=false")
            split=endpoint.foundation.partition_sql("accounts")
            source = f"""SELECT
                CURRENCY_CODE currency,ORDERING_ACCOUNT sender,BENEFICIARY_ACCOUNT receiver,ORDERING_BIC8 bank,
                TRANSACTION_TYPE_CODE route,gap_count>0 has_gap,
                list_transform(list_filter(string_split(BIC8_PATH,';'),lambda x:x<>'...'),
                               lambda b:substr(b,5,2)) countries,
                ts_utc < TIMESTAMP '2023-07-01' training
                FROM read_parquet('dataset/payments.parquet')
                WHERE ANOMALY_TYPE IS NULL AND {split}='explore'"""
            con.execute(f'CREATE VIEW scope AS {source}')
            con.execute("""CREATE TEMP TABLE country_mode AS
                WITH modes AS (
                    SELECT countries[1] country,currency FROM scope WHERE training
                    GROUP BY countries[1],currency
                    QUALIFY sum(count(*)) OVER(PARTITION BY countries[1])>=100
                    AND row_number() OVER(PARTITION BY countries[1]
                        ORDER BY count(*) DESC,currency)=1
                )
                SELECT country,currency,
                    list(currency ORDER BY country) OVER()[
                        1 + ((row_number() OVER(ORDER BY country)-1+7) % count(*) OVER())
                    ] wrong_currency
                FROM modes""")
            con.execute("""CREATE TEMP TABLE frequency AS
                SELECT map(list(currency),list(p)) mass FROM (
                    SELECT currency,count(*)/sum(count(*)) OVER() p
                    FROM scope WHERE training GROUP BY currency
                ) frequencies""")
            con.execute("""CREATE TEMP TABLE modes AS SELECT
                map(list(country),list(currency)) actual,
                map(list(country),list(coalesce(wrong_currency,currency))) wrong
                FROM country_mode""")
            evaluation = source.replace("='explore'", "='confirm'") if args.phase == 'validate' else source
            con.execute(f'CREATE VIEW evaluation AS {evaluation}')
            con.execute("""CREATE VIEW predictions AS
                WITH mapped AS (
                    SELECT s.*,list_transform(countries,lambda c:actual[c]) choices,
                        list_transform(countries,lambda c:wrong[c]) wrong_choices
                    FROM evaluation s CROSS JOIN modes WHERE NOT training
                )
                SELECT *,not list_contains(list_transform(choices,lambda x:x IS NULL),true) eligible,
                    list_sum(list_transform(list_distinct(choices),lambda x:mass[x])) union_frequency
                FROM mapped CROSS JOIN frequency""")
            result=con.execute("""SELECT count(*) scoped,
                count(*) FILTER(WHERE eligible) eligible,
                count(DISTINCT sender) FILTER(WHERE eligible) senders,
                count(DISTINCT receiver) FILTER(WHERE eligible) receivers
                FROM predictions""")
            coverage=([c[0] for c in result.description],result.fetchall())
            result=con.execute("""SELECT
                CASE WHEN grouping(route)=1 THEN 'All' ELSE route END route,
                CASE WHEN grouping(k)=1 THEN 'All' ELSE k::VARCHAR END visible_banks,
                'All' distinct_currencies,
                CASE WHEN grouping(has_gap)=1 THEN 'All' ELSE has_gap::VARCHAR END gap,
                count(*) n,count(DISTINCT sender) senders,count(DISTINCT receiver) receivers,
                round(avg((currency=choices[1])::INT),6) first_share,
                round(avg((currency=choices[-1])::INT),6) last_share,
                round(avg((currency=choices[1] OR currency=choices[-1])::INT),6) endpoint_share,
                round(avg(list_contains(choices,currency)::INT),6) path_share,
                round(avg(list_contains(wrong_choices,currency)::INT),6) wrong_path_share,
                round(avg(union_frequency),6) union_frequency_baseline,
                CASE WHEN count(*) FILTER(WHERE NOT list_contains(choices,currency)) BETWEEN 1 AND 99
                     THEN '<100' ELSE count(*) FILTER(WHERE NOT list_contains(choices,currency))::VARCHAR END unexplained
                FROM (
                    SELECT *,least(len(countries),5) k,least(list_unique(choices),4) cardinality
                    FROM predictions WHERE eligible
                ) subset
                GROUP BY GROUPING SETS ((),(route,k),(has_gap))
                HAVING count(*)>=1000 AND count(DISTINCT sender)>=100
                    AND count(DISTINCT receiver)>=100
                ORDER BY route,visible_banks,distinct_currencies,gap""")
            score=([c[0] for c in result.description],result.fetchall())
            result=con.execute("""SELECT least(list_unique(choices),4) distinct_currencies,
                count(*) n,count(DISTINCT sender) senders,count(DISTINCT receiver) receivers,
                round(avg(list_contains(choices,currency)::INT),6) path_share,
                round(avg(list_contains(wrong_choices,currency)::INT),6) wrong_path_share,
                round(avg(union_frequency),6) union_frequency_baseline
                FROM predictions WHERE eligible GROUP BY 1
                HAVING count(*)>=1000 AND count(DISTINCT sender)>=100
                    AND count(DISTINCT receiver)>=100 ORDER BY 1""")
            cardinality=([c[0] for c in result.description],result.fetchall())
            result = con.execute("""SELECT bank,count(*) n,
                sum(list_contains(choices,currency)::INT) matches,
                sum(list_contains(choices,currency)::INT-union_frequency) lift_frequency,
                sum(list_contains(choices,currency)::INT-list_contains(wrong_choices,currency)::INT) lift_wrong,
                count(*) FILTER(WHERE len(countries)>2) multibank,
                sum(CASE WHEN len(countries)>2 THEN list_contains(choices,currency)::INT
                    -(currency=choices[1] OR currency=choices[-1])::INT ELSE 0 END) lift_endpoint
                FROM predictions WHERE eligible GROUP BY bank ORDER BY bank""")
            stats = np.asarray([row[1:] for row in result.fetchall()],dtype=float)
            rng = np.random.default_rng(20261116)
            samples = []
            for _ in range(1000):
                total = stats[rng.integers(0,len(stats),len(stats))].sum(axis=0)
                samples.append([total[1]/total[0],total[2]/total[0],total[3]/total[0],total[5]/total[4]])
            intervals = np.quantile(samples,[.005,.995],axis=0)
            labels = ['membership','lift vs union frequency','lift vs shifted map','multibank lift vs endpoints']
            uncertainty = (['statistic','low99','high99'],[(label,*intervals[:,i]) for i,label in enumerate(labels)])
            cov = coverage[1][0]
            passed = cov[1]/cov[0]>=.98 and min(cov[2:])>=100 and len(stats)>=100 and bool(np.all(intervals[0]>=[.98,.50,.50,.02]))
            shared_banks = con.execute("""SELECT count(DISTINCT bank)
                FROM predictions WHERE eligible AND bank IN (
                    SELECT DISTINCT bank FROM scope WHERE training
                )""").fetchone()[0]
            decision = (['all_criteria_met','ordering_banks','shared_training_ordering_banks'],[(passed,len(stats),shared_banks)])
        lines=["# H-A08: Currency membership in visible path-country modes","",
            f"Phase {args.phase}; freeze {args.freeze or 'not frozen'}. Pre-July bit-0 country modes score July.",
            "Only paths with all country modes supported enter membership comparisons.",
            "The wrong map circularly shifts seven sorted supported countries, preserving country-level mode frequencies.",
            "Five visible banks and four distinct currencies denote their capped upper groups. Phase 0, Round 1 and A03-A07 exposure applies.",""]
        for title,(columns,rows) in [("Coverage",coverage),("Membership and controls",score),("Set cardinality control",cardinality),("Bank-cluster sensitivity",uncertainty),("Practical decision",decision)]:
            lines += ["## "+title,"","| "+" | ".join(columns)+" |","| "+" | ".join(["---"]*len(columns))+" |"]
            lines += ["| "+" | ".join(map(str,row))+" |" for row in rows]
            lines.append("")
        (HERE/f"out/H-A08_path_currency_set_{args.phase}.md").write_text("\n".join(lines),encoding="utf-8")
        print(f"OK: aggregate path-currency {args.phase} saved. Criteria met: {passed}.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())
