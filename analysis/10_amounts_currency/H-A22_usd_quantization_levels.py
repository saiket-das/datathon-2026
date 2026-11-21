"""Explore USD quantization levels and leading-digit point masses.

Run: uv run python analysis/10_amounts_currency/H-A22_usd_quantization_levels.py
Only positive unlabelled July both-account bit-0 payments; aggregate output.
No validation population is queried and no generator mixture is assumed.
"""
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys

import duckdb

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("foundation", HERE.parent / "00_prep/scientific_checks.py")
foundation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(foundation)


def table(columns: list[str], rows: list[tuple]) -> list[str]:
    """Render verified aggregate cells as Markdown."""
    return ["| " + " | ".join(columns) + " |",
            "| " + " | ".join(["---"] * len(columns)) + " |"] + [
                "| " + " | ".join(map(str, row)) + " |" for row in rows]


def main() -> int:
    """Characterize nested grids without selecting a new confirmation test."""
    if datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        return 1
    try:
        with duckdb.connect() as con:
            con.execute("SET memory_limit='512MB'; SET threads=1; SET temp_directory=''; SET preserve_insertion_order=false")
            split = foundation.partition_sql("accounts")
            con.execute(f"""CREATE TEMP TABLE scope AS
                SELECT USD_AMOUNT amount, ORDERING_ACCOUNT sender,
                    BENEFICIARY_ACCOUNT receiver,
                    floor(log10(USD_AMOUNT))::INT magnitude,
                    pow(10, floor(log10(USD_AMOUNT))) place
                FROM read_parquet('dataset/payments.parquet')
                WHERE {split}='explore' AND CURRENCY_CODE='USD'
                    AND ANOMALY_TYPE IS NULL AND USD_AMOUNT>0
                    AND ts_utc>=TIMESTAMP '2023-07-01'""")
            con.execute("""CREATE VIEW shape AS SELECT *,
                floor(amount/place+1e-10)::INT lead_digit,
                abs(amount-round(amount))<1e-6 whole,
                abs(amount-round(amount/place)*place)<1e-6 q1,
                abs(amount-round(amount/(place/10))*(place/10))<1e-6 q2,
                abs(amount-round(amount/(place/100))*(place/100))<1e-6 q3,
                abs(amount-round(amount/(place/1000))*(place/1000))<1e-6 q4
                FROM scope""")
            support = con.execute("""SELECT count(*) n,count(DISTINCT sender) senders,
                count(DISTINCT receiver) receivers,
                count(*) FILTER(WHERE magnitude BETWEEN 2 AND 6) selected,
                count(*) FILTER(WHERE magnitude NOT BETWEEN 2 AND 6) excluded
                FROM shape""").fetchall()
            result = con.execute("""SELECT magnitude,count(*) n,
                count(DISTINCT sender) senders,count(DISTINCT receiver) receivers,
                round(avg(q1::INT),6) one_sig,
                round(avg((q2 AND NOT q1)::INT),6) second_only,
                round(avg((q3 AND NOT q2)::INT),6) third_only,
                round(avg((q4 AND NOT q3)::INT),6) fourth_only,
                round(avg(whole::INT),6) whole,
                round(avg((NOT whole)::INT),6) fractional
                FROM shape WHERE magnitude BETWEEN 2 AND 6 GROUP BY magnitude ORDER BY magnitude""")
            cols = [c[0] for c in result.description]
            levels = result.fetchall()
            # Suppress the entire family if a complementary cohort is too small.
            if any(min(row[1:4]) < 100 for row in levels):
                raise ValueError("Unsafe magnitude family")
            result = con.execute("""SELECT lead_digit,count(*) n,
                count(DISTINCT sender) senders,count(DISTINCT receiver) receivers,
                count(*) FILTER(WHERE q1) one_sig_n,
                count(DISTINCT sender) FILTER(WHERE q1) one_sig_senders,
                count(DISTINCT receiver) FILTER(WHERE q1) one_sig_receivers,
                round(avg(q1::INT),6) one_sig_share,
                round(avg(whole::INT),6) whole_share
                FROM shape WHERE magnitude BETWEEN 2 AND 6
                GROUP BY lead_digit ORDER BY lead_digit""")
            leading_cols = [c[0] for c in result.description]
            digits = result.fetchall()
            if len(digits) != 9 or any(min(row[1:7]) < 100 or row[1]-row[4] < 100 for row in digits):
                raise ValueError("Unsafe digit family")
        lines = ["# H-A22 — USD quantization level screen", "",
            "Exploration only: positive unlabelled July USD both-account bit-0.",
            "Phase0/Round1 and A02/A10/A18 rounding exposure applies. A19 exposed UTC daily alignment; A09/A13 exposed rate movement. No new holdout is claimed.",
            "512 MB, one thread, no spill. No data, account or bank identifiers exported.", "",
            "## Population", ""] + table(["n", "senders", "receivers", "selected_decades_2_to_6", "excluded_decades"], support)
        lines += ["", "## Nested significant-digit grid increments", ""] + table(cols, levels)
        lines += ["", "## Leading-digit grid point masses, pooled selected decades", ""] + table(leading_cols, digits)
        lines += ["", "Grid predicates describe exact compatibility within absolute USD tolerance1e-6, not latent rounding operations. The first four columns of shares form nested-grid increments; whole/fractional overlap those increments. Leading bins are [d,d+1) in decimal mantissa, so point masses sit at bin boundaries. Their shares are not a fitted continuous-density control. Rounding can move values across observed decades. No mixture weights or causal generation stages are identified.", ""]
        (HERE / "out/H-A22_usd_quantization_levels_explore.md").write_text("\n".join(lines), encoding="utf-8")
        print("OK: aggregate USD quantization exploration saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
