"""Measure structural semantics and audit candidate validation partitions; infer no rules.

Run from the repository root:
    uv run python analysis/00_prep/scientific_checks.py
Writes safe aggregates to analysis/00_prep/out/scientific_checks.md. Optional
--src and --out support invented test fixtures. No source data is changed or copied.
All SQL is preserved below. DuckDB uses 2GB, two threads and no disk spilling.
"""

import argparse
from pathlib import Path
import sys

import duckdb

ROOT = Path(__file__).resolve().parents[2]
LABELS = (
    "ROMANCE_SCAM", "FAT_FINGER_MISTAKE", "CEO_SCAM", "DUPLICATE_PAYMENT",
    "ACCOUNT_REPLACEMENT_SCAM", "CUSTOMER_RECALL",
)
Table = tuple[list[str], list[tuple[object, ...]]]


def bucket(column: str) -> str:
    """Stable UTF-8 MD5 parity; same literal identifier gets the same bit in either role."""
    return f"(('0x' || substr(md5({column}), 1, 8))::UBIGINT % 2)"


def partition_sql(scheme: str) -> str:
    """Return one mutually exclusive assignment; crossing entities remain excluded."""
    sender, receiver = bucket("ORDERING_ACCOUNT"), bucket("BENEFICIARY_ACCOUNT")
    ordering, beneficiary = bucket("ORDERING_BIC8"), bucket("BENEFICIARY_BIC8")
    conditions = {
        "sender": (f"{sender}=0", f"{sender}=1"),
        "accounts": (f"{sender}=0 AND {receiver}=0", f"{sender}=1 AND {receiver}=1"),
        "banks": (f"{ordering}=0 AND {beneficiary}=0", f"{ordering}=1 AND {beneficiary}=1"),
        "time": (
            "ts_utc >= TIMESTAMP '2023-05-01' AND ts_utc < TIMESTAMP '2023-07-01'",
            "ts_utc >= TIMESTAMP '2023-07-01' AND ts_utc < TIMESTAMP '2023-07-31'",
        ),
    }
    explore, confirm = conditions[scheme]
    return f"CASE WHEN {explore} THEN 'explore' WHEN {confirm} THEN 'confirm' ELSE 'excluded' END"


def query(con: duckdb.DuckDBPyConnection, sql: str) -> Table:
    """Fetch only explicitly aggregated queries supplied by this module."""
    result = con.execute(sql)
    return [column[0] for column in result.description], result.fetchall()


STRUCTURE_SQL = """
WITH s AS (
  SELECT *, string_split(BIC8_PATH, ';') entries,
         list_filter(string_split(BIC8_PATH, ';'), lambda x: x <> '...') visible
  FROM t
), p AS (
  SELECT *, len(entries)-len(visible) gaps,
    list_sum(list_transform(range(1, len(visible)), lambda i:
      (substr(visible[i],5,2) <> substr(visible[i+1],5,2))::INT)) country_changes
  FROM s
)
SELECT count(*) records,
 count(*) FILTER (WHERE path_len IS DISTINCT FROM len(entries)) helper_path_bad,
 count(*) FILTER (WHERE gap_count IS DISTINCT FROM gaps) helper_gap_bad,
 count(*) FILTER (WHERE ts_utc IS DISTINCT FROM make_timestamp(EPOCH_SECONDS*1000000)) helper_time_bad,
 count(*) FILTER (WHERE ord_country IS DISTINCT FROM substr(ORDERING_BIC8,5,2)
                    OR ben_country IS DISTINCT FROM substr(BENEFICIARY_BIC8,5,2)) helper_country_bad,
 count(*) FILTER (WHERE PARTICIPANT_COUNT IS DISTINCT FROM len(entries)) participants_vs_entries,
 count(*) FILTER (WHERE PARTICIPANT_COUNT IS DISTINCT FROM len(visible)) participants_vs_visible,
 count(*) FILTER (WHERE (TRANSACTION_TYPE_CODE='Direct') IS DISTINCT FROM (PARTICIPANT_COUNT=2)) direct_iff_two_bad,
 count(*) FILTER (WHERE (CONTINUITY_QFLAG='N') IS DISTINCT FROM (gaps>0)) continuity_bad,
 count(*) FILTER (WHERE CURRENCY_CONVERSION_COUNT > PARTICIPANT_COUNT-1) fx_exceeds_links,
 count(*) FILTER (WHERE CURRENCY_CONVERSION_COUNT IS DISTINCT FROM country_changes) fx_vs_country_changes,
 count(*) FILTER (WHERE CURRENCY_CONVERSION_COUNT > country_changes) fx_exceeds_country_changes,
 count(*) FILTER (WHERE ORDERING_BIC8 IS DISTINCT FROM entries[1]) ordering_endpoint_mismatch,
 count(*) FILTER (WHERE BENEFICIARY_BIC8 IS DISTINCT FROM entries[-1]) beneficiary_endpoint_mismatch
FROM p
"""


def structural_checks(con: duckdb.DuckDBPyConnection) -> dict[str, Table]:
    """Measure definitions and exceptions without asserting a generator architecture."""
    tables = {"Structural counts (whole dataset)": query(con, STRUCTURE_SQL)}
    for role in ("ORDERING", "BENEFICIARY"):
        tables[f"Account consistency: {role}"] = query(con, f"""
          WITH a AS (
            SELECT {role}_ACCOUNT account, count(*) n,
              min({role}_TYPE) t0, max({role}_TYPE) t1,
              min({role}_BIC8) b0, max({role}_BIC8) b1
            FROM t GROUP BY 1
          ) SELECT count(*) accounts, count(*) FILTER (WHERE n>1) reused_accounts,
              count(*) FILTER (WHERE t0<>t1) multi_type,
              count(*) FILTER (WHERE b0<>b1) multi_bank FROM a
        """)
        # Repeated exact details must share a hash and occur at least twice. Hash collisions
        # can only add candidates; exact grouping below removes them. No token hash is used.
        con.execute(f"""CREATE OR REPLACE TEMP TABLE detail_candidates AS
          SELECT hash({role}_DETAILS) h FROM t GROUP BY 1
          HAVING count(*)>1
        """)
        tables[f"Visible details to tokens: {role}"] = query(con, f"""
          SELECT count(*) inconsistent_detail_groups, coalesce(sum(n),0) affected_rows
          FROM (SELECT {role}_DETAILS, count(*) n FROM t
            WHERE hash({role}_DETAILS) IN (SELECT h FROM detail_candidates)
            GROUP BY 1 HAVING min({role}_TOKENS) IS DISTINCT FROM max({role}_TOKENS))
        """)
    tables["Cross-role identity consistency"] = query(con, """
      WITH a AS (SELECT ORDERING_ACCOUNT account, min(ORDERING_TYPE) t0, max(ORDERING_TYPE) t1,
        min(ORDERING_BIC8) b0, max(ORDERING_BIC8) b1 FROM t GROUP BY 1),
      b AS (SELECT BENEFICIARY_ACCOUNT account, min(BENEFICIARY_TYPE) t0, max(BENEFICIARY_TYPE) t1,
        min(BENEFICIARY_BIC8) b0, max(BENEFICIARY_BIC8) b1 FROM t GROUP BY 1)
      SELECT count(*) identifiers_in_both_roles,
        count(*) FILTER (WHERE a.t0 IS DISTINCT FROM b.t0 OR a.t1 IS DISTINCT FROM b.t1) type_disagreement,
        count(*) FILTER (WHERE a.b0 IS DISTINCT FROM b.b0 OR a.b1 IS DISTINCT FROM b.b1) bank_disagreement
      FROM a JOIN b USING(account)
    """)
    return tables


def overlap(con: duckdb.DuckDBPyConnection, expressions: list[str]) -> Table:
    """Count literal entities present in both active partitions, including across roles."""
    members = " UNION ALL ".join(
        f"SELECT {expr} entity, split FROM p WHERE split IN ('explore','confirm')"
        for expr in expressions
    )
    return query(con, f"""SELECT count(*) shared_entities FROM
      (SELECT entity FROM ({members}) GROUP BY 1 HAVING min(split)<>max(split))""")


def validation_checks(con: duckdb.DuckDBPyConnection) -> dict[str, Table]:
    """Audit coverage, leakage, sample support and descriptive stability of fixed schemes."""
    tables: dict[str, Table] = {}
    labels = ",".join(f"'{label}'" for label in LABELS)
    for scheme in ("sender", "accounts", "banks", "time"):
        print(f"Auditing partition: {scheme}", flush=True)
        con.execute(f"CREATE OR REPLACE TEMP VIEW p AS SELECT *, {partition_sql(scheme)} split FROM t")
        coverage = query(con, """
          WITH g AS (SELECT split,count(*) n,
            round(median(USD_AMOUNT),2) amount_median,median(TOTAL_DURATION) duration_median,
            round(avg((ORDERING_TYPE='B')::INT),6) business_sender_share,
            round(avg((TRANSACTION_TYPE_CODE='Direct')::INT),6) direct_share
          FROM p GROUP BY 1)
          SELECT s.split,coalesce(n,0) n,
            round(100.0*coalesce(n,0)/sum(n) OVER(),4) pct,
            amount_median,duration_median,business_sender_share,direct_share
          FROM (VALUES ('explore'),('confirm'),('excluded')) s(split)
          LEFT JOIN g USING(split) ORDER BY 1
        """)
        tables[f"{scheme}: coverage and baseline stability"] = coverage
        source_n = con.execute("SELECT count(*) FROM t").fetchone()[0]
        if sum(int(row[1]) for row in coverage[1]) != source_n:
            raise ValueError("partition coverage failed")
        row_overlap = overlap(con, ["ROW_ID"])[1][0][0]
        account_overlap = overlap(con, ["ORDERING_ACCOUNT", "BENEFICIARY_ACCOUNT"])[1][0][0]
        sender_overlap = overlap(con, ["ORDERING_ACCOUNT"])[1][0][0]
        bank_overlap = overlap(con, ["ORDERING_BIC8", "BENEFICIARY_BIC8"])[1][0][0]
        path_bank_overlap = overlap(con, [
            "unnest(list_filter(string_split(BIC8_PATH,';'), lambda x: x<>'...'))"
        ])[1][0][0]
        tables[f"{scheme}: overlap audit"] = (
            ["row_ids", "sender_ids", "account_ids_either_role", "endpoint_bank_ids", "visible_path_bank_ids"],
            [(row_overlap, sender_overlap, account_overlap, bank_overlap, path_bank_overlap)],
        )
        if row_overlap or (scheme == "sender" and sender_overlap):
            raise ValueError("partition record/sender separation failed")
        if (scheme == "accounts" and account_overlap) or (scheme == "banks" and bank_overlap):
            raise ValueError("partition entity separation failed")
        tables[f"{scheme}: anomaly support (all label values allowlisted)"] = query(con, f"""
          WITH g AS (SELECT split,CASE WHEN ANOMALY_TYPE IS NULL THEN 'UNLABELLED'
            WHEN ANOMALY_TYPE IN ({labels}) THEN ANOMALY_TYPE ELSE 'OTHER_LABEL' END label,
            count(*) n,count(DISTINCT ORDERING_ACCOUNT) senders,
            count(DISTINCT BENEFICIARY_ACCOUNT) receivers
          FROM p GROUP BY 1,2), grid AS (
            SELECT s.split,l.label FROM (VALUES ('explore'),('confirm'),('excluded')) s(split)
            CROSS JOIN (VALUES ('UNLABELLED'),('OTHER_LABEL'),
              {','.join(f"('{label}')" for label in LABELS)}) l(label))
          SELECT split,label,coalesce(n,0) n,coalesce(senders,0) senders,coalesce(receivers,0) receivers,
            CASE WHEN coalesce(n,0)=0 THEN 'absent'
              WHEN n<100 OR senders<100 OR receivers<100 THEN 'limited'
              ELSE 'displayable; power not assessed' END support
          FROM grid LEFT JOIN g USING(split,label) ORDER BY 2,1
        """)
        for feature in ("CURRENCY_CODE", "TRANSACTION_TYPE_CODE", "ORDERING_TYPE||BENEFICIARY_TYPE"):
            tables[f"{scheme}: composition distance for {feature}"] = query(con, f"""
              WITH g AS (SELECT split,{feature} category,count(*) n FROM p
                WHERE split IN ('explore','confirm') GROUP BY 1,2),
              s AS (SELECT *,n::DOUBLE/sum(n) OVER(PARTITION BY split) share FROM g),
              v AS (SELECT category,
                coalesce(max(share) FILTER(WHERE split='explore'),0) e,
                coalesce(max(share) FILTER(WHERE split='confirm'),0) c FROM s GROUP BY 1)
              SELECT round(sum(abs(e-c))/2,6) total_variation FROM v
            """)
        for dimension in ("strftime(ts_utc,'%Y-%m')", "(ROW_ID-1)//1000000"):
            tables[f"{scheme}: stability by {dimension}"] = query(con, f"""
              SELECT split,{dimension} block,count(*) n,round(median(USD_AMOUNT),2) amount_median,
                count(ANOMALY_TYPE) labelled FROM p GROUP BY 1,2 ORDER BY 2,1
            """)
    return tables


def render(tables: dict[str, Table]) -> str:
    """Suppress small subgroup cells and their other statistics, never entity identifiers."""
    parts = ["# Scientific foundation: executed aggregate checks", "",
             "Run: `uv run python analysis/00_prep/scientific_checks.py`", "",
             f"DuckDB {duckdb.__version__}; 2GB memory limit; two threads; UTC; no disk spill.",
             "Measurements are full-data descriptions, not independent confirmation or causal rules.",
             "Subgroups with fewer than 100 records are suppressed; small entity-support counts are masked."]
    for title, (columns, rows) in tables.items():
        parts += ["", f"## {title}", "", "| " + " | ".join(columns) + " |",
                  "| " + " | ".join("---" for _ in columns) + " |"]
        for row in rows:
            subgroup_n = int(row[columns.index("n")]) if "n" in columns else None
            small = subgroup_n is not None and subgroup_n < 100
            cells = []
            for column, value in zip(columns, row):
                if small and column not in ("split", "label", "block", "support"):
                    value = (0 if subgroup_n == 0 else "<100") if column == "n" else "suppressed"
                elif column in ("senders", "receivers", "labelled") and 0 < int(value) < 100:
                    value = "<100"
                cells.append(str(value).replace("|", "\\|"))
            parts.append("| " + " | ".join(cells) + " |")
    return "\n".join(parts) + "\n"


def main() -> int:
    """Run locally; publish only an aggregate Markdown report after every check completes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", type=Path, default=ROOT / "dataset/payments.parquet")
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "out/scientific_checks.md")
    args = parser.parse_args()
    if not args.src.is_file():
        print("ERROR: Parquet source not found; run build_parquet.py first.", file=sys.stderr)
        return 1
    if args.out.suffix.lower() != ".md" or args.out.resolve() == args.src.resolve():
        print("ERROR: output must be a separate Markdown file.", file=sys.stderr)
        return 1
    con = duckdb.connect()
    try:
        con.execute("SET memory_limit='2GB'; SET threads=2; SET TimeZone='UTC'; SET temp_directory=''")
        con.execute("CREATE VIEW t AS SELECT * FROM read_parquet('" +
                    args.src.as_posix().replace("'", "''") + "')")
        source = query(con, """SELECT count(*) records,count(DISTINCT ROW_ID) distinct_row_ids,
          count(*) FILTER(WHERE ORDERING_ACCOUNT IS NULL OR BENEFICIARY_ACCOUNT IS NULL
            OR ORDERING_BIC8 IS NULL OR BENEFICIARY_BIC8 IS NULL OR ts_utc IS NULL
            OR BIC8_PATH IS NULL OR ORDERING_TYPE IS NULL OR BENEFICIARY_TYPE IS NULL
            OR ORDERING_DETAILS IS NULL OR BENEFICIARY_DETAILS IS NULL
            OR ORDERING_TOKENS IS NULL OR BENEFICIARY_TOKENS IS NULL
            OR EPOCH_SECONDS IS NULL OR USD_AMOUNT IS NULL OR CURRENCY_CODE IS NULL
            OR TOTAL_DURATION IS NULL OR CONTINUITY_QFLAG IS NULL
            OR CURRENCY_CONVERSION_COUNT IS NULL OR PARTICIPANT_COUNT IS NULL) missing_required,
          min(ts_utc) start_utc,max(ts_utc) end_utc FROM t""")
        n, unique, missing, *_ = source[1][0]
        if not n or n != unique or missing:
            raise ValueError("source identity/completeness check failed")
        tables = {"Source coverage": source}
        print("Measuring structural semantics (aggregates only)...", flush=True)
        tables.update(structural_checks(con))
        print("Auditing fixed candidate partitions (aggregates only)...", flush=True)
        tables.update(validation_checks(con))
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(render(tables), encoding="utf-8")
        print("OK: all checks completed; aggregate report written.")
        return 0
    except Exception as exc:
        # DuckDB errors can contain source values. Never print exception text or a traceback.
        print(f"ERROR: {type(exc).__name__}; details hidden to protect source values. No report written.",
              file=sys.stderr)
        return 1
    finally:
        con.close()


if __name__ == "__main__":
    sys.exit(main())
