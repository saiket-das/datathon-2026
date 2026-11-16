# H-000: <short title>

Copy this file to `H-<owner letter><number>_<short_name>.md`, for example `H-A01_amount_by_party_pair.md`. The owner letter keeps IDs from colliding.

- **Owner:** A / B / C
- **Status:** exploratory | confirmation-ready | replicated | rejected | uncertain
- **Script / exact command / commit:** `uv run python analysis/<folder>/<script>.py`; <commit>
- **Chart:** `analysis/<folder>/out/<file>.png`

## Proposed rule and scope
When <condition>, <variable> changes by <effect> relative to <baseline>, for <population>.
List input/outcome variables, unit of analysis, exclusions, and why this is more than a definition.

## Test plan (freeze before confirmation)
While developing this hypothesis, query only the selected exploration partition. Do not
examine confirmation or robustness results until the proposed rule, comparator, acceptance
criteria and validation design are frozen in a commit. Record that commit and any prior exposure below.

- Comparator, statistic and effect-size/exception tolerance:
- Alternative explanations and controls:
- Falsification criterion (what result would reject or limit the proposed rule):
- Partition scheme, exact predicate/seed, eligible coverage and effective entity support:
- Primary confirmation test and separately labelled bank/time robustness checks:
- Freeze commit/time; any prior access to confirmation outcomes:

Use the [shared validation protocol](../../docs/03_execution_plan.md#6-shared-scientific-foundation-and-validation).
Phase 0 already inspected full-data aggregates; no partition is wholly unseen data.

## Discovery evidence
Calculation/chart, denominator, effect size, coverage (count/share), exceptions and uncertainty.

## Confirmation and robustness results
Report the unchanged test's result, support, uncertainty and exceptions. Separate primary
confirmation from exploratory sensitivity checks. Record failures and any post-freeze changes;
a revised rule needs fresh confirmation, not relabelling the failed test.

## Assessment
Final wording and scope; confidence and limitations. Distinguish documented definition,
dataset-exact relationship, replicated association and unresolved mechanism. Functional
dependence alone does not establish causal direction or the original generating code.

## Real-world explanation (interpretation, not evidence)
Why a real payment system might behave like this, and one alternative explanation.
