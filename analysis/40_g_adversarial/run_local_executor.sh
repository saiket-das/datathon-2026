#!/usr/bin/env bash
# G read-only dataset executor. Git receives only reviewed aggregates.
# Usage: bash analysis/40_g_adversarial/run_local_executor.sh YYYY FULL40CHARFREEZESHA
set -euo pipefail
cd "$(dirname "\${BASH_SOURCE[0]}")/../.."
YEAR="\${1:-}"
FREEZE="\${2:-}"
BRANCH="codex/r2-g-falsification"
REPO="saiket-das/datathon-2026"
if [[ ! "$YEAR" =~ ^20[0-9]{2}$ ]]; then
  echo "ERROR: provide explicit year after inspecting aggregate period support" >&2
  exit 2
fi
if [[ ! "$FREEZE" =~ ^[0-9a-f]{40}$ ]]; then
  echo "ERROR: provide frozen protocol+script full Git SHA" >&2
  exit 2
fi
if [[ "$(git branch --show-current)" != "$BRANCH" ]]; then
  echo "ERROR: wrong branch; no run or publication" >&2
  exit 2
fi
REMOTE="$(git remote get-url origin)"
if [[ "$REMOTE" != "https://github.com/$REPO.git" &&
      "$REMOTE" != "git@github.com:$REPO.git" &&
      "$REMOTE" != "https://github.com/$REPO" ]]; then
  echo "ERROR: remote not the exact approved repository" >&2
  exit 2
fi
if [[ -n "$(git status --porcelain --untracked-files=normal)" ]]; then
  echo "ERROR: expected clean worktree before test" >&2
  exit 2
fi
if [[ ! -s dataset/payments.parquet ]]; then
  echo "ERROR: local sponsor Parquet absent" >&2
  exit 2
fi
# Git receives only code hashes and aggregates; no sponsor data is added.
uv run pytest
uv run python analysis/40_g_adversarial/R-G01_visible_endpoints.py \
  --phase validate --train-period "\${YEAR}-05" --eval-period "\${YEAR}-07" \
  --freeze-commit "$FREEZE"

REPORT="analysis/40_g_adversarial/out/R-G01_aggregates.md"
LEDGER="analysis/40_g_adversarial/G_LEDGER.md"
if [[ ! -s "$REPORT" ]]; then
  echo "ERROR: no aggregate report; not committing" >&2
  exit 3
fi
REPORT_SHA="$(shasum -a 256 "$REPORT" | awk '{print $1}')"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
{
 echo
 echo "## R-G01 external local executor, \${STAMP} UTC"
 echo "- Recovery head before execution: $(git rev-parse HEAD)"
 echo "- Original frozen test commit: \${FREEZE}"
 echo "- Data: local dataset/payments.parquet, not added to Git; year \${YEAR}"
 echo "- Program: R-G01_visible_endpoints.py; actual dataset script and pytest executed."
 echo "- Aggregate report SHA256: \${REPORT_SHA}"
 echo "- Report: analysis/40_g_adversarial/out/R-G01_aggregates.md"
 echo "- Status: executed internally on reused synthetic dataset, NOT independent confirmation."
 echo "- Read report for denominators, exclusions, failures and negative-control results."
} >> "$LEDGER"
git add -- "$REPORT" "$LEDGER"
CHANGED="$(git diff --cached --name-only)"
if [[ "$CHANGED" != "$REPORT"$'\n'"$LEDGER" &&
      "$CHANGED" != "$LEDGER"$'\n'"$REPORT" ]]; then
  echo "ERROR: unexpected staged contents; refuse publication" >&2
  git reset -- "$REPORT" "$LEDGER" >&2
  exit 3
fi
git diff --cached --check
git commit -m "G: R-G01 supervised local aggregate-only replication"
git push origin "HEAD:refs/heads/\${BRANCH}"
echo "G-R01 EXECUTED: pushed aggregate commit $(git rev-parse HEAD)"
