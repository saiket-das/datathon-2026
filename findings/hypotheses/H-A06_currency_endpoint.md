# H-A06: Currency code associates with the first visible path-bank country

- **Owner:** A
- **Status at freeze:** confirmation-ready
- **Command:** `uv run python analysis/10_amounts_currency/H-A06_currency_endpoint.py`
- **Internal validation:** add `--phase validate --freeze SHA`.

## Rule and scope

A modal payment-currency code learned separately for each first visible
path-bank country predicts July currency codes more accurately than analogous
declared-sender and path-receiver country maps. This is a conditional categorical
association. Bank and corridor selection or latent metadata may explain it.
The USD-normalised amount does not reveal a payment's original denomination.
The prediction does not establish which feature was generated first.

Train on unlabelled both-account bit-0 payments before July. Each predictor
uses its own country-specific currency mode with at least 100 training rows,
tie-broken by currency text. Unsupported categories fall back to the same
global training currency mode. Every July score row enters every predictor,
including fallback cases. No test outcomes fit the modes.

## Frozen test plan

- Primary score population is all unlabelled July payments in both-account
  bit-1. All analytical columns remain available, but no amount is needed for
  this claim. Cross-bit and labelled rows are excluded.
- Require at least 100 scoring senders, receivers and declared ordering
  banks. Entire 99% ordering-bank cluster sensitivity intervals must be
  at least .90 for first-path-country accuracy, .02 for paired accuracy
  lift over declared sender country, and .50 for paired lift over path
  receiver country. All criteria must pass. Fail the whole practical claim
  if any criterion fails.
- Uncertainty uses 1,000 whole declared-ordering-bank resamples with
  replacement, NumPy seed 20261116, .005/.995 percentile intervals.
  Training-estimate uncertainty and dependence across shared entities
  remain unaccounted for. These are conditional cluster sensitivity
  intervals.
- Global mode, declared receiver and path receiver are comparisons on the
  same rows. Route and endpoint-country-agreement tables are descriptive
  controls. All strata require at least 1,000 payments and 100 each
  senders/receivers. Pooled tests retain every score row.
- Audit same-role sender, receiver and ordering-bank overlap with training.
  Account strings separate by the bit predicate in primary validation.
  Cross-role/path-bank overlap can remain and is not eliminated by this
  design. A future audit or sensitivity is labelled separately.
- Freeze the executable and shared helper before validation. Code checks
  ancestor identity and byte-equivalent executable/helper content. Do not
  change criteria after observing outcomes.

## Discovery evidence

In July bit-0 development, 749,066 unlabelled rows across 91,004 senders and
277,916 receivers yield first-path-country accuracy 93.321%, declared-sender
89.307%, path-receiver 30.727% and global 30.465%.

Where only the sending endpoint country disagrees (34,100 rows), first-path
accuracy is 93.364% versus declared-sender 9.252%. When both countries disagree,
1,641 rows give 93.723% versus 9.202%. Direct/Indirect/Covered first-path
accuracy is 94.664% / 90.887% / 91.913%. This heterogeneity is retained.

An exploratory combined overlap query exceeded the 512MB cap. The same
counts are now computed sequentially, retaining the population and one-thread
memory limit. No validation data was accessed by this development change.

The bank-cluster development intervals are [.929985,.936233] for first-path
accuracy, [.039279,.041114] for lift over declared sender, and
[.583506,.669211] for lift over path receiver. There are 5,748 declared
ordering banks. Earlier months share 71,655 senders, 102,533 receivers and
5,600 ordering banks with development scoring.

## Exposure and inference boundaries

Phase 0 exposed full-data currency and structural aggregates. Round 1 A01/A02
used both-account bit-1 records and exposed currency/amount/party summaries.
A03 exposed FX predictions and A05 directional counts on bit-1. The current
Julys and literal entities therefore have prior exposure. The saved A06
development script/report uses bit-0 only. No fresh independent holdout
exists here; any passed frozen test supports internal transfer only.

The first path bank and declared sender bank usually agree, making much
pooled accuracy shared. The mismatch strata demonstrate sensitivity to
which field is used, but mismatches can be selected by latent corridor or
bank attributes. The modes partly encode geography and currency prevalence.
No causal direction or universal country-currency rule is identified.

## Validation and robustness results

Pending at freeze.

## Assessment

Use the exact conditional predictive scope and disclose all prior exposure.
Keep the earlier A03 failed near-exact threshold and A05 upper-bound claim intact.
