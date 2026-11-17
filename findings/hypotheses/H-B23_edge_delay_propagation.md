# H-B23 Adjacent Direct directional delays transfer to three-bank paths

- **Status:** confirmation-ready
- **Command:** `uv run python analysis/20_routing_time/H-B23_edge_delay_propagation.py --phase explore`
- **Internal test:** replace the phase with `--phase confirm --freeze SHA`.

## Candidate and frozen evaluation

Use a pair-specific symmetric baseline, then test where to add the
directional duration component inferred from separate Direct payments.
If added delays are predominantly inherited from adjacent directed
pairs, the observed path duration should be much closer to the
adjacent-only model than to an outer-endpoint surcharge. This separates
two contexts that can share a Covered label association in B19.

- Population is UTC May–July 2023, unlabelled v2/3 with both declared
  endpoint-bank MD5 parity bits zero. Strip placeholders to identify
  visible banks. Learn May Direct medians using at least five payments
  per direction. For each unordered pair, use the shorter median as
  its baseline. For each ordered pair, subtract that baseline from its
  own median to obtain a nonnegative directional excess. Keep pairs
  whose shorter median is below 100 seconds.
- Use only three-bank paths with all three visible identities distinct
  and all three short-baseline pairs (both adjacent and outer) fitted.
  The shared path baseline is the sum of the two adjacent shorter
  medians. Estimate one additive offset in June as the median
  observed-minus-baseline residual among paths for which both the sum
  of adjacent excesses and the outer excess are at most 20 seconds.
- Freeze this baseline recipe and apply it in July. Primary comparison
  is among matched paths with a sum of adjacent excesses over 20 seconds,
  an outer excess over 20 seconds, or both. Compare four same-row
  predictions using the common June shift. Add no excess, add both
  adjacent excesses, add the outer excess only, or add all three.
- Joint acceptance requires at least 1% of scoped July v3 payments
  matched, at least 1,000 matched and 500 marked payments, and 100
  distinct banks in each of the three roles among marked paths.
  Adjacent-only mean absolute error must be at most 16 seconds.
  The lower end of the 99% paired relative MAE reduction must be at
  least .50 against each of the other three models under each of
  three separate bank-role resamples. Use 1,000 draws with seed20261116.
  All gates apply. Any failed threshold remains failed. Report pooled
  and supported strata descriptively, without letting them rescue a
  failed primary criterion.
- Dependence can persist across bank roles, repeated outer corridors,
  accounts and reused Direct medians. The intervals are conditional
  sensitivity checks. The model compares excess placement relative to
  a selected baseline. It does not identify physical processing times.

## Exploration and exposure

June matches 4,326 of 211,787 paths (2.04%) across 164 origins, 152
receivers, 132 interior banks and 2,306 outer corridors. The June
shift is −13 seconds. The overall adjacent-only MAE is 7.83 seconds,
versus 88.35 for zero excess, 106.16 for outer-only and 54.43 for both.
Among 863 adjacent-marked/outer-unmarked paths the median observed
excess is 297 seconds, while the mean fitted adjacent and outer
excesses are 307.33 and 1.32 seconds. The marked population and all
three role-specific resampling checks are in the aggregate report.

Phase 0 and B01–B19 outcomes were exposed, including B15 known-edge
sum compared with a maximum and endpoint model. B20 used June Covered
propensities. B21 and B22 explored exact reverse-path and slow-pair
support. The new July same-row directional excess comparison remains
unopened before freeze. Its July payment rows, corridors, banks and
possibly accounts overlap prior research. It is internal validation.
The narrow scope and five-witness selection can miss other timing
regimes, interior arrangements or outer effects.

## Frozen internal result

The unchanged July test passed at freeze
`af07496a8a81d970bbb30531c1a4f484ec03fa55` (17 November 2026,
10:44:59 MYT). The locked −13 second shift applies to 3,111 of
151,146 scoped paths (2.06%). The primary subset has 1,099 marked
paths, 733 outer corridors, 114 origins, 130 receivers, and 109
interior banks.

| Added excess | Mean absolute error in seconds |
| --- | ---: |
| Adjacent only | 7.263 |
| No directional excess | 244.262 |
| Outer only | 289.970 |
| Adjacent plus outer | 132.056 |

Adjacent-only is within 20 seconds on 95.81%. The smallest lower 99%
relative MAE reductions across the three bank-role sensitivities
are 95.81% against no excess, 96.65% against outer only, and 91.21%
against adding both. Of 645 supported adjacent-marked paths with
unmarked outer pairs, the median observed excess is 310 seconds.
The fitted adjacent mean is 311.17 seconds and the outer mean is
1.16. Cells with marked outer pairs lack separate role support, so
their route-specific timing remains unresolved.

Adjacent ordered pairs carry the transferable duration component on
this selected population. B19's association between the outer Covered
label and Direct direction can coexist with that rule. The July
results do not recover the exact mechanism for choosing direction
states or extrapolate to unsupported edges or longer visible paths.
These specific July outcomes are now exposed.
[Aggregate report](../../analysis/20_routing_time/out/H-B23_edge_delay_propagation_confirm.md).
