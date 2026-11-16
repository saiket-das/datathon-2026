"""Screen coherence of daily modal amount scales across currencies.

Run: uv run python analysis/10_amounts_currency/H-A09_modal_scale_coherence.py
Bit-0 exploration only. Daily peaks and dates remain in memory; export broad aggregates.
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


def main() -> int:
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        return 1
    try:
        with duckdb.connect() as con:
            con.execute("SET memory_limit='512MB'; SET threads=1; SET temp_directory=''; SET preserve_insertion_order=false")
            split=foundation.partition_sql("accounts")
            con.execute(f"""CREATE VIEW scope AS SELECT CURRENCY_CODE currency,
                USD_AMOUNT a,cast(ts_utc AS DATE) obs_date,ORDERING_ACCOUNT sender,
                BENEFICIARY_ACCOUNT receiver
                FROM read_parquet('dataset/payments.parquet')
                WHERE ANOMALY_TYPE IS NULL AND USD_AMOUNT>=100 AND USD_AMOUNT<2000000
                    AND {split}='explore'""")
            con.execute("""CREATE TEMP TABLE anchors AS
                WITH masses AS (
                    SELECT currency,obs_date,a,pow(10,floor(log10(a))) base,count(*) n
                    FROM scope GROUP BY currency,obs_date,a
                ), peaks AS (
                    SELECT *,row_number() OVER(PARTITION BY currency,obs_date,base
                        ORDER BY n DESC,a) rank FROM masses
                ), selected AS (
                    SELECT *,row_number() OVER(PARTITION BY currency,obs_date
                        ORDER BY base DESC,n DESC,a) choice
                    FROM peaks WHERE rank=1 AND n>=20
                )
                SELECT currency,obs_date,a/base scale,n FROM selected WHERE choice=1""")
            con.execute("""CREATE TEMP TABLE changes AS SELECT currency,obs_date,scale,n,
                ln(scale/lag(scale) OVER(PARTITION BY currency ORDER BY obs_date)) delta,
                obs_date-lag(obs_date) OVER(PARTITION BY currency ORDER BY obs_date) gap
                FROM anchors""")
            queries={
                "Daily peak support and stability": """SELECT currency,count(*) dates,sum(n) peak_payments,
                    round(stddev_pop(ln(scale)),6) log_scale_sd,
                    count(*) FILTER(WHERE gap=1) adjacent_days,
                    round(avg((abs(delta)<ln(1.1))::INT) FILTER(WHERE gap=1),6) small_change_share,
                    round(max(abs(delta)) FILTER(WHERE gap=1),6) max_log_jump
                    FROM changes GROUP BY currency HAVING count(*)>=60 AND sum(n)>=1000 ORDER BY currency""",
                "Same-day currency-change agreement": """SELECT count(*) currency_pairs,
                    min(matched_dates) min_days,max(matched_dates) max_days,
                    round(median(correlation),6) median_correlation,
                    round(min(correlation),6) minimum_correlation,
                    round(max(correlation),6) maximum_correlation
                    FROM (
                        SELECT a.currency ca,b.currency cb,count(*) matched_dates,corr(a.delta,b.delta) correlation
                        FROM changes a JOIN changes b ON a.obs_date=b.obs_date AND a.currency<b.currency
                        WHERE a.gap=1 AND b.gap=1 AND abs(a.delta)<ln(1.1) AND abs(b.delta)<ln(1.1)
                        GROUP BY 1,2 HAVING count(*)>=60
                    ) pairs WHERE correlation IS NOT NULL AND isfinite(correlation)""",
            }
            lines=["# H-A09: Daily modal-scale coherence","",
                "Exploration only, unlabelled both-account bit-0. Phase0/Round1/A03-A08 exposure applies.",
                "A daily amount peak with at least 20 payments is chosen at the highest supported decade.",
                "This generic peak is not an identified exchange rate. Changes over 10% can signal denominator switches.",
                "No date-specific peak, currency-pair identity or transaction is exported.",""]
            for title,query in queries.items():
                result=con.execute(query); columns=[c[0] for c in result.description]; rows=result.fetchall()
                lines += ["## "+title,"","| "+" | ".join(columns)+" |","| "+" | ".join(["---"]*len(columns))+" |"]
                lines += ["| "+" | ".join(map(str,row))+" |" for row in rows]
                lines.append("")
        (HERE/"out/H-A09_modal_scale_coherence_explore.md").write_text("\n".join(lines),encoding="utf-8")
        print("OK: aggregate modal-scale exploration report saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())
