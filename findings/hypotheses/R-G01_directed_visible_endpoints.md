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
## Immutable R-G01 validation specification · Frozen before July outcome access

**FROZEN_PERIODS: 2023-05 -> 2023-07**

- **Training interval (UTC inclusive/exclusive):** `2023-05-01T00:00:00Z <= ts_utc < 2023-06-01T00:00:00Z`, operationalized by `--train-period 2023-05`, using UTC `strftime(to_timestamp(EPOCH_SECONDS),'%Y-%m')`.
- **Designated validation interval (UTC inclusive/exclusive):** `2023-07-01T00:00:00Z <= ts_utc < 2023-08-01T00:00:00Z`, operationalized by `--eval-period 2023-07`. **DO NOT query July routing labels or paths before this protocol and executable exist in one immutable Git commit.**
- **Calendar-period exposure:** Coordinator-attested G-PERIODS job `g-periods-61a039d` (2026-11-17 10:18 MYT), exit 0. Only `EPOCH_SECONDS` was queried: April 2023 = 6,161, May 2023 = 3,044,400, June 2023 = 4,050,160, July 2023 = 2,899,279; unfiltered total = 10,000,000. These are **NOT** Covered/Indirect eligible denominators, error observations, or new independent confirmation. Private full JSON and source SHA256 remain local. Script commit `61a039d7112dced23a934c328a715da019f997f3`, script SHA256 `c6be68e96f95e9086dbd77031d0045daf87eee2a06ebb782e23534f58f6b1dc1`, private result SHA256 `40e9ca81daa7ad13841cc005b7fd018a60cbae75cd35252cc5eac75b3aaaa612`; values received through coordinator handoff, not independently retrieved from the private executor by G.
- **Dataset and source eligibility:** The exact organiser synthetic dataset, all rows for the two frozen calendar months, no sampling. The executable currently accepts one complete readable Parquet input via `--data` (default `dataset/payments.parquet`), never a partial single partition. A read-only single-file mount must be verified by the separately approved executor before validation; if only five parts are mounted, **STOP** and perform a reviewed input-adapter change followed by a **new** pre-outcome freeze (without changing scientific definitions). Compare private source SHA256 with G-PERIODS provenance locally. No row-level export.
- **Frozen scientific definitions:** All eligibility, parsing, May-pure support rules, July novel-path predicate and control definitions in the preceding sections are unchanged. No labels from June are fit; no April outcomes are inspected for this exercise. May model fitting is deterministic full-population counting, no random seed. The reserved July outcome is first accessed only by a separately approved `--phase validate` job.
- **Frozen control plan:** Directed pair against unordered pair, first-only and last-only bank, ordered visible-BIC country pair, reverse direction, seen-versus-novel paths, May-pure versus conflicted and unseen keys. Report target-support coverage on all three predeclared denominators, class exclusions, and all unsupported/conflicted groups; pair and bank overlaps are dependence limitations.
- **Frozen primary decision criteria:** (i) any error among May-pure-supported July novel-path Covered/Indirect records falsifies the operational **zero-error** rule on that eligible scope; (ii) conditional support under 90% of July novel-path endpoint-valid Covered/Indirect records prohibits any “generally deterministic” wording; (iii) a simpler control with equal or lower errors at equal or greater coverage prevents claiming a uniquely directed-pair generator. Each criterion is evaluated separately, including conjunction failures. No interpolation, post hoc exceptions, or eligibility changes are permitted to rescue failure.
- **Frozen uncertainty:** Exact error counts, full denominators, distinct directed pairs and bank support. Compute payment-level one-sided Clopper-Pearson 95% upper bounds as **optimistic** independence approximations; include pair-level failure count and distinct-bank support sensitivity, explicitly not an independent cluster confidence interval. Do not infer causal ordering or exact generator code.
- **Frozen decision status categories:** internal same-dataset reimplementation **agrees**, **disagrees**, or **insufficient eligibility/support**; never “independently confirmed.” Note prior whole-dataset/May-July shared entity exposure and the previously published B12 aggregate `167,205/0`; no G validation labels or outputs have been accessed as of this freeze.
- **Frozen code artifact:** `analysis/40_g_adversarial/R-G01_visible_endpoints.py` at the **same Git freeze commit that stores this protocol**. Do not modify its bytes after freeze. An entirely new scientific test, if necessary, requires a new freeze entry and must not overwrite this frozen version.
- **Exact validation command once separately approved:** `uv run python analysis/40_g_adversarial/R-G01_visible_endpoints.py --phase validate --train-period 2023-05 --eval-period 2023-07 --freeze-commit <FULL_FREEZE_COMMIT_SHA> --data <EXACT_VERIFIED_FULL_PARQUET_MOUNT>`.
- **Access guard:** Verify Git branch and frozen script/protocol bytes, approved queue job identity, local source fingerprint, prior results disclosure status, and a private result-output location before invoking validation; no direct Chat execution, public GitHub Action or unauthorised queue launch. Keep all generated aggregates local for disclosure review.
- **Freeze record location:** Immutable Git commit containing this document (and the unchanged executable), full SHA/time recorded separately in append-only G ledger. Do not edit this document just to insert its own commit SHA and thereby invalidate the frozen bytes.

## Outcome register (reserved; DO NOT backfill before approved July evaluation)

- **May exploratory query:** NOT RUN by G.
- **July validation outcome:** NOT OPENED by G.
- **Eligible May/July population denominators:** UNKNOWN.
- **Supported / conflicted / unseen pairs:** UNKNOWN.
- **Errors and comparison controls:** NOT TESTED.
- **Source full-file validation mount:** NOT ESTABLISHED by G.
- **Separate G queue R-G01 approval:** NOT GRANTED in this Chat.

