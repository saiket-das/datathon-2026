"""H-F02 exploratory FX-duration confounding checks. NOT a frozen validation.

Run from repository root:
    uv run python analysis/40_cross_mechanisms/H-F02_bank_path_confounding.py --data-dir /absolute/local/parquet-directory

The source must be either dataset/payments.parquet or all five verified
payments_part_XX_of_05.parquet files. No row-level data or entity values are
printed or saved. S4 exact-path exploratory support check is opt-in using
--include-exact-path because its cardinality may exceed laptop RAM.
Report: analysis/40_cross_mechanisms/out/H-F02_bank_path_confounding.md.
This program cannot run at or beyond 2026-11-18 20:00 Asia/Kuala_Lumpur.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import sys

import duckdb

ROOT = Path(__file__).resolve().parents[2]
REPORT = Path(__file__).parent / "out/H-F02_bank_path_confounding.md"
CUTOFF_UTC = datetime(2026, 11, 18, 12, tzinfo=timezone.utc)

EXPECTED_SHA = (
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
    "ANOMALY_TYPE", "ts_utc", "ord_country", "ben_country", "path_len", "gap_count",
}
S0 = ["route", "participants", "currency", "party_pair", "gaps"]
SCHEMES = {
    "S0": (S0, ""),
    "S1": (S0 + ["ord_country", "ben_country"], ""),
    "S2": (S0 + ["ord_bank", "ben_bank"], ""),
    "S3": (S0 + ["ord_country", "ben_country", "amount_band"], ""),
    "S4": (S0 + ["path"], "AND route = 'Direct'"),
}


def guard() -> None:
    if datetime.now(timezone.utc) >= CUTOFF_UTC:
        raise TimeoutError("Scientific cutoff reached")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            guard()
            h.update(chunk)
    return h.hexdigest()


def get_sources(data_dir: Path) -> tuple[list[Path], bool]:
    one = data_dir / "payments.parquet"
    if one.is_file():
        return [one], False
    files = [data_dir / f"payments_part_{i:02d}_of_05.parquet" for i in range(1, 6)]
    if not all(p.is_file() for p in files):
        raise FileNotFoundError("Require complete local Parquet dataset")
    return files, True


def source_expr(paths: list[Path]) -> str:
    quoted = ["'" + p.as_posix().replace("'", "''") + "'" for p in paths]
    return quoted[0] if len(quoted) == 1 else "[" + ",".join(quoted) + "]"


def scheme_query(keys: list[str], condition: str) -> str:
    k = ", ".join(keys)
    return f"""
      WITH g AS (
         SELECT {k}, fx, count(*) n,
                avg(ln(1.0 + seconds)) d,
                avg(ln(1.0 + amount)) a
         FROM dev
         WHERE fx IN (0, 1) {condition}
         GROUP BY {k}, fx
      ), p AS (
         SELECT {k},
                max(n) FILTER (WHERE fx = 0) n0,
                max(n) FILTER (WHERE fx = 1) n1,
                max(d) FILTER (WHERE fx = 0) d0,
                max(d) FILTER (WHERE fx = 1) d1,
                max(a) FILTER (WHERE fx = 0) a0,
                max(a) FILTER (WHERE fx = 1) a1
         FROM g GROUP BY {k}
      ), paired AS (
         SELECT n0, n1, least(n0,n1) w, d1-d0 dd, a1-a0 da
         FROM p WHERE n0 >= 100 AND n1 >= 100
      )
      SELECT count(*) matched_strata,
             coalesce(sum(n0),0) matched_n_fx0,
             coalesce(sum(n1),0) matched_n_fx1,
             coalesce(sum(w),0) total_weight,
             sum(w*dd)/nullif(sum(w),0) duration_log_diff,
             sum(w*da)/nullif(sum(w),0) amount_log_diff,
             count(*) FILTER (WHERE dd < 0) negative_duration_strata,
             count(*) FILTER (WHERE dd > 0) positive_duration_strata
      FROM paired
    """


def fmt(v: object) -> str:
    if v is None:
        return "unsupported"
    if isinstance(v, float):
        return f"{v:.6f}"
    return str(v)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", type=Path, default=ROOT / "dataset")
    ap.add_argument("--out", type=Path, default=REPORT)
    ap.add_argument("--include-exact-path", action="store_true")
    args = ap.parse_args()
    try:
        guard()
        if args.out.suffix.lower() != ".md" or args.out.resolve().is_relative_to(args.data_dir.resolve()):
            raise ValueError("Must write aggregate Markdown outside sponsor data directory")
        paths, split = get_sources(args.data_dir.resolve())
        file_shas = [digest(p) for p in paths]
        if split and tuple(file_shas) != EXPECTED_SHA:
            raise ValueError("Manifest SHA-256 mismatch; stop")
        con = duckdb.connect()
        try:
            con.execute("SET threads=2; SET memory_limit='3GB'; SET TimeZone='UTC'")
            con.execute("CREATE TEMP VIEW payments AS SELECT * FROM read_parquet(" +
                        source_expr(paths) + ")")
            column_names = {r[0] for r in con.execute("DESCRIBE payments").fetchall()}
            if column_names != REQUIRED:
                raise ValueError("Expected exact 26-column dataset schema")
            n_all, n_id = con.execute(
                "SELECT count(*), count(DISTINCT ROW_ID) FROM payments"
            ).fetchone()
            if n_all != 10_000_000 or n_id != n_all:
                raise ValueError("Unexpected source population or ROW_ID duplication")
            if split:
                for path in paths:
                    guard()
                    n_part = con.execute(
                        "SELECT count(*) FROM read_parquet(" + source_expr([path]) + ")"
                    ).fetchone()[0]
                    if n_part != 2_000_000:
                        raise ValueError("Part row count mismatch")

            # H-F01 exact development eligibility, no July validation records.
            con.execute("""
                CREATE TEMP VIEW dev AS
                SELECT TRANSACTION_TYPE_CODE route,
                       PARTICIPANT_COUNT participants,
                       CURRENCY_CODE currency,
                       ORDERING_TYPE || BENEFICIARY_TYPE party_pair,
                       gap_count gaps,
                       CURRENCY_CONVERSION_COUNT fx,
                       USD_AMOUNT amount,
                       TOTAL_DURATION AS seconds,
                       ORDERING_BIC8 ord_bank, BENEFICIARY_BIC8 ben_bank,
                       ord_country, ben_country, BIC8_PATH path,
                       CAST(LEAST(31, floor(log2(1.0 + USD_AMOUNT))) AS INTEGER)
                         amount_band
                FROM payments
                WHERE ts_utc >= TIMESTAMP '2023-05-01'
                  AND ts_utc < TIMESTAMP '2023-07-01'
                  AND ANOMALY_TYPE IS NULL
                  AND TOTAL_DURATION >= 0 AND USD_AMOUNT >= 0
                  AND PARTICIPANT_COUNT BETWEEN 2 AND 5
                  AND CURRENCY_CONVERSION_COUNT BETWEEN 0 AND 3
            """)
            guard()
            total, total_fx0, total_fx1 = con.execute("""
                SELECT count(*),
                       count(*) FILTER (WHERE fx=0),
                       count(*) FILTER (WHERE fx=1)
                FROM dev
            """).fetchone()

            rows = []
            for name, (keys, condition) in SCHEMES.items():
                guard()
                if name == "S4" and not args.include_exact_path:
                    rows.append((name, "not run (opt-in)", *(["-"] * 9)))
                    continue
                values = con.execute(scheme_query(keys, condition)).fetchone()
                strata, n0, n1, wt, logd, loga, neg, pos = values
                rows.append((name, strata, n0, n1, wt, logd, loga, neg, pos,
                             (100*n0/total_fx0 if total_fx0 else None),
                             (100*n1/total_fx1 if total_fx1 else None)))

            guard()
            lines = [
                "# H-F02 — FX duration selection and support audit",
                "",
                "**Status: exploratory only; no confirmation, freeze, CI or causal claim.**",
                f"UTC produced: {datetime.now(timezone.utc).isoformat()}",
                f"Script SHA-256: {digest(Path(__file__))}",
                f"Full dataset: {n_all}; unique ROW_ID: {n_id}; columns: {len(column_names)}",
                f"Data source files: {len(paths)}; all-source SHA-256: " +
                ", ".join(file_shas),
                f"Verified against split manifest: {split}",
                f"Development eligible n: {total}; FX=0 n: {total_fx0}; FX=1 n: {total_fx1}",
                "Period: 2023-05-01 (inclusive) to 2023-07-01 (exclusive) UTC.",
                "Eligibility: anomaly null, amount/duration nonnegative, participants 2–5, FX 0–3.",
                "Each matched stratum must support >=100 rows in EACH FX state.",
                "Weights = min(n0,n1); contrast FX1 minus FX0 of mean log(1+outcome).",
                "",
                "| Scheme | Matched strata | FX0 eligible matched | FX1 eligible matched | Weight | Duration log diff | Amount log diff | Negative duration strata | Positive duration strata | FX0 coverage % | FX1 coverage % |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
            for row in rows:
                lines.append("| " + " | ".join(fmt(value) for value in row) + " |")
            lines += [
                "",
                "S0: route×participants×currency×B/C pair×gap count.",
                "S1: S0 plus both BIC endpoint countries; S2: S0 plus exact directed BIC endpoints.",
                "S3: S1 plus fixed clipped floor(log2(1+USD_AMOUNT)) amount band.",
                "S4: S0 plus exact ordered BIC8_PATH for Direct only; optional memory-heavy check.",
                "",
                "## Scientific limitations",
                "",
                "- This is a descriptive matched comparison. Apparent attenuation can reflect",
                "  dramatically different overlapping subsets rather than confounding removal.",
                "- No row-level uncertainty interval is valid under shared senders, banks,",
                "  intermediary nodes, time and path dependencies; no inferential CI is claimed.",
                "- S2/S4 may lose support. An unsupported within-path effect is not zero.",
                "- The amount contrast diagnoses mix, not an always-null placebo.",
                "- All entity/path group keys remain inside DuckDB; no row or identifier published.",
                "- H-F01 report and coordinator execution metadata must be recovered separately.",
                "- July outcomes are not queried for this hypothesis.",
                "",
            ]
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text("\n".join(lines), encoding="utf-8")
            print("OK: H-F02 exploratory aggregate report written; request coordinator review.")
            return 0
        finally:
            con.close()
    except Exception as exc:
        # Raw-valued SQL errors may be sensitive. Never print exception messages/traces.
        print("ERROR: " + type(exc).__name__ +
              "; details withheld to protect sponsor data. No verified report.",
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
