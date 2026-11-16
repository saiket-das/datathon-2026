# Investigator G · Adversarial replication

Independent research owner: **G**, separate from A/B/C and blind D/E discovery.
All work is discovery-only and stops at **2026-11-18 20:00 MYT**.

Files:
- G_LEDGER.md: append-only exposure, failed tests and recovery ledger.
- R-G01_visible_endpoints.py: independent B12 operationalisation, training, control models, eligibility denominator audit and dependent-unit sensitivity.
- test_R_G01.py: synthetic fixture tests that do not access the sponsor dataset.
- run_local_executor.sh: opt-in *local* execution path with branch/remote guards. Not a cloud executor.
- out/R-G01_aggregates.md: generated aggregate report after a real local dataset run. NEVER fabricate this file to appear executed.
- ../../findings/hypotheses/R-G01_directed_visible_endpoints.md: frozen test plan and assumptions.

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

The local executor runs uv run pytest, then the frozen script; writes the aggregate
Markdown under G's out/; records ignored execution metadata under
dataset/g_executor/; appends a run entry to G_LEDGER.md; and pushes only
that checked aggregate report and ledger to codex/r2-g-falsification
after checking the remote is exactly the user-authorised repository. Use only
on the authorised team machine and within the temporary disclosure scope.

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
