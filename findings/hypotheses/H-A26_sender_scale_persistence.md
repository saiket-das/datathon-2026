# H-A26 — Persistent sender amount scale versus shared bank context

Owner A. Exploratory only. Own-history advantage over matched peers was
not demonstrated, and the candidate was not taken to internal validation.

## Proposed mechanism and design

A persistent sender-specific amount parameter would create month-to-month
dependence in residual log amounts beyond shared currency, party and bank
context. A competing explanation is a common contextual scale plus
payment-level variation.

Run `uv run --locked python analysis/10_amounts_currency/H-A26_sender_scale_persistence.py`.
Query positive unlabelled both-account bit-0 only. Fit currency/party-pair
mean log amounts in May with at least 1,000 rows. Require ≥10 May and ≥10
June payments per sender/currency/party cell. Retain cells with at least
one other sender with the same declared ordering bank, currency and party
pair. Rotate May means one place in sorted sender order to obtain a
different peer per cell. No sender or bank identity is exported.

Compare prediction of the June cell mean using zero residual, own May mean,
and the rotated peer's May mean. Average squared errors within each sender
first. Compute correlations between each sender's equally averaged month
means. Use 1,000 ordering-bank resamples, seed20261117, nominal99% ratios.
The exploratory screen required ≥1,000 senders,100 banks, correlation≥.5
and both upper99 own/base and own/peer MSE ratios≤.80. This screen was
not frozen for confirmation.

As an additional exploration, center both month means on the equal-cell
mean for their bank/currency/party group separately within each month,
then repeat the equal-sender correlation and squared-error comparisons.
This uses June outcomes for descriptive centering. It is not a fitted
future prediction or an out-of-sample null test.

## Evidence and competing explanations

June has 1,043,095 scoped payments and 929,549 baseline-covered.
The history-support floor gives 10,890 cells; the peer requirement retains
8,545 cells across 6,163 senders and 958 banks, with 476,291 June payments
(45.66% of scoped). Excluded users and low-count cells remain outside scope.

The raw May/June correlation is .6372. Own history's squared-error ratio
to zero residual is .8400, nominal99% bank sensitivity [.7781,.9030].
Its ratio to the matched peer is1.0370 [.9860,1.0880]. The proposed
own-history advantage fails the exploratory screen.

After group centering the correlation is .0190. Own-history error is
2.1906 times the centred zero-residual baseline and1.0342 times the
centred peer error. The descriptive dependence is consistent with shared
context driving much of the pooled persistence. The design cannot
distinguish bank metadata, country context, sender selection or other
group-level mechanisms, nor exclude smaller sender-specific effects.
No threshold or significance claim follows from the centred correlation.

## Exposure and limitations

Phase0 reported full-data account and amount structure. A01 tested party
scale on known account partitions. A12/A21 exposed currency/party and
country residual outcomes, including July bit-1. A02/A10/A13/A19 and
A24/A25 exposed rate and denomination context. A26 queries only previously
explored bit-0 May/June. Repeated customers, receivers, banks, corridors
and selected matched histories remain dependent. No July query was made
for this new outcome, and no independent confirmation is claimed.

[Aggregate evidence](../../analysis/10_amounts_currency/out/H-A26_sender_scale_persistence_explore.md).
