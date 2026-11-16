# H-B11_same_path_duration_noise: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 1536MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% first-visible-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Population and pairing coverage

| visible | source_payments | visible_paths | pairs | first_path_banks | paired_row_share |
| --- | --- | --- | --- | --- | --- |
| 2 | 1005689 | 192851 | 434352 | 3801 | 0.863790 |
| 3 | 370978 | 344873 | 19607 | 1067 | 0.105704 |
| 4 | 137022 | 136957 | <100 or thin bank support | suppressed | suppressed |
| 5 | 50120 | 50120 | 0 | 0 | 0.000000 |

## Primary tests for two and three visible banks; longer counts descriptive

| visible | n | banks | mean_square | MS_lo99 | MS_hi99 | TV_gain_over_visible_shape_lo99 | TV_gain_over_visible_shape_hi99 | meets_numeric_gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 434352 | 3801 | 100.353478 | 99.684406 | 101.058417 | 0.000000 | 0.000000 | True |
| 3 | 19607 | 1067 | 98.815627 | 95.262581 | 102.555761 | 0.085368 | 0.099606 | True |

## Six-bin total variation and 99% first-path-bank resampling intervals

| visible | model | TV | low | high |
| --- | --- | --- | --- | --- |
| 2 | fixed Gamma(2,5) | 0.001490 | 0.000479 | 0.003662 |
| 2 | matched exponential | 0.063482 | 0.061620 | 0.065592 |
| 2 | matched normal | 0.075218 | 0.073108 | 0.077080 |
| 2 | shape = visible count | 0.001490 | 0.000479 | 0.003662 |
| 3 | fixed Gamma(2,5) | 0.002461 | 0.001351 | 0.012050 |
| 3 | matched exponential | 0.062424 | 0.053440 | 0.071851 |
| 3 | matched normal | 0.076277 | 0.066850 | 0.085575 |
| 3 | shape = visible count | 0.101196 | 0.093532 | 0.108893 |

## One-second bins through 40 seconds, then 41+; descriptive

| visible | model | TV |
| --- | --- | --- |
| 2 | fixed Gamma(2,5) | 0.003083 |
| 2 | matched exponential | 0.067886 |
| 2 | matched normal | 0.076984 |
| 2 | shape = visible count | 0.003083 |
| 3 | fixed Gamma(2,5) | 0.016974 |
| 3 | matched exponential | 0.070536 |
| 3 | matched normal | 0.079183 |
| 3 | shape = visible count | 0.110982 |

## Absolute difference distribution; small tail cells masked

| visible | seconds | event_count | observed_share | model_share |
| --- | --- | --- | --- | --- |
| 2 | 0 | 21734 | 0.050038 | 0.049836 |
| 2 | 1–5 | 188010 | 0.432852 | 0.433912 |
| 2 | 6–10 | 115192 | 0.265204 | 0.265006 |
| 2 | 11–20 | 87568 | 0.201606 | 0.200644 |
| 2 | 21–40 | 21126 | 0.048638 | 0.049067 |
| 2 | 41+ | 722 | 0.001662 | 0.001535 |
| 3 | 0 | 967 | 0.049319 | 0.049836 |
| 3 | 1–5 | 8517 | 0.434386 | 0.433912 |
| 3 | 6–10 | 5228 | 0.266639 | 0.265006 |
| 3 | 11–20 | 3904 | 0.199113 | 0.200644 |
| 3 | 21–40 | 969 | 0.049421 | 0.049067 |
| 3 | 41+ | <100 | suppressed | 0.001535 |

## Controls with at least 100 pairs and 100 first visible banks

| visible | group | n | banks | mean_square | p50/p90/p99 seconds | differences_over_100s |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | All paired rows | 434352 | 3801 | 100.353478 | [6, 16, 30] | 0 |
| 2 | Different senders and receivers | 339169 | 3281 | 100.382718 | [6, 16, 30] | 0 |
| 2 | Different UTC month | 212870 | 3381 | 100.447254 | [6, 16, 30] | 0 |
| 2 | Only one payment has a placeholder | 41064 | 2243 | 101.753093 | [6, 16, 30] | 0 |
| 2 | Both Direct | 434352 | 3801 | 100.353478 | [6, 16, 30] | 0 |
| 2 | Pair mean below 100 s | 260846 | 1773 | 100.142076 | [6, 16, 30] | 0 |
| 2 | Pair mean from 100 to below 1,000 s | 76803 | 1512 | 100.342799 | [6, 16, 30] | 0 |
| 2 | Pair mean at least 1,000 s | 96703 | 2469 | 100.932194 | [6, 16, 30] | 0 |
| 3 | All paired rows | 19607 | 1067 | 98.815627 | [6, 16, 30] | 0 |
| 3 | Different senders and receivers | 15108 | 932 | 99.440032 | [6, 16, 30] | 0 |
| 3 | Different UTC month | 9693 | 907 | 98.623852 | [6, 16, 30] | 0 |
| 3 | Only one payment has a placeholder | 3478 | 626 | 99.636573 | [6, 16, 31] | 0 |
| 3 | Both Indirect | 16457 | 1002 | 99.151729 | [6, 16, 30] | 0 |
| 3 | Both Covered | 3150 | 254 | 97.059683 | [6, 16, 30] | 0 |
| 3 | Pair mean below 100 s | 7756 | 507 | 97.740330 | [6, 16, 30] | 0 |
| 3 | Pair mean from 100 to below 1,000 s | 6389 | 581 | 100.223509 | [6, 17, 30] | 0 |
| 3 | Pair mean at least 1,000 s | 5462 | 546 | 98.695716 | [6, 16, 29] | 0 |

## Overall two and three visible-bank decision

| pass |
| --- |
| True |
