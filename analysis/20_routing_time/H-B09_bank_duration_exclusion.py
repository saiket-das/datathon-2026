"""Screen a persistent visible-bank low-duration exclusion signature.

Run from repository root:
    uv run python analysis/20_routing_time/H-B09_bank_duration_exclusion.py --phase explore
Frozen internal validation uses --phase confirm --freeze SHA after committing a complete plan.
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys
import duckdb
import numpy as np
from scipy.stats import beta

ROOT = Path(__file__).resolve().parents[2]


def upper_bound(affected: int, banks: int) -> float:
    """One-sided 99% binomial bound, conditional on an independence assumption."""
    return 1.0 if affected == banks else float(beta.ppf(.99, affected+1, banks-affected))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("explore", "confirm"), default="explore")
    parser.add_argument("--freeze")
    args = parser.parse_args()
    if args.phase=="explore" and datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError("Research cutoff reached")
    if args.phase=="confirm":
        if not args.freeze or len(args.freeze)!=40 or any(c not in "0123456789abcdef" for c in args.freeze):
            raise ValueError("Full freeze SHA required")
        subprocess.run(["git","merge-base","--is-ancestor",args.freeze,"HEAD"],cwd=ROOT,check=True)
        original=subprocess.check_output(["git","show",f"{args.freeze}:analysis/20_routing_time/H-B09_bank_duration_exclusion.py"],cwd=ROOT)
        plan=subprocess.check_output(["git","show",f"{args.freeze}:findings/hypotheses/H-B09_bank_duration_exclusion.md"],cwd=ROOT)
        if original!=Path(__file__).read_bytes().replace(b"\r\n",b"\n") or b"**Status:** confirmation-ready" not in plan:
            raise ValueError("Unchanged executable and frozen complete plan required")
    with duckdb.connect(config={"memory_limit":"512MB","threads":1,"temp_directory":""}) as c:
        c.execute("SET TimeZone='UTC'")
        c.execute("""
            CREATE VIEW source AS SELECT TOTAL_DURATION AS duration, PARTICIPANT_COUNT AS v,
            TRANSACTION_TYPE_CODE AS route, ORDERING_BIC8 AS ordering_bank,
            ORDERING_ACCOUNT AS sender,BENEFICIARY_ACCOUNT AS receiver,
            list_filter(string_split(BIC8_PATH,';'),lambda x:x<>'...') AS p,month(ts_utc) AS mon
            FROM read_parquet('dataset/payments.parquet')
            WHERE ANOMALY_TYPE IS NULL AND ts_utc>=TIMESTAMP '2023-05-01'
              AND ts_utc<TIMESTAMP '2023-08-01'
              AND (('0x'||substr(md5(ORDERING_BIC8),1,8))::UBIGINT%2)=0
              AND (('0x'||substr(md5(BENEFICIARY_BIC8),1,8))::UBIGINT%2)=0
        """)
        c.execute("""
            CREATE TEMP TABLE fit AS SELECT bank,count(*) n,count_if(duration<100) fast
            FROM source,unnest(p)t(bank) WHERE v=2 AND mon=5
            GROUP BY bank HAVING count(*)>=100 ORDER BY bank
        """)
        training=c.execute("SELECT bank,n,fast=0 slow FROM fit ORDER BY bank").fetchall()
        rng=np.random.default_rng(20261116)
        labels={}
        for lower,upper in ((100,300),(300,1000),(1000,3000),(3000,10000),(10000,10**20)):
            rows=[row for row in training if lower<=row[1]<upper]
            shuffled=rng.permutation([row[2] for row in rows])
            labels.update({row[0]:bool(label) for row,label in zip(rows,shuffled)})
        c.execute("ALTER TABLE fit ADD COLUMN shuffled BOOLEAN")
        c.executemany("UPDATE fit SET shuffled=? WHERE bank=?",[(label,bank) for bank,label in labels.items()])
        month=6 if args.phase=="explore" else 7
        c.execute(f"""
            CREATE VIEW evaluated AS
            SELECT e.*,
            (f1.fast=0)::INT+(f2.fast=0)::INT+
            CASE WHEN v>=3 THEN (f3.fast=0)::INT ELSE 0 END+
            CASE WHEN v>=4 THEN (f4.fast=0)::INT ELSE 0 END+
            CASE WHEN v>=5 THEN (f5.fast=0)::INT ELSE 0 END AS slow_count,
            f1.shuffled::INT+f2.shuffled::INT+
            CASE WHEN v>=3 THEN f3.shuffled::INT ELSE 0 END+
            CASE WHEN v>=4 THEN f4.shuffled::INT ELSE 0 END+
            CASE WHEN v>=5 THEN f5.shuffled::INT ELSE 0 END AS shuffled_count,
            f1.bank IS NOT NULL AND f2.bank IS NOT NULL
            AND (v<3 OR f3.bank IS NOT NULL) AND (v<4 OR f4.bank IS NOT NULL)
            AND (v<5 OR f5.bank IS NOT NULL) AS eligible
            FROM source e LEFT JOIN fit f1 ON p[1]=f1.bank
            LEFT JOIN fit f2 ON p[2]=f2.bank LEFT JOIN fit f3 ON p[3]=f3.bank
            LEFT JOIN fit f4 ON p[4]=f4.bank LEFT JOIN fit f5 ON p[5]=f5.bank
            WHERE e.mon={month} AND v BETWEEN 2 AND 5
        """)
        total,eligible=c.execute("SELECT count(*),count_if(eligible) FROM evaluated").fetchone()
        fitted,slow=c.execute("SELECT count(*),count_if(fast=0) FROM fit").fetchone()
        lines=[f"# H-B09 bank-duration exclusion: {args.phase}","",
               f"Freeze: {args.freeze or 'exploration only'}. May training, month {month} evaluation.",
               "Unlabelled endpoint-bit0/0, visible counts2–5.512MB, one thread, no spill.",
               "Phase0/Round1/Round2 duration/path/calendar exposure applies. Reused populations are internal.",
               f"Training: {fitted:,} supported banks, {slow:,} zero-fast banks.",
               f"Evaluation: {total:,} payments, {eligible:,} supported paths ({eligible/total:.4%}).","",
               "| Model | Any exclusion bank | Payments | Ordering banks | Senders | Receivers | Duration<100 count | Share |",
               "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
        results={}
        for model,column in (("May bank labels","slow_count"),("Exposure-bin permutation","shuffled_count")):
            for flag in (False,True):
                row=c.execute(f"""SELECT count(*),count(DISTINCT ordering_bank),count(DISTINCT sender),count(DISTINCT receiver),
                                  count_if(duration<100) FROM evaluated WHERE eligible AND ({column}>0)=?""",[flag]).fetchone()
                n,banks,senders,receivers,fast=row
                results[(model,flag)]=row
                if min(n,banks,senders,receivers)<100:
                    lines.append(f"| {model} | {flag} | Suppressed | — | — | — | — | — |")
                else:
                    event="<100" if 0<fast<100 else f"{fast:,}"
                    lines.append(f"| {model} | {flag} | {n:,} | {banks:,} | {senders:,} | {receivers:,} | {event} | {fast/n:.6%} |")
        primary=results[("May bank labels",True)]
        comparator=results[("Exposure-bin permutation",True)]
        n,banks,senders,receivers,fast=primary
        affected=c.execute("""SELECT count(*) FROM (SELECT ordering_bank FROM evaluated WHERE eligible AND slow_count>0
                               GROUP BY ordering_bank HAVING count_if(duration<100)>0)""").fetchone()[0]
        bound=upper_bound(affected,banks)
        passed=(eligible/total>=.50 and n>=5000 and min(banks,senders,receivers)>=100 and fast/n<=.001
                and bound<=.03 and min(comparator[:4])>=100 and comparator[-1]/comparator[0]-fast/n>=.10)
        lines+=["",f"Affected ordering-bank fraction99% upper: {bound:.8f}.",
                f"Criteria {'PASS' if passed else 'FAIL'} ({'pilot only' if args.phase=='explore' else 'frozen internal test'}).",
                "The binomial bound assumes independent ordering-bank clusters. Shared path banks can violate this assumption.",
                "An exposure-matched bank-label permutation is a falsification control, not an exchangeable randomisation test.",
                "", "## Route and visible-count controls","",
                "| Route | Visible | Payments | Ordering banks | Fast count | Fast share |",
                "| --- | --- | ---: | ---: | ---: | ---: |"]
        rows=c.execute("""SELECT route,v,count(*),count(DISTINCT ordering_bank),count_if(duration<100)
                          FROM evaluated WHERE eligible AND slow_count>0 GROUP BY route,v
                          HAVING count(*)>=100 AND count(DISTINCT ordering_bank)>=100
                          AND count(DISTINCT sender)>=100 AND count(DISTINCT receiver)>=100 ORDER BY route,v""").fetchall()
        for route,v,n,banks,fast in rows:
            event="<100" if 0<fast<100 else f"{fast:,}"
            lines.append(f"| {route} | {v} | {n:,} | {banks:,} | {event} | {fast/n:.6%} |")
        shared_sender=c.execute("""
            SELECT count(DISTINCT sender) FROM evaluated WHERE eligible
            AND sender IN (SELECT sender FROM source WHERE mon=5 AND v=2)
        """).fetchone()[0]
        shared_receiver=c.execute("""
            SELECT count(DISTINCT receiver) FROM evaluated WHERE eligible
            AND receiver IN (SELECT receiver FROM source WHERE mon=5 AND v=2)
        """).fetchone()[0]
        shared_ordering=c.execute("""
            SELECT count(DISTINCT ordering_bank) FROM evaluated WHERE eligible
            AND ordering_bank IN (SELECT ordering_bank FROM source WHERE mon=5 AND v=2)
        """).fetchone()[0]
        used_fit=c.execute("""
            SELECT count(DISTINCT bank) FROM evaluated,unnest(p)t(bank) WHERE eligible
        """).fetchone()[0]
        lines+=["","## Entity overlap audit","",
                "Whole eligible evaluation cohort versus full May Direct training records. No source rows overlap across months.",
                "| Shared same-role senders | Shared same-role receivers | Shared declared ordering banks | Used May-fitted visible banks |",
                "| ---: | ---: | ---: | ---: |",
                f"| {shared_sender:,} | {shared_receiver:,} | {shared_ordering:,} | {used_fit:,} |",
                "All eligible visible banks are May-fitted by construction. Either-role account, intermediary and text dependencies remain."]
    out=Path(__file__).parent/"out"/f"H-B09_bank_duration_exclusion_{args.phase}.md"
    out.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(f"Saved B09 aggregates. Criteria {'PASS' if passed else 'FAIL'}.")


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source details hidden.",file=sys.stderr)
        sys.exit(1)
