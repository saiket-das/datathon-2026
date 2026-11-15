"""Step 1: first-pass profile of the dataset (counts, nulls, categorical mixes, time, amounts).

Run from the repo root, after build_parquet.py:
    uv run python analysis/00_prep/profile.py
Prints aggregate tables only; no raw records. Exits with status 1 if the Parquet file
is missing or any query fails, so a broken setup cannot pass unnoticed.
Optional: --src overrides the Parquet path (used by the tests).
"""
import argparse
import pathlib
import sys

import duckdb

parser = argparse.ArgumentParser(description="Aggregate profile of dataset/payments.parquet")
parser.add_argument("--src", type=pathlib.Path,
                    default=pathlib.Path(__file__).resolve().parents[2] / "dataset" / "payments.parquet")
SRC = parser.parse_args().src
if not SRC.is_file():
    sys.exit(f"ERROR: {SRC} not found. Run analysis/00_prep/build_parquet.py first (see dataset/README.md).")

con = duckdb.connect()
con.execute("SET memory_limit='5GB'; SET threads=8; SET TimeZone='UTC'")
con.execute("CREATE VIEW t AS SELECT * FROM '" + SRC.as_posix().replace("'", "''") + "'")
failed = []
def q(title, sql):
    print("\n##", title)
    try: print(con.sql(sql).df().to_string(max_rows=60, max_colwidth=60))
    except Exception as e:
        failed.append(title); print("ERR", e)
q("overall", """SELECT count(*) n,
 min(EPOCH_SECONDS::BIGINT) tmin, max(EPOCH_SECONDS::BIGINT) tmax,
 to_timestamp(min(EPOCH_SECONDS::BIGINT)) dmin, to_timestamp(max(EPOCH_SECONDS::BIGINT)) dmax,
 approx_count_distinct(CURRENCY_CODE) ccy, approx_count_distinct(ORDERING_BIC8) obic, approx_count_distinct(BENEFICIARY_BIC8) bbic,
 approx_count_distinct(BIC8_PATH) paths, approx_count_distinct(ORDERING_ACCOUNT) oacc, approx_count_distinct(BENEFICIARY_ACCOUNT) bacc,
 min(USD_AMOUNT::DOUBLE) amin, median(USD_AMOUNT::DOUBLE) amed, avg(USD_AMOUNT::DOUBLE) aavg, max(USD_AMOUNT::DOUBLE) amax,
 min(TOTAL_DURATION::BIGINT) dumin, median(TOTAL_DURATION::BIGINT) dumed, max(TOTAL_DURATION::BIGINT) dumax
 FROM t""")
q("nulls", "SELECT " + ",".join(f"sum(({c} IS NULL OR {c}::VARCHAR='')::INT) {c}" for c in
 "EPOCH_SECONDS CURRENCY_CODE USD_AMOUNT ORDERING_BIC8 BENEFICIARY_BIC8 BIC8_PATH TOTAL_DURATION CONTINUITY_QFLAG CURRENCY_CONVERSION_COUNT PARTICIPANT_COUNT TRANSACTION_TYPE_CODE ORDERING_ACCOUNT BENEFICIARY_ACCOUNT ORDERING_DETAILS ORDERING_TOKENS BENEFICIARY_DETAILS BENEFICIARY_TOKENS ORDERING_TYPE BENEFICIARY_TYPE ANOMALY_TYPE".split()) + " FROM t")
for c in ["ANOMALY_TYPE","TRANSACTION_TYPE_CODE","CONTINUITY_QFLAG","CURRENCY_CONVERSION_COUNT","PARTICIPANT_COUNT","ORDERING_TYPE||'->'||BENEFICIARY_TYPE"]:
    q(c, f"SELECT {c} v, count(*) n, round(100.0*count(*)/sum(count(*)) over(),4) pct, round(median(USD_AMOUNT::DOUBLE),2) med_amt, round(median(TOTAL_DURATION::BIGINT)) med_dur FROM t GROUP BY 1 ORDER BY n DESC")
q("currency top", "SELECT CURRENCY_CODE v, count(*) n, round(100.0*count(*)/sum(count(*)) over(),3) pct, round(median(USD_AMOUNT::DOUBLE),2) med FROM t GROUP BY 1 ORDER BY n DESC LIMIT 40")
q("type x participants x continuity", "SELECT TRANSACTION_TYPE_CODE, PARTICIPANT_COUNT, CONTINUITY_QFLAG, count(*) n, sum((BIC8_PATH LIKE '%...%')::INT) dots, min(len(string_split(BIC8_PATH,';'))) minlen, max(len(string_split(BIC8_PATH,';'))) maxlen FROM t GROUP BY ALL ORDER BY 1,2,3")
q("monthly", "SELECT strftime(to_timestamp(EPOCH_SECONDS::BIGINT),'%Y-%m') m, count(*) n, sum((ANOMALY_TYPE IS NOT NULL)::INT) anom FROM t GROUP BY 1 ORDER BY 1")
q("day of week UTC (0 = Sunday)", "SELECT dayofweek(to_timestamp(EPOCH_SECONDS::BIGINT)) dow, count(*) n FROM t GROUP BY 1 ORDER BY 1")
q("hour UTC", "SELECT hour(to_timestamp(EPOCH_SECONDS::BIGINT) AT TIME ZONE 'UTC') h, count(*) n FROM t GROUP BY 1 ORDER BY 1")
q("amount roundness", "SELECT sum((USD_AMOUNT::DOUBLE = round(USD_AMOUNT::DOUBLE))::INT) whole, sum((USD_AMOUNT::DOUBLE % 100 = 0)::INT) x100, sum((USD_AMOUNT::DOUBLE % 1000=0)::INT) x1000, count(*) n FROM t")
q("top amounts", "SELECT USD_AMOUNT, count(*) n FROM t GROUP BY 1 ORDER BY n DESC LIMIT 15")
q("repeated rows (same timestamp, amount, both accounts and path)", "SELECT count(*) groups, sum(c) rows FROM (SELECT count(*) c FROM t GROUP BY EPOCH_SECONDS,USD_AMOUNT,ORDERING_ACCOUNT,BENEFICIARY_ACCOUNT,BIC8_PATH HAVING count(*)>1)")
q("acct reuse", "SELECT approx_quantile(c,[0.5,0.9,0.99,0.999]) qs, max(c) mx FROM (SELECT count(*) c FROM t GROUP BY ORDERING_ACCOUNT)")
q("bic country ord (chars 5-6) top", "SELECT substr(ORDERING_BIC8,5,2) c, count(*) n, approx_count_distinct(ORDERING_BIC8) bics FROM t GROUP BY 1 ORDER BY n DESC LIMIT 25")
if failed:
    sys.exit(f"\nFAILED: {len(failed)} profile queries raised an error: {', '.join(failed)}")
print("\nOK: all profile queries ran.")
