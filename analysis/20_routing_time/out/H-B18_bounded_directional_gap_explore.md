# H-B18_bounded_directional_gap: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 768MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% canonical first-visible-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Cohort coverage

| all_direct | supported_pairs | supported_payments | short_pairs | eligible_pairs | eligible_pair_share |
| --- | --- | --- | --- | --- | --- |
| 1005689 | 3196 | 230724 | 3103 | 511 | 0.159887 |

## Fixed comparison with first-bank resampling

| n | banks | uniform_TV | uniform_TV_upper99 | triangular_TV | TV_gain_lower99 | TV_gain_upper99 | share_above620_upper99 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 511 | 170 | 0.023821 | 0.075668 | 0.241691 | 0.142254 | 0.242568 | 0.000000 |

## Gap histogram

| interval_seconds | count | observed | uniform | triangular |
| --- | --- | --- | --- | --- |
| (20,120] | <100 | suppressed | 0.172414 | 0.315101 |
| (120,240] | 102 | 0.199609 | 0.206897 | 0.299643 |
| (240,360] | 101 | 0.197652 | 0.206897 | 0.214031 |
| (360,480] | 108 | 0.211350 | 0.206897 | 0.128419 |
| (480,600] | 102 | 0.199609 | 0.206897 | 0.042806 |
| >600 | <100 | suppressed | 0.000000 | 0.000000 |

## Endpoint and split-period controls

| group | eligible_pairs | payments | canonical_first_banks | gap_p10_p50_p90_p99 | above620_share | split_reference_pairs | absolute_drift_p50_p90_p99 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Primary | 511 | 57861 | 170 | [79.0, 314.0, 529.5, 589.95] | 0.000000 | 463 | [2.5, 7.0, 12.0] |
| Declared endpoints agree | 501 | 54841 | 167 | [79.0, 317.0, 534.0, 590.0] | 0.000000 | 452 | [2.5, 7.0, 11.745000000000005] |

## Frozen decision

| pass |
| --- |
| True |
