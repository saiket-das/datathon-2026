# H-A21 — First-path country context in log payment amounts

- **Owner:** A
- **Status at freeze:** ready for reused-population internal validation
- **Reproduce:** `uv run python analysis/10_amounts_currency/H-A21_country_amount_context.py`
- **Validation:** append `--phase validate --freeze SHA`.

## Proposed relationship

Adding an origin-country residual correction to a currency/party log-amount
mean improves prediction across months and separated account strings. The
country is taken from the first visible path bank. This is a statistical
conditional mean relationship. Country, bank selection, customer composition
and latent geography may all contribute. It identifies no wealth measure
or original generating order.

## Frozen method and criteria

- Train on positive, unlabelled both-account bit-0 payments before July.
  Fit a mean natural-log USD amount per currency and ordering/beneficiary
  party-type pair, requiring at least 1,000 training rows per group.
- Compute training residuals from that baseline. Fit their mean by
  first visible bank-country, requiring 100 training rows per country.
  Fit the same correction separately by last visible country as a
  comparator. Retain July score rows covered by both country maps and
  the currency/party baseline for identical-row comparisons.
- The primary internal validation population is positive, unlabelled July
  both-account bit-1. Cross-bit payments are excluded. No score-side
  location, scale, threshold or coefficient is estimated.
- Require at least 90% eligible coverage of scoped rows, 100 eligible
  senders and receivers, and 100 declared ordering-bank clusters.
  The entire 99% bank-cluster interval for row-weighted corrected/base MSE
  must lie at or below .98, corrected/receiver-corrected MSE at or below
  .99, and equal-sender corrected/base MSE at or below .98.
  All criteria are required. Preserve any failed threshold.
- Equal-sender MSE is the mean of each sending account's mean squared
  error, giving each sender equal weight. Declared sender bank is stable
  under the shared foundation. Resample whole declared ordering banks
  1,000 times, NumPy seed20261117, .005/.995 percentiles. Shared country,
  bank/corridor factors, receivers and training estimates are not made
  independent by this interval.
- A negative correction circularly rotates the source-country fitted
  effects seven positions among lexically sorted countries. This
  preserves category-level effect values while changing assignments.
  Its transaction-weighted frequency may change. Record its MSE on the
  same rows without using it to alter primary criteria.
- Report a naive sum of source and receiver corrections and same-party
  descriptive strata. These comparisons address whether simply adding
  more country corrections helps. Strata require 1,000 rows and 100
  distinct senders and receivers. Record declared-bank training overlap.
- Commit this plan and complete executable before bit-1 scoring. Verify
  executable/helper equality and freeze ancestry. Do not update
  criteria or fit to validation outcomes after the freeze.

## Exploration

The pre-July bit-0 fit has 144 currency/party means, 126 source-country
corrections and 185 receiver-country corrections. July bit-0 has 749,066
scoped and 705,162 jointly covered rows, 76,955 senders, 263,424 receivers
and 5,301 declared ordering banks. The training set shares 5,196 of those
banks.

Baseline row MSE is4.624390. Corrected/base ratios are .960970 for source,
.994971 for receiver and .965367 for their naive sum. The sender-balanced
source ratio is .966796, whereas receiver is1.001085. The rotated source
correction gives1.112163 under equal-sender weighting. Thus receiver
correction and naive addition do not explain the source correction's
comparative gain.

Exploration upper99 bounds are .979515 for row model/base, .980652 for
row model/receiver, and .978160 for equal-sender model/base. The original
exploration criteria pass before validation. Party-pair additive ratios
range .962674 to .972612. The simpler source correction remains the
selected model.

## Prior exposure

Phase0 exposed full-data amount, party and currency summaries. A01
evaluated business-type scale differences on both-account confirmation.
A12 standardized log amounts by currency/party and exposed July bit-1
moments and bins. A02/A10 exposed rounding/scaling on some of the same
records. A03-A20 added FX, country-mode and currency outcomes and
supported the first-path location choice. The new country-residual MSE
was only examined on bit-0 before freeze. These are reused records with
shared banks/countries, so an internal pass cannot supply an independent
holdout claim.

## Validation and robustness results

Freeze: `b82670542b97fa295cf719d7cd48a978af035f55`.
Exact command:
`uv run --locked python analysis/10_amounts_currency/H-A21_country_amount_context.py --phase validate --freeze b82670542b97fa295cf719d7cd48a978af035f55`.

The frozen all-criteria claim **failed**. Of 699,603 scoped July bit-1
payments, 656,546 were jointly covered (93.8455%), from 75,374 senders,
255,885 receivers and 5,228 declared ordering banks. Of those banks,
4,045 also occur in training. Baseline MSE is4.575395. Source/base MSE
ratio is .975232, a descriptive 2.4768% reduction, but its99% bank-cluster
interval is [.965461,.984483]. The required upper bound was .98.

The source/receiver ratio interval [.965073,.984096] meets its .99
ceiling. Equal-sender source/base ratio .969730 has interval
[.958215,.979533], meeting .98. All support requirements pass. The
receiver correction alone has ratio1.000448 and shifted-country control
1.315288; the naive source-plus-receiver correction .976804 remains worse
than source alone. These descriptive controls do not reverse the failed
primary threshold. No criterion or model was adjusted after scoring.

[Complete aggregate result](../../analysis/10_amounts_currency/out/H-A21_country_amount_context_validate.md).
The executable verifies its own and shared-helper content against the
freeze before reading the scoring population. Before freeze,
`uv run --locked pytest` passed68 tests and `git diff --check` passed.

## Assessment

A pass supports the specified conditional mean predictor on covered reused
records. It does not establish a country effect under intervention or
identify the generator's economic inputs. Preserve earlier failed tests,
including A03, under their original identities.
