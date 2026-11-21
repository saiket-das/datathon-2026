"""Explore whether path gaps concentrate the frozen H-A03 FX-count residuals.

Run from the repository root:
    uv run python analysis/10_amounts_currency/H-A04_fx_gap_residuals.py

Both-account exploration only. Save grouped counts and rates; never export rows.
"""
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("fx_country_classes", HERE / "H-A03_fx_country_classes.py")
fx_model = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fx_model)


def main() -> int:
    """Measure gap-stratified signed errors with the unchanged exploration fit."""
    cutoff = datetime(2026, 11, 18, 12, tzinfo=timezone.utc)
    if datetime.now(timezone.utc) >= cutoff:
        print("Research cutoff reached. Exploration closed.", file=sys.stderr)
        return 1
    try:
        with fx_model.connect() as con:
            # Add the prepared gap count to the existing model's required columns.
            split = fx_model.foundation.partition_sql("accounts")
            con.execute(f"""CREATE OR REPLACE VIEW source AS
                SELECT ORDERING_ACCOUNT oa, BENEFICIARY_ACCOUNT ba, ANOMALY_TYPE,
                       CURRENCY_CONVERSION_COUNT fx, TRANSACTION_TYPE_CODE route,
                       gap_count,
                       list_filter(string_split(BIC8_PATH, ';'), lambda x: x <> '...') path,
                       {split} split
                FROM read_parquet('dataset/payments.parquet')""")
            fx_model.train(con)
            fx_model.score(con, "explore")
            totals = fx_model.query(con, """SELECT
                count(*) payments, count(*) FILTER (WHERE eligible) eligible,
                count(*) FILTER (WHERE eligible AND predicted <> fx) mismatches
                FROM scored""")
            details = fx_model.query(con, """WITH grouped AS (
                SELECT
                    CASE WHEN grouping(route) = 1 THEN 'All' ELSE route END route,
                    CASE WHEN grouping(length) = 1 THEN 'All' ELSE length::VARCHAR END visible_banks,
                    has_gap, count(*) n, count(DISTINCT oa) senders,
                    count(DISTINCT ba) receivers,
                    count(*) FILTER (WHERE predicted > fx) overpredict,
                    count(*) FILTER (WHERE predicted < fx) underpredict
                FROM (
                    SELECT route, least(len(path), 5) length, gap_count > 0 has_gap,
                           oa, ba, predicted, fx
                    FROM scored WHERE eligible
                ) AS eligible_rows
                GROUP BY GROUPING SETS ((route,length,has_gap), (has_gap))
                HAVING count(*) >= 1000 AND count(DISTINCT oa) >= 100
                    AND count(DISTINCT ba) >= 100
            )
            SELECT route, visible_banks, has_gap, n, senders, receivers,
                CASE WHEN overpredict + underpredict >= 100 OR overpredict + underpredict = 0
                     THEN round(100.0 * (overpredict + underpredict) / n, 4)::VARCHAR ELSE '<100 errors' END error_pct,
                CASE WHEN overpredict >= 100 OR overpredict = 0 THEN overpredict::VARCHAR ELSE '<100' END overpredict,
                CASE WHEN underpredict >= 100 OR underpredict = 0 THEN underpredict::VARCHAR ELSE '<100' END underpredict
            FROM grouped ORDER BY route, visible_banks, has_gap""")
            assert sum(row[3] for row in details[1] if row[0] == "All") == totals[1][0][1]
        tables = {"Unlabelled multibank coverage": totals, "Signed errors by gap and route-length group": details}
        report = fx_model.render("H-A04: FX residuals and path gaps", tables, "exploration only")
        report = report.replace(
            "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
            "Only both-account exploration records queried. Five visible banks denotes five or more."
        )
        output = HERE / "out/H-A04_fx_gap_residuals_explore.md"
        output.write_text(report, encoding="utf-8")
        print("OK: aggregate exploration report written.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
