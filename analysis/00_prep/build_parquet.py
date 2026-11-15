"""Step 0: convert the organiser CSV to a typed Parquet file (one-off, ~few minutes).

Run from the repo root:
    uv run --with duckdb --with pandas python analysis/00_prep/build_parquet.py

Input : dataset/swift_umdac_datathon_2026_fictitious_payment_data.csv  (never committed)
Output: dataset/payments.parquet                                        (git-ignored)

Decisions (also recorded in the issues log):
- DISCLAIMER is dropped: it is populated on the first record only and is not payment data.
- Party-detail fields contain embedded line breaks, so the file is read quote-aware.
- ROW_ID keeps the original record order (1-based) so order-dependent structure can be tested.
- Cheap, purely definitional helper columns are added (prefixed with lower case):
    ts_utc        EPOCH_SECONDS as a UTC timestamp
    ord_country   characters 5-6 of ORDERING_BIC8
    ben_country   characters 5-6 of BENEFICIARY_BIC8
    path_len      number of ';'-separated elements in BIC8_PATH (including '...' placeholders)
    gap_count     number of '...' placeholders in BIC8_PATH
"""
import pathlib
import duckdb

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "dataset" / "swift_umdac_datathon_2026_fictitious_payment_data.csv"
OUT = ROOT / "dataset" / "payments.parquet"
TMP = ROOT / "dataset" / ".duckdb_tmp"

con = duckdb.connect()
con.execute(f"SET memory_limit='5GB'; SET threads=8; SET temp_directory='{TMP}'; SET preserve_insertion_order=true")
con.execute(f"""
COPY (
  SELECT
    row_number() OVER ()                         AS ROW_ID,
    EPOCH_SECONDS::BIGINT                        AS EPOCH_SECONDS,
    CURRENCY_CODE,
    USD_AMOUNT::DOUBLE                           AS USD_AMOUNT,
    ORDERING_BIC8, BENEFICIARY_BIC8, BIC8_PATH,
    TOTAL_DURATION::BIGINT                       AS TOTAL_DURATION,
    CONTINUITY_QFLAG,
    CURRENCY_CONVERSION_COUNT::INTEGER           AS CURRENCY_CONVERSION_COUNT,
    PARTICIPANT_COUNT::INTEGER                   AS PARTICIPANT_COUNT,
    TRANSACTION_TYPE_CODE,
    ORDERING_ACCOUNT, BENEFICIARY_ACCOUNT,
    ORDERING_DETAILS, ORDERING_TOKENS, BENEFICIARY_DETAILS, BENEFICIARY_TOKENS,
    ORDERING_TYPE, BENEFICIARY_TYPE, ANOMALY_TYPE,
    make_timestamp(EPOCH_SECONDS::BIGINT * 1000000) AS ts_utc,
    substr(ORDERING_BIC8, 5, 2)                  AS ord_country,
    substr(BENEFICIARY_BIC8, 5, 2)               AS ben_country,
    len(string_split(BIC8_PATH, ';'))            AS path_len,
    list_count(list_filter(string_split(BIC8_PATH, ';'), lambda x: x = '...')) AS gap_count
  FROM read_csv('{SRC}', header=true, quote='"', escape='"', all_varchar=true, parallel=false)
) TO '{OUT}' (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 500000)
""")
print(con.sql(f"""SELECT count(*) n, min(ROW_ID) r0, max(ROW_ID) r1, min(ts_utc) t0, max(ts_utc) t1,
  sum((ANOMALY_TYPE IS NOT NULL)::INT) labelled, sum(gap_count>0) gaps, sum((CONTINUITY_QFLAG='N')::INT) qn
  FROM '{OUT}'""").df().to_string())
print(con.sql(f"SELECT ROW_ID, EPOCH_SECONDS, CURRENCY_CODE, USD_AMOUNT, BIC8_PATH FROM '{OUT}' WHERE ROW_ID<=3 ORDER BY 1").df().to_string())
