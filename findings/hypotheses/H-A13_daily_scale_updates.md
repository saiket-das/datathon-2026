# H-A13 — Bounded daily updates of reciprocal amount scales

- **Owner:** A
- **Status at freeze:** ready for internal re-extraction
- **Command:** `uv run python analysis/10_amounts_currency/H-A13_daily_scale_updates.py`

## Proposed mechanism

For CHF, EUR and GBP, the reciprocal of the amount-implied USD scale changes
by roughly a bounded multiplicative step per UTC day. A uniform relative
update over ±1.5% is a candidate approximation. Test it against a zero-centred
Gaussian with matching variance. A09's weak cross-currency co-movement remains
consistent with several processes, including currency-specific updates.

## Frozen test plan

- Use unlabelled both-account bit-0 for discovery and bit-1 for internal
  re-extraction, over the full available date span. Restrict payment amounts
  to [100, 2,000,000) and currencies to CHF, EUR, GBP and USD. Report scoped
  payments and the dates excluded for lack of supported anchors.
- For each currency/date/observed USD magnitude decade select its modal
  exact amount, ties ascending. Require at least 20 matching payments.
  Select the largest supported decade and divide its mode by the decade
  base to estimate scale. No learned date rate is shared across splits.
- Compare consecutive observed UTC dates only when their difference is
  exactly one day. Primary change is previous scale/current scale minus
  one. Direct-scale change and USD's constant scale are controls.
- Require ≥40 transitions for each primary currency and USD, zero primary
  inverse increments beyond absolute .01501, zero USD variation, pooled
  inverse uniform KS ≤.12 and Gaussian KS exceeding uniform KS by ≥.015.
  Any failure rejects the compound claim. The .00001 margin allows for
  observed anchor-cent precision. Report exceptions without trimming.
- Report 99% percentile sensitivity using 1,000 circular seven-observed-date
  blocks drawn jointly across currencies with seed 20261117. The interval
  diagnostics do not determine the practical decision. They condition on
  selected anchors and serve as sensitivity checks for time dependence,
  rather than iid KS inference. Missing dates, selected anchors and shared
  latent dates can affect both shape and support.
- Freeze prior to bit-1 scoring and run with `--phase validate --freeze SHA`.
  Report unchanged thresholds and eligibility. The test assesses stability
  of measured updates across transaction sets on overlapping calendar dates.

## Discovery and prior exposure

Bit-0 provides 60 CHF, 90 EUR and 69 GBP adjacent-day updates. Three direct
changes exceed the candidate bound. The reciprocal scale has none. Pooled
inverse KS distances are .076878 for uniform and .109225 for Gaussian.
The magnitude and orientation were selected after looking at bit-0 increments.
The selected rates are amount-implied and could reflect a table lookup,
different anchor denominations or a different bounded distribution.

Phase 0 and A01 exposed calendar and amount summaries. A02 and A10 exposed
currency roundness and shared date scales on these same bit-1 records.
A03–A08 and A11 exposed route and currency relations, and A12 exposed July
conditional log-amount shape. A09 exposed bit-0 scale stability and
co-movement. Dates, bank/corridor and path entities can overlap across
account sets. A14 uses only bit-0. No independent rate innovation sample
or fresh time period follows from this design.

## Confirmation and robustness results

Pending at freeze.

## Assessment

A pass would support a bounded reciprocal-scale approximation on supported
dates and currencies. It would leave independence, exact innovation
distribution and source-code identification open.
