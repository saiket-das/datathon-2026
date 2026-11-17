# H-A23 — Preferred USD mantissa-five point mass

Owner A. Ready for frozen reused-population internal validation.

## Proposed output constraint

There is a preferred exact amount anchor at5 ×10^k beyond a generic
one-significant-digit grid. In selected USD neighborhoods, the exact
mantissa5 point-mass/background odds exceed the corresponding pooled
mantissa4/6 odds by at least3, including the entire99% declared-bank
bootstrap interval. A matched mantissa7 versus6/8 comparison does not
show a similarly large preference.

This is an output-distribution constraint. A rounding operator favoring
particular values, direct selection of fixed standard values, and latent
amount mixtures are distinct possible mechanisms. The test cannot choose
between them. Simple density normalization assumes the smooth background
is informative about point intensity; highly localized unobserved density
or amount-dependent selection remains an alternative.

## Frozen population, executable and criteria

- Command: `uv run --locked python analysis/10_amounts_currency/H-A23_preferred_five_anchor.py`.
  Internal validation appends `--phase validate --freeze SHA`.
- Positive, unlabelled USD payments with timestamp July2023 UTC. Explore
  both-account bit-0 only. Freeze the complete code and this plan before
  scoring both-account bit-1; cross-bit records are excluded.
- Define observed magnitude m=floor(log10(amount)), mantissa=amount/10^m.
  Select m=3,4,5 and symmetric windows within .4 of integer mantissas
  d=4,5,6,7,8. Windows are disjoint. A point is within absolute USD1e-6
  of d×10^m; background is every other selected row in the same window.
  Report all selected/excluded counts. No daily scale is inferred for USD.
- Primary ratio: (point5/background5) divided by
  ((point4+point6)/(background4+background6)). Require lower99 bound>=3.
- Negative comparison: (point7/background7) divided by
  ((point6+point8)/(background6+background8)). Require its entire99%
  interval inside [.5,2]. This is a prespecified comparator, not proof
  that the full distribution is smooth.
- Also require primary point-estimate ratios>=3 separately for observed
  magnitude3 and pooled magnitudes4–5. Report their complete4/5/6 counts.
  The7/8 control is pooled only: the exploration's higher-magnitude
  digit8 point-sender cell is100, so finer cells are unsuitable for
  stable disclosure. No validation cell has been opened when choosing
  this pooling.
- Require at least15,000 selected payments and100 distinct senders,
  receivers and declared ordering banks. Every printed point/background
  count and corresponding distinct-sender/receiver count must be>=100.
  If that family fails support, do not export it and record an incomplete
  or unsupported result rather than weaken the support rule.
- Aggregate ten point/background counts per declared ordering bank.
  Resample whole banks1000 times, NumPy seed20261117; use .005/.995
  percentile intervals. All criteria required, no post-score tuning.
  This handles within-bank dependence only. Country/corridor factors,
  receivers and repeated data exposure are not made independent.
- Validate freeze ancestry and exact executable/shared-helper bytes
  before accessing the bit-1 population. Keep512MB, one thread, no spill;
  output only safe aggregate Markdown, no identifiers or row extracts.

## Exploration before freeze

A22 found a mantissa5 spike in boundary-aligned bins. The symmetric-window
design selects28,553 of129,847 July bit-0 USD payments;101,294 excluded,
8,127 senders,18,567 receivers and1,588 banks. Mantissa5 has2,910 points
and5,665 background rows; pooled4/6 has881 points and11,649 background.
Primary odds ratio6.792127,99% interval[6.098357,7.554614]. Negative
ratio .927355, interval[.744138,1.152449]. Primary ratios are6.778932
for magnitude3 and6.793723 for magnitudes4–5. All proposed criteria pass
on exploration before the freeze. The complete safe count tables are in
the matching exploration report.

## Exposure and limits

Phase0 full-data aggregates and Round1 amount/currency confirmation are
already exposed. A02/A10/A18 exposed rounding patterns; A22 identified
preferred mantissas using July bit-0. A19 exposed UTC daily alignment
and A09/A13 rate behavior. A21 exposed country-context prediction,
including reused July bit-1. A12 exposed standardized log-amount moments
and bins on those records. These USD bit-1 records cannot be relabelled
an independent holdout. A pass is supported internal replication under
a frozen test, not independent confirmation or recovery of the original
generator. No sponsor data or identifiers leave the local machine.

## Validation result

Pending at freeze. Preserve all failures, including A03 and A21.
