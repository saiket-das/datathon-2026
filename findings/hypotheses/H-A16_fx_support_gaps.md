# H-A16 — FX currency-map coverage without the class filter

- **Owner:** A
- **Status at freeze:** ready for a reused-account internal test
- **Command:** `uv run python analysis/10_amounts_currency/H-A16_fx_support_gaps.py`
- **Validation:** append `--freeze SHA`

## Proposed mechanism and scope

A14's FX count uses only the currency mode map. Its separate FX-trained
class map was needed for comparison. Removing that eligibility filter
should recover substantial coverage without introducing errors. For paths
with an unknown mode, transitions with both endpoints mapped should
bound the recorded count from below. At most one additional change is
allowed per unscored edge.

## Test plan

- Fit the exact A14 pre-July unlabelled bit-0 modal currency map with
  ≥100 first-visible-country payments and lexical currency ties. Use the
  A03 class graph as the independent support comparator. Also diagnose
  the map accepting every nonempty country training group. This weak
  map leaves any never observed countries unknown and has no acceptance
  threshold.
- Score July unlabelled paths with more than two visible banks, omitting
  gaps as in A14. Explore bit-0 and score bit-1 only after freeze.
  Split by the two original support flags. Report covered and omitted
  counts and errors. Positive event counts below 100 are masked. Mark
  complements smaller than 100 for weak-map coverage.
- Accept if strong mode-only eligibility covers ≥99% of scope, adds
  ≥1,000 payments absent from the class-map scope with ≥100 distinct
  senders, receivers and declared ordering banks, and returns zero
  mode-count errors and zero partial-bound violations. The bounds
  are edgewise necessary conditions and leave many joint assignments
  possible. Any failure rejects the scoped claim at the frozen threshold.
- Report 99% percentile sensitivity for coverage and the newly scored
  fraction from 1,000 whole ordering-bank resamples with seed 20261117.
  These intervals condition on maps and connected geography. They do
  not determine the finite-population acceptance decision.
- Verify executable, plan and helper contents against the freeze before
  scoring. No map fitting uses evaluation FX outcomes.

## Exploration and exposure

July bit-0 has 275,211 scoped multibank payments and 271,176 jointly
supported. Removing the class requirement adds 3,452 correctly counted
payments with 2,306 senders, 2,803 receivers and 954 ordering banks.
Another 583 paths have neither map at the original support floor. The
weak modal map covers nearly all, and all its scored counts match.
Zero observed counts fall outside the edgewise bounds.

Phase 0 structural aggregates and A03/A05 exposed earlier FX constraints.
A08 and A14 exposed July bit-1 currency support, with exactly 3,632 A14
excluded rows known. A14 exposed recorded FX agreement only within joint
support. A11 used a related sparse-transition population and A15 screened
currency endpoint alternatives on July bit-0. This new analysis partitions
that previously known exclusion count and reuses banks, dates and
corridors. Its evaluation is internal even though account IDs differ
across splits. A17 is an amount analysis developed on bit-0.

## Confirmation and robustness results

Pending at freeze.

## Assessment

Separating the support requirements can test whether the old filter hid
contradictions or mostly removed otherwise predictable payments. Weak
mode fits and edgewise bounds are diagnostics of the remaining gap.
