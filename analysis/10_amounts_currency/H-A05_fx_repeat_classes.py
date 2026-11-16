"""Test whether the H-A03 class-change count tightens the country-count upper bound.

Run: uv run python analysis/10_amounts_currency/H-A05_fx_repeat_classes.py
Internal validation: add --phase validate --freeze <commit>. Uses the unchanged H-A03 fit.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("fx_country_classes", HERE / "H-A03_fx_country_classes.py")
fx_model = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fx_model)

SCREEN = """WITH metrics AS (
    SELECT route, gap_count > 0 has_gap, oa, ba, fx, predicted, country_predicted, wrong_predicted,
           list_unique(groups) - 1 unique_classes
    FROM scored WHERE eligible
), grouped AS (
    SELECT CASE WHEN grouping(route)=1 THEN 'All' ELSE route END route,
           CASE WHEN grouping(has_gap)=1 THEN 'All' ELSE has_gap::VARCHAR END gap,
           CASE WHEN grouping(reentry)=1 THEN 'All' ELSE reentry::VARCHAR END reentry,
           count(*) n, count(DISTINCT oa) senders, count(DISTINCT ba) receivers,
           count(*) FILTER (WHERE country_predicted > predicted) tighter_bound,
           count(*) FILTER (WHERE fx > country_predicted) above_country,
           count(*) FILTER (WHERE fx > predicted) above_class,
           count(*) FILTER (WHERE fx > wrong_predicted) above_shifted_class,
           count(*) FILTER (WHERE fx < predicted) below_class,
           count(*) FILTER (WHERE predicted <> fx AND unique_classes=fx) repeat_repaired,
           count(*) FILTER (WHERE predicted=fx AND unique_classes<>fx) repeat_broken,
           count(*) FILTER (WHERE predicted <> fx AND greatest(0,predicted-1)=fx) minus_one_repaired
    FROM (
        SELECT *, predicted > unique_classes AS reentry FROM metrics
    ) rows
    GROUP BY GROUPING SETS ((),(reentry),(route,has_gap,reentry))
    HAVING count(*) >= 1000 AND count(DISTINCT oa) >= 100 AND count(DISTINCT ba) >= 100
)
SELECT route,gap,reentry,n,senders,receivers,
       CASE WHEN tighter_bound BETWEEN 1 AND 99 THEN '<100' ELSE tighter_bound::VARCHAR END tighter_bound,
       CASE WHEN above_country BETWEEN 1 AND 99 THEN '<100' ELSE above_country::VARCHAR END above_country,
       CASE WHEN above_class BETWEEN 1 AND 99 THEN '<100' ELSE above_class::VARCHAR END above_class,
       CASE WHEN above_shifted_class BETWEEN 1 AND 99 THEN '<100' ELSE above_shifted_class::VARCHAR END above_shifted_class,
       CASE WHEN below_class BETWEEN 1 AND 99 THEN '<100' ELSE below_class::VARCHAR END below_class,
       CASE WHEN repeat_repaired BETWEEN 1 AND 99 THEN '<100' ELSE repeat_repaired::VARCHAR END repeat_repaired,
       CASE WHEN repeat_broken BETWEEN 1 AND 99 THEN '<100' ELSE repeat_broken::VARCHAR END repeat_broken,
       CASE WHEN minus_one_repaired BETWEEN 1 AND 99 THEN '<100' ELSE minus_one_repaired::VARCHAR END minus_one_repaired
FROM grouped ORDER BY route,gap,reentry"""


def main() -> int:
    """Save only grouped checks of country/class bounds and class reentry."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=["explore", "validate"], default="explore")
    parser.add_argument("--freeze")
    args = parser.parse_args()
    if args.phase == "explore" and datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        print("Research cutoff reached. Exploration closed.", file=sys.stderr)
        return 1
    try:
        if args.phase == "validate":
            if not args.freeze:
                raise ValueError("Validation requires a freeze commit.")
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", args.freeze, "HEAD"],
                cwd=fx_model.ROOT, check=True, capture_output=True,
            )
            freeze = subprocess.check_output(
                ["git", "rev-parse", args.freeze], cwd=fx_model.ROOT, text=True,
            ).strip()
            sources = [
                Path(__file__).resolve(),
                Path(fx_model.__file__),
                Path(fx_model.foundation.__file__),
                fx_model.ROOT / "findings/hypotheses/H-A05_fx_repeat_classes.md",
            ]
            for path in sources:
                frozen = subprocess.check_output(
                    ["git", "show", f"{freeze}:{path.relative_to(fx_model.ROOT).as_posix()}"],
                    cwd=fx_model.ROOT, stderr=subprocess.DEVNULL,
                )
                expected = frozen.replace(b"\r\n", b"\n")
                current = path.read_bytes().replace(b"\r\n", b"\n")
                if path.suffix == ".md":
                    # Results may be appended after the frozen methods and exposure sections.
                    marker = b"\n## Validation and robustness results"
                    expected = expected.split(marker, 1)[0]
                    current = current.split(marker, 1)[0]
                if expected != current:
                    raise ValueError("Current test differs from the freeze.")
        else:
            freeze = "exploration only"
        with fx_model.connect() as con:
            split = fx_model.foundation.partition_sql("accounts")
            con.execute(f"""CREATE OR REPLACE VIEW source AS
                SELECT ORDERING_ACCOUNT oa, BENEFICIARY_ACCOUNT ba, ORDERING_BIC8 ob, ANOMALY_TYPE,
                       CURRENCY_CONVERSION_COUNT fx, TRANSACTION_TYPE_CODE route,
                       gap_count,
                       list_filter(string_split(BIC8_PATH, ';'), lambda x: x <> '...') path,
                       {split} split
                FROM read_parquet('dataset/payments.parquet')""")
            fx_model.train(con)
            fx_model.score(con, args.phase)
            table = fx_model.query(con, SCREEN)
            _, [(n, eligible, tightened, senders, receivers, banks, violations)] = fx_model.query(con, """
                SELECT count(*), count(*) FILTER (WHERE eligible),
                       count(*) FILTER (WHERE eligible AND predicted < country_predicted),
                       count(DISTINCT oa) FILTER (WHERE eligible AND predicted < country_predicted),
                       count(DISTINCT ba) FILTER (WHERE eligible AND predicted < country_predicted),
                       count(DISTINCT ob) FILTER (WHERE eligible AND predicted < country_predicted),
                       count(*) FILTER (WHERE eligible AND fx > predicted)
                FROM scored""")
        decision = eligible * 10 >= n * 9 and tightened * 10 >= eligible and min(senders, receivers, banks) >= 100 and violations == 0
        support = (
            ["scoped", "eligible", "tightened", "tightened_senders", "tightened_receivers",
             "tightened_ordering_banks", "violations", "all_criteria_met"],
            [(n, eligible, tightened, senders, receivers, banks,
             "<100" if 0 < violations < 100 else violations, decision)],
        )
        report = fx_model.render(
            "H-A05: FX bounds and repeat-class alternatives",
            {"Primary scoped coverage and decision": support, "Bound violations and candidate corrections": table},
            freeze,
        ).replace(
            "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
            "Both-account bit-0 exploration only." if args.phase == "explore" else
            "Both-account bit-1 internal validation. Records, support and unsigned errors were previously exposed.",
        )
        report += "\nSee the H-A05 exposure audit for Phase 0, Round 1 and A03/A04 constraints.\n"
        (HERE / f"out/H-A05_fx_repeat_classes_{args.phase}.md").write_text(report, encoding="utf-8")
        print(f"OK: aggregate {args.phase} report written. All criteria met: {decision}.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
