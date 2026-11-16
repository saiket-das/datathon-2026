"""Screen whether two-bank exceptions explain multibank FX residuals.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A11_fx_transition_residuals.py
After freezing, add --phase validate --freeze SHA for reused-account validation.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("fx_model", HERE / "H-A03_fx_country_classes.py")
fx = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fx)


def main() -> int:
    """Test cross-route transfer for pathways with one unambiguous transition."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=["explore", "validate"], default="explore")
    parser.add_argument("--freeze")
    args = parser.parse_args()
    if datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        print("Research cutoff reached.")
        return 1
    try:
        if args.phase == "validate":
            if not args.freeze:
                raise ValueError("Freeze required.")
            subprocess.run(["git", "merge-base", "--is-ancestor", args.freeze, "HEAD"],
                           cwd=fx.ROOT, check=True, capture_output=True)
            paths = [Path(__file__).resolve(), Path(fx.__file__), Path(fx.foundation.__file__),
                     fx.ROOT / "findings/hypotheses/H-A11_fx_transition_residuals.md"]
            for path in paths:
                frozen = subprocess.check_output(
                    ["git", "show", f"{args.freeze}:{path.relative_to(fx.ROOT).as_posix()}"],
                    cwd=fx.ROOT, stderr=subprocess.DEVNULL,
                )
                marker = b"\n## Confirmation and robustness results"
                if frozen.replace(b"\r\n", b"\n").split(marker)[0] != path.read_bytes().replace(b"\r\n", b"\n").split(marker)[0]:
                    raise ValueError("Freeze mismatch.")
        with fx.connect() as con:
            fx.train(con)
            fx.score(con, args.phase)
            con.execute("""CREATE TEMP TABLE two_bank AS
                SELECT substr(path[1],5,2) origin, substr(path[-1],5,2) destination,
                  count(*) training_n,avg((fx=0)::INT) zero_share
                FROM source WHERE split='explore' AND ANOMALY_TYPE IS NULL
                  AND ts_utc<TIMESTAMP '2023-07-01' AND len(path)=2
                GROUP BY 1,2 HAVING count(*)>=100""")
            con.execute("""CREATE VIEW single_transition AS
                WITH pairs AS (
                    SELECT route,oa,ba,ob,fx,
                      list_filter(range(1,len(groups)),lambda i:groups[i]<>groups[i+1])[1] idx,
                      countries
                    FROM scored WHERE eligible AND predicted=1
                      AND ts_utc>=TIMESTAMP '2023-07-01'
                )
                SELECT p.*,training_n,zero_share,
                    CASE WHEN training_n IS NULL THEN 'Unsupported'
                      WHEN zero_share=0 THEN 'No zero FX in two-bank training'
                      WHEN zero_share=1 THEN 'Always zero FX in two-bank training'
                      ELSE 'Mixed two-bank training' END category
                FROM pairs p LEFT JOIN two_bank t
                    ON p.countries[idx]=t.origin AND p.countries[idx+1]=t.destination""")
            summary = fx.query(con, """WITH grouped AS (
                SELECT CASE WHEN grouping(category)=1 THEN 'All' ELSE category END training,
                   CASE WHEN grouping(route)=1 THEN 'All' ELSE route END route,
                   count(*) n,count(DISTINCT oa) senders,count(DISTINCT ba) receivers,
                   count(DISTINCT ob) banks,count(*) FILTER(WHERE fx=0) residuals,
                   count(*) FILTER(WHERE fx>1) above_class,
                   avg(zero_share) transferred_two_bank_rate
                FROM single_transition GROUP BY GROUPING SETS((),(category),(category,route))
                HAVING count(*)>=1000 AND count(DISTINCT oa)>=100 AND count(DISTINCT ba)>=100
            )
            SELECT training,route,n,senders,receivers,banks,
                CASE WHEN residuals BETWEEN 1 AND 99 THEN '<100' ELSE residuals::VARCHAR END residuals,
                CASE WHEN residuals BETWEEN 1 AND 99 THEN NULL ELSE residuals/n END residual_share,
                CASE WHEN above_class BETWEEN 1 AND 99 THEN '<100' ELSE above_class::VARCHAR END above_class,
                transferred_two_bank_rate
            FROM grouped ORDER BY training,route""")
            decision = fx.query(con, """WITH counts AS (
                SELECT count(*) n,count(training_n) supported,
                   count(DISTINCT oa) FILTER(WHERE training_n IS NULL) unsupported_senders,
                   count(DISTINCT ba) FILTER(WHERE training_n IS NULL) unsupported_receivers,
                   count(DISTINCT ob) FILTER(WHERE training_n IS NULL) unsupported_banks,
                   count(*) FILTER(WHERE training_n IS NOT NULL AND fx<>1) supported_errors,
                   count(*) FILTER(WHERE training_n IS NULL AND fx=0) unsupported_zero,
                   count(*) FILTER(WHERE fx>1) above_bound
                FROM single_transition
            )
            SELECT supported/n support_share,unsupported_senders,unsupported_receivers,
                unsupported_banks, coalesce(supported/n>=0.80 AND supported<n
                 AND supported_errors=0 AND above_bound=0
                 AND unsupported_zero/(n-supported)>=0.01
                 AND least(unsupported_senders,unsupported_receivers,unsupported_banks)>=100,
                 false) all_criteria_met
            FROM counts""")
        report = fx.render("H-A11 — Single-transition FX residuals",
            {"July multibank residuals by pre-July directed two-bank evidence": summary,
             "Frozen decision and support": decision}, args.freeze or "exploration")
        if args.phase == "explore":
            report = report.replace(
                "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
                "Both-account bit-0 exploration only. A03–A08 outcome exposure applies.")
        report += ("\nThe existing H-A03 graph uses all bit-0 two-bank dates. Only the "
                   "directed two-bank rates in this diagnostic use pre-July dates. "
                   "Undisplayed small cells remain in the pooled denominator. "
                   "No country pair or bank identity is exported.\n")
        (HERE / f"out/H-A11_fx_transition_residuals_{args.phase}.md").write_text(report, encoding="utf-8")
        print("OK: aggregate FX transition screen saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
