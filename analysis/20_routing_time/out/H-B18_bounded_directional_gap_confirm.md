# H-B18_bounded_directional_gap: confirm

Freeze: 1979ad17f1431755e99d54a4579ade48eb35c71d.
DuckDB 2.0.0; 768MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% canonical first-visible-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Cohort coverage

| all_direct | supported_pairs | supported_payments | short_pairs | eligible_pairs | eligible_pair_share |
| --- | --- | --- | --- | --- | --- |
| 411335 | 973 | 50641 | 942 | 289 | 0.297020 |

## Fixed comparison with first-bank resampling

| n | banks | uniform_TV | uniform_TV_upper99 | triangular_TV | TV_gain_lower99 | TV_gain_upper99 | share_above620_upper99 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 289 | 127 | 0.036630 | 0.116289 | 0.257841 | 0.111180 | 0.242568 | 0.000000 |

## Gap histogram

| interval_seconds | count | observed | uniform | triangular |
| --- | --- | --- | --- | --- |
| (20,120] | <100 | suppressed | 0.172414 | 0.315101 |
| (120,240] | <100 | suppressed | 0.206897 | 0.299643 |
| (240,360] | <100 | suppressed | 0.206897 | 0.214031 |
| (360,480] | <100 | suppressed | 0.206897 | 0.128419 |
| (480,600] | <100 | suppressed | 0.206897 | 0.042806 |
| >600 | 0 | 0.000000 | 0.000000 | 0.000000 |

## Endpoint and split-period controls

| group | eligible_pairs | payments | canonical_first_banks | gap_p10_p50_p90_p99 | above620_share | split_reference_pairs | absolute_drift_p50_p90_p99 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Primary | 289 | 18169 | 127 | [75.8, 318.0, 533.0, 592.9200000000001] | 0.000000 | 209 | [3.0, 7.5, 11.459999999999994] |
| Declared endpoints agree | 280 | 17094 | 124 | [76.9, 316.75, 527.0999999999999, 591.3149999999999] | 0.000000 | 198 | [3.0, 7.5, 11.5] |

## Frozen decision

| pass |
| --- |
| True |
