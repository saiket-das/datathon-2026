"""Compare FX equivalence residuals with independently learned currency modes.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A14_currency_class_disagreement.py
Frozen internal test: add --phase validate --freeze SHA.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import subprocess
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("fx",HERE/"H-A03_fx_country_classes.py")
fx = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fx)


def main() -> int:
    """Screen a missed-equivalence explanation without fitting to count residuals."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("explore","validate"), default="explore")
    parser.add_argument("--freeze")
    args = parser.parse_args()
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        print("Research cutoff reached.")
        return 1
    try:
        if args.phase == "validate":
            if not args.freeze:
                raise ValueError("Freeze required")
            subprocess.run(["git","merge-base","--is-ancestor",args.freeze,"HEAD"],
                           cwd=fx.ROOT,check=True,capture_output=True)
            files = (Path(__file__).resolve(),Path(fx.__file__),Path(fx.foundation.__file__),
                     fx.ROOT/"findings/hypotheses/H-A14_currency_class_disagreement.md")
            marker = b"\n## Confirmation and robustness results"
            for path in files:
                frozen = subprocess.check_output(
                    ["git","show",f"{args.freeze}:{path.relative_to(fx.ROOT).as_posix()}"],
                    cwd=fx.ROOT,stderr=subprocess.DEVNULL,
                ).replace(b"\r\n",b"\n")
                if frozen.split(marker)[0] != path.read_bytes().replace(b"\r\n",b"\n").split(marker)[0]:
                    raise ValueError("Freeze mismatch")
        with fx.connect() as con:
            fx.train(con)
            fx.score(con,args.phase)
            con.execute("""CREATE TEMP TABLE modes AS
              SELECT substr(path[1],5,2) country,currency FROM source
              WHERE split='explore' AND ANOMALY_TYPE IS NULL
                AND ts_utc<TIMESTAMP '2023-07-01'
              GROUP BY 1,2
              QUALIFY sum(count(*)) OVER(PARTITION BY country)>=100
                AND row_number() OVER(PARTITION BY country ORDER BY count(*) DESC,currency)=1""")
            con.execute("""CREATE VIEW comparison AS
              WITH mapped AS (
                SELECT s.*,list_transform(countries,lambda c:currency_map[c]) modes
                FROM scored s CROSS JOIN
                  (SELECT map(list(country),list(currency)) currency_map FROM modes)
              ), counts AS (
                SELECT *,list_sum(list_transform(range(1,len(modes)),
                  lambda i:(modes[i]<>modes[i+1])::INT)) currency_changes
                FROM mapped WHERE eligible AND ts_utc>=TIMESTAMP '2023-07-01'
                  AND NOT list_contains(list_transform(modes,lambda x:x IS NULL),true)
              )
              SELECT *,CASE WHEN currency_changes<predicted THEN 'Fewer currency-mode changes'
                  WHEN currency_changes=predicted THEN 'Equal counts'
                  ELSE 'More currency-mode changes' END comparison
              FROM counts""")
            coverage = fx.query(con,"""SELECT
              (SELECT count(*) FROM scored WHERE ts_utc>=TIMESTAMP '2023-07-01') scoped,
              count(*) eligible,count(DISTINCT oa) senders,count(DISTINCT ba) receivers
              FROM comparison""")
            table = fx.query(con,"""WITH g AS (
              SELECT CASE WHEN grouping(comparison)=1 THEN 'All' ELSE comparison END category,
                count(*) n,count(DISTINCT oa) senders,count(DISTINCT ba) receivers,
                count(*) FILTER(WHERE fx<>predicted) class_errors,
                count(*) FILTER(WHERE fx<>currency_changes) mode_errors,
                count(*) FILTER(WHERE fx<>predicted AND fx=currency_changes) repaired,
                count(*) FILTER(WHERE fx=predicted AND fx<>currency_changes) broken,
                count(*) FILTER(WHERE fx>currency_changes) above_mode_bound,
                avg((currency=modes[1])::INT) first_mode_match
              FROM comparison GROUP BY GROUPING SETS((),(comparison))
              HAVING count(*)>=1000 AND count(DISTINCT oa)>=100 AND count(DISTINCT ba)>=100)
              SELECT category,n,senders,receivers,
                CASE WHEN class_errors BETWEEN 1 AND 99 THEN '<100' ELSE class_errors::VARCHAR END class_errors,
                CASE WHEN mode_errors BETWEEN 1 AND 99 THEN '<100' ELSE mode_errors::VARCHAR END mode_errors,
                CASE WHEN repaired BETWEEN 1 AND 99 THEN '<100' ELSE repaired::VARCHAR END repaired,
                CASE WHEN broken BETWEEN 1 AND 99 THEN '<100' ELSE broken::VARCHAR END broken,
                CASE WHEN above_mode_bound BETWEEN 1 AND 99 THEN '<100' ELSE above_mode_bound::VARCHAR END above_mode_bound,
                first_mode_match FROM g ORDER BY category""")
            bank_rows = con.execute("""SELECT count(*) n,
                count(*) FILTER(WHERE fx<>predicted) class_errors,
                count(*) FILTER(WHERE fx<>currency_changes) mode_errors,
                count(*) FILTER(WHERE fx>currency_changes) violations
                FROM comparison GROUP BY ob ORDER BY ob""").fetchall()
            banks = np.asarray(bank_rows,dtype=np.int64)
            total = banks.sum(axis=0)
            rng = np.random.default_rng(20261117)
            lifts = []
            for _ in range(1000):
                n, class_errors, mode_errors, _ = banks[rng.integers(0,len(banks),len(banks))].sum(axis=0)
                lifts.append((class_errors-mode_errors)/n)
            low,high = np.quantile(lifts,[.005,.995])
            scoped,eligible,senders,receivers = coverage[1][0]
            passed = (eligible/scoped>=.95 and min(senders,receivers,len(banks))>=100
                      and total[1]>=100 and total[2]==0 and total[3]==0 and low>=.002)
            decision = (["ordering_banks","lift_low99","lift_high99","all_criteria_met"],
                        [(len(banks),float(low),float(high),passed)])
        report=fx.render("H-A14 — FX-class versus currency-mode changes",
            {"Coverage":coverage,"Missed equivalence and counterexamples":table,
             "Ordering-bank sensitivity":decision},args.freeze or "exploration only")
        if args.phase == "explore":
            report=report.replace(
                "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
                "Both-account bit-0 exploration only. Phase 0 and A01–A13 exposure applies.")
        report+="\nCountry modes use currency outcomes while classes use two-bank FX counts. Both can encode shared metadata. Neither map identifies legal native currencies.\n"
        (HERE/f"out/H-A14_currency_class_disagreement_{args.phase}.md").write_text(report,encoding="utf-8")
        print("OK: aggregate currency-class disagreement saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())
