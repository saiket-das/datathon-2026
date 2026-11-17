# H-A24 — A shared EUR amount scale across sender party types

Owner A. Ready for internal re-extraction after freeze.

## Proposed relationship

A date-specific EUR scale measured independently on business-sender and
consumer-sender high-value amounts is shared by all four party pairs.
The distinct amount distributions in A01 can coexist with this shared scale.
Comparisons of high-value modes and low-value grids give separate observable
constraints. Denomination aliases or shared date metadata remain alternatives.

## Frozen method and criteria

Run `uv run --locked python analysis/10_amounts_currency/H-A24_party_scale_transfer.py`.
Append `--freeze SHA` for validation. Use positive, unlabelled payments in
both-account bit-0 for development and bit-1 for internal re-extraction.
Fit both modes anew within the selected account split, without carrying
a date-specific rate from bit-0 to bit-1.

For each currency, date and sender type B/C, group exact amounts in
[1,000,2,000,000). Require 20 payments at a mass point. Choose the point
with largest decimal base, then largest frequency, then smallest amount.
Divide by its decimal base. For each date shared by the two independently
fit sender groups compare the ratio of the fitted scales.

EUR is primary. Require ≥50 common dates, at least 99% of ratios within
absolute log distance .0001 of one, and ≥60% eligible coverage of all scoped
EUR small payments. Evaluate amounts in [10,900), disjoint from anchor
training. Each date must support both B/C fits. For every party pair BB,
BC, CB and CC require ≥1,000 eligible payments and ≥100 senders/receivers.
Compare whole-unit compatibility under the two rate estimates using
each rate's cent-propagation tolerance in A10. Require the upper 99%
date-block sensitivity bound on per-payment disagreement ≤.002 for each
of the four pairs.

Use 1,000 circular seven-observed-date blocks per pair, seed20261117,
.005/.995 percentile bounds. They condition on fitted rates and account
selection and leave related banks, counterparties and cross-date dependence
beyond the block open. All primary conditions must pass. CHF, GBP and USD
are descriptive checks. Never shift the primary currency after results.

## Exploration and exposure

EUR has 71 common dates. All fitted ratios are within .0001 in log units.
All four displayed party pairs have fit disagreement below .0002. Consumer
anchors are in smaller supported decades than many business anchors.
This motivated the primary scope. CHF has 26 common dates and GBP14,
too few for the same primary date criterion; USD51 and rates exactly
one serve as a descriptive constant-scale comparison.

Known exposure includes full-data Phase0 currency/party summaries and A01
scale contrasts, A02/A10/A19 rate-grid outcomes on both bit populations,
A12 log-shape outcomes, A13 reciprocal updates and A21's failed country
correction. A22/A23 exposed USD heaping. A24 newly compares separately
fit party-type scale estimates. Dates, banks, countries and earlier records
overlap across splits. It supplies no independent new rate innovations.

## Confirmation and robustness results

Frozen at `559bdce5a72fd02708fd4249c683df3fb956d086`, 17 November
2026 16:12:53 MYT. The unchanged internal test **failed**.
The EUR fits shared 73 dates, with 72 scale ratios near one (98.63%),
below the required 99%. The other ratio was .20000014, approximately
a factor-five alias. The data do not determine whether it represents
different native units, a selected denomination or another effect.

EUR small-amount coverage was 188,480 of 200,142 (94.17%). All four
party-pair display-support conditions passed. However upper 99%
date-block disagreement bounds were .004345 BB, .003770 BC, .004995
CB and .003881 CC, each exceeding the .002 criterion. Point estimates
were .001415, .001042, .001370 and .000983. Strong typical agreement
does not reverse any failed threshold. No day was removed or scale
adjusted after scoring.

[Full aggregate result](../../analysis/10_amounts_currency/out/H-A24_party_scale_transfer_validate.md).

## Assessment

The frozen stringent compatibility claim failed on a reused-account
sample. A possible factor-five denomination alias is a separate
exploratory lead. Original amount distribution, heaping probabilities,
party effects on denomination and stage ordering remain unresolved.
