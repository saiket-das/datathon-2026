"""
G-PERIODS: read-only, UTC calendar support audit for the approved local G queue.

Run from repository root (after G queue approval, inside the existing offline Docker executor):
  uv run python analysis/40_g_adversarial/G_period_support.py \
    --data /READ_ONLY_MOUNT/payments.parquet \
    --script-commit FULL40CHARCOMMIT --approved-job-id QUEUE_JOB_ID \
    --private-output /PRIVATE_RESULT_MOUNT/g-periods.json

OR replace --data with --data-dir /READ_ONLY_MOUNT for exactly five
payments_part_XX_of_05.parquet files. Never guess mount paths; use the
executor's verified read-only mapping.

Only the EPOCH_SECONDS column is selected. No labels, FX, banks, paths,
amounts, text, records or July *validation outcomes* are read. All results,
file names, source fingerprints and metadata remain local; no GitHub push.
This is PRE-FREEZE inspection, not a replication or confirmation.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid
from zoneinfo import ZoneInfo

import duckdb

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_REL = "analysis/40_g_adversarial/G_period_support.py"
BRANCH = "codex/r2-g-falsification"
CUTOFF = datetime(2026, 11, 18, 20, 0, tzinfo=ZoneInfo("Asia/Kuala_Lumpur"))
PARTS = tuple(f"payments_part_{i:02}_of_05.parquet" for i in range(1, 6))


def resolve_sources(data: Path | None, data_dir: Path | None) -> tuple[str, list[Path]]:
    """Accept a single complete source or exactly five manifest-style partitions."""
    if (data is None) == (data_dir is None):
        raise ValueError("Supply exactly one of --data or --data-dir")
    if data is not None:
        path = data.expanduser().resolve(strict=True)
        if not path.is_file() or path.suffix.lower() != ".parquet":
            raise ValueError("The --data target must be an existing Parquet file")
        return "single_parquet", [path]

    directory = data_dir.expanduser().resolve(strict=True)
    if not directory.is_dir():
        raise ValueError("--data-dir must be an existing directory")
    full = directory / "payments.parquet"
    present_parts = sorted(p.name for p in directory.glob("payments_part_*.parquet"))
    if full.is_file() and present_parts:
        raise ValueError("Ambiguous input: both unsplit and partitioned Parquet present")
    if full.is_file():
        return "single_parquet", [full.resolve(strict=True)]
    if present_parts != list(PARTS):
        raise ValueError("Expected exactly five named payments_part_XX_of_05.parquet files")
    return "five_parquet_parts", [
        (directory / filename).resolve(strict=True) for filename in PARTS
    ]


def source_fingerprint(paths: list[Path]) -> list[dict]:
    """Stream cryptographic hashes; results must stay in private executor output."""
    result = []
    for path in paths:
        before = path.stat()
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
                digest.update(chunk)
        after = path.stat()
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise RuntimeError("Source changed while being fingerprinted")
        result.append({
            "source_name": path.name, "size_bytes": after.st_size,
            "mtime_ns": after.st_mtime_ns, "sha256_private": digest.hexdigest()
        })
    return result


def period_counts(paths: list[Path]) -> list[dict]:
    """Only EPOCH_SECONDS is projected; month boundaries are explicitly UTC."""
    conn = duckdb.connect(database=":memory:")
    try:
        conn.execute("SET TimeZone = 'UTC'")
        rows = conn.execute("""
            SELECT strftime(to_timestamp(EPOCH_SECONDS), '%Y-%m') AS utc_month,
                   count(*) AS n
            FROM read_parquet(?)
            GROUP BY 1 ORDER BY 1
        """, [[str(p) for p in paths]]).fetchall()
        return [{"utc_month": month, "count": int(n)} for month, n in rows]
    finally:
        conn.close()


def validate_commit(commit: str) -> None:
    """Bind executable to exact committed Git contents without network access."""
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Provide exact 40-character approved --script-commit")
    def run(*args: str) -> bytes:
        return subprocess.run(
            ["git", *args], cwd=ROOT, check=True, capture_output=True
        ).stdout
    actual_head = run("rev-parse", "HEAD").decode().strip()
    if actual_head != commit:
        raise ValueError("Local checkout HEAD does not match the approved commit")
    branch = run("symbolic-ref", "--short", "--quiet", "HEAD").decode().strip() if (
        subprocess.run(["git", "symbolic-ref", "--quiet", "HEAD"], cwd=ROOT,
                       capture_output=True).returncode == 0
    ) else "DETACHED"
    if branch not in (BRANCH, "DETACHED"):
        raise ValueError("Checkout is not G's dedicated branch or detached approved commit")
    committed_script = run("show", f"{commit}:{SCRIPT_REL}")
    if committed_script != (ROOT / SCRIPT_REL).read_bytes():
        raise ValueError("Working script differs from the approved commit")


def write_private_atomic(output: Path, report: dict) -> None:
    """Only explicit private output; no network, no Git, no publication."""
    final = output.expanduser().resolve(strict=False)
    if final.suffix.lower() != ".json":
        raise ValueError("Private output must use .json")
    if final.is_relative_to(ROOT) and not final.is_relative_to(
        ROOT / "dataset" / "g_executor"
    ):
        raise ValueError("Private output cannot live in a Git-trackable repository folder")
    final.parent.mkdir(parents=True, exist_ok=True)
    temp = final.with_name(final.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        temp.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(temp, final)
    finally:
        temp.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--data", type=Path)
    src.add_argument("--data-dir", type=Path)
    ap.add_argument("--script-commit", required=True)
    ap.add_argument("--approved-job-id", required=True)
    ap.add_argument("--private-output", required=True, type=Path)
    args = ap.parse_args(argv)

    if datetime.now(ZoneInfo("Asia/Kuala_Lumpur")) >= CUTOFF:
        raise SystemExit("Scientific cutoff reached; refuse to execute")
    if not re.fullmatch(r"[A-Za-z0-9._:-]{3,128}", args.approved_job_id):
        ap.error("A concrete approved G queue job ID is required")

    validate_commit(args.script_commit)
    mode, paths = resolve_sources(args.data, args.data_dir)
    before = source_fingerprint(paths)
    counts = period_counts(paths)
    after = source_fingerprint(paths)
    if before != after:
        raise SystemExit("INPUT INTEGRITY FAILURE: source bytes/stat changed; output withheld")

    total = sum(row["count"] for row in counts)
    if total != 10_000_000:
        raise SystemExit(
            f"Unexpected total record count {total}; expected 10000000; output withheld"
        )
    report = {
        "status": "completed_periods_only",
        "scientific_phase": "pre_freeze_calendar_support",
        "no_july_validation_outcomes_accessed": True,
        "utc_finished": datetime.now(timezone.utc).isoformat(),
        "approved_job_id": args.approved_job_id,
        "git_commit": args.script_commit,
        "script_sha256": hashlib.sha256((ROOT / SCRIPT_REL).read_bytes()).hexdigest(),
        "duckdb_version": duckdb.__version__,
        "python_version": sys.version.split()[0],
        "source_mode": mode,
        "source_fingerprints_private": after,
        "calendar_period_counts": counts,
        "total_rows": total,
        "statement": "One source synthetic dataset; five parts are not independent replicates",
    }
    write_private_atomic(args.private_output, report)
    print("G periods-only execution completed; private result file written.")
    print("Job:", args.approved_job_id, "Commit:", args.script_commit)
    print("Input mode:", mode, "Total rows:", total)
    print("Only UTC calendar counts and private source fingerprints produced.")
    print("No July validation labels or other payment attributes accessed.")


if __name__ == "__main__":
    main()
