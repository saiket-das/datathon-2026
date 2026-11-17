#!/usr/bin/env bash
# G R-G01 validation: operator-invoked ONLY after a separately approved G queue job.
# Usage (inside approved offline Docker):
# bash analysis/40_g_adversarial/run_local_executor.sh \
#   APPROVED_G_JOB_ID /VERIFIED_READ_ONLY_MOUNT/payments.parquet
# Never invoke this wrapper from CI or Chat. No auto-push or report publication.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
BRANCH="codex/r2-g-falsification"
REPO="saiket-das/datathon-2026"
FREEZE="09807e62e4155229b64feec23362c31f197cd3a3"
JOB_ID="${1:-}"
DATA="${2:-}"
if [[ ! "$JOB_ID" =~ ^g-[a-zA-Z0-9_-]{5,100}$ ]]; then
  echo "ERROR: genuine separately approved G validation queue job ID required" >&2
  exit 2
fi
if [[ -z "$DATA" || "$DATA" != /* || ! -f "$DATA" || ! -s "$DATA" ]]; then
  echo "ERROR: explicit absolute path to complete, verified read-only Parquet required" >&2
  exit 2
fi
if [[ "$(git branch --show-current)" != "$BRANCH" ]]; then
  echo "ERROR: wrong branch" >&2; exit 2
fi
REMOTE="$(git remote get-url origin)"
if [[ "$REMOTE" != "https://github.com/$REPO.git" &&
      "$REMOTE" != "git@github.com:$REPO.git" &&
      "$REMOTE" != "https://github.com/$REPO" ]]; then
  echo "ERROR: unexpected remote" >&2; exit 2
fi
if [[ -n "$(git status --porcelain --untracked-files=normal)" ]]; then
  echo "ERROR: worktree must be clean" >&2; exit 2
fi
# Validate that the freeze commit is an ancestor and the frozen bytes match.
git merge-base --is-ancestor "$FREEZE" HEAD || {
  echo "ERROR: frozen commit not ancestor" >&2; exit 2;
}
for FILE in analysis/40_g_adversarial/R-G01_visible_endpoints.py \
            findings/hypotheses/R-G01_directed_visible_endpoints.md; do
  EXPECTED="$(git rev-parse "$FREEZE:$FILE")"
  ACTUAL="$(git hash-object "$FILE")"
  if [[ "$EXPECTED" != "$ACTUAL" ]]; then
    echo "ERROR: frozen artifact changed: $FILE" >&2; exit 2
  fi
done
# Refuse an existing output, including a stale report from an earlier run.
REPORT="analysis/40_g_adversarial/out/R-G01_aggregates.md"
METADATA="dataset/g_executor/R-G01_metadata.json"
if [[ -e "$REPORT" || -e "$METADATA" ]]; then
  echo "ERROR: stale output exists; operator must archive privately before new run" >&2
  exit 2
fi
# Fail closed unless both output directories resolve OUTSIDE the public Git checkout.
# Operators must mount them on private writable storage (symlinks are acceptable).
# Checking directories, not only file paths, avoids accidentally writing an
# unreviewed report into a Git-tracked public checkout.
CHECKOUT="$(pwd -P)"
for OUTDIR in "analysis/40_g_adversarial/out" "dataset/g_executor"; do
  if [[ ! -d "$OUTDIR" ]]; then
    echo "ERROR: private output directory missing: $OUTDIR" >&2; exit 2
  fi
  RESOLVED="$(cd "$OUTDIR" && pwd -P)"
  if [[ "$RESOLVED" == "$CHECKOUT" || "$RESOLVED" == "$CHECKOUT/"* ]]; then
    echo "ERROR: output directory resolves inside public checkout: $OUTDIR" >&2
    exit 2
  fi
  if [[ ! -w "$OUTDIR" ]]; then
    echo "ERROR: private output directory not writable: $OUTDIR" >&2; exit 2
  fi
done
# Private fingerprint from the approved periods-only job MUST be passed by the
# operator inside the offline container. Never print the digest or publish it.
if [[ ! "${G_PERIODS_SOURCE_SHA256:-}" =~ ^[0-9a-f]{64}$ ]]; then
  echo "ERROR: G_PERIODS_SOURCE_SHA256 must contain verified private source digest" >&2
  exit 2
fi
ACTUAL_SHA="$(sha256sum "$DATA" | awk '{print $1}')"
if [[ "$ACTUAL_SHA" != "$G_PERIODS_SOURCE_SHA256" ]]; then
  echo "ERROR: input does not match the private periods-only source fingerprint" >&2
  exit 2
fi
# Read ONLY EPOCH_SECONDS before validation. A matching SHA already binds the
# same source bytes, but this independently checks the required 10M-row scope.
uv run python - "$DATA" <<'PY'
import sys
import duckdb
p = sys.argv[1]
con = duckdb.connect(":memory:")
try:
    count = con.execute(
        "SELECT count(EPOCH_SECONDS) FROM read_parquet(?)", [p]
    ).fetchone()[0]
finally:
    con.close()
if count != 10_000_000:
    raise SystemExit("ERROR: expected exactly 10,000,000 non-null EPOCH_SECONDS rows")
PY
# The queue operator MUST independently authenticate job approval, read-only
# input mount, Docker isolation, and private output mounts. This wrapper checks
# job-ID syntax, not approval authenticity.
uv run pytest
uv run python analysis/40_g_adversarial/R-G01_visible_endpoints.py \
  --phase validate --train-period 2023-05 --eval-period 2023-07 \
  --freeze-commit "$FREEZE" --data "$DATA"
if [[ ! -s "$REPORT" || ! -s "$METADATA" ]]; then
  echo "ERROR: fresh report or metadata missing" >&2; exit 3
fi
printf '%s\n' \
  "R-G01 local execution complete; no publication authorised." \
  "Approved-job identifier (operator supplied, not independently verified): $JOB_ID" \
  "Freeze commit: $FREEZE" \
  "Local report: $REPORT" \
  "Report SHA256: $(sha256sum "$REPORT" | awk '{print $1}')" \
  "Review overlapping totals, percentages, confidence bounds and suppressed cells before release."
