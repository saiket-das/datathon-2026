# H-A10 — High-value peaks predict low-value amount rounding

- **Owner:** A
- **Status at freeze:** ready for a reused-account internal test
- **Script:** `uv run python analysis/10_amounts_currency/H-A10_cross_denomination.py`
- **Evidence:** `analysis/10_amounts_currency/out/H-A10_cross_denomination_explore.md`

## Proposed rule and scope

For CHF and GBP on supported UTC dates, a scale inferred from frequent
amounts of USD 10,000 or more predicts a whole-unit grid among USD 10 to
under 900. The same-day scale should explain a substantially larger share
than scales from other dates. The amount ranges are disjoint. The rule tests
an observable implication of a shared day/currency conversion factor across
denominations. It leaves the scale's absolute units and the original code
unidentified. Treat unlabelled payments as a selection, with no legitimacy claim.

## Test plan

- Learn from unlabelled both-account bit-0 payments in [10,000, 2,000,000).
  Within currency/date and USD magnitude decade, group exact amounts. Keep
  peaks with at least 20 payments. Select the largest supported decade, then
  largest frequency, then smallest amount. Divide its amount by the
  corresponding power of 10 to obtain a scale. All dates may be used for fit.
- Evaluate unlabelled [10, 900) payments in each currency/date with both a
  fitted scale and a scale seven supported currency dates later. Use MD5
  both-account bit-0 for exploration and bit-1 for internal validation per
  `partition_sql('accounts')`. The shared split excludes cross-bit rows.
- Compare with that later scale and the currency's median fitted scale.
  For each candidate scale r and own-date decade base b, grid compatibility
  is `abs(a-r*round(a/r)) <= 0.005+0.005*a/r/b+1e-8`. The same tolerance
  policy applies to all controls. The shifted comparator need not have the
  same anchor decade; the own-date base controls tolerance on the same row.
- **Both CHF and GBP must pass**: at least 50% of scoped payments eligible,
  at least 1,000 eligible payments and 100 senders and receivers each, at
  least 30 eligible dates with 100 or more payments, at least 25% same-day
  fit, at least 20 percentage points of lift over each comparator and at
  least 80% of supported dates with a 10-point or greater same-day lift
  over the union of both comparator fits. If either currency fails, record
  the scope failure with unchanged thresholds. Smaller dates enter pooled
  results. Date weighting checks concentration; no iid interval or
  generalisation to future dates is assumed.
- EUR is a benchmark with outcome exposure in A02. USD is a date-invariant
  grid control. SGD is a scope check with visibly poorer anchor stability
  and coverage. Their flags are descriptive and do not enter the primary
  decision. No other currencies or alternate validation schemes are tested.
- Fit and scoring are rerun unchanged after freezing script, dependencies
  and this plan. Dates and entities such as banks are shared. Interpret
  large lift on matched days as supporting day/currency scaling, while
  allowing coordinated synthetic lookup tables or a different integer
  denomination as alternatives.

## Discovery and prior exposure

CHF fits 40.7997% of 38,015 eligible payments and GBP fits 40.4663% of
61,199. CHF later/constant fits are 0.9838%/0.7155%, GBP 1.0327%/1.3039%.
Coverage is 83.28% and 84.77%. Daily lifts over the union of both controls
meet 10 points on 65 of 65 and 65 of 66 supported dates. EUR separately
fits 40.46%. SGD coverage is 19.24% across 11 supported dates, below the
scope requirements. USD's three rates produce the same 40.44% fit.
The A09 weak co-movement screen informed the currency selection.

Known exposure includes Phase 0 full-data profiles and validation composition,
A01 account-controlled amount/party-type aggregates, A02 EUR and USD grid
and amount results on these bit-1 records, A03/A05 FX scores, A06/A08 July
currency/path outcomes and A04/A07/A09 exploration comparisons. A11 also
screens bit-0 FX outcomes. No CHF or GBP results for this new low-value
grid endpoint on bit-1 were examined before freeze. This test reuses known
records, dates and bank geography. Literal accounts remain separated in
both roles. It tests transfer across account sets and amount ranges.

## Confirmation and robustness results

Frozen at `f31764d04d8d4280281ace5f0e8c0dbc8cb1dff5` on 16 November 2026
at 21:36:36 MYT. Run the script with `--phase validate --freeze` and that SHA.
Both primary currencies passed every threshold. The [aggregate report](../../analysis/10_amounts_currency/out/H-A10_cross_denomination_validate.md)
retains the full control and coverage results.

| Currency | Eligible | Coverage | Same day | Later date | Constant | Dates with 10-point lift |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CHF | 33,405 | 83.74% | 41.11% | 0.88% | 0.66% | 65 of 65 |
| GBP | 41,019 | 85.08% | 40.36% | 0.97% | 1.26% | 65 of 66 |

The corresponding off-grid majorities are 58.89% and 59.64%. SGD again
failed the coverage and supported-date requirements (19.03%, 11 dates).
USD's three fits were identical at 40.41%. EUR fit 40.35% and remains
a benchmark with prior outcome exposure.

## Assessment

A date-specific scale transfers from large amounts to small amounts for
CHF and GBP on the reused-account internal test. Shared dates and bank
geography limit transfer claims. An observed fit share cannot identify
the exact component weight because accidental matches and missed grid
members are possible.
