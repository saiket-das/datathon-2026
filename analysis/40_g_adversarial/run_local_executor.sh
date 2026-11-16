#!/usr/bin/env bash
# G read-only dataset executor. Git receives only reviewed aggregates.
# Usage: bash analysis/40_g_adversarial/run_local_executor.sh YYYY FULL40CHARFREEZESHA
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
YEAR="${1:-}"
FREEZE="${2:-}"
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
  --phase validate --train-period "${YEAR}-05" --eval-period "${YEAR}-07" \
  --freeze-commit "$FREEZE"

# Privacy gate: NEVER auto-stage, commit, or push a generated report.
# Derived percentages, intervals, or overlapping marginals can reconstruct
# suppressed small cells even when individual counts are masked.
REPORT="analysis/40_g_adversarial/out/R-G01_aggregates.md"
if [[ ! -s "$REPORT" ]]; then
  echo "ERROR: no local aggregate report" >&2
  exit 3
fi
printf '%s\\n' "R-G01 dataset computation finished locally; publication NOT authorised by this script." \\
  "Review all counts, complementary totals, rates, bounds and subgroup intersections" \\
  "for disclosure before any separate human-approved aggregate-only commit." \\
  "Local report: $REPORT" \\
  "Report SHA256: $(shasum -a 256 "$REPORT" | awk '{print $1}')"
