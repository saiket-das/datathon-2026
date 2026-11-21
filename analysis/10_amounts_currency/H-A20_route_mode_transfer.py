"""Explore whether FX currency modes transfer across route categories.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A20_route_mode_transfer.py
Frozen internal test: add --freeze SHA after committing the code and plan.
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
    """Assess route-specific currency maps on exactly the same July paths."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze")
    args = parser.parse_args()
    phase = "validate" if args.freeze else "explore"
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        return 1
    try:
        if args.freeze:
            subprocess.run(["git","merge-base","--is-ancestor",args.freeze,"HEAD"],
                           cwd=fx.ROOT,check=True,capture_output=True)
            files = (Path(__file__).resolve(),Path(fx.__file__),Path(fx.foundation.__file__),
                     fx.ROOT/"findings/hypotheses/H-A20_route_mode_transfer.md")
            marker = b"\n## Confirmation and robustness results"
            for path in files:
                frozen = subprocess.check_output(
                    ["git","show",f"{args.freeze}:{path.relative_to(fx.ROOT).as_posix()}"],
                    cwd=fx.ROOT,stderr=subprocess.DEVNULL,
                ).replace(b"\r\n",b"\n")
                if frozen.split(marker)[0]!=path.read_bytes().replace(b"\r\n",b"\n").split(marker)[0]:
                    raise ValueError("Freeze mismatch")
        split = "confirm" if args.freeze else "explore"
        with fx.connect() as con:
            con.execute("""CREATE TEMP TABLE maps AS WITH votes AS (
              SELECT if(len(path)=2,'two','multi') training,
                substr(path[1],5,2) country,currency,count(*) n
              FROM source WHERE split='explore' AND ANOMALY_TYPE IS NULL
                AND ts_utc<TIMESTAMP '2023-07-01'
              GROUP BY 1,2,3
            ), modes AS (
              SELECT training,country,currency FROM votes
              QUALIFY sum(n) OVER(PARTITION BY training,country)>=100
                AND row_number() OVER(PARTITION BY training,country
                    ORDER BY n DESC,currency)=1
            )
            SELECT training,map(list(country),list(currency)) currencies FROM modes GROUP BY 1""")
            con.execute(f"""CREATE VIEW scored AS WITH mapped AS (
              SELECT oa,ba,ob,fx,route,
                 list_transform(path,lambda b:t.currencies[substr(b,5,2)]) two_modes,
                 list_transform(path,lambda b:m.currencies[substr(b,5,2)]) multi_modes
              FROM source CROSS JOIN maps t CROSS JOIN maps m
              WHERE split='{split}' AND ANOMALY_TYPE IS NULL
                AND ts_utc>=TIMESTAMP '2023-07-01' AND len(path)>=2
                AND t.training='two' AND m.training='multi'
            ) SELECT *,
                list_count(two_modes)=len(two_modes) two_ok,
                list_count(multi_modes)=len(multi_modes) multi_ok,
                list_sum(list_transform(range(1,len(two_modes)),
                    lambda i:(two_modes[i]<>two_modes[i+1])::INT)) two_pred,
                list_sum(list_transform(range(1,len(multi_modes)),
                    lambda i:(multi_modes[i]<>multi_modes[i+1])::INT)) multi_pred
              FROM mapped""")
            support = fx.query(con,"""SELECT route,count(*) n,
                count(*) FILTER(WHERE two_ok) two_mapped,
                count(*) FILTER(WHERE multi_ok) multi_mapped,
                count(*) FILTER(WHERE two_ok AND multi_ok) joint_mapped
                FROM scored GROUP BY 1 ORDER BY 1""")
            outcomes = fx.query(con,"""WITH g AS (
                SELECT route,count(*) n,count(DISTINCT oa) senders,
                  count(DISTINCT ba) receivers,count(DISTINCT ob) banks,
                  count(*) FILTER(WHERE fx<>two_pred) two_errors,
                  count(*) FILTER(WHERE fx<>multi_pred) multi_errors,
                  count(*) FILTER(WHERE two_pred<>multi_pred) disagreement
                FROM scored WHERE two_ok AND multi_ok
                GROUP BY 1 HAVING count(*)>=1000 AND count(DISTINCT oa)>=100
                   AND count(DISTINCT ba)>=100
              ) SELECT route,n,senders,receivers,banks,
                CASE WHEN two_errors BETWEEN 1 AND 99 THEN '<100' ELSE two_errors::VARCHAR END two_errors,
                CASE WHEN multi_errors BETWEEN 1 AND 99 THEN '<100' ELSE multi_errors::VARCHAR END multi_errors,
                CASE WHEN disagreement BETWEEN 1 AND 99 THEN '<100' ELSE disagreement::VARCHAR END disagreement
                FROM g ORDER BY 1""")
            assert all(row[4]<=min(row[2],row[3])<=row[1] for row in support[1])
            bank_rows = con.execute("""SELECT route,count(*) n,
                count(*) FILTER(WHERE two_ok AND multi_ok) joint_n,
                count(*) FILTER(WHERE two_ok AND multi_ok AND (fx<>two_pred OR fx<>multi_pred)) errors
                FROM scored GROUP BY route,ob ORDER BY route,ob""").fetchall()
            rng = np.random.default_rng(20261117)
            decisions = []
            for route in ("Covered","Direct","Indirect"):
                bank = np.asarray([row[1:] for row in bank_rows if row[0]==route])
                n,joint,errors = bank.sum(axis=0)
                coverage_draws = []
                for _ in range(1000):
                    draw_n,draw_joint,_ = bank[rng.integers(len(bank),size=len(bank))].sum(axis=0)
                    coverage_draws.append(draw_joint/draw_n)
                low,high = np.quantile(coverage_draws,[.005,.995])
                displayed = any(row[0]==route for row in outcomes[1])
                passed = (displayed and joint/n>=.98 and len(bank)>=100 and errors==0)
                decisions.append((route,joint/n,len(bank),float(low),float(high),passed))
            decision = (["route","joint_coverage","scoped_ordering_banks","coverage_low99",
                         "coverage_high99","pass"],decisions)
        output = fx.render("H-A20 — Currency mode transfer across training routes",
            {"July route coverage":support,"FX count errors on jointly mapped rows":outcomes,
             "Routing coverage sensitivity and decision":decision},args.freeze or "exploration")
        if not args.freeze:
            output = output.replace(
                "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
                "Both-account bit-0 only. Phase 0 and A01–A19 prior exposure applies.")
        output += ("\nTraining uses payment currencies and first visible countries, without FX labels. "
                   "Route categories in scoring are supplied labels. Training categories use visible "
                   "path length. Joint support prevents coverage differences from distorting accuracy.\n")
        (HERE/f"out/H-A20_route_mode_transfer_{phase}.md").write_text(output,encoding="utf-8")
        print("OK: aggregate route transfer screen saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())
