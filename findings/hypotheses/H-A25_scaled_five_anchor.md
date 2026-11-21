# H-A25 — Preferred mantissa five after daily currency scaling

Owner A. Ready for a reused-account internal test.

## Proposed output constraint

The preference for nominal 5×10^k values observed in USD also appears after
converting CHF, EUR and GBP amounts by an amount-implied daily scale.
This is compatible with a common preferred-denomination component before
currency transformation. Directly selected USD values and other latent
lookup systems remain possible explanations.

## Frozen method and criteria

Run `uv run --locked python analysis/10_amounts_currency/H-A25_scaled_five_anchor.py`.
For internal validation append `--freeze SHA`. Fit daily scales solely
on positive unlabelled bit-0 payments, separately per currency, using
A10's highest supported exact-amount mode in [10,000,2,000,000). Require
≥20 occurrences, order by descending decimal base and frequency, then
ascending amount, and divide by decimal base.

Develop on unlabelled bit-0 payments, evaluate on bit-1 after freeze,
all available dates. Convert amounts under USD9,000 using the fixed
bit-0 rate. Select native observed magnitude two or three and disjoint
symmetric mantissa windows ±.4 around 4,5,6,7,8. Include a date/magnitude
only if its entire largest window endpoint 8.4×place×rate is under
USD9,000. This prevents clipping the highest comparator window and
keeps fitting and evaluation amount ranges disjoint.

Define point compatibility using absolute dollar difference ≤
.005+.005×target_native_amount/anchor_base+1e-8. Other payments in the
window form the local background. This propagates output and fitted-anchor
cent rounding, conditional on the selected anchor denomination. Take
point/background odds at5 relative to pooled4/6. For control take7
relative to pooled6/8.

CHF, EUR and GBP are co-primary. Every primary currency must have ≥50
selected dates, ≥100 ordering banks and ≥100 payments, senders and
receivers in every printed point and background cell. Suppress a whole
currency family if its five cells lack this support and classify it
unsupported. Require lower99 primary odds ≥3 and entire99 control odds
inside [.5,2], for all three primary currencies. USD is descriptive.
All primary criteria required.

Use 1,000 whole declared ordering-bank resamples, RNG20261117, sequential
currency order CHF/EUR/GBP/USD, .005/.995 percentile intervals. They
condition on fixed fitted rates and handle only within-bank dependence.
The nominal 99% intervals are per currency and contrast. Connected banks,
dates, shared country effects, training and denominational ambiguity remain.
Freeze executable, this plan and helpers before designated outcomes.

## Exploration and exposure

The initial screen considered only4/5/6, then added7/8 and a clipping
exclusion before freezing. Point/background odds for preferred5 after
the complete-window control are 6.8866 CHF, 6.9720 EUR and 6.9247 GBP.
Their lower99 bounds are 6.1304,6.5633,6.2208 and the respective seven
controls' entire intervals lie inside [.5,2]. No designated bit-1
scaled-five outcome informed this selection.

A01/A12/A21 exposed log-amount summaries and models on reused accounts.
A02/A10/A13/A19 exposed daily grids, scale changes and UTC alignment.
A18/A22/A23 exposed USD rounding and preferred-five point masses, with
A23 already tested on July bit-1. A24's failed re-extraction selected the
factor-five ambiguity as a plausible mechanism question. A25 uses bit-0
rates across known dates. The new CHF/EUR/GBP output constraint is an
internal same-dataset test with shared dates, network entities and prior
payment records. It supplies no independent rate or economic sample.

## Confirmation and robustness results

Freeze `ee8a5c55b97d31404ff3a28d444a4eca9c36abcf`, 17 November 2026
16:18:22 MYT. The unchanged internal test passed all three primary
currencies. Selected sample counts were 14,466 CHF, 68,535 EUR and
15,650 GBP payments, with 72,91,73 dates. The corresponding under-9,000
scoped counts were 108,456,488,287,111,916. Windows, date support and
denomination restrictions account for the exclusions.

| Currency | Five ratio | Nominal 99% bank interval | Seven control | Control interval |
| --- | ---: | ---: | ---: | ---: |
| CHF | 6.4404 | 5.7384–7.3664 | 1.0341 | .8399–1.2436 |
| EUR | 6.9461 | 6.5260–7.4179 | .9607 | .8671–1.0770 |
| GBP | 7.0102 | 6.0396–7.9446 | .9025 | .6997–1.1264 |

The USD descriptive ratio was 7.3193. Complete support checks passed,
including point/background entity counts at all five anchors.
[Aggregate results](../../analysis/10_amounts_currency/out/H-A25_scaled_five_anchor_validate.md).

## Assessment

Preferred denomination structure transfers to the three scaled currencies
on reused account records and supported dates. Mixture weight, exact
quantization operator, causal order and unique native units remain
unresolved. A24's failed scale-re-extraction criteria retain their scope.
