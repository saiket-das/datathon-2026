"""Local-only helpers for B's frozen investigations; no standalone analysis.

Run the hypothesis scripts documented in this folder's README from the repository root.
"""

import argparse
import importlib.util
from pathlib import Path
import subprocess

import duckdb
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
spec = importlib.util.spec_from_file_location("foundation", ROOT / "analysis/00_prep/scientific_checks.py")
foundation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foundation)
Table = tuple[list[str], list[tuple]]


def arguments(script: str) -> argparse.Namespace:
    """Require an ancestor freeze commit containing unchanged executable code."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("explore", "confirm"), default="explore")
    parser.add_argument("--freeze")
    args = parser.parse_args()
    if args.phase == "confirm":
        if not args.freeze:
            parser.error("confirmation requires --freeze <committed-plan-SHA>")
        paths = [f"analysis/20_routing_time/{script}.py", "analysis/20_routing_time/routing_common.py"]
        subprocess.run(["git", "merge-base", "--is-ancestor", args.freeze, "HEAD"], cwd=ROOT, check=True)
        subprocess.run(["git", "diff", "--exit-code", "--quiet", args.freeze, "--", *paths], cwd=ROOT, check=True)
        plan = subprocess.check_output(
            ["git", "show", f"{args.freeze}:findings/hypotheses/{script}.md"], cwd=ROOT, text=True
        )
        if "**Status:** confirmation-ready" not in plan:
            raise ValueError("freeze commit must contain a confirmation-ready plan")
    return args


def connect() -> duckdb.DuckDBPyConnection:
    """Prepare a lazy source view. Materialised payment tables stay in local memory."""
    con = duckdb.connect(config={"memory_limit": "2GB", "threads": 2, "temp_directory": ""})
    con.execute("SET TimeZone='UTC'")
    src = (ROOT / "dataset/payments.parquet").as_posix().replace("'", "''")
    con.execute(f"CREATE VIEW source AS SELECT *, {foundation.partition_sql('banks')} split FROM read_parquet('{src}')")
    return con


def selected(con: duckdb.DuckDBPyConnection, split: str) -> None:
    """Materialise only the requested bank partition, with no detail/token/amount fields."""
    if split not in ("explore", "confirm"):
        raise ValueError("invalid split")
    con.execute(f"""CREATE OR REPLACE TEMP TABLE sample AS
      SELECT ROW_ID, TOTAL_DURATION::DOUBLE d, PARTICIPANT_COUNT v, gap_count g,
        TRANSACTION_TYPE_CODE route, ANOMALY_TYPE IS NOT NULL labelled,
        ORDERING_BIC8 ob, BENEFICIARY_BIC8 bb, ORDERING_ACCOUNT oa, BENEFICIARY_ACCOUNT ba,
        string_split(BIC8_PATH,';') path, ts_utc,
        ORDERING_TYPE||BENEFICIARY_TYPE pair, CURRENCY_CONVERSION_COUNT fx,
        CURRENCY_CODE currency
      FROM source WHERE split='{split}'""")


def table(con: duckdb.DuckDBPyConnection, sql: str) -> Table:
    """Fetch explicitly aggregate queries only; bank-level arrays stay local and unprinted."""
    result = con.execute(sql)
    return [x[0] for x in result.description], result.fetchall()


def remember_exploration(con: duckdb.DuckDBPyConnection) -> None:
    """Keep local entity sets for an audit of the actual unlabelled eligible populations."""
    members = {
        "rows": "SELECT ROW_ID entity FROM sample WHERE NOT labelled",
        "accounts": "SELECT oa entity FROM sample WHERE NOT labelled UNION SELECT ba FROM sample WHERE NOT labelled",
        "endpoints": "SELECT ob entity FROM sample WHERE NOT labelled UNION SELECT bb FROM sample WHERE NOT labelled",
        "paths": "SELECT DISTINCT unnest(list_filter(path,lambda x:x<>'...')) entity FROM sample WHERE NOT labelled",
    }
    for name, sql in members.items():
        con.execute(f"CREATE TEMP TABLE exploration_{name} AS {sql}")


def overlaps(con: duckdb.DuckDBPyConnection, relation: str, where: str) -> Table:
    """Count shared entities, including cross-role identities; return no identifiers."""
    members = {
        "rows": f"SELECT ROW_ID entity FROM {relation} WHERE {where}",
        "accounts": f"SELECT oa entity FROM {relation} WHERE {where} UNION SELECT ba FROM {relation} WHERE {where}",
        "endpoints": f"SELECT ob entity FROM {relation} WHERE {where} UNION SELECT bb FROM {relation} WHERE {where}",
        "paths": f"SELECT DISTINCT unnest(list_filter(path,lambda x:x<>'...')) entity FROM {relation} WHERE {where}",
    }
    counts = [con.execute(f"SELECT count(*) FROM ({sql}) e SEMI JOIN exploration_{name} USING(entity)").fetchone()[0]
              for name, sql in members.items()]
    return ["row_ids", "either_role_accounts", "endpoint_banks", "visible_path_banks"], [tuple(counts)]


def report(stem: str, phase: str, freeze: str | None, tables: dict[str, Table]) -> None:
    """Write only safe aggregate Markdown, suppressing groups with inadequate support."""
    parts = [f"# {stem}: {phase}", "", f"Freeze: {freeze or 'not yet frozen'}.",
             f"DuckDB {duckdb.__version__}; 2GB; two threads; UTC; no spill.",
             "No identifiers or payment records are exported. Counts below 100 are suppressed.",
             "Any reported intervals are 99% ordering-bank cluster resampling sensitivity intervals, not proof of independent banks."]
    for title, (columns, rows) in tables.items():
        parts += ["", f"## {title}", "", "| " + " | ".join(columns) + " |",
                  "| " + " | ".join(["---"] * len(columns)) + " |"]
        for row in rows:
            small = "n" in columns and row[columns.index("n")] < 100
            unsupported = any(name in columns and row[columns.index(name)] < 100
                              for name in ("senders", "receivers", "banks"))
            cells = []
            for key, value in zip(columns, row):
                if (small or unsupported) and key not in ("group", "cell", "n"):
                    value = "suppressed"
                elif key == "n" and small:
                    value = "<100" if value else "0"
                elif isinstance(value, (float, np.floating)):
                    value = f"{value:.6f}"
                cells.append(str(value).replace("|", "\\|"))
            parts.append("| " + " | ".join(cells) + " |")
    OUT.mkdir(exist_ok=True)
    (OUT / f"{stem}_{phase}.md").write_text("\n".join(parts) + "\n", encoding="utf-8")


def cluster_draws(stats: np.ndarray) -> np.ndarray:
    """Resample whole ordering-bank sufficient statistics, without outputting identifiers."""
    rng = np.random.default_rng(20261116)
    k = len(stats)
    if k < 100:
        raise ValueError("insufficient ordering-bank clusters")
    return rng.multinomial(k, np.full(k, 1 / k), size=1000) @ stats


def interval(values: np.ndarray) -> tuple[float, float]:
    """A fixed 99% percentile interval; accounts and intermediary banks can still overlap."""
    return tuple(float(x) for x in np.quantile(values, [0.005, 0.995]))
