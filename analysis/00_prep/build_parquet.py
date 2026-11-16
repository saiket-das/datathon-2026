"""Step 0: convert the organiser CSV to a typed Parquet file (one-off, ~few minutes).

Run from the repo root:
    uv run python analysis/00_prep/build_parquet.py

Input : dataset/swift_umdac_datathon_2026_fictitious_payment_data.csv  (never committed)
Output: dataset/payments.parquet                                        (git-ignored)

Options:
    --verify-only   check an existing Parquet against the CSV without rebuilding (~1-2 min)
    --independent   also re-read the CSV with Python's own csv parser (slower, see below)
    --src, --out    override the two paths (used by the tests)
    --show-error-detail   print DuckDB's full error text when something fails. That text can
                          quote a value or a whole line from the CSV, so it is off by default:
                          never paste it into an AI chat, an issue or a pull request.
The DUCKDB_MEMORY_LIMIT environment variable overrides the 5GB memory cap.

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

Safety: the Parquet is written to a temporary file, verified, and only then moved into
place, so a failed run never replaces an existing payments.parquet. Only aggregate checks
are printed, never records.

What the verification does. For every record an MD5 digest is taken over its position in
the file and all 20 original columns; the digests are combined (XOR and sum) into one
fingerprint. The fingerprint of a second, separate read of the CSV is compared with the
fingerprint of the Parquet as read back from disk. A changed, swapped, reordered, missing
or unreadable value changes the fingerprint.

What it does not prove.
- It is a digest comparison, not a value-by-value comparison: two different files giving
  the same fingerprint is possible in principle, but not a realistic outcome of accidental
  damage.
- Both reads use DuckDB's CSV parser, and record order is taken from DuckDB's sequential
  read. A parser fault that repeats identically in both reads would not be seen.
  --independent narrows this: it recomputes the CSV fingerprint with Python's csv module
  and hashlib, which share no code with DuckDB.
- Numbers are compared after conversion (the text "1.50" and the value 1.5 are equal). The
  count of numeric fields whose text is not exactly reproduced by its typed value is reported.
- The five helper columns are not in the fingerprint; they are recomputed from the stored
  columns and compared.
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
NUMERIC = {**{c: "BIGINT" for c in INTEGERS}, "USD_AMOUNT": "DOUBLE"}
HELPERS = {  # helper column -> its definition in terms of stored columns
    "ts_utc": "make_timestamp(EPOCH_SECONDS * 1000000)",
    "ord_country": "substr(ORDERING_BIC8, 5, 2)",
    "ben_country": "substr(BENEFICIARY_BIC8, 5, 2)",
    "path_len": "len(string_split(BIC8_PATH, ';'))",
    "gap_count": "list_count(list_filter(string_split(BIC8_PATH, ';'), lambda x: x = '...'))",
}


def fingerprint_sql(source, row_id, fields):
    """SQL returning (records, xor_hi, xor_lo, sum_hi, sum_lo) over one MD5 digest per record.

    Each record is serialised as '<row id>|' followed by every field as '<byte length>:<text>'
    ('N' for a missing value), which cannot be confused across field boundaries.
    """
    text = " || ".join(f"coalesce(strlen({f}) || ':' || {f}, 'N')" for f in fields)
    return f"""
      SELECT count(*), bit_xor(hi), bit_xor(lo), sum(hi::HUGEINT), sum(lo::HUGEINT)
      FROM (SELECT ('0x' || substr(h, 1, 16))::UBIGINT AS hi, ('0x' || substr(h, 17, 16))::UBIGINT AS lo
            FROM (SELECT md5(({row_id})::VARCHAR || '|' || {text}) AS h FROM {source}))"""


def python_fingerprint(src):
    """The same fingerprint computed without DuckDB: Python's csv parser and hashlib."""
    import csv
    import hashlib

    csv.field_size_limit(2**31 - 1)
    canon = {"BIGINT": lambda v: str(int(v)), "DOUBLE": lambda v: repr(float(v))}
    n = xor_hi = xor_lo = sum_hi = sum_lo = 0
    with open(src, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        picks = [(header.index(c), canon.get(NUMERIC.get(c))) for c in COLUMNS]
        for n, row in enumerate(reader, 1):
            parts = [f"{n}|"]
            for index, convert in picks:
                value = row[index]
                if value == "":
                    parts.append("N")
                else:
                    if convert:
                        value = convert(value)
                    parts.append(f"{len(value.encode('utf-8'))}:{value}")
            digest = hashlib.md5("".join(parts).encode("utf-8")).hexdigest()
            hi, lo = int(digest[:16], 16), int(digest[16:], 16)
            xor_hi ^= hi; xor_lo ^= lo; sum_hi += hi; sum_lo += lo
    return (n, xor_hi, xor_lo, sum_hi, sum_lo)


def verify(con, src, parquet, independent=False):
    """Compare a Parquet file with the CSV. Returns (problems, stats); prints nothing."""
    csv_read = f"read_csv({sql_str(src)}, header=true, quote='\"', escape='\"', all_varchar=true"
    pq_read = f"read_parquet({sql_str(parquet)})"  # explicit reader: the temporary file does not end in .parquet
    problems = []

    # 1. Record count from a parallel CSV read (a different scan path from the sequential one).
    csv_n = con.sql(f"SELECT count(*) FROM {csv_read})").fetchall()[0][0]

    # 2. Row-level fingerprint: sequential CSV read (file order) against the Parquet read back from disk.
    typed = [f"({c}::{NUMERIC[c]})::VARCHAR" if c in NUMERIC else c for c in COLUMNS]
    inexact = " + ".join(f"count(*) FILTER ({c} <> ({c}::{NUMERIC[c]})::VARCHAR)" for c in NUMERIC)
    csv_seq = f"(SELECT row_number() OVER () AS rid, * FROM {csv_read}, parallel=false))"
    csv_fp = con.sql(fingerprint_sql(csv_seq, "rid", typed)).fetchall()[0]
    inexact_n = con.sql(f"SELECT {inexact} FROM {csv_read})").fetchall()[0][0]
    pq_fp = con.sql(fingerprint_sql(pq_read, "ROW_ID", [f"{c}::VARCHAR" for c in COLUMNS])).fetchall()[0]

    # 3. Structure of the Parquet: row ids, helper columns, summary counts.
    helpers = ", ".join(f"count(*) FILTER ({name} IS DISTINCT FROM {expr})" for name, expr in HELPERS.items())
    cols = [r[0] for r in con.sql(f"DESCRIBE SELECT * FROM {pq_read}").fetchall()]
    nulls = ", ".join(f"count(*) - count({c})" for c in cols if c != "ANOMALY_TYPE")
    n, r0, r1, t0, t1, labelled, gaps, qn, *rest = con.sql(f"""
      SELECT count(*), min(ROW_ID), max(ROW_ID), min(ts_utc), max(ts_utc), count(ANOMALY_TYPE),
             count(*) FILTER (gap_count > 0), count(*) FILTER (CONTINUITY_QFLAG = 'N'), {helpers}, {nulls}
      FROM {pq_read}""").fetchall()[0]
    helper_bad, null_counts = rest[:len(HELPERS)], rest[len(HELPERS):]

    if cols != ["ROW_ID", *COLUMNS, *HELPERS]:
        problems.append("Parquet columns are not the expected 26 columns in the expected order")
    if n == 0:
        problems.append("no records were read")
    if not (n == csv_n == csv_fp[0] == pq_fp[0]):
        problems.append(f"record counts differ: CSV {csv_n} (parallel read), {csv_fp[0]} (sequential read), Parquet {n}")
    if (r0, r1) != (1, n):
        problems.append(f"ROW_ID runs {r0}..{r1}, expected 1..{n}")
    if csv_fp != pq_fp:
        problems.append("row-level fingerprint differs between the CSV and the Parquet: at least one value, "
                        "row position or record differs")
    wrong = [name for name, bad in zip(HELPERS, helper_bad) if bad]
    if wrong:
        problems.append(f"helper columns do not match their definition: {', '.join(wrong)}")
    if independent and not problems:
        if python_fingerprint(src) != pq_fp:
            problems.append("independent check failed: the fingerprint computed with Python's csv parser "
                            "differs from the Parquet")
    stats = dict(n=n, r0=r0, r1=r1, t0=t0, t1=t1, labelled=labelled, gaps=gaps, qn=qn,
                 missing=sum(1 for v in null_counts if v), inexact=inexact_n, independent=independent)
    return problems, stats


def report(stats):
    print(f"    records            {stats['n']:,} (same count from two separate CSV reads)")
    print("    content            row-level MD5 fingerprint of all 20 original columns matches the CSV, in file order")
    if stats["independent"]:
        print("    independent check  fingerprint recomputed with Python's csv parser also matches")
    print(f"    numeric text       {stats['inexact']:,} numeric fields whose CSV text differs from its typed value")
    print(f"    ROW_ID             {stats['r0']}..{stats['r1']}")
    print(f"    ts_utc             {stats['t0']} .. {stats['t1']}")
    print(f"    anomaly-labelled   {stats['labelled']:,}")
    print(f"    paths with a gap   {stats['gaps']:,}   CONTINUITY_QFLAG = N: {stats['qn']:,}")
    print(f"    columns containing missing values (ANOMALY_TYPE excluded): {stats['missing']}")
    if stats["missing"]:
        print("    NOTE: missing values found. Nothing was dropped; log it in findings/issues_log.md.")


def connect(spill_dir):
    con = duckdb.connect()
    con.execute(f"SET memory_limit={sql_str(os.environ.get('DUCKDB_MEMORY_LIMIT', '5GB'))}")
    con.execute(f"SET temp_directory={sql_str(spill_dir / '.duckdb_tmp')}")
    con.execute("SET threads=8; SET preserve_insertion_order=true")
    return con


def sql_str(value):
    """Quote a path or setting as a SQL string literal."""
    text = value.as_posix() if isinstance(value, pathlib.Path) else str(value)
    return "'" + text.replace("'", "''") + "'"


SHOW_ERROR_DETAIL = False


def describe(exc):
    """Error text that is safe to display: DuckDB messages can quote values from the data."""
    if SHOW_ERROR_DETAIL or isinstance(exc, RuntimeError):  # RuntimeError: our own aggregate-only messages
        return str(exc)
    return (f"{type(exc).__name__} (detail hidden because it may quote a record; "
            "re-run with --show-error-detail to see it locally)")


def build(src, out, independent=False):
    if not src.is_file():
        sys.exit(f"ERROR: input CSV not found: {src}\nSee dataset/README.md for how to get it.")
    out.parent.mkdir(parents=True, exist_ok=True)
    partial = out.with_name(out.name + ".partial")
    partial.unlink(missing_ok=True)
    con = connect(out.parent)
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
          FROM read_csv({sql_str(src)}, header=true, quote='"', escape='"', all_varchar=true, parallel=false)
        ) TO {sql_str(partial)} (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 500000)
        """)
        problems, stats = verify(con, src, partial, independent)
        if problems:
            raise RuntimeError("verification failed: " + "; ".join(problems))
    except Exception as exc:
        partial.unlink(missing_ok=True)
        sys.exit(f"ERROR: build failed, {out.name} was left untouched.\n{describe(exc)}")
    finally:
        con.close()

    os.replace(partial, out)
    print(f"OK  wrote {out}")
    report(stats)


def verify_only(src, out, independent=False):
    for path in (src, out):
        if not path.is_file():
            sys.exit(f"ERROR: file not found: {path}")
    try:
        problems, stats = verify(connect(out.parent), src, out, independent)
    except Exception as exc:
        problems = [f"the file could not be read back: {describe(exc)}"]
    if problems:
        sys.exit(f"ERROR: {out.name} does NOT match the CSV. Rebuild it.\n" + "\n".join(problems))
    print(f"OK  {out} matches the CSV")
    report(stats)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert the organiser CSV to dataset/payments.parquet")
    parser.add_argument("--src", type=pathlib.Path, default=DEFAULT_SRC)
    parser.add_argument("--out", type=pathlib.Path, default=DEFAULT_OUT)
    parser.add_argument("--verify-only", action="store_true", help="check the existing Parquet, do not rebuild")
    parser.add_argument("--independent", action="store_true", help="also re-read the CSV with Python's csv parser")
    parser.add_argument("--show-error-detail", action="store_true",
                        help="print full DuckDB errors (may quote a record; keep it local)")
    args = parser.parse_args()
    SHOW_ERROR_DETAIL = args.show_error_detail
    (verify_only if args.verify_only else build)(args.src, args.out, args.independent)
