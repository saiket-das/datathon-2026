"""Explore whether USD heaping varies with amount magnitude and party type.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A18_usd_heaping_shape.py
Only unlabelled both-account bit-0 payments. Outputs broad aggregates.
"""
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("fx",HERE/"H-A03_fx_country_classes.py")
fx = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fx)


def main() -> int:
    """Compare decimal place and significant digit heaping."""
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        return 1
    try:
        with fx.connect() as con:
            split = fx.foundation.partition_sql("accounts")
            con.execute(f"""CREATE VIEW scope AS
                SELECT USD_AMOUNT amount,ORDERING_ACCOUNT oa,BENEFICIARY_ACCOUNT ba,
                  ORDERING_TYPE||BENEFICIARY_TYPE parties
                FROM read_parquet('dataset/payments.parquet')
                WHERE {split}='explore' AND CURRENCY_CODE='USD'
                  AND ANOMALY_TYPE IS NULL AND ts_utc>=TIMESTAMP '2023-07-01'
                  AND USD_AMOUNT>0""")
            con.execute("""CREATE VIEW shape AS
                SELECT *,floor(log10(amount))::INT magnitude,
                  round(amount*100)::BIGINT cents,
                  pow(10,floor(log10(amount))) place
                FROM scope""")
            support = fx.query(con,"""SELECT count(*) n,count(DISTINCT oa) senders,
                count(DISTINCT ba) receivers FROM shape""")
            tables = fx.query(con,"""WITH groups AS (
                SELECT CASE WHEN grouping(parties)=1 THEN 'All' ELSE parties END parties,
                  magnitude,count(*) n,count(DISTINCT oa) senders,count(DISTINCT ba) receivers,
                  avg((cents%100=0)::INT) integer_share,
                  avg((cents%100=50)::INT) half_only_share,
                  avg((abs(amount-round(amount/place)*place)<.000001)::INT) one_digit,
                  avg((abs(amount-round(amount/(place/10))*(place/10))<.000001)::INT) two_digit
                FROM shape GROUP BY GROUPING SETS ((magnitude),(magnitude,parties))
                HAVING count(*)>=2000 AND count(DISTINCT oa)>=100 AND count(DISTINCT ba)>=100
              ) SELECT parties,magnitude,n,senders,receivers,round(integer_share,5) integer_share,
                  round(half_only_share,5) half_only_share,round(one_digit,5) one_digit,
                  round(two_digit,5) two_digit FROM groups ORDER BY 1,2""")
        assert support[1][0][0] >= sum(row[2] for row in tables[1] if row[0]=="All")
        report = fx.render("H-A18 — USD decimal place versus significant digit heaping",
            {"July bit-0 positive unlabelled USD":support,"Magnitude and party groups":tables},"exploration")
        report = report.replace(
            "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
            "Both-account bit-0 only. Phase 0 and A01–A17 prior exposure applies.")
        report += ("\nSignificant digit predicates mean divisible by the decimal place inferred "
                   "from the observed amount, allowing USD-floating representation error. "
                   "They do not identify how many digits were rounded before output. "
                   "Displayed groups overlap and omit small group cells.\n")
        (HERE/"out/H-A18_usd_heaping_shape_explore.md").write_text(report,encoding="utf-8")
        print("OK: aggregate USD heaping screen saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())
