"""Audit unsupported FX paths and score currency modes without the class filter.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A16_fx_support_gaps.py
Internal validation: add --freeze SHA after committing the executable and plan.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import subprocess
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
STEM = Path(__file__).stem
SPEC = importlib.util.spec_from_file_location("fx", HERE / "H-A03_fx_country_classes.py")
fx = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fx)


def main() -> int:
    """Compare map coverage without assigning outcomes to unmapped paths."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze")
    args = parser.parse_args()
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        return 1
    phase = "validate" if args.freeze else "explore"
    try:
        if args.freeze:
            subprocess.run(["git","merge-base","--is-ancestor",args.freeze,"HEAD"],
                           cwd=fx.ROOT,check=True,capture_output=True)
            paths = (Path(__file__).resolve(),Path(fx.__file__),Path(fx.foundation.__file__),
                     fx.ROOT/f"findings/hypotheses/{STEM}.md")
            for path in paths:
                old = subprocess.check_output(
                    ["git","show",f"{args.freeze}:{path.relative_to(fx.ROOT).as_posix()}"],
                    cwd=fx.ROOT,stderr=subprocess.DEVNULL,
                ).replace(b"\r\n",b"\n")
                marker = b"\n## Confirmation and robustness results"
                if old.split(marker)[0]!=path.read_bytes().replace(b"\r\n",b"\n").split(marker)[0]:
                    raise ValueError("Freeze mismatch")
        with fx.connect() as con:
            fx.train(con)
            fx.score(con,phase)
            con.execute("""CREATE TEMP TABLE currency_map AS WITH votes AS (
                SELECT substr(path[1],5,2) country,currency,count(*) votes
                FROM source WHERE split='explore' AND ANOMALY_TYPE IS NULL
                  AND ts_utc<TIMESTAMP '2023-07-01'
                GROUP BY 1,2
            ), modes AS (
              SELECT country,currency,sum(votes) OVER(PARTITION BY country) n
              FROM votes QUALIFY row_number() OVER(PARTITION BY country ORDER BY votes DESC,currency)=1
            ) SELECT map(list(country) FILTER(WHERE n>=100),
                         list(currency) FILTER(WHERE n>=100)) strong,
                     map(list(country),list(currency)) any_mode FROM modes""")
            con.execute("""CREATE VIEW audit AS WITH mapped AS (
                SELECT eligible as class_ok,oa,ba,ob,fx,predicted,route,countries,
                  list_transform(countries,lambda c:strong[c]) modes,
                  list_transform(countries,lambda c:any_mode[c]) weak_modes
                FROM scored CROSS JOIN currency_map WHERE ts_utc>=TIMESTAMP '2023-07-01'
            ), counts AS (
                SELECT *,
                  list_count(modes)=len(modes) mode_ok,
                  list_count(weak_modes)=len(weak_modes) weak_ok,
                  list_sum(list_transform(range(1,len(modes)),lambda i:
                     coalesce((modes[i]<>modes[i+1])::INT,0))) known_changes,
                  list_sum(list_transform(range(1,len(modes)),lambda i:
                     (modes[i] IS NULL OR modes[i+1] IS NULL)::INT)) unscored_edges,
                  list_sum(list_transform(range(1,len(weak_modes)),lambda i:
                     (weak_modes[i]<>weak_modes[i+1])::INT)) weak_changes
                FROM mapped
            ) SELECT *,CASE WHEN mode_ok AND class_ok THEN 'Jointly supported'
                            WHEN mode_ok THEN 'Currency mode only'
                            WHEN class_ok THEN 'FX class only'
                            ELSE 'Neither map' END support
              FROM counts""")
            tables = {}
            tables["Support and observed outcomes"] = fx.query(con,"""WITH g AS (
              SELECT CASE WHEN grouping(support)=1 THEN 'All' ELSE support END support_group,
                count(*) n,count(DISTINCT oa) senders,count(DISTINCT ba) receivers,
                count(DISTINCT ob) banks,
                count(*) FILTER(WHERE mode_ok) mode_eligible,
                count(*) FILTER(WHERE mode_ok AND fx<>known_changes) mode_errors,
                count(*) FILTER(WHERE class_ok AND fx<>predicted) class_errors,
                count(*) FILTER(WHERE weak_ok) weak_eligible,
                count(*) FILTER(WHERE weak_ok AND fx<>weak_changes) weak_errors,
                count(*) FILTER(WHERE fx<known_changes OR fx>known_changes+unscored_edges) impossible
              FROM audit GROUP BY GROUPING SETS((),(support))
              HAVING count(*)>=100 AND count(DISTINCT oa)>=100 AND count(DISTINCT ba)>=100
            ) SELECT support_group,n,senders,receivers,banks,
                CASE WHEN mode_eligible BETWEEN 1 AND 99 THEN '<100' ELSE mode_eligible::VARCHAR END mode_eligible,
                CASE WHEN mode_errors BETWEEN 1 AND 99 THEN '<100' ELSE mode_errors::VARCHAR END mode_errors,
                CASE WHEN class_errors BETWEEN 1 AND 99 THEN '<100' ELSE class_errors::VARCHAR END class_errors,
                CASE WHEN weak_eligible BETWEEN 1 AND 99 THEN '<100'
                     WHEN n-weak_eligible BETWEEN 1 AND 99 THEN 'within 100 of n'
                     ELSE weak_eligible::VARCHAR END weak_eligible,
                CASE WHEN weak_errors BETWEEN 1 AND 99 THEN '<100' ELSE weak_errors::VARCHAR END weak_errors,
                CASE WHEN impossible BETWEEN 1 AND 99 THEN '<100' ELSE impossible::VARCHAR END outside_partial_bounds
              FROM g ORDER BY support_group""")
            n, eligible, new, senders, receivers, banks, all_errors, violations = con.execute("""
              SELECT count(*),count(*) FILTER(WHERE mode_ok),
                count(*) FILTER(WHERE mode_ok AND NOT class_ok),
                count(DISTINCT oa) FILTER(WHERE mode_ok AND NOT class_ok),
                count(DISTINCT ba) FILTER(WHERE mode_ok AND NOT class_ok),
                count(DISTINCT ob) FILTER(WHERE mode_ok AND NOT class_ok),
                count(*) FILTER(WHERE mode_ok AND fx<>known_changes),
                count(*) FILTER(WHERE fx<known_changes OR fx>known_changes+unscored_edges)
              FROM audit""").fetchone()
            passed = (eligible/n>=.99 and new>=1000 and min(senders,receivers,banks)>=100
                      and all_errors==0 and violations==0)
            assert 0 <= new <= eligible <= n
            bank_counts = np.asarray(con.execute("""SELECT count(*),
                count(*) FILTER(WHERE mode_ok),
                count(*) FILTER(WHERE mode_ok AND NOT class_ok)
                FROM audit GROUP BY ob ORDER BY ob""").fetchall())
            rng = np.random.default_rng(20261117)
            sensitivity = []
            for _ in range(1000):
                sample = bank_counts[rng.integers(len(bank_counts), size=len(bank_counts))].sum(axis=0)
                sensitivity.append(sample[1:]/sample[0])
            bounds = np.quantile(sensitivity,[.005,.995],axis=0)
            tables["Ordering-bank sensitivity"] = (["measure","low99","high99"],
                [(label,*bounds[:,i]) for i,label in enumerate(("coverage","fraction newly scored"))])
            tables["Prespecified decision"] = (["scoped","mode_eligible","mode_only","mode_excluded",
                "all_criteria_met"],[(n,eligible,new,n-eligible,passed)])
        report = fx.render("H-A16 — FX support gaps and map-only transfer",tables,args.freeze or "exploration")
        if not args.freeze:
            report = report.replace(
                "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
                "July both-account bit-0 evaluation only.")
        report += ("\nPartial bounds count changes on supported edges and allow zero or one per edge "
                   "with an unknown endpoint. They do not solve joint constraints across adjacent unknown edges. "
                   "Weak modes are a diagnostic below the 100-payment support floor. "
                   "Positive small cells are masked and undisplayed small groups remain in the pooled total.\n")
        (HERE/f"out/{STEM}_{phase}.md").write_text(report,encoding="utf-8")
        print(f"OK: aggregate {phase} coverage audit saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())
