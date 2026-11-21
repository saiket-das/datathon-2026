"""Test exploration-trained latent country classes as an FX-step mechanism.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A03_fx_country_classes.py --phase explore
Validation uses --phase validate --freeze SHA after the full design is committed.
Sponsor records and learned bank identifiers are never exported.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import importlib.util
from pathlib import Path
import subprocess
import sys
from zoneinfo import ZoneInfo

import duckdb
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STEM = "H-A03_fx_country_classes"
_spec = importlib.util.spec_from_file_location("foundation", ROOT / "analysis/00_prep/scientific_checks.py")
foundation = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(foundation)


def components(pairs: list[tuple[str, str, int, int]]) -> dict[str, str]:
    """Join country pairs with >=100 observations and zero observed conversions."""
    parent: dict[str, str] = {}
    def find(x: str) -> str:
        parent.setdefault(x, x)
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    for a, b, n, zero in sorted(pairs):
        if n < 100:
            continue
        find(a); find(b)
        if zero == n:
            ra, rb = sorted((find(a), find(b)))
            parent[rb] = ra
    return {x: find(x) for x in sorted(parent)}


def connect() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.execute("SET memory_limit='512MB'; SET threads=1; SET temp_directory=''; SET preserve_insertion_order=false")
    con.execute(f"""CREATE VIEW source AS SELECT ROW_ID,ORDERING_ACCOUNT oa,BENEFICIARY_ACCOUNT ba,
       ORDERING_BIC8 ob,USD_AMOUNT,CURRENCY_CODE currency,ts_utc,ANOMALY_TYPE,
       CURRENCY_CONVERSION_COUNT fx,TRANSACTION_TYPE_CODE route,
       list_filter(string_split(BIC8_PATH,';'),lambda x:x<>'...') path,
       {foundation.partition_sql('accounts')} split FROM read_parquet('dataset/payments.parquet')""")
    return con


def train(con: duckdb.DuckDBPyConnection) -> dict[str, str]:
    pairs = con.execute("""SELECT substr(path[1],5,2),substr(path[-1],5,2),count(*),
      count(*) FILTER(WHERE fx=0) FROM source WHERE split='explore' AND ANOMALY_TYPE IS NULL
      AND len(path)=2 GROUP BY 1,2 HAVING count(*)>=100""").fetchall()
    mapping = components(pairs)
    assert len(mapping) >= 10
    con.execute("CREATE TEMP TABLE classes(country VARCHAR PRIMARY KEY,group_id VARCHAR,wrong_id VARCHAR)")
    countries = sorted(mapping)
    con.executemany("INSERT INTO classes VALUES (?,?,?)", [(x, mapping[x], mapping[countries[(i+7)%len(countries)]]) for i,x in enumerate(countries)])
    return mapping


def score(con: duckdb.DuckDBPyConnection, phase: str) -> None:
    split = 'confirm' if phase == 'validate' else 'explore'
    con.execute(f"""CREATE VIEW chosen AS SELECT * FROM source
      WHERE split='{split}' AND ANOMALY_TYPE IS NULL AND len(path)>2""")
    # Only small country mappings are materialised; paths/records remain lazy views.
    con.execute("""CREATE VIEW scored AS WITH p AS (SELECT *,
      list_transform(path,lambda b:substr(b,5,2)) countries FROM chosen), m AS (
      SELECT *,list_transform(countries,lambda x:group_map[x]) groups,
        list_transform(countries,lambda x:wrong_map[x]) wrong_groups FROM p CROSS JOIN (SELECT map(list(country),list(group_id)) group_map,map(list(country),list(wrong_id)) wrong_map FROM classes))
      SELECT *, NOT list_contains(list_transform(groups,lambda x:x IS NULL),true) eligible,
        list_sum(list_transform(range(1,len(groups)),lambda i:(groups[i]<>groups[i+1])::INT)) predicted,
        list_sum(list_transform(range(1,len(countries)),lambda i:(countries[i]<>countries[i+1])::INT)) country_predicted,
        list_sum(list_transform(range(1,len(wrong_groups)),lambda i:(wrong_groups[i]<>wrong_groups[i+1])::INT)) wrong_predicted
      FROM m""")


def query(con: duckdb.DuckDBPyConnection, sql: str) -> tuple[list[str], list[tuple]]:
    r=con.execute(sql)
    return [c[0] for c in r.description],r.fetchall()


def render(title: str, tables: dict[str, tuple[list[str], list[tuple]]], freeze: str) -> str:
    parts=[f"# {title}","",f"Freeze: {freeze}.","512MB; one thread; no disk spill. Aggregates only.",
      "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
      "Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate."]
    for caption,(columns,rows) in tables.items():
        parts += ["","## "+caption,"","| "+" | ".join(columns)+" |","| "+" | ".join(['---']*len(columns))+" |"]
        for row in rows:
            parts.append("| "+" | ".join(map(str,row))+" |")
    return "\n".join(parts)+"\n"


def main() -> int:
    con=None
    try:
        parser=argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--phase',choices=['explore','validate'],default='explore')
        parser.add_argument('--freeze')
        args=parser.parse_args()
        if args.phase=='explore' and datetime.now(ZoneInfo('Asia/Kuala_Lumpur'))>=datetime(2026,11,18,20,tzinfo=ZoneInfo('Asia/Kuala_Lumpur')):
            raise ValueError('Research cutoff reached')
        freeze=args.freeze or 'not frozen; exploration only'
        if args.phase=='validate':
            if not args.freeze: raise ValueError('Freeze SHA required')
            for path in [Path(__file__).relative_to(ROOT),Path('analysis/00_prep/scientific_checks.py')]:
                frozen=subprocess.check_output(['git','show',f'{args.freeze}:{path.as_posix()}'],cwd=ROOT)
                assert frozen.replace(b'\r\n',b'\n')==(ROOT/path).read_bytes().replace(b'\r\n',b'\n')
        con=connect(); mapping=train(con); score(con,args.phase)
        tables={}
        tables['Training graph support']=query(con,"""SELECT count(*) supported_countries,count(DISTINCT group_id) learned_groups
          FROM classes""")
        tables['Coverage']=query(con,"""SELECT count(*) n,sum(eligible::INT) eligible_n,avg(eligible::INT) eligible_share,
          count(DISTINCT oa) senders,count(DISTINCT ba) receivers FROM scored""")
        tables['Primary eligible multibank comparisons']=query(con,"""SELECT count(*) n,count(DISTINCT oa) senders,
          count(DISTINCT ba) receivers,sum((predicted=fx)::INT) exact_matches,
          avg((predicted=fx)::INT) exact_share,avg((country_predicted=fx)::INT) country_baseline,
          avg((wrong_predicted=fx)::INT) wrong_mapping,avg(abs(predicted-fx)) mean_absolute_error,
          max(abs(predicted-fx)) largest_error FROM scored WHERE eligible""")
        rows=con.execute("""SELECT ob,count(*),sum((predicted=fx)::INT),sum((country_predicted=fx)::INT)
          FROM scored WHERE eligible GROUP BY ob ORDER BY ob""").fetchall()
        numeric=np.array([r[1:] for r in rows],dtype=float); rng=np.random.default_rng(20261116)
        boot=[]
        for _ in range(1000):
            totals=numeric[rng.integers(0,len(rows),len(rows))].sum(axis=0)
            boot.append((totals[1]/totals[0],(totals[1]-totals[2])/totals[0]))
        intervals=np.quantile(boot,[.005,.995],axis=0)
        tables['99% ordering-bank cluster sensitivity intervals']=(['statistic','low','high'],[
          ('exact match',*intervals[:,0]),('lift over country transitions',*intervals[:,1])])
        cov=tables['Coverage'][1][0]; primary=tables['Primary eligible multibank comparisons'][1][0]
        passed=cov[2]>=.90 and min(primary[1:3])>=100 and intervals[0,0]>=.995 and intervals[0,1]>=.02
        tables['Frozen practical decision']=(['passes','coverage_floor','exact_lower_floor','lift_lower_floor'],[(bool(passed),.90,.995,.02)])
        tables['Route sensitivity']=query(con,"""SELECT route,count(*) n,count(DISTINCT oa) senders,
          count(DISTINCT ba) receivers,avg((predicted=fx)::INT) exact_share,
          avg((country_predicted=fx)::INT) country_baseline FROM scored WHERE eligible GROUP BY route
          HAVING count(*)>=100 AND count(DISTINCT oa)>=100 AND count(DISTINCT ba)>=100 ORDER BY route""")
        tables['Eligible identity and overlap audit']=query(con,"""WITH current_banks AS (
          SELECT DISTINCT unnest(path) bank FROM scored WHERE eligible), training_banks AS (
          SELECT DISTINCT unnest(path) bank FROM source WHERE split='explore'
          AND ANOMALY_TYPE IS NULL AND len(path)=2)
          SELECT (SELECT count(*) FROM scored WHERE eligible) n,
          (SELECT count(DISTINCT ROW_ID) FROM scored WHERE eligible) distinct_rows,
          (SELECT count(*) FROM current_banks) visible_banks,
          (SELECT count(*) FROM current_banks JOIN training_banks USING(bank)) shared_training_banks""")
        tables['Month sensitivity']=query(con,"""SELECT month(ts_utc) period,count(*) n,
          count(DISTINCT oa) senders,count(DISTINCT ba) receivers,avg((predicted=fx)::INT) exact_share
          FROM scored WHERE eligible GROUP BY 1 HAVING count(*)>=100
          AND count(DISTINCT oa)>=100 AND count(DISTINCT ba)>=100 ORDER BY 1""")
        out=HERE/'out'/f'{STEM}_{args.phase}.md'
        out.write_text(render(f'H-A03: {args.phase} country-class FX transitions',tables,freeze),encoding='utf-8')
        print(f'OK: {args.phase} aggregate report written; practical decision={passed}')
        return 0
    except Exception as exc:
        print(f'ERROR: {type(exc).__name__}; source values hidden.',file=sys.stderr)
        return 1
    finally:
        if con is not None: con.close()


if __name__=='__main__':
    sys.exit(main())