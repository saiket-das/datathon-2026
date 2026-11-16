# H-A08: Payment currency is usually in the visible-path country-mode set

- **Owner:** A
- **Status at freeze:** confirmation-ready
- **Command:** `uv run python analysis/10_amounts_currency/H-A08_path_currency_set.py`
- **Internal validation:** add `--phase validate --freeze SHA`.

## Rule and scope

A currency-mode set inferred from the countries of all visible banks covers
payment currency more often than endpoint-only modes and non-geographic
comparators. This is a compatibility relationship on observed currencies.
The proposed rule leaves exceptions and cannot identify which bank or stage
selected denomination. Latent route selection and shared country metadata
are alternative explanations.

Use unlabelled both-account bit-0 records before July to learn the modal
currency per first visible country, with at least 100 training payments
per country. Tie-break by currency text. Apply that same country map to
each visible bank in a scored July path. Ignore placeholders for this
membership comparison. Every visible country must have a supported map.
Countries are never pooled with outside currency data.

## Frozen validation plan

- Fit only pre-July bit-0. Score July bit-1, unlabelled, all routes. Require
  at least 98% of all score rows eligible, with at least 100 senders,
  receivers and declared ordering-bank clusters in eligible scoring.
- Require entire 99% ordering-bank cluster sensitivity intervals at or above
  .98 for all-path membership, .50 for membership minus union-frequency
  baseline, .50 for membership minus shifted-map membership, and .02 for
  multibank membership minus endpoint membership. All must pass.
- Union-frequency baseline is the sum of pre-July global currency
  probabilities for the exact distinct currencies in the path's learned
  set. It controls the particular set's cardinality and marginal currency
  popularity under independent currency draws. It does not control
  corridor or bank composition.
- The shifted-country map circularly rotates the sorted supported countries
  by seven, preserving marginal modes across country categories. Score the
  same paths and rows. This preserves per-row country-path length and
  duplicate-country pattern, but distinct mapped-currency count and
  transaction-weighted mode frequencies can change. This is a fixed
  misspecification control, not a statistical randomisation test.
- Separately display membership and both baselines by distinct actual-set
  cardinality (1, 2, 3, 4+), route/visible length (2, 3, 4, 5+) and gaps.
  These are overlapping diagnostics. Keep every eligible row in the
  pooled decision. Display groups only with at least 1,000 payments and
  100 senders and receivers. Mask positive outside-set counts below 100.
- Resample whole declared ordering banks with replacement 1,000 times,
  NumPy seed 20261116, .005/.995 percentiles. This conditions on fitted
  maps. Training uncertainty, correlated country/bank effects and shared
  intermediate entities remain unaccounted for.
- Audit eligible declared ordering banks shared with the pre-July training set. Both-role account parity separates literal account strings. Intermediary bank/country overlap remains possible.
- Freeze the complete executable and helper versions before bit-1 set
  membership scoring. The code verifies ancestry and executable/helper
  equivalence. Retain failed criteria and do not refit or relax acceptance.

## Exploration evidence and controls

July bit-0 has 749,066 unlabelled payments. There are 747,835 eligible
(99.8357%), 90,726 senders and 277,364 receivers.
All-path membership is 98.6974%, first-only 93.3770%, and endpoints 97.1499%.
There are 9,741 unexplained currencies. The shifted map covers 22.4424%,
while the exact-set union-frequency baseline is 29.0105%.

With one/two/three/four-or-more distinct mapped currencies, observed
membership is 98.6735% / 98.5696% / 98.9237% / 99.2351%. The corresponding
union-frequency baselines are 23.0508% / 25.9738% / 35.8882% / 45.6213%.
The gain therefore persists within these displayed opportunity groups.
The country permutation covers 38.8043% / 19.2856% / 22.6656% / 25.4016%.

Direct paths have only endpoints and reach 98.5224% membership, leaving
6,992 outside the set. Multibank path membership reaches 98.8784–99.3900%
in displayed Indirect lengths, with endpoint-only coverage declining
to 91.6700% in 5+ visible-bank paths. Both positive fit and residual
exceptions remain in the report.

Adding cardinality into the original multi-group query exceeded512MB.
The same cardinality screen now runs separately under the original
512MB/one-thread/no-spill limit. This affected exploration only.

## Prior exposure

Phase 0 exposed full-data currency distributions and route semantics.
Round 1 A01/A02 exposed currency/value outcomes on both-account bit-1.
A03/A05 exposed unsigned/signed FX count results there. A06 already
evaluated first-path, last-path and declared-country currency prediction
for these July bit-1 records, with route/mismatch strata. A07 explored
receiving-country alternatives within bit-0 exceptions. The new all-path
set endpoint is chosen after those outcomes and never gets an independent
holdout label. Literal accounts split by both-role parity, but bank,
country, path and latent generator attributes can overlap. Internal
confirmation can support a further association, conditional on this
exposure.

## Validation and robustness results

Pending at freeze.

## Assessment

A pass supports bounded path-set compatibility on eligible reused records.
It does not prove original denomination choice, sampling probabilities,
causality or generator stage order. A03's failed exact criterion,
A05's upper-bound scope and A06's association limits remain.
