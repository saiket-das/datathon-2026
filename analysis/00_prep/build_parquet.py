"""Step 0: convert the organiser CSV to a typed Parquet file (one-off, ~few minutes).

Run from the repo root:
    uv run python analysis/00_prep/build_parquet.py

Input : dataset/swift_umdac_datathon_2026_fictitious_payment_data.csv  (never committed)
Output: dataset/payments.parquet                                        (git-ignored)

Optional: --src and --out override the two paths (used by the tests);
the DUCKDB_MEMORY_LIMIT environment variable overrides the 5GB memory cap.

Decisions (also recorded in the issues log):
- DISCLAIMER is dropped: it is populated on the first record only and is not payment data.
- Party-detail fields contain embedded line breaks, so the file is read quote-aware.
- ROW_ID keeps the original record order (1-based) so order-dependent structure can be tested.
- No record is filtered out. A value that cannot be cast to its type stops the build.
- Cheap, purely definitional helper columns are added (prefixed with lower case):
    ts_utc        EPOCH_SECONDS as a UTC timestamp
    ord_country   characters 5-6 of ORDERING_BIC8
    ben_country   characters 5-6 of BENEFICIARY_BIC8
    path_len      number of ';'-separated elements in BIC8_PATH (including '...' placeholders)
    gap_count     number of '...' placeholders in BIC8_PATH

Safety: the Parquet is written to a temporary file, checked, and only then moved into
place, so a failed run never leaves a half-written or unchecked payments.parquet and
never destroys an existing good one. Only aggregate checks are printed, never records.
"""
import argparse
import os
import pathlib
import sys

import duckdb

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_SRC = ROOT / "dataset" / "swift_umdac_datathon_2026_fictitious_payment_data.csv"
DEFAULT_OUT = ROOT / "dataset" / "payments.parquet"


COLUMNS = """EPOCH_SECONDS CURRENCY_CODE USD_AMOUNT ORDERING_BIC8 BENEFICIARY_BIC8 BIC8_PATH TOTAL_DURATION
CONTINUITY_QFLAG CURRENCY_CONVERSION_COUNT PARTICIPANT_COUNT TRANSACTION_TYPE_CODE ORDERING_ACCOUNT
BENEFICIARY_ACCOUNT ORDERING_DETAILS ORDERING_TOKENS BENEFICIARY_DETAILS BENEFICIARY_TOKENS ORDERING_TYPE
BENEFICIARY_TYPE ANOMALY_TYPE""".split()
INTEGERS = {"EPOCH_SECONDS", "TOTAL_DURATION", "CURRENCY_CONVERSION_COUNT", "PARTICIPANT_COUNT"}
# One exact number per column, compared between CSV and Parquet: the sum for integer
# columns, the sum in whole cents for the amount, the total text length otherwise.
FINGERPRINT = ", ".join(
    f"sum({c}::BIGINT)" if c in INTEGERS
    else f"sum(round({c}::DOUBLE * 100)::HUGEINT)" if c == "USD_AMOUNT"
    else f"sum(length({c}))"
    for c in COLUMNS)


def sql_str(value):
    """Quote a path or setting as a SQL string literal."""
    text = value.as_posix() if isinstance(value, pathlib.Path) else str(value)
    return "'" + text.replace("'", "''") + "'"


def build(src, out):
    if not src.is_file():
        sys.exit(f"ERROR: input CSV not found: {src}\nSee dataset/README.md for how to get it.")
    out.parent.mkdir(parents=True, exist_ok=True)
    partial = out.with_name(out.name + ".partial")
    partial.unlink(missing_ok=True)
    read = f"read_csv({sql_str(src)}, header=true, quote='\"', escape='\"', all_varchar=true"

    con = duckdb.connect()
    con.execute(f"SET memory_limit={sql_str(os.environ.get('DUCKDB_MEMORY_LIMIT', '5GB'))}")
    con.execute(f"SET temp_directory={sql_str(out.parent / '.duckdb_tmp')}")
    con.execute("SET threads=8; SET preserve_insertion_order=true")
    try:
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
          FROM {read}, parallel=false)
        ) TO {sql_str(partial)} (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 500000)
        """)

        # Aggregate-only verification of the temporary file against an independent CSV pass.
        # Every column is fully read back, so a damaged file fails here instead of later.
        csv_n, *csv_sums = con.sql(f"SELECT count(*), {FINGERPRINT} FROM {read})").fetchall()[0]
        pq_n, *pq_sums = con.sql(f"SELECT count(*), {FINGERPRINT} FROM read_parquet({sql_str(partial)})").fetchall()[0]
        n, r0, r1, t0, t1, labelled, gaps, qn, missing = _summary(con, partial)
        problems = []
        if n == 0:
            problems.append("no records were read")
        if pq_n != csv_n:
            problems.append(f"Parquet has {pq_n} records but the CSV has {csv_n}")
        if (r0, r1) != (1, n):
            problems.append(f"ROW_ID runs {r0}..{r1}, expected 1..{n}")
        differing = [c for c, a, b in zip(COLUMNS, csv_sums, pq_sums) if a != b]
        if differing:
            problems.append(f"content differs between CSV and Parquet in: {', '.join(differing)}")
        if problems:
            raise RuntimeError("; ".join(problems))
    except Exception as exc:
        partial.unlink(missing_ok=True)
        sys.exit(f"ERROR: build failed, {out.name} was left untouched.\n{exc}")

    os.replace(partial, out)
    print(f"OK  wrote {out}")
    print(f"    records            {n:,} (record count and every column match the CSV)")
    print(f"    ROW_ID             {r0}..{r1}")
    print(f"    ts_utc             {t0} .. {t1}")
    print(f"    anomaly-labelled   {labelled:,}")
    print(f"    paths with a gap   {gaps:,}   CONTINUITY_QFLAG = N: {qn:,}")
    print(f"    columns containing missing values (ANOMALY_TYPE excluded): {missing}")
    if missing:
        print("    NOTE: missing values found. Nothing was dropped; log it in findings/issues_log.md.")


def _summary(con, parquet):
    src = f"read_parquet({sql_str(parquet)})"  # explicit reader: the temporary file does not end in .parquet
    cols = [r[0] for r in con.sql(f"DESCRIBE SELECT * FROM {src}").fetchall()]
    nulls = ", ".join(f"count(*) - count({c})" for c in cols if c != "ANOMALY_TYPE")
    row = con.sql(f"""
      SELECT count(*), min(ROW_ID), max(ROW_ID), min(ts_utc), max(ts_utc),
             count(ANOMALY_TYPE), count(*) FILTER (gap_count > 0),
             count(*) FILTER (CONTINUITY_QFLAG = 'N'), {nulls}
      FROM {src}""").fetchall()[0]
    return (*row[:8], sum(1 for v in row[8:] if v))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert the organiser CSV to dataset/payments.parquet")
    parser.add_argument("--src", type=pathlib.Path, default=DEFAULT_SRC)
    parser.add_argument("--out", type=pathlib.Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    build(args.src, args.out)
