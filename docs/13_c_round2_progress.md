# Investigator C Round 2 progress register

Start: 16 November 2026. Branch: `codex/r2-c-entity-mechanisms`, based on
Round 1 PR #5 revision `3f801e90bce616a8aff213c1cce5f409feb5934d`.
Research cutoff: 18 November 2026, 20:00 MYT.

## Exposure and validation policy

Phase 0 exposed full-data structural, balance and label-support aggregates.
Round 1 exposed sender-bit-0 and sender-bit-1 anomaly summaries and C01/C02
copy-burst outcomes. A/B outcome summaries were also available to the coordinator.
Use sender MD5 bit 0 for exploration. Reused bit-1 records permit frozen internal
validation of specifically unexamined outcomes. Shared entities and prior exposure
limit the evidence strength. The freeze records the script, comparator, criteria
and validation design before reading the designated outcomes.

All sponsor processing uses the existing local ignored Parquet with one DuckDB
thread, a 512MB memory limit and disk spilling disabled. Query outputs are
aggregate and minimum support rules govern display. Unlabelled payments are a
comparison population of unknown legitimacy.

## Progress

| Candidate | Mechanism or finding | Validation | Evidence strength | Blockers | Submission impact |
| --- | --- | --- | --- | --- | --- |
| [C03 immediate source-neighbour edit](../findings/hypotheses/H-C03_adjacent_edit.md) | Neither account matches at either adjacent offset in the three supported classes | Exploration only | Rejected | Recall neighbour cohorts lack support. Different positions and replacement of both accounts remain open. | Useful negative control for extending the C01/C02 batch patterns |
| [C04 literal LINEBREAK marker](../findings/hypotheses/H-C04_literal_linebreak.md) | More than 4.97M rows per role contain line feeds without the proposed literal marker | Exploration only | Rejected | Structured encoding remains unresolved. | Narrow token interpretation caveat |
| [C05 scam endpoint concordance](../findings/hypotheses/H-C05_scam_endpoint_agreement.md) | Two scam labels preserve observed receiving endpoint agreement in discovery, while sender disagreement persists | Freeze and internal validation pending | Exploratory | Covered cohorts are sparse. Prior bit-1 exposure and shared entities limit independence. | Potential constraint on the generator's observable fields |
| Beneficiary profile reuse | The two scam labels seldom reuse exact beneficiary detail strings within the same beneficiary account | Discovery lead only | Unresolved | Account support, activity, bank and cohort mix confound the comparison. | Substitution mechanism remains open |

## Search ledger

1. Read original case-study appendix and Rules sections 2/3 using local pypdf.
2. Cancelled a disjunctive neighbour scan before output due to poor runtime.
   The replacement used an exact candidate-row hash join over the same population.
3. An exploratory profile query with an unlabelled sample exceeded 512MB. Narrowing
   to the four labelled cohorts and running a separate unlabelled control showed
   exact beneficiary-detail reuse is limited even in unlabelled payments.
   The initial account substitution interpretation lacks adequate support.
4. The document's semantic token examples prompted C04. A later aggregate
   character-format check found structured punctuation common in token strings.
   Encoding grammar and context sensitivity remain unresolved.
5. Compared the two endpoint fields within labelled and unlabelled routes.
   Zero receiving mismatch with nonzero ordering mismatch prompted C05.

## Handoff

Run the frozen C05 plan with sender-bit-1 internal validation after the exact
freeze commit. Preserve every criterion outcome and any coverage failure.
Source-order and literal-marker candidates were rejected during discovery and
have no associated validation run. Round 1 C01/C02, scripts and evidence retain
their original scope. Four unresolved label mechanisms remain open.