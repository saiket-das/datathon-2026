# H-A09 — Co-movement of inferred daily modal amount scales

- **Owner:** A
- **Status:** exploratory, weak common-movement candidate
- **Command:** `uv run python analysis/10_amounts_currency/H-A09_modal_scale_coherence.py`

## Proposed rule and scope

A dominant common daily factor would produce substantial positive
co-movement across currencies with stable repeated amount peaks.
The existing bit-0 screen compares day-to-day log changes in peaks
after dividing by their decimal magnitude. It requires 20 payments
for a peak and selects the highest supported decade per currency/date.
The measure is compatible with denomination effects as well as rate changes.

## Discovery evidence

Among three finite correlations with at least 60 shared adjacent days
and both changes within 10%, the median is 0.0749 and the range is
0.0690–0.0836. USD's chosen scale is constant. SGD has six changes
outside the stability filter among 45 adjacent dates. The
[exploration report](../../analysis/10_amounts_currency/out/H-A09_modal_scale_coherence_explore.md)
keeps date and payment support alongside dispersion.

## Validation and assessment

No frozen confirmation or formal covariance test was pursued. The small
positive correlations give little basis for a dominant common-factor model.
The date-overlap filter, changing denominations and small number of currency
pairs limit interpretation. CHF and GBP stability motivated the separate
H-A10 cross-denomination test. The exploratory files already existed locally
at the start of this continuation. Phase 0, Round 1 and A03–A08 exposure
applies. The screen and its rerun use unlabelled both-account bit-0 only.
