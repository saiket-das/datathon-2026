# Investigator G · Adversarial replication

Independent research owner: **G**, separate from A/B/C and blind D/E discovery.
All work is discovery-only and stops at **2026-11-18 20:00 MYT**.

Files:
- G_LEDGER.md: append-only exposure, failed tests and recovery ledger.
- R-G01_visible_endpoints.py: independent B12 operationalisation, training, control models, eligibility denominator audit and dependent-unit sensitivity.
- test_R_G01.py: synthetic fixture tests that do not access the sponsor dataset.
- run_local_executor.sh: opt-in *local* execution path with branch/remote guards and a mandatory manual publication gate. Not a cloud executor.
- out/R-G01_aggregates.md: generated aggregate report after a real local dataset run. NEVER fabricate this file to appear executed.
- ../../findings/hypotheses/R-G01_directed_visible_endpoints.md: frozen test plan and assumptions.


## G-PERIODS: EXISTING APPROVAL QUEUE HANDOFF (NOT YET SUBMITTED)

The user reports an existing Windows local executor with separate E/F/G approval
queues, Docker network disabled, read-only Parquet mounts, memory/time limits,
and local-only results. This Chat cannot inspect its Windows filesystem,
queue schema, Docker bind targets or approval status. **Do not invent a queue
path, create an unapproved job, bypass approval, or claim it has run.**

The new G-only script G_period_support.py has **no dependence** on a particular
mount path and changes **none** of the R-G01 scientific definitions. It accepts:

- --data /real/read-only/mount/payments.parquet for the complete Parquet; OR
- --data-dir /real/read-only/mount/ for all five exact
  payments_part_01_of_05.parquet through payments_part_05_of_05.parquet files.
- --script-commit FULL_COMMIT_SHA must equal checkout HEAD and the committed
  script bytes.
- --approved-job-id REAL_G_QUEUE_APPROVAL_ID from the existing approval gate.
- --private-output /real/private/results/path/g-periods.json, or ignored
  dataset/g_executor/g-periods.json when the checkout is writable.

The G queue operator must inspect its own actual mounts/permissions and
queue schema, approve ONLY the periods phase, and then submit/run the exact
command under the existing sandbox. Do not execute the sponsor dataset
outside that approved path.

**G-PERIODS deliberately projects only EPOCH_SECONDS**; it returns UTC
calendar-month counts, total rows (expected 10 million), exact script commit,
Docker/Python/DuckDB-related metadata, and source SHA256 digests computed
both before and after the query. Output is a local private JSON file. It
does not query TRANSACTION_TYPE_CODE, July classification outcomes, payment
identifiers, FX, BIC8_PATH or any account details. No automatic publication.

Example command **template only, NOT an approved/submitted job**:

~~~bash
uv run python analysis/40_g_adversarial/G_period_support.py \
  --data-dir /ACTUAL_VERIFIED_READ_ONLY_MOUNT \
  --script-commit FULL_COMMIT_SHA \
  --approved-job-id REAL_G_QUEUE_APPROVAL_ID \
  --private-output /ACTUAL_PRIVATE_OUTPUT_MOUNT/g-periods.json
~~~

The executor must return status/exit code, exact commit, private JSON and
timestamp; Investigator G must first recover these privately, then select
and commit literal FROZEN_PERIODS: YYYY-05 -> YYYY-07 and the final
R-G01 executable. **No R-G01 validation before that commit.** The
R-G01 validator currently expects a *single* full Parquet source; if
G-PERIODS finds only split mounts, change solely its input adapter
and regression-test it BEFORE freezing, without changing path/label rules.

## R-G01 frozen validation · operator instructions (2026-11-17)

The pre-freeze G-PERIODS job `g-periods-61a039d` is reported by the coordinator as successful, using ONLY `EPOCH_SECONDS` (10,000,000 unfiltered records; May 2023: 3,044,400; July 2023: 2,899,279). This is calendar exposure, **not** eligibility or validation. Its source fingerprint and full JSON stay private.

**Immutable scientific freeze:** `09807e62e4155229b64feec23362c31f197cd3a3`, containing `FROZEN_PERIODS: 2023-05 -> 2023-07` and the exact unchanged R-G01 validator. The executable trains on all May 2023 UTC Covered/Indirect endpoint-valid rows and reserves July 2023 UTC for the designated outcome test. Do not modify either frozen file, or read July outcomes before an approved validation job.

**Current blocker:** no separate approved R-G01 validation job ID or verified complete single-file Parquet mount has been supplied to Investigator G. A previous *periods-only* approval is not a validation approval. If the executor exposes only five split parts, **STOP**; the frozen validator currently requires a complete single file. A new input-only adapter and pre-outcome re-freeze would be necessary.

The operator must independently authenticate the G queue approval and Docker's offline, read-only complete source. **New fail-closed checks:** provide the private G-PERIODS source fingerprint through `G_PERIODS_SOURCE_SHA256` (64 lowercase hex characters, never printed or committed); the wrapper compares the complete input SHA256 before reading validation labels, and checks 10,000,000 non-null `EPOCH_SECONDS` entries with a period-only preflight. Both `analysis/40_g_adversarial/out` and `dataset/g_executor` must already be writable private directory mounts or symlinks resolving **outside** the public Git checkout; the wrapper rejects in-checkout output paths. It does not authenticate the queue ID, prove Docker isolation/read-only mounts, or guarantee concurrent immutability. A matching ID regex proves nothing. Maintain a clean checkout on `codex/r2-g-falsification`.

**Approved-job execution template, NOT an approval or a command executed by Chat:**

~~~bash
bash analysis/40_g_adversarial/run_local_executor.sh \
  ACTUAL_APPROVED_G_VALIDATION_JOB_ID \
  /ACTUAL_VERIFIED_READ_ONLY_MOUNT/payments.parquet
~~~

The wrapper hardcodes the exact freeze and UTC cohorts, verifies branch, remote, clean tree, freeze ancestry and file bytes, refuses pre-existing outputs, checks private output directory resolution, validates private input SHA256 and the 10M-row EPOCH_SECONDS-only preflight, runs `uv run pytest` and invokes the frozen validator. It then checks that private report and metadata exist. An approved job must independently ensure the output paths are on private writable storage, not a public checkout. The validator's source SHA256 guard checks pre/post bytes but does not prove source immutability against swap/reversion.

**Post-run handling:** keep `analysis/40_g_adversarial/out/R-G01_aggregates.md` and `dataset/g_executor/R-G01_metadata.json` private until a disclosure review. Confirm report hash and job identity, full eligible/unsupported denominators, exact failures, negative controls, clustering and overlap. Suppressed small counts may be reconstructed from totals, percentages or Clopper-Pearson bounds; never auto-publish. A separate reviewed aggregate-only Git publication may be approved later. The result is at most an internal same-dataset reimplementation, never independent dataset confirmation.

**Next research direction:** if validation remains blocked, prepare an independently testable input compatibility or disclosure safety improvement without changing the frozen scientific rules. Continue R-G02/B14 only after R-G01's first controlled attempt or a documented durable blocker.

## Limitations

The protocol's visible endpoint definition is independently constructed.
It is not a guaranteed exact replica of B12's original selection rule. If
the source differs, report discrepancies before reading B12's code.
May/July partitions share entities and previous aggregate exposure.
