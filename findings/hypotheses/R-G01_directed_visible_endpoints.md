# R-G01 · Independently reconstruct B12 visible-endpoint classification

**Owner:** Investigator G. **Status:** protocol/code preparation, NO executed dataset evidence.
**Pre-exposure:** B12's aggregate statement, including reported 167,205 July eligible novel paths / 0 errors, read via coordination snapshot. Original B12 implementation intentionally NOT read before writing this independent protocol and code.
**Scientific status:** A correctly implemented re-run of the same 10M-record synthetic dataset is NOT independent dataset confirmation.

## Operational definition (G's test, not a claim about B's hidden implementation)

- Train cohort: calendar May within an explicitly supplied `YYYY-MM` UTC period.
- Test cohort: calendar July within an explicitly supplied `YYYY-MM` UTC period, after protocol/code freeze.
- Labels: exactly `Covered` or `Indirect` from `TRANSACTION_TYPE_CODE`. Exclude Direct/other labels from primary analysis, but report their totals.
- Visible BIC nodes: split `BIC8_PATH` by `;`, trim whitespace, retain tokens matching `^[A-Z0-9]{8}$` and remove ellipsis/non-BIC tokens. Eligible endpoints require at least two retained visible nodes. First and last *visible* BIC nodes define a directed pair, not necessarily physical `ORDERING_BIC8` and `BENEFICIARY_BIC8`.
- Novel July path: the exact raw `BIC8_PATH` string did not occur among training-cohort Covered/Indirect eligible paths. Report both all July and novel-path subset; path novelty does NOT imply pair novelty.
- Training rule: a directed pair is *pure supported* iff it has one observed class and at least one May payment. In case of both classes, mark the pair conflicted and exclude from this pure-map accuracy; separately report excluded support. Never treat abstentions as successes.
- Primary measurement: error rate among July novel paths with May pure directed-pair support, and coverage against (a) all July Covered/Indirect records, (b) all valid-visible-endpoint July Covered/Indirect records, (c) novel-path eligible July records.
- Alternative rules: unordered endpoint pair; first-bank-only; last-bank-only; directed visible endpoint country pair. All are learned on May, evaluated on *identical July subsets*, and compared both at their own coverage and at common support. Reverse direction uses May map for `(last,first)`.
- Negative controls: compare seen vs novel full paths; reverse vs forward ordered pairs; pure vs conflicted training keys; require denominator counts for unseen directed pairs, missing/invalid paths, class exclusions, overlapping account/banks if fields available.
- Uncertainty: one-sided Clopper-Pearson upper error bound for payment units labelled optimistic; repeat at the unique directed-pair level (pair fails if any covered payment misclassified). Record distinct first/last banks as clustering sensitivity, not as independent observations. Never claim cluster-adjusted CI is a proof of independence.

## Proposed frozen acceptance criteria, BEFORE accessing July outcomes

The goal is falsification and scope clarification, not declaring B12 “true.” The following practical checkpoints are fixed for G's first frozen test:

1. Executable pipeline and aggregate-only output succeed; zero identifying records leave the runtime.
2. Primary directed map on July novel paths: report exact error count, eligible population, coverage and pair-level exception counts. A single error falsifies the **zero-error G-operational rule for supported pairs**; it does not automatically falsify B12's original differing eligibility.
3. Never call “generally deterministic” if pure-map eligible coverage is under 90% of novel-path endpoint-valid Covered/Indirect records; if under 90%, retain the within-eligible result only.
4. If a simpler control attains the same error count or better **at equal or greater coverage** on the common target cohort, the specifically *directed-pair* generative interpretation is not uniquely supported.
5. Report at least one adverse subset, or explicitly report none found and the number eligible.
6. Verdict: reimplementation agrees/disagrees/insufficient information, **internal same-dataset only**. No independent confirmation designation.

The above rule definitions are G-created, potentially different from B12. Freeze a Git commit containing BOTH this protocol and the script before any designated July outcome access. Use `--freeze-commit <full SHA>` for `--phase validate`; the runner enforces script/protocol equality with that commit.

## Execution controls

- Inspect timing support without reading labels: `uv run python analysis/40_g_adversarial/R-G01_visible_endpoints.py --phase periods`.
- May exploration only: `uv run python analysis/40_g_adversarial/R-G01_visible_endpoints.py --phase explore --train-period YYYY-05`.
- Frozen July evaluation: `uv run python analysis/40_g_adversarial/R-G01_visible_endpoints.py --phase validate --train-period YYYY-05 --eval-period YYYY-07 --freeze-commit <FULL_40_CHARACTER_SHA>`.
- Data: `dataset/payments.parquet`, local only. Output: privacy-reviewed aggregated Markdown in `analysis/40_g_adversarial/out/R-G01_aggregates.md`, ignored local executor metadata under `dataset/g_executor/`.
- No dataset rows, BIC strings, path strings, account names, tokens, or examples are printed/saved.
- Never claim a run occurred without actual stdout/metadata, execution log and subsequent Git recovery.

## Discovery and validation record

- **May exploratory query:** NOT RUN.
- **July validation outcome:** NOT OPENED BY G.
- **Frozen calendar periods:** NOT YET SELECTED. Periods-only scan is permitted; after learning supported year, append the exact literal `FROZEN_PERIODS: YYYY-05 -> YYYY-07` to this protocol and commit BEFORE running validation. The script rejects uncommitted period choices. Do not substitute periods after inspecting label outcomes.
- **Freeze SHA:** PENDING PERIOD-SPECIFIC COMMIT.
- **Observed numerators/denominators:** NONE from G.
- **Unsupported cohorts:** NOT YET COUNTED.
- **Failures/controls:** NOT YET TESTED.
