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
