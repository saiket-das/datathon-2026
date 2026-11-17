# H-A20 — Route transfer of payment-currency mode maps

- **Owner:** A
- **Status at freeze:** ready for reused-account internal test
- **Command:** `uv run python analysis/10_amounts_currency/H-A20_route_mode_transfer.py`
- **Validation:** append `--freeze SHA`

## Proposed mechanism and competing explanations

The FX count's country-currency equivalences are stable across route
types. Maps trained using payment currencies from two-bank and multibank
paths should agree on FX counts across the supplied July route labels.
Route-specific payment currency mixtures can change which mode wins.
Exact transition agreement can also survive some differences in currency
label as long as the equality structure along paths is unchanged.

## Frozen test

- Fit first visible country modes from unlabelled pre-July bit-0
  payments without FX labels. Fit separately for exactly two and more
  than two visible banks. Require 100 observations per country in each
  training stratum and use lexical currency ties.
- Score July unlabelled rows with at least two visible banks. Require
  every visible country to appear in both independently fitted maps
  for same-row comparison. Record both individual coverage totals.
  Compare number of adjacent mode changes with reported FX count.
- Explore bit-0 and internally evaluate bit-1 after the freeze.
  For each of supplied Direct, Indirect and Covered, require ≥98%
  joint coverage, ≥1,000 jointly covered payments, ≥100 distinct
  senders and receivers and ≥100 scoped ordering banks, with zero
  errors by either rule on joint support. All three routes must pass.
- Report 99% ordering-bank percentile coverage sensitivity with
  1,000 resamples and seed 20261117. Bank clustering does not remove
  cross-bank dependence or account for fitting uncertainty. Zero
  observed errors are a practical finite-population decision.
- Mask small positive error counts. Export no country modes, bank
  names or row-level paths. Verify the executable and plan match
  the committed freeze before accessing bit-1.

## Exploration and exposure

Both maps are jointly evaluable on 744,893 July bit-0 rows (99.44%),
including 471,552 Direct, 241,284 Indirect and 32,057 Covered. The
two-bank map alone covers 746,499 of 749,066. No count errors or
prediction disagreements appear on the joint population. Varying the
training route mix therefore provides a falsification attempt on the
currency-mode map without using an FX-labeled training target.

Phase 0 and A03/A05/A11 exposed counts and class errors. A06/A08 exposed
currency-path associations and route strata. A14 and A16 exposed July
bit-1 currency-mode accuracy and support for maps fitted across routes.
A15 compared endpoint substitutions on bit-0. A20 changes training
strata and includes supplied Direct in evaluation. This test reuses
July, known account partitions, bank networks and corridors. Training
groups share dates and countries and are disjoint by record category.
The new fit contrast does not supply independent confirmation.

## Confirmation and robustness results

The unchanged test passed all routes at
`a045ce3340ccc00df5e8aee0918d719f1d0474a2`. The joint maps scored
695,472 of 699,603 July bit-1 payments, with zero errors for either
map. The joint counts were 439,703 of 442,037 Direct, 228,199 of
229,801 Indirect and 27,570 of 27,765 Covered. Both maps left 4,131
outside the joint comparison, and the two-bank map alone covered
696,744. The lowest route-specific 99% coverage sensitivity bound
was 98.88% for Covered. [Aggregate validation](../../analysis/10_amounts_currency/out/H-A20_route_mode_transfer_validate.md).

## Assessment

The count rule is stable across training route mixtures and supplied
score labels on covered paths. Latent route selection and the source of
denomination assignments remain open.
