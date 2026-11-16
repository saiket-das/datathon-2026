"""H-F01 exploratory pilot: FX steps, route complexity, duration, and payment mix.

Exact command, from repository root:
    uv run python analysis/40_cross_mechanisms/H-F01_fx_route_duration.py

Optional, for the five locally mounted split Parquet files:
    uv run python analysis/40_cross_mechanisms/H-F01_fx_route_duration.py --data-dir /path/to/parts

Writes ONLY aggregate Markdown to analysis/40_cross_mechanisms/out/H-F01_fx_route_duration.md.
Exploration: unlabelled May and June 2023 payments only. JULY IS NOT READ AS
A VALIDATION POPULATION FOR ANY H-F01 OUTCOME. This script is *not* a freeze.
No bank/account identifiers or individual rows are printed or exported.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import sys

import duckdb

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = ROOT / "dataset"
OUT = Path(__file__).parent / "out" / "H-F01_fx_route_duration.md"

# SHA-256 of supplied five-part manifest. This public metadata is not a payment row.
PART_SHA = (
    "a2a81483abbfa9a5a8b2d284386ccc3a1aa510276c0a310996d9d4b6e569eb6f",
    "86f491806ca0aef869839569bc4f12708959fdd93dc87a2fd36330257e878148",
    "f4b422b8c91e448e74dc05f9ed66007dda0be839c03864db913ca579ae3c8897",
    "6312f1ad764160b5e53a3acd9b49cd01f7f8041ed15c495436094e8438c9a68a",
    "1424a038942f9c67099a68657516a4b3a3f6252253a92510657d5692b4aba567",
)

REQUIRED = {
    "ROW_ID", "EPOCH_SECONDS", "CURRENCY_CODE", "USD_AMOUNT",
    "ORDERING_BIC8", "BENEFICIARY_BIC8", "BIC8_PATH", "TOTAL_DURATION",
    "CONTINUITY_QFLAG", "CURRENCY_CONVERSION_COUNT", "PARTICIPANT_COUNT",
    "TRANSACTION_TYPE_CODE", "ORDERING_ACCOUNT", "BENEFICIARY_ACCOUNT",
    "ORDERING_DETAILS", "ORDERING_TOKENS", "BENEFICIARY_DETAILS",
    "BENEFICIARY_TOKENS", "ORDERING_TYPE", "BENEFICIARY_TYPE",
    "ANOMALY_TYPE", "ts_utc", "ord_country", "ben_country", "path_len",
    "gap_count",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source_files(data_dir: Path) -> tuple[list[Path], bool]:
    single = data_dir / "payments.parquet"
    if single.is_file():
        return [single], False
    files = [data_dir / f"payments_part_{i:02d}_of_05.parquet" for i in range(1, 6)]
    if all(p.is_file() for p in files):
        return files, True
    raise FileNotFoundError("All five local Parquet parts (or canonical payments.parquet) are required")


def markdown_table(columns: list[str], rows: list[tuple]) -> str:
    lines = ["| " + " | ".join(columns) + " |",
             "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(x).replace("|", "\\|") for x in row) + " |")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", type=Path, default=DEFAULT_DATA)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--skip-hash", action="store_true",
                    help="Only for local fixture debugging; never use for verified full-data runs")
    args = ap.parse_args()
    if args.out.suffix != ".md" or args.out.resolve().is_relative_to(args.data_dir.resolve()):
        print("ERROR: reports must be Markdown outside dataset directory.", file=sys.stderr)
        return 1
    try:
        files, is_split = source_files(args.data_dir.resolve())
        fingerprints = [sha256_file(p) for p in files] if not args.skip_hash else []
        if is_split and not args.skip_hash and tuple(fingerprints) != PART_SHA:
            raise ValueError("Split file SHA-256 differs from provided manifest")
        con = duckdb.connect()
        try:
            con.execute("SET threads=2; SET memory_limit='2GB'; SET TimeZone='UTC';")
            con.execute("SET preserve_insertion_order=false;")
            # Source paths are local filenames, escaped as SQL literals; never made public.
            literals = [("'" + str(p).replace("'", "''") + "'") for p in files]
            expression = literals[0] if len(files) == 1 else "[" + ",".join(literals) + "]"
            con.execute("CREATE TEMP VIEW payments AS SELECT * FROM read_parquet(" + expression + ")")
            cols = set(x[0] for x in con.execute("DESCRIBE payments").fetchall())
            if len(cols) != 26 or not REQUIRED.issubset(cols):
                raise ValueError("Payment schema is missing required fields")
            count, distinct_id = con.execute(
                "SELECT COUNT(*), COUNT(DISTINCT ROW_ID) FROM payments"
            ).fetchone()
            if count != 10_000_000 or distinct_id != count:
                raise ValueError("Expected ten million unique ROW_IDs")
            if is_split:
                for path in files:
                    literal = "'" + str(path).replace("'", "''") + "'"
                    n = con.execute("SELECT COUNT(*) FROM read_parquet(" + literal + ")").fetchone()[0]
                    if n != 2_000_000:
                        raise ValueError("Manifest part count mismatch")

            # Only development months; never issue H-F01 confirmation queries here.
            con.execute("""
                CREATE TEMP VIEW dev AS
                SELECT TRANSACTION_TYPE_CODE AS route,
                       PARTICIPANT_COUNT AS participants,
                       CURRENCY_CONVERSION_COUNT AS fx,
                       CURRENCY_CODE AS currency,
                       ORDERING_TYPE || BENEFICIARY_TYPE AS party_pair,
                       gap_count AS gaps, TOTAL_DURATION AS seconds,
                       USD_AMOUNT AS amount, ORDERING_ACCOUNT AS sender
                FROM payments
                WHERE ts_utc >= TIMESTAMP '2023-05-01'
                  AND ts_utc < TIMESTAMP '2023-07-01'
                  AND ANOMALY_TYPE IS NULL
                  AND TOTAL_DURATION >= 0 AND USD_AMOUNT >= 0
                  AND PARTICIPANT_COUNT BETWEEN 2 AND 5
                  AND CURRENCY_CONVERSION_COUNT BETWEEN 0 AND 3
            """)
            ndev = con.execute("SELECT COUNT(*) FROM dev").fetchone()[0]
            base = con.execute("""
                SELECT route, participants,
                       CASE WHEN fx >= 2 THEN '2+' ELSE CAST(fx AS VARCHAR) END AS fx_bin,
                       COUNT(*) AS n, COUNT(DISTINCT sender) AS n_senders,
                       ROUND(MEDIAN(seconds),1) AS median_seconds,
                       ROUND(MEDIAN(amount),2) AS median_usd
                FROM dev
                GROUP BY ALL HAVING COUNT(*) >= 100
                ORDER BY route, participants, fx_bin
            """).fetchall()
            base_all = con.execute("""
                SELECT COUNT(*) AS cells, SUM(n) AS represented
                FROM (SELECT COUNT(*) n FROM dev
                      GROUP BY route, participants,
                          CASE WHEN fx>=2 THEN '2+' ELSE CAST(fx AS VARCHAR) END
                      HAVING COUNT(*)>=100)
            """).fetchone()
            matched = con.execute("""
                WITH g AS (
                    SELECT route, participants, currency, party_pair, gaps, fx,
                           COUNT(*) n,
                           AVG(LN(1.0 + seconds)) ld,
                           AVG(LN(1.0 + amount)) la
                    FROM dev WHERE fx IN (0,1)
                    GROUP BY route, participants, currency, party_pair, gaps, fx
                ), p AS (
                    SELECT route, participants, currency, party_pair, gaps,
                           MAX(n) FILTER (WHERE fx=0) n0,
                           MAX(n) FILTER (WHERE fx=1) n1,
                           MAX(ld) FILTER (WHERE fx=0) d0,
                           MAX(ld) FILTER (WHERE fx=1) d1,
                           MAX(la) FILTER (WHERE fx=0) a0,
                           MAX(la) FILTER (WHERE fx=1) a1
                    FROM g GROUP BY route, participants, currency, party_pair, gaps
                ), eligible AS (
                    SELECT *, LEAST(n0,n1) w FROM p WHERE n0>=100 AND n1>=100
                )
                SELECT COUNT(*) strata, COALESCE(SUM(n0),0) n_fx0,
                       COALESCE(SUM(n1),0) n_fx1, COALESCE(SUM(w),0) total_w,
                       SUM(w*(d1-d0))/NULLIF(SUM(w),0) duration_log_diff,
                       SUM(w*(a1-a0))/NULLIF(SUM(w),0) amount_log_diff,
                       MIN(n0) smallest_fx0_cell, MIN(n1) smallest_fx1_cell
                FROM eligible
            """).fetchone()
            # Sender support <100 is suppressed even when payment count is large.
            displayed_base = [tuple(row[:4]) +
                              ((row[4] if row[4] >= 100 else "<100"),) +
                              tuple(row[5:]) for row in base]
            parts = [
                "# H-F01 — exploratory route, FX and duration pilot", "",
                "Scientific status: **EXPLORATORY ONLY; NO VALIDATION OPENED OR FREEZE CLAIMED.**",
                "Population: all unlabelled rows dated May 1 (inclusive) through July 1",
                "(exclusive), 2023 UTC, with non-negative USD amount and duration,",
                "2–5 participants and 0–3 FX steps. Results reflect row dependence;",
                "no causal direction, hidden source code or independent replication is inferred.", "",
                f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
                f"Source file count: {len(files)}; full-data rows: {count:,}; unique ROW_ID: {distinct_id:,}.",
                f"Required schema columns present: {len(REQUIRED)} of {len(REQUIRED)}.",
                f"SHA-256 verified against split manifest: {is_split and not args.skip_hash}.",
                f"Source SHA-256 fingerprints: {', '.join(fingerprints) if fingerprints else 'not computed'}.",
                f"Development eligible denominator: {ndev:,}.", "",
                "## Supported coarse cells (each >=100 records)", "",
                markdown_table(["route","participants","fx_bin","n","distinct_senders",
                                "median_seconds","median_usd"], displayed_base),
                "", f"Coarse cells included: {base_all[0] or 0}; represented rows: {base_all[1] or 0}.",
                "Unsupported cells (<100 rows) are not shown.", "",
                "## Within-stratum comparison, FX=1 minus FX=0", "",
                "Strata: route × participants × currency × B/C party pair × gap count.",
                "Both FX states must have >=100 rows in each retained stratum.",
                "Weight per stratum: min(n_FX0, n_FX1).",
                "Effects are mean log(1+outcome) contrasts, **not causal FX stage effects**.",
                "Amount contrast is a payment-mix confounding diagnostic, not a randomized placebo.",
                markdown_table(
                    ["matched_strata","n_fx0","n_fx1","total_weight",
                     "duration_log_diff","amount_log_diff",
                     "min_n_fx0","min_n_fx1"],
                    [tuple(round(x,6) if isinstance(x,float) else x for x in matched)]
                ),
                "", "## Limitations and next falsifications", "",
                "- Currency and route-cell matching cannot remove sender, beneficiary or",
                "  intermediary-bank selection; those identities are never exported.",
                "- Repeated accounts and banks violate row-level independence. No formal CI",
                "  is claimed from this aggregate pilot; cluster bootstrap belongs in a future freeze.",
                "- A large residual USD amount contrast would weaken a pure processing-time account.",
                "- Examine bank/path selection and account-level support before choosing a",
                "  frozen hypothesis. July outcomes remain unopened by this script.",
                "- No E-specific cross-review until E independently freezes and releases findings.",
                ""
            ]
            args.out.parent.mkdir(parents=True,exist_ok=True)
            args.out.write_text("\n".join(parts),encoding="utf-8")
            print("OK: full-source checks and exploratory aggregates completed; report written.")
            return 0
        finally:
            con.close()
    except Exception as exc:
        # SQL/path errors can contain source values. Never print exception text.
        print("ERROR: " + type(exc).__name__ + "; details suppressed; no verified result.",
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
