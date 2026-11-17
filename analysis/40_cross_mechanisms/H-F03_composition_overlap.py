"""H-F03: fixed-population FX composition contrasts and bank-pair overlap (EXPLORATORY).

Run from repository root with approved offline read-only source mounts:
    python analysis/40_cross_mechanisms/H-F03_composition_overlap.py --data-dir /mnt/f-parquet

Run entirely synthetic, no sponsor data:
    python analysis/40_cross_mechanisms/H-F03_composition_overlap.py --self-test

Equivalent pinned environment: uv run python <same script> <same arguments>.
Writes PRIVATE report only to dataset/private_reports/H-F03_composition_overlap.md,
inside the repository's git-ignored dataset tree; NEVER commit that output.
No identifying bank/path/account strings, row samples or dataset results go to stdout.
All actual payment outcomes queried are May–June 2023 UTC, FX state 0 or 1.
No July outcome queries, frozen validation, causal claim or independent confirmation.
The coordinator must independently verify the five input digests against its
approved LOCAL manifest and approve any further use of the private output.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import math
import os
from pathlib import Path
import sys

import duckdb

ROOT = Path(__file__).resolve().parents[2]
PRIVATE_ROOT = ROOT / "dataset" / "private_reports"
PRIVATE_REPORT = PRIVATE_ROOT / "H-F03_composition_overlap.md"
CUTOFF_UTC = datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc)
THRESHOLDS = (1, 5, 10, 25, 50, 100)
S0 = ("route", "participants", "currency", "party_pair", "gaps")
S1 = S0 + ("ord_country", "ben_country")
S3 = S1 + ("amount_band",)
ALL_COLUMNS = frozenset((
    "ROW_ID", "EPOCH_SECONDS", "CURRENCY_CODE", "USD_AMOUNT",
    "ORDERING_BIC8", "BENEFICIARY_BIC8", "BIC8_PATH", "TOTAL_DURATION",
    "CONTINUITY_QFLAG", "CURRENCY_CONVERSION_COUNT", "PARTICIPANT_COUNT",
    "TRANSACTION_TYPE_CODE", "ORDERING_ACCOUNT", "BENEFICIARY_ACCOUNT",
    "ORDERING_DETAILS", "ORDERING_TOKENS", "BENEFICIARY_DETAILS",
    "BENEFICIARY_TOKENS", "ORDERING_TYPE", "BENEFICIARY_TYPE",
    "ANOMALY_TYPE", "ts_utc", "ord_country", "ben_country", "path_len",
    "gap_count",
))
PAIRS = (("P0", "S0", S0), ("P1", "S0", S0), ("P1", "S1", S1),
         ("P3", "S0", S0), ("P3", "S1", S1), ("P3", "S3", S3))


def cutoff_guard() -> None:
    if datetime.now(timezone.utc) >= CUTOFF_UTC:
        raise TimeoutError("F discovery research cutoff reached")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            cutoff_guard()
            block = stream.read(8 * 1024 * 1024)
            if not block:
                return digest.hexdigest()
            digest.update(block)


def source_paths(data_dir: Path) -> list[Path]:
    paths = [data_dir / f"payments_part_{i:02d}_of_05.parquet"
             for i in range(1, 6)]
    if not all(p.is_file() for p in paths):
        raise FileNotFoundError("Require every one of the five source Parquet parts")
    return paths


def read_parquet_literal(paths: list[Path]) -> str:
    escaped = ["'" + p.as_posix().replace("'", "''") + "'" for p in paths]
    return "[" + ", ".join(escaped) + "]"


def configure(con: duckdb.DuckDBPyConnection, scratch: Path) -> None:
    scratch.mkdir(parents=True, exist_ok=True)
    con.execute("SET threads=2")
    con.execute("SET memory_limit='3GB'")
    con.execute("SET TimeZone='UTC'")
    con.execute("SET preserve_insertion_order=false")
    # Scratch holds private, potentially row-derived intermediate data.
    temp = scratch.resolve().as_posix().replace("'", "''")
    con.execute("SET temp_directory='" + temp + "'")


def setup_development(con: duckdb.DuckDBPyConnection) -> None:
    """Build only the FX0/FX1 May–June development rows, excluding anomalies."""
    cutoff_guard()
    con.execute("""
        CREATE TEMP TABLE dev AS
        SELECT TRANSACTION_TYPE_CODE AS route,
               PARTICIPANT_COUNT AS participants,
               CURRENCY_CODE AS currency,
               ORDERING_TYPE || BENEFICIARY_TYPE AS party_pair,
               gap_count AS gaps,
               ord_country AS ord_country,
               ben_country AS ben_country,
               ORDERING_BIC8 AS ord_bank,
               BENEFICIARY_BIC8 AS ben_bank,
               CURRENCY_CONVERSION_COUNT AS fx,
               ln(1.0 + TOTAL_DURATION) AS log_duration,
               ln(1.0 + USD_AMOUNT) AS log_amount,
               CAST(least(31, floor(log2(1.0 + USD_AMOUNT))) AS INTEGER)
                   AS amount_band
        FROM payments_source
        WHERE ts_utc >= TIMESTAMP '2023-05-01'
          AND ts_utc < TIMESTAMP '2023-07-01'
          AND ANOMALY_TYPE IS NULL
          AND TOTAL_DURATION >= 0 AND USD_AMOUNT >= 0
          AND PARTICIPANT_COUNT BETWEEN 2 AND 5
          AND CURRENCY_CONVERSION_COUNT IN (0,1)
    """)


def support(con: duckdb.DuckDBPyConnection, name: str,
            population: str, keys: tuple[str, ...]) -> None:
    """Retain strata with >=100 records for EACH FX state, no post-hoc tuning."""
    cutoff_guard()
    group = ", ".join(keys)
    con.execute(f"""
        CREATE TEMP TABLE support_{name} AS
        SELECT {group}
        FROM {population}
        GROUP BY {group}
        HAVING count(*) FILTER (WHERE fx=0) >= 100
           AND count(*) FILTER (WHERE fx=1) >= 100
    """)
    con.execute(f"""
        CREATE TEMP VIEW {name} AS
        SELECT d.* FROM {population} d
        INNER JOIN support_{name} s USING ({group})
    """)


def setup_populations(con: duckdb.DuckDBPyConnection) -> None:
    support(con, "P0", "dev", S0)
    support(con, "P1", "P0", S1)
    support(con, "P3", "P1", S3)


def decomposition_sql(population: str, keys: tuple[str, ...],
                      outcome: str) -> str:
    """A single SQL row contains no identifying stratum/entity values."""
    if outcome not in ("log_duration", "log_amount"):
        raise ValueError("Unexpected outcome")
    if (population, keys) not in ((p, k) for p, _, k in PAIRS):
        raise ValueError("Unexpected population/stratum definition")
    group = ", ".join(keys)
    return f"""
      WITH grouped AS (
        SELECT {group}, fx, count(*) AS n, avg({outcome}) AS mu
        FROM {population}
        GROUP BY {group}, fx
      ), pivoted AS (
        SELECT {group},
               max(n) FILTER (WHERE fx=0) AS n0,
               max(n) FILTER (WHERE fx=1) AS n1,
               max(mu) FILTER (WHERE fx=0) AS mu0,
               max(mu) FILTER (WHERE fx=1) AS mu1
        FROM grouped GROUP BY {group}
      ), paired AS (
        SELECT n0, n1, mu0, mu1
        FROM pivoted WHERE n0 > 0 AND n1 > 0
      ), normalized AS (
        SELECT n0, n1, mu0, mu1,
               n0::DOUBLE / sum(n0) OVER () AS p0,
               n1::DOUBLE / sum(n1) OVER () AS p1,
               (n0+n1)::DOUBLE / sum(n0+n1) OVER () AS p_pool,
               least(n0,n1) AS n_min
        FROM paired
      )
      SELECT count(*) AS strata,
             coalesce(sum(n0),0) AS n0, coalesce(sum(n1),0) AS n1,
             sum(p1*mu1) - sum(p0*mu0) AS observed,
             sum(p0*(mu1-mu0)) AS within_fx0,
             sum((p1-p0)*mu1) AS composition_fx0,
             sum(p1*(mu1-mu0)) AS within_fx1,
             sum((p1-p0)*mu0) AS composition_fx1,
             sum((p0+p1)*(mu1-mu0)/2) AS within_symmetric,
             sum((p1-p0)*(mu1+mu0)/2) AS composition_symmetric,
             sum(p_pool*(mu1-mu0)) AS within_pooled,
             sum(n_min*(mu1-mu0))/nullif(sum(n_min),0) AS within_min_weight,
             sum(abs(p1-p0))/2 AS composition_tv,
             count(*) FILTER (WHERE mu1 > mu0) AS positive_strata,
             count(*) FILTER (WHERE mu1 < mu0) AS negative_strata
      FROM normalized
    """


METRICS = ("strata", "n0", "n1", "observed", "within_fx0",
           "composition_fx0", "within_fx1", "composition_fx1",
           "within_symmetric", "composition_symmetric", "within_pooled",
           "within_min_weight", "composition_tv", "positive_strata",
           "negative_strata")


def decompose(con: duckdb.DuckDBPyConnection, population: str,
              keys: tuple[str, ...], outcome: str) -> dict[str, object]:
    cutoff_guard()
    result = con.execute(decomposition_sql(population, keys, outcome)).fetchone()
    if result is None:
        raise ValueError("Missing aggregate result")
    data = dict(zip(METRICS, result, strict=True))
    if data["strata"] == 0:
        return data
    if data["n0"] <= 0 or data["n1"] <= 0:
        raise ValueError("Missing FX support")
    observed = data["observed"]
    for inside, outside in (("within_fx0", "composition_fx0"),
                            ("within_fx1", "composition_fx1"),
                            ("within_symmetric", "composition_symmetric")):
        if not math.isclose(observed, data[inside] + data[outside],
                            rel_tol=0, abs_tol=1e-8):
            raise ArithmeticError("Weighted decomposition did not close")
    if not (-1e-9 <= data["composition_tv"] <= 1.000000001):
        raise ArithmeticError("Invalid total variation")
    return data


def population_counts(con: duckdb.DuckDBPyConnection,
                      name: str) -> tuple[int, int, int]:
    cutoff_guard()
    n, n0, n1 = con.execute(f"""
        SELECT count(*) AS n,
               count(*) FILTER (WHERE fx=0) AS n0,
               count(*) FILTER (WHERE fx=1) AS n1
        FROM {name}
    """).fetchone()
    if n != n0+n1:
        raise ArithmeticError("FX population conservation failed")
    return int(n), int(n0), int(n1)


def pair_overlap(con: duckdb.DuckDBPyConnection,
                 population: str) -> tuple[dict[str, int], list[tuple]]:
    """All bank strings remain internal to the source's DuckDB connection."""
    cutoff_guard()
    label = "full" if population == "dev" else "fixed"
    con.execute(f"""
        CREATE TEMP TABLE pairs_{label} AS
        SELECT ord_bank, ben_bank,
               count(*) FILTER (WHERE fx=0) AS n0,
               count(*) FILTER (WHERE fx=1) AS n1
        FROM {population}
        GROUP BY ord_bank, ben_bank
    """)
    summary = con.execute(f"""
        SELECT count(*) AS n_pairs,
               count(*) FILTER (WHERE n0>0 AND n1>0) AS shared_pairs,
               count(*) FILTER (WHERE n0>0 AND n1=0) AS fx0_only_pairs,
               count(*) FILTER (WHERE n0=0 AND n1>0) AS fx1_only_pairs
        FROM pairs_{label}
    """).fetchone()
    if summary[0] != summary[1]+summary[2]+summary[3]:
        raise ArithmeticError("Bank pair support partition failed")
    thresholds = ",".join(str(v) for v in THRESHOLDS)
    rows = con.execute(f"""
        WITH levels AS (SELECT unnest([{thresholds}]) AS min_per_state)
        SELECT levels.min_per_state,
               count(*) FILTER (WHERE n0 >= levels.min_per_state
                                 AND n1 >= levels.min_per_state) AS matched_pairs,
               coalesce(sum(n0) FILTER (WHERE n0 >= levels.min_per_state
                                       AND n1 >= levels.min_per_state),0)
                   AS retained_fx0,
               coalesce(sum(n1) FILTER (WHERE n0 >= levels.min_per_state
                                       AND n1 >= levels.min_per_state),0)
                   AS retained_fx1
        FROM pairs_{label} CROSS JOIN levels
        GROUP BY levels.min_per_state ORDER BY levels.min_per_state
    """).fetchall()
    if tuple(int(row[0]) for row in rows) != THRESHOLDS:
        raise AssertionError("Missing preselected overlap thresholds")
    for previous, current in zip(rows, rows[1:]):
        if any(int(current[i]) > int(previous[i]) for i in (1,2,3)):
            raise ArithmeticError("Bank overlap should be nonincreasing")
    fields = ("observed_pairs", "both_state_pairs", "fx0_only_pairs",
              "fx1_only_pairs")
    return dict(zip(fields, map(int, summary), strict=True)), rows


def number(value: object) -> str:
    if value is None:
        return "unsupported"
    if isinstance(value, float):
        return f"{value:.9f}"
    return str(value)


def report_table(columns: tuple[str, ...], rows: list[tuple]) -> list[str]:
    lines = ["| " + " | ".join(columns) + " |",
             "| " + " | ".join("---" for _ in columns) + " |"]
    for cells in rows:
        lines.append("| " + " | ".join(number(x) for x in cells) + " |")
    return lines


def self_test() -> None:
    """Invented source-typed fixture also exercises the real SQL projection."""
    con = duckdb.connect()
    try:
        # The earlier H-F02 failure occurred BEFORE creating its dev view.
        # For H-F03, test the actual setup_development SQL, not a prebuilt dev.
        con.execute("""
          CREATE TEMP TABLE payments_source (
            TRANSACTION_TYPE_CODE VARCHAR, PARTICIPANT_COUNT INTEGER,
            CURRENCY_CODE VARCHAR, ORDERING_TYPE VARCHAR,
            BENEFICIARY_TYPE VARCHAR, gap_count INTEGER,
            ord_country VARCHAR, ben_country VARCHAR,
            ORDERING_BIC8 VARCHAR, BENEFICIARY_BIC8 VARCHAR,
            CURRENCY_CONVERSION_COUNT INTEGER, TOTAL_DURATION DOUBLE,
            USD_AMOUNT DOUBLE, ts_utc TIMESTAMP, ANOMALY_TYPE VARCHAR
          )
        """)
        rows = []
        for cc, bn, amount, n0, n1, duration0, duration1 in (
            ("US", "BANK_A", 127, 150, 200, 100, 120),
            ("GB", "BANK_B", 255, 180, 140, 220, 130),
        ):
            for fx, n, duration in ((0, n0, duration0), (1, n1, duration1)):
                rows.extend([("Direct", 2, "USD", "B", "C", 0, cc, "SG",
                              bn, "BANK_Z", fx, float(duration),
                              float(amount), datetime(2023, 5, 15), None)] * n)
        con.executemany(
            "INSERT INTO payments_source VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows)
        setup_development(con)
        setup_populations(con)
        n0, n1, n3 = (population_counts(con, name) for name in ("P0","P1","P3"))
        if n0 != n1 or n1 != n3 or n0[0] != len(rows):
            raise AssertionError("Synthetic common-support nesting failed")
        for p, _, grouping in PAIRS:
            for y in ("log_duration", "log_amount"):
                v = decompose(con, p, grouping, y)
                if v["strata"] == 0:
                    raise AssertionError("Synthetic fixture unexpectedly unsupported")
        summary, levels = pair_overlap(con, "dev")
        if summary["observed_pairs"] != 2 or levels[-1][1] != 2:
            raise AssertionError("Synthetic bank overlap failed")
    finally:
        con.close()
    print("OK: H-F03 invented-source SQL and decomposition checks passed; no sponsor data accessed.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", type=Path, default=ROOT / "dataset")
    ap.add_argument("--self-test", action="store_true",
                    help="Execute invented-fixture checks without payment files")
    args = ap.parse_args()
    try:
        cutoff_guard()
        if args.self_test:
            self_test()
            return 0
        PRIVATE_ROOT.mkdir(parents=True, exist_ok=True)
        sources = source_paths(args.data_dir.resolve())
        fingerprints = [file_sha256(p) for p in sources]
        cutoff_guard()
        con = duckdb.connect()
        try:
            configure(con, PRIVATE_ROOT / ".duckdb_tmp")
            con.execute("CREATE TEMP VIEW payments_source AS SELECT * FROM read_parquet(" +
                        read_parquet_literal(sources) + ")")
            columns = {item[0] for item in con.execute("DESCRIBE payments_source").fetchall()}
            if columns != ALL_COLUMNS:
                raise ValueError("Unexpected source schema")
            cutoff_guard()
            n_all, unique_row_ids = con.execute(
                "SELECT count(*), count(DISTINCT ROW_ID) FROM payments_source"
            ).fetchone()
            if n_all != 10_000_000 or unique_row_ids != n_all:
                raise ValueError("Expected ten million distinct source rows")
            for p in sources:
                cutoff_guard()
                query = "SELECT count(*) FROM read_parquet(" + read_parquet_literal([p]) + ")"
                n_part = con.execute(query).fetchone()[0]
                if n_part != 2_000_000:
                    raise ValueError("Split source part count mismatch")

            setup_development(con)
            universe = population_counts(con, "dev")
            setup_populations(con)
            counts = {name: population_counts(con, name) for name in ("P0","P1","P3")}
            if not (universe[1] >= counts["P0"][1] >= counts["P1"][1] >= counts["P3"][1]
                    and universe[2] >= counts["P0"][2] >= counts["P1"][2] >= counts["P3"][2]):
                raise ArithmeticError("Nested support or state coverage violated")

            decompositions = []
            for population, scheme, keys in PAIRS:
                for outcome in ("log_duration", "log_amount"):
                    data = decompose(con, population, keys, outcome)
                    n, n0, n1 = counts[population]
                    if data["strata"] != 0 and (int(data["n0"]) != n0
                                                or int(data["n1"]) != n1):
                        raise ArithmeticError("Decomposition rows not equal to fixed population")
                    decompositions.append((population, scheme, outcome, data))

            overlap = {}
            for pop in ("dev", "P0"):
                overlap[pop] = pair_overlap(con, pop)

            cutoff_guard()
            script_hash = file_sha256(Path(__file__))
            lines = [
                "# H-F03 — PRIVATE exploratory composition / bank-overlap results",
                "",
                "**Confidential local result. Never commit, paste publicly, or expose as a GitHub artifact.**",
                "**Exploratory only; no freeze, validation, independent confirmation or causal claims.**",
                f"UTC produced: {datetime.now(timezone.utc).isoformat()}",
                f"Script SHA-256: {script_hash}",
                f"Full-source records (structure check only): {n_all}",
                f"Full-source distinct ROW_ID (structure check only): {unique_row_ids}",
                f"Required source columns: {len(columns)}",
                "Five observed local source SHA-256 digests (compare privately to approved manifest):",
                *["- Part " + str(i+1) + ": " + sha
                  for i,sha in enumerate(fingerprints)],
                "IMPORTANT: hashes were computed; a coordinator must compare to the private approved",
                "manifest before describing this output as source-verified.",
                "",
                "## Development cohort",
                "",
                "UTC May 1 through June 30 2023. Unlabelled, nonnegative USD amount/duration,",
                "participants 2–5, FX exactly 0 or 1. No July payment outcomes read.",
                "Each supported stratum >=100 payments per FX state.",
            ]
            un, u0, u1 = universe
            table = []
            for name in ("P0","P1","P3"):
                n, n0, n1 = counts[name]
                table.append((name,n,n0,n1,100*n0/u0 if u0 else None,
                              100*n1/u1 if u1 else None))
            lines += report_table(
                ("Population","n","FX0 n","FX1 n","FX0 universe coverage %",
                 "FX1 universe coverage %"),
                [("Universe", un, u0, u1, 100.0, 100.0)] + table)
            lines += [
                "",
                "P0: S0 coarse support; P1: P0 restricted to S1 country support;",
                "P3: P1 restricted to S3 amount-band support.",
                "Within P1, compare S0 vs S1 on EXACT SAME ROWS. Within P3, compare",
                "S0, S1 and S3 on EXACT SAME ROWS. Different P's are selected samples.",
                "",
                "## Algebraic decomposition within fixed populations",
                "",
                "FX1 minus FX0; all outcomes are means of log(1+value).",
                "For a given fixed P, D=W0+C0=W1+C1=Wsym+Csym.",
                "Pooled within is an alternative reference; the pooled residual is D-Wpooled.",
                "Min-weight within uses min(n_fx0,n_fx1) as the reference weighting.",
                "TV is the total variation between FX-specific stratum distributions.",
            ]
            for p, scheme, outcome, data in decompositions:
                lines.append(f"### {p}/{scheme}/{outcome}")
                if data["strata"] == 0:
                    lines.extend(["", "Unsupported: no common-support strata at this resolution.",""])
                    continue
                lines += report_table(
                    ("Strata","n0","n1","D","W0","C0","W1","C1",
                     "Wsym","Csym","Wpooled","D-Wpooled","Wmin",
                     "Stratum TV","Positive Δ strata","Negative Δ strata"),
                    [(data["strata"], data["n0"], data["n1"], data["observed"],
                      data["within_fx0"], data["composition_fx0"],
                      data["within_fx1"], data["composition_fx1"],
                      data["within_symmetric"], data["composition_symmetric"],
                      data["within_pooled"],
                      data["observed"]-data["within_pooled"],
                      data["within_min_weight"], data["composition_tv"],
                      data["positive_strata"], data["negative_strata"])])
                lines.append("")
            lines += [
                "## Exact directed bank-pair FX overlap",
                "",
                "Aggregate pair counts only. Bank identities never exported.",
                "Thresholds were selected before any H-F03 outcome was read.",
            ]
            for pop in ("dev","P0"):
                summary, levels = overlap[pop]
                lines += [
                    f"### Population {pop}",
                    "Bank-pair groups: " + str(summary["observed_pairs"]),
                    "Both-state pairs: " + str(summary["both_state_pairs"]),
                    "FX0-only pairs: " + str(summary["fx0_only_pairs"]),
                    "FX1-only pairs: " + str(summary["fx1_only_pairs"]),
                ]
                u0_local, u1_local = ((universe[1], universe[2]) if pop=="dev"
                                      else (counts["P0"][1], counts["P0"][2]))
                levels_out = [(t,pairs,n0,n1,
                               100*n0/u0_local if u0_local else None,
                               100*n1/u1_local if u1_local else None)
                              for t,pairs,n0,n1 in levels]
                lines += report_table(
                    ("Min per FX","Qualifying directed pairs","Retained FX0",
                     "Retained FX1","FX0 coverage %","FX1 coverage %"),
                    levels_out)
                lines.append("")
            lines += [
                "## Scientific limitations and counterexamples",
                "",
                "- Reference choice changes W and C without changing their exact sum D;",
                "  none of these W/C components identifies a causal step of the generator.",
                "- P0/P1/P3 have nested but DIFFERENT support. Only within a fixed P can",
                "  changing matched resolution be interpreted without population switching.",
                "- Shared accounts/banks/routes/time make rows dependent; no CI is reported.",
                "- Exact-bank positivity may fail for sampling and/or hidden structural reasons.",
                "- Amount conditioning may induce selection/collider effects; amount is not",
                "  a clean negative-control outcome.",
                "- Existing H-F01/H-F02 private results were known before this exploratory",
                "  investigation; July outcomes have not been read by this script.",
                "- S4 exact path was not part of H-F03 and was not run.",
                "- Any public disclosure requires explicit review including complementary",
                "  small-cell reconstruction; this report is PRIVATE by default.",
                "",
            ]
            PRIVATE_ROOT.mkdir(parents=True, exist_ok=True)
            temp_report = PRIVATE_REPORT.with_suffix(".md.partial")
            temp_report.write_text("\n".join(lines), encoding="utf-8")
            cutoff_guard()
            os.replace(temp_report, PRIVATE_REPORT)
            print("OK: H-F03 exploratory PRIVATE report written locally; coordinator review required.")
            return 0
        finally:
            con.close()
    except Exception as exc:
        # DuckDB paths, parsing failures or exception payloads may contain sponsor values.
        print("ERROR: " + type(exc).__name__ +
              "; details intentionally withheld to protect sponsor data.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
