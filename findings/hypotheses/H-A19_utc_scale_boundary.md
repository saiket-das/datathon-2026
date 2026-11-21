# H-A19 — The effective UTC date of the EUR amount scale

- **Owner:** A
- **Status at freeze:** ready for reused-account internal evaluation
- **Command:** `uv run python analysis/10_amounts_currency/H-A19_utc_scale_boundary.py`
- **Validation:** append `--freeze SHA`

## Proposed mechanism and scope

The inferred EUR amount scale uses the same UTC date even near midnight.
A lagged or advanced daily assignment should fit better with an adjacent
calendar day's rate in at least one boundary window. This is a test of
observable alignment over two-hour windows.

## Frozen test

- Learn A10's highest supported exact modal amount divided by its decimal
  base from [10,000,2,000,000) unlabelled bit-0 rows. Each date/currency
  anchor requires ≥20 occurrences. Sort by descending base and count,
  then ascending amount. Reuse that map unchanged.
- Score [10,900) unlabelled same-currency payments. Require supported
  anchors on the preceding, current and following consecutive calendar
  dates. The code uses the prepared UTC timestamp. Use bit-0 in exploration
  and both-account bit-1 for the internal test.
- Primary tests are EUR 00:00–01:59 and 22:00–23:59 UTC separately. Compare
  same-day unit-grid compatibility against the union of hits under both
  neighboring dates. For each rate r and its own anchor base b use the
  symmetric cent-rounding tolerance .005+.005*a/r/b+1e-8 in dollars.
- Require EUR eligibility ≥95% overall and both windows to have ≥1,000
  payments on ≥50 dates, same-day fit ≥30%, and lower 99% paired lift
  ≥25 points. Use 1,000 circular seven-observed-date block resamples for
  each window, seed 20261117. They condition on the fitted rate and treat
  time block dependence descriptively. A failure rejects the compound rule.
- Keep other hours, CHF and GBP descriptive. Display comparisons only
  for cells with at least 1,000 payments and 100 senders and receivers.
  Suppress day-level rates and all identities. Verify frozen code and plan.

## Exploration and prior exposure

EUR has 197,714 eligible of 201,796 scoped bit-0 payments. Same-day fit is
41.28% on 5,707 early-window payments and 39.40% on 8,836 late-window
payments, each spanning 89 dates. Neighbor-day fits individually are at
most 1.04% in those windows. CHF boundary strata are below display
support. GBP is descriptive because of its smaller early sample.

A02/A10 used these currencies, dates and account sets in other rounding
tests. A13 showed daily bounds. Earlier comparisons used date-shifted
rates, with no frozen midnight window comparison. This experiment uses
a new contrast on reused date scales and scored populations. Shared bank,
country, account neighborhoods and date effects remain possible.

## Confirmation and robustness results

The unchanged bit-1 test passed both windows at
`5b6b952ed029696e0991df60d677998a64cc7c4c`.
From 200,142 scoped EUR payments, 195,974 were eligible (97.92%).
The early window had 5,151 payments and 40.09% same-day fit. Its
paired lift was 38.38 points, 99% date-block sensitivity 36.52–40.18.
The late window had 8,028 payments and 40.60% same-day fit. Its lift
was 38.48 points, interval 36.71–40.22. Both span 89 supported dates.
GBP early and both CHF boundary windows are below display support.
[Aggregate validation](../../analysis/10_amounts_currency/out/H-A19_utc_scale_boundary_validate.md).

## Assessment

The same-day rate best describes the grid near both sides of UTC midnight
in these windows. The result leaves the exact change instant, internal
clock and smaller intraday exception populations open.
