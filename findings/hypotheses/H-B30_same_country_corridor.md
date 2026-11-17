# H-B30 Origin-matched bank-country association with Covered states

- **Status:** confirmation-ready
- **Explore:** `uv run python analysis/20_routing_time/H-B30_same_country_corridor.py --phase explore`.
- **Internal test:** replace phase with `--phase confirm --freeze <SHA>`.

## Candidate

Among corridors from the same origin, the Covered label is more frequent
when the two visible endpoint banks have the same two-character country
field. This could reflect a country relationship entering state selection.
Correlated counterparty selection, unobserved bank attributes or country
composition can also generate it. Bank country does not establish customer
residence, physical distance or local payment status.

## Frozen population and estimator

Reuse B20's loader only. Unlabelled v3–5 Covered/Indirect, both declared
endpoint-bank MD5 bits zero, visible first/last bank after removing
placeholders. Group each month's directed pairs once and retain pure
labels. Target periods are June for discovery and July for internal
validation. Each directed corridor has equal weight within its group.
Unlike B20 prediction, known target corridors may recur from May.

Require receiver banks to have at least 25 pure May corridors as receivers.
Estimate their May Covered share smoothed toward the May global share
using ten global pseudo-corridors. For every target origin, compare mean
class on same-country versus different-country corridors. Require at
least five corridors in each group. Each origin then contributes one
unweighted contrast. Repeat on residual class minus May receiver probability
to probe receiver-composition differences. The source geography is fixed
within origin, while receiver identities and currencies can differ.

As a negative control, repeat the group construction using
`substr(md5(origin),1,1)<substr(md5(receiver),1,1)` with the same group
support rule. This deterministic hash-order split has no proposed geographic
meaning, but finite-bank chance associations remain possible.

## Acceptance, uncertainty and controls

Require at least 100 matched origins. For raw and receiver-adjusted
contrasts, resample complete origin pairs of contrasts 1,000 times with
NumPy seed20261117. Both central 99% intervals must lie above +.02.
Require at least 100 placebo-supported origins and absolute mean placebo
effect at most .02. Every gate must pass. No threshold changes after July.
Report full receiver-supported and retained matched populations, source
and receiver counts, payments, and same-country counts.

The origin resampling retains shared receivers, countries, corridors and
potentially accounts and dates. It is a conditional sensitivity interval.
The adjustment fixes May estimates and cannot remove all receiver/currency
or latent-state confounding. This measures an association at selected
origins, without a causal intervention or new-bank generalization.

## Discovery and prior exposure

June has 76,831 receiver-supported corridors, 276,082 payments, 3,925
origins and 784 receivers. The matched contrasts retain 201 origins.
Raw contrast is +.042490, 99% interval [.029064,.057195]. Adjusted
contrast is +.041821, interval [.028602,.056466]. Placebo is −.002440
across 528 supported origins. The final report includes matched population
coverage. Source country agreement occurs on bank fields, not necessarily
on the declared fields because endpoints can disagree.

Phase 0 and B01–B29 were exposed before this plan. July reused outcomes
include route class, origin propensity and durations from previous work.
The exact origin-matched July country contrast, adjustment and placebo
remain unopened before freeze. Thus this is internal validation on reused
records, not independent confirmation. The June outcomes guided the
criteria. No outside geography data is incorporated.
