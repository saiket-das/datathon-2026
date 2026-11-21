# H-A14 — Adjacent country currency modes and FX count

- **Owner:** A
- **Status at freeze:** ready for a reused-account internal test
- **Command:** `uv run python analysis/10_amounts_currency/H-A14_currency_class_disagreement.py`

## Proposed mechanism

FX count equals the number of adjacent changes in the currency modes
mapped onto visible path countries. Country modes are learned from the
payment currency associated with first visible path country. Equivalent
currencies between different countries can account for missing merges
in the FX-trained H-A03 graph. Shared upstream metadata, path selection
and a lookup of equivalent countries are competing explanations.

## Frozen test plan

- Use the existing H-A03 fit on unlabelled bit-0 two-bank payments across
  available dates. Independently of FX labels, learn first-visible-country
  payment currency modes on pre-July unlabelled bit-0 payments, with at least
  100 payments per country. Ties use lexical currency order.
- Score July unlabelled paths with more than two visible banks. Ignore gap
  placeholders. Both maps must support every visible country. Compute the
  change count for each map on the same rows. Use the published account
  partition predicate. Score bit-0 for exploration and bit-1 for validation.
- Practical acceptance requires ≥95% coverage of scoped records, ≥100
  senders, receivers and ordering banks, ≥100 errors from the class-count
  comparator, zero errors or upper-bound violations from the currency-mode
  count, and a lower 99% paired bank-resampling lift ≥.002. Failure of any
  criterion rejects the scoped compound claim. Use 1,000 whole ordering-bank
  resamples, seed 20261117. The interval conditions on the maps and does
  not account for related banks, shared corridors or training uncertainty.
- Retain both repaired and broken cases and report shape by inferred-count
  disagreement. Suppress positive event counts below 100. No identifiers,
  modes by country, or payment rows are exported. Currency mode is an
  empirical proxy. No substitution into the earlier frozen A03/A05 tests.
- Freeze the exact implementation and this plan before running
  `--phase validate --freeze SHA`. No alternate validation populations or
  currency map adjustments after accessing designated outcomes.

## Discovery and prior exposure

July bit-0 has 275,211 scoped and 271,176 eligible rows, 53,625 senders and
122,429 receivers. All 1,051 H-A03 errors occur where the currency-mode
count is smaller. The new count repairs all 1,051 and breaks zero prior
correct predictions. All other 270,125 eligible rows have equal counts.
The July scope excludes 4,035 rows lacking joint support.

Phase 0 described full-data structural bounds. A01/A02/A10/A12 examined
amount outcomes on reused accounts. A03 and A05 revealed errors and signs
of the frozen FX-trained map on account bit-1. A11 scored the single-change
subset on July bit-1. A06/A08 exposed currency/path membership associations
on July bit-1 and selected the currency mode map motivation. A04/A07/A09
and A13 development were on bit-0. No prior frozen test compared adjacent
mode changes with recorded FX counts on July bit-1. Literal endpoints
split by account parity, but calendar dates, banks, corridors, path
entities and earlier scored records overlap.

## Confirmation and robustness results

The unchanged test passed at freeze `7bd948fa5a5663bb9fc3d57ebd35bb567f4ab38f`.
Of 257,566 scoped July bit-1 payments, 253,934 were jointly mapped (98.59%)
and 3,632 lacked joint support. Eligible counts included 52,571 senders,
119,287 receivers and 4,838 declared ordering banks. Mode changes repaired
all 1,036 class-count errors, with zero new errors or bound violations.
The absolute gain was 0.408 percentage points, with a 99% ordering-bank
sensitivity interval of 0.325 to 0.521 points.
[Full aggregate results](../../analysis/10_amounts_currency/out/H-A14_currency_class_disagreement_validate.md).

## Assessment

Adjacent currency-mode changes recover the observed count on the jointly
supported July internal test. Every FX-trained class mismatch there falls
where the mode map implies fewer transitions. Scope is limited to mapped
multibank paths on reused records. A03's frozen failure retains its original
scope. The underlying currency assignment and stage ordering remain open.
