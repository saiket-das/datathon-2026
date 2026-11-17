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

## Step 1: Verify local dataset without opening target labels

From the repository root on the machine holding the original dataset:

~~~bash
uv run pytest
uv run python analysis/40_g_adversarial/R-G01_visible_endpoints.py --phase periods
~~~

This prints only calendar-month record totals to identify the correct year.
The data file must be dataset/payments.parquet and is never sent to GitHub.

## Step 2: Execute after a designated Git freeze

Freeze commit must contain the entire R-G01 protocol and executable. Record the
full SHA and chosen train/evaluation periods *before* viewing July outcomes.

~~~bash
bash analysis/40_g_adversarial/run_local_executor.sh YYYY FULL_40_CHARACTER_FREEZE_COMMIT
~~~

The local executor runs uv run pytest, then the frozen script; writes a LOCAL aggregate
Markdown under G's out/ and ignored execution metadata under dataset/g_executor/.
It deliberately does NOT stage, commit, or push the generated report. A human must
review complementary counts, percentages, uncertainty bounds and subgroup intersections
for recoverable small cells, then explicitly approve any separate aggregate-only
publication on the G branch. Use only on the authorised team machine.

It does not run automatically just because a ChatGPT task has been scheduled.
No GitHub Actions job should be supplied the raw sponsor dataset or a path to it.

## Step 3: Recover

Next G iteration fetches G_LEDGER.md, R-G01_aggregates.md (if present),
and the branch head commit. Confirm report SHA and the prior freeze commit.
Classify output as same-dataset replication, never as fresh independent confirmation.

## Limitations

The protocol's visible endpoint definition is independently constructed.
It is not a guaranteed exact replica of B12's original selection rule. If
the source differs, report discrepancies before reading B12's code.
May/July partitions share entities and previous aggregate exposure.
