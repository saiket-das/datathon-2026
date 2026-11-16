"""
R-G01: independently operationalise the directed visible-BIC endpoint label hypothesis.

Run from repository root:
  uv run python analysis/40_g_adversarial/R-G01_visible_endpoints.py --phase periods
  uv run python analysis/40_g_adversarial/R-G01_visible_endpoints.py --phase explore --train-period YYYY-05
  uv run python analysis/40_g_adversarial/R-G01_visible_endpoints.py --phase validate --train-period YYYY-05 --eval-period YYYY-07 --freeze-commit FULL40CHARSHA

This script reads only dataset/payments.parquet and prints/writes aggregates.
Its July evaluation must only be run after a Git commit freezes BOTH this file
and findings/hypotheses/R-G01_directed_visible_endpoints.md. No examples, BICs,
path strings, accounts, individual payment records or other identifying outputs.
A successful validation is an internal same-dataset replication, NOT independent
dataset confirmation.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import duckdb
from scipy.stats import beta

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_REL = "analysis/40_g_adversarial/R-G01_visible_endpoints.py"
PROTOCOL_REL = "findings/hypotheses/R-G01_directed_visible_endpoints.md"
KEYS = {"directed": "directed_key",
        "unordered": "unordered_key",
        "first": "first_bic",
        "last": "last_bic",
        "country": "country_key"}
MAP_NAMES = tuple(KEYS) + ("reverse",)


def verify_freeze(commit: str, train_period: str, eval_period: str) -> None:
    """Require frozen byte-identical protocol and executable from Git history."""
    if not re.fullmatch(r"[0-9a-f]{40}", commit or ""):
        raise SystemExit("Validation requires --freeze-commit FULL40CHARSHA")
    for rel in (SCRIPT_REL, PROTOCOL_REL):
        frozen = subprocess.run(
            ["git", "show", f"{commit}:{rel}"],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout
        live = (ROOT / rel).read_bytes()
        if frozen != live:
            raise SystemExit(f"Frozen file changed: {rel}; refuse validation")
    # Validation calendar periods must themselves have been fixed in the frozen
    # protocol commit, rather than selected after looking at test outcomes.
    marker = f"FROZEN_PERIODS: {train_period} -> {eval_period}"
    frozen_protocol = (ROOT / PROTOCOL_REL).read_text(encoding="utf-8")
    if marker not in frozen_protocol:
        raise SystemExit("Validation cohort not frozen: add FROZEN_PERIODS to the protocol, commit, then retry")
    # An ancestor may be checked out later; the immutable commit is the freeze.


def sha256_file(path: Path) -> str:
    """Stream a private input-byte fingerprint without loading Parquet into Python."""
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def parse_period(value: str) -> str:
    if not re.fullmatch(r"20[0-9]{2}-(0[1-9]|1[0-2])", value):
        raise argparse.ArgumentTypeError("Period must be YYYY-MM")
    return value


def upper_one_sided(k: int, n: int) -> str:
    """Clopper-Pearson 95% upper error bound; independent-unit assumption."""
    if n == 0:
        return "undefined"
    if k == n:
        return "100.000000%"
    return f"{100.0 * beta.ppf(0.95, k + 1, n - k):.6f}%"


def safe_count(x: int | None) -> str:
    """Public Markdown suppresses positive counts below ten."""
    n = int(x or 0)
    return "[1–9 suppressed]" if 0 < n < 10 else str(n)


def pct(k: int, n: int) -> str:
    return "n/a" if not n else f"{100 * k / n:.4f}%"


def scalar_counts(conn: duckdb.DuckDBPyConnection, query: str) -> dict:
    cursor = conn.execute(query)
    cols = [c[0] for c in cursor.description]
    row = cursor.fetchone()
    return dict(zip(cols, row)) if row else {}


def table_create(conn: duckdb.DuckDBPyConnection, name: str, stmt: str) -> None:
    # Fixed hard-coded table identifiers and SQL, never interpolated from data.
    conn.execute(f"CREATE TEMP TABLE {name} AS {stmt}")


def generate_selected(conn: duckdb.DuckDBPyConnection, data: Path,
                      train_period: str, eval_period: str | None) -> None:
    periods = [train_period] + ([eval_period] if eval_period else [])
    literals = ",".join("'" + p + "'" for p in periods)
    # Rows and BIC strings remain strictly inside in-process DuckDB TEMP tables.
    path_literal = data.as_posix().replace("'", "''")
    table_create(conn, "selected", f"""
        WITH source AS (
            SELECT strftime(to_timestamp(EPOCH_SECONDS), '%Y-%m') AS period,
                   TRANSACTION_TYPE_CODE AS label,
                   BIC8_PATH AS path,
                   list_filter(
                       string_split(coalesce(BIC8_PATH, ''), ';'),
                       lambda x: regexp_full_match(trim(x), '^[A-Z0-9]{{8}}$')
                   ) AS visible
            FROM read_parquet('{path_literal}')
            WHERE strftime(to_timestamp(EPOCH_SECONDS), '%Y-%m') IN ({literals})
        )
        SELECT period, label, path,
               array_length(visible) AS node_count,
               trim(list_extract(visible, 1)) AS first_bic,
               trim(list_extract(visible, array_length(visible))) AS last_bic
        FROM source
    """)


def make_cohort(conn: duckdb.DuckDBPyConnection,
                table: str, period: str) -> None:
    table_create(conn, table, f"""
        SELECT path, label, first_bic, last_bic,
               first_bic || '>' || last_bic AS directed_key,
               least(first_bic, last_bic) || '>' ||
                 greatest(first_bic, last_bic) AS unordered_key,
               substr(first_bic, 5, 2) || '>' ||
                 substr(last_bic, 5, 2) AS country_key
        FROM selected
        WHERE period = '{period}' AND label IN ('Covered', 'Indirect')
          AND node_count >= 2
    """)


def build_maps(conn: duckdb.DuckDBPyConnection) -> None:
    for map_name, column in KEYS.items():
        table_create(conn, "m_" + map_name, f"""
            SELECT {column} AS lookup_key, count(*) AS n,
                   count(*) FILTER (WHERE label = 'Covered') AS c,
                   count(*) FILTER (WHERE label = 'Indirect') AS i
            FROM may GROUP BY 1
        """)


def build_eval(conn: duckdb.DuckDBPyConnection) -> None:
    table_create(conn, "may_paths", "SELECT DISTINCT path FROM may")
    joined = [
        f"LEFT JOIN m_{name} AS {name} ON {name}.lookup_key = j.{key}"
        for name, key in KEYS.items()
    ]
    joined.append(
        "LEFT JOIN m_directed AS reverse "
        "ON reverse.lookup_key = j.last_bic || '>' || j.first_bic"
    )
    selected = [
        f"{name}.n AS {name}_n, {name}.c AS {name}_c, "
        f"{name}.i AS {name}_i"
        for name in MAP_NAMES
    ]
    table_create(conn, "test", f"""
        SELECT j.*, (mp.path IS NULL) AS novel_path,
               {', '.join(selected)}
        FROM july AS j
        LEFT JOIN may_paths AS mp ON mp.path = j.path
        {' '.join(joined)}
    """)


def model_pred(alias: str) -> str:
    return (f"CASE WHEN {alias}_c > 0 AND {alias}_i = 0 THEN 'Covered' "
            f"WHEN {alias}_i > 0 AND {alias}_c = 0 THEN 'Indirect' "
            "ELSE NULL END")


def model_pure(alias: str) -> str:
    return f"({alias}_n IS NOT NULL AND ({alias}_c = 0 OR {alias}_i = 0))"


def summarize_model(conn: duckdb.DuckDBPyConnection,
                    name: str, where: str) -> dict:
    pure = model_pure(name)
    bad = f"({pure} AND label <> {model_pred(name)})"
    return scalar_counts(conn, f"""
        SELECT count(*) AS total,
               count(*) FILTER (WHERE {name}_n IS NOT NULL) AS known,
               count(*) FILTER (WHERE {pure}) AS supported,
               count(*) FILTER (WHERE {name}_c > 0 AND {name}_i > 0) AS conflict,
               count(*) FILTER (WHERE {name}_n IS NULL) AS unseen,
               count(*) FILTER (WHERE {bad}) AS errors,
               count(DISTINCT directed_key) FILTER (WHERE {pure}) AS pair_units,
               count(DISTINCT directed_key) FILTER (WHERE {bad}) AS bad_pair_units,
               count(DISTINCT first_bic) FILTER (WHERE {pure}) AS first_banks,
               count(DISTINCT last_bic) FILTER (WHERE {pure}) AS last_banks
        FROM test WHERE {where}
    """)


def paired_control(conn: duckdb.DuckDBPyConnection,
                   name: str, where: str) -> dict:
    common = f"{model_pure('directed')} AND {model_pure(name)}"
    return scalar_counts(conn, f"""
       SELECT count(*) FILTER (WHERE {common}) AS common_n,
              count(*) FILTER (WHERE {common}
                AND label <> {model_pred('directed')}) AS directed_errors,
              count(*) FILTER (WHERE {common}
                AND label <> {model_pred(name)}) AS control_errors,
              count(DISTINCT directed_key)
                FILTER (WHERE {common}) AS common_pairs
       FROM test WHERE {where}
    """)


def diagnostic(conn: duckdb.DuckDBPyConnection, period: str) -> dict:
    return scalar_counts(conn, f"""
        SELECT count(*) AS all_rows,
               count(*) FILTER (
                 WHERE label IN ('Covered', 'Indirect')) AS target_label_rows,
               count(*) FILTER (
                 WHERE label IN ('Covered', 'Indirect')
                   AND node_count >= 2) AS target_valid_rows,
               count(*) FILTER (
                 WHERE label IN ('Covered', 'Indirect')
                   AND node_count < 2) AS missing_visible_endpoints,
               count(*) FILTER (
                 WHERE label NOT IN ('Covered', 'Indirect') OR label IS NULL
               ) AS other_labels
        FROM selected WHERE period = '{period}'
    """)


def prepare_report(conn: duckdb.DuckDBPyConnection, phase: str,
                   train: str, evaluate: str | None, freeze: str | None,
                   data: Path) -> str:
    may_diag = diagnostic(conn, train)
    may_map = scalar_counts(conn, """
        SELECT count(*) AS distinct_directed_pairs,
               count(*) FILTER (WHERE c > 0 AND i > 0) AS conflicted_pairs,
               sum(n) FILTER (WHERE c > 0 AND i > 0) AS conflicted_train_payments
        FROM m_directed
    """)
    lines = [
        "# R-G01 aggregate execution report",
        "",
        f"- Phase: **{phase}**; May train period: **{train}**.",
        f"- Evaluation period: **{evaluate or 'NOT ACCESSED'}**.",
        f"- Freeze SHA: {freeze or 'NOT FROZEN / NO VALIDATION'}.",
        "- Source: local dataset/payments.parquet; no rows exported.",
        f"- Dataset bytes (not a cryptographic fingerprint): {data.stat().st_size}.",
        "- Extraction: first/last 8-character BIC-style visible path tokens;",
        "  this is G's operationalisation, not a claim about B's code.",
        "- Status: internal same-dataset test only; never independent dataset confirmation.",
        "",
        "## Training period denominators",
        "",
        "| Population | Count |",
        "|---|---:|",
    ]
    for key, label in (
        ("all_rows", "May all records"),
        ("target_label_rows", "May Covered/Indirect"),
        ("target_valid_rows", "May Covered/Indirect with >=2 visible BICs"),
        ("missing_visible_endpoints", "May Covered/Indirect invalid endpoints"),
        ("other_labels", "May other or missing labels"),
    ):
        lines.append(f"| {label} | {safe_count(may_diag[key])} |")
    for key, label in (
        ("distinct_directed_pairs", "Distinct May directed endpoint pairs"),
        ("conflicted_pairs", "May label-conflicted directed pairs"),
        ("conflicted_train_payments", "Payments in conflicted May pairs"),
    ):
        lines.append(f"| {label} | {safe_count(may_map[key])} |")
    if phase == "explore":
        lines += ["", "No July evaluation labels or paths were read in exploration mode."]
        return "\n".join(lines) + "\n"

    july_diag = diagnostic(conn, evaluate)
    lines += [
        "",
        "## July eligibility / selection",
        "",
        "| Population | Count |",
        "|---|---:|",
    ]
    for key, label in (
        ("all_rows", "July all records"),
        ("target_label_rows", "July Covered/Indirect"),
        ("target_valid_rows", "July Covered/Indirect with >=2 visible BICs"),
        ("missing_visible_endpoints", "July Covered/Indirect invalid endpoints"),
        ("other_labels", "July other or missing labels"),
    ):
        lines.append(f"| {label} | {safe_count(july_diag[key])} |")
    for subset, where in (("all", "TRUE"), ("novel-path", "novel_path"),
                          ("May-seen-path", "NOT novel_path")):
        total = scalar_counts(conn, f"""
            SELECT count(*) AS n,
                   count(*) FILTER (WHERE label='Covered') AS covered,
                   count(*) FILTER (WHERE label='Indirect') AS indirect,
                   count(DISTINCT directed_key) AS directed_pairs,
                   count(DISTINCT first_bic) AS distinct_first_banks,
                   count(DISTINCT last_bic) AS distinct_last_banks
            FROM test WHERE {where}
        """)
        lines += [
            "",
            f"## Evaluation subset: {subset}",
            "",
            f"Eligible July records: {safe_count(total['n'])}; "
            f"Covered: {safe_count(total['covered'])}; "
            f"Indirect: {safe_count(total['indirect'])}; "
            f"distinct pairs: {safe_count(total['directed_pairs'])}; "
            f"distinct sending/receiving visible banks: "
            f"{safe_count(total['distinct_first_banks'])}/"
            f"{safe_count(total['distinct_last_banks'])}.",
            "",
            "| May map / control | Known | Pure-supported | Conflicted | Unseen | "
            "Errors on pure support | Supported share | Optimistic upper 95% error |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for name in MAP_NAMES:
            result = summarize_model(conn, name, where)
            n, k = int(result["supported"]), int(result["errors"])
            lines.append(
                f"| {name} | {safe_count(result['known'])} | "
                f"{safe_count(n)} | {safe_count(result['conflict'])} | "
                f"{safe_count(result['unseen'])} | {safe_count(k)} | "
                f"{pct(n, int(result['total']))} | {upper_one_sided(k,n)} |"
            )
            if name == "directed":
                lines += [
                    "",
                    "Directed support dependence audit: "
                    f"{safe_count(result['pair_units'])} distinct pair clusters, "
                    f"{safe_count(result['bad_pair_units'])} clusters with at least "
                    "one error; "
                    f"{safe_count(result['first_banks'])} distinct first banks and "
                    f"{safe_count(result['last_banks'])} last banks.",
                    "Optimistic one-sided cluster-level upper 95% error bound: "
                    f"{upper_one_sided(int(result['bad_pair_units']), int(result['pair_units']))}; "
                    "pair clusters still share banks and countries.",
                    "",
                ]
        lines += [
            "",
            "| Control vs directed on common pure-supported records | Common n | "
            "Directed errors | Control errors | Distinct directed pairs |",
            "|---|---:|---:|---:|---:|",
        ]
        for name in MAP_NAMES:
            if name == "directed":
                continue
            r = paired_control(conn, name, where)
            lines.append(
                f"| {name} | {safe_count(r['common_n'])} | "
                f"{safe_count(r['directed_errors'])} | "
                f"{safe_count(r['control_errors'])} | "
                f"{safe_count(r['common_pairs'])} |"
            )
    lines += [
        "",
        "## Interpretation gate",
        "",
        "Failures, lack of support, and benchmark equivalence are reported as-is.",
        "Do not infer a unique generative rule or independent dataset confirmation.",
        "The May/July source may share banks, route templates and historical exposure.",
        "Any quantitative claim must be revisited against the frozen eligibility rules.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("periods", "explore", "validate"),
                        required=True)
    parser.add_argument("--data", type=Path,
                        default=ROOT / "dataset/payments.parquet")
    parser.add_argument("--train-period", type=parse_period)
    parser.add_argument("--eval-period", type=parse_period)
    parser.add_argument("--freeze-commit")
    args = parser.parse_args()
    data = args.data.expanduser().resolve()
    if not data.is_file():
        raise SystemExit(f"Missing local dataset file: {data}")
    if args.phase == "validate":
        if not args.train_period or not args.eval_period:
            parser.error("Validation needs --train-period and --eval-period")
        if args.train_period == args.eval_period:
            parser.error("Training and validation periods cannot coincide")
        if args.eval_period <= args.train_period:
            parser.error("Evaluation period must follow training period")
        verify_freeze(args.freeze_commit, args.train_period, args.eval_period)
    elif args.phase == "explore":
        if not args.train_period or args.eval_period:
            parser.error("Explore needs May --train-period; no eval period")
    else:
        if args.eval_period or args.train_period:
            parser.error("Periods mode takes no train/evaluation periods")

    # Fingerprint before opening the input; validation is invalid if bytes change.
    input_sha256_before = sha256_file(data) if args.phase != "periods" else None
    conn = duckdb.connect(database=":memory:")
    conn.execute("SET TimeZone = 'UTC'")  # Calendar cohorts are UTC, not machine-local.
    try:
        if args.phase == "periods":
            source = data.as_posix().replace("'", "''")
            results = conn.execute(f"""
                SELECT strftime(to_timestamp(EPOCH_SECONDS),'%Y-%m') AS period,
                       count(*) AS payment_count
                FROM read_parquet('{source}') GROUP BY 1 ORDER BY 1
            """).fetchall()
            print("PERIOD SUPPORT: aggregate monthly row counts only")
            for period, count in results:
                print(f"{period}: {safe_count(count)}")
            return

        generate_selected(conn, data, args.train_period,
                          args.eval_period if args.phase == "validate" else None)
        make_cohort(conn, "may", args.train_period)
        build_maps(conn)
        if args.phase == "validate":
            make_cohort(conn, "july", args.eval_period)
            build_eval(conn)
        report = prepare_report(
            conn, args.phase, args.train_period, args.eval_period,
            args.freeze_commit, data)
    finally:
        conn.close()

    # Only aggregate Markdown is eligible for Git; metadata stays under ignored dataset/.
    output = ROOT / "analysis/40_g_adversarial/out/R-G01_aggregates.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    code_hash = hashlib.sha256((ROOT / SCRIPT_REL).read_bytes()).hexdigest()
    # Fingerprint the exact local source after the query; keep digest private.
    # A concurrent file mutation is not ruled out: execute on immutable input.
    input_sha256 = sha256_file(data)
    metadata = {
        "dataset_sha256_private": input_sha256,
        "phase": args.phase,
        "train_period": args.train_period,
        "eval_period": args.eval_period,
        "freeze_commit": args.freeze_commit,
        "source_path_is_local": True,
        "source_size_bytes": data.stat().st_size,
        "source_mtime_ns": data.stat().st_mtime_ns,
        "script_sha256": code_hash,
        "utc_completed": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version.split()[0],
        "duckdb_version": duckdb.__version__,
        "result": "aggregate_report_written",
        "report_sha256": hashlib.sha256(report.encode()).hexdigest()
    }
    logpath = ROOT / "dataset/g_executor/R-G01_metadata.json"
    logpath.parent.mkdir(parents=True, exist_ok=True)
    logpath.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print("AGGREGATE OUTPUT:", output.relative_to(ROOT))
    print("LOCAL EXECUTION METADATA:", logpath.relative_to(ROOT))
    print("Report SHA256:", metadata["report_sha256"])


if __name__ == "__main__":
    main()
