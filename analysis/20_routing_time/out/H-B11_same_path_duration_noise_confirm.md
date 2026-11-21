# H-B11_same_path_duration_noise: confirm

Freeze: 9489c1a051237433c0a6fbbbd260e602b2e27521.
DuckDB 2.0.0; 1536MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% first-visible-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Population and pairing coverage

| visible | source_payments | visible_paths | pairs | first_path_banks | paired_row_share |
| --- | --- | --- | --- | --- | --- |
| 2 | 411335 | 116938 | 162341 | 2915 | 0.789337 |
| 3 | 151146 | 145172 | 4794 | 674 | 0.063435 |
| 4 | 55865 | 55862 | <100 or thin bank support | suppressed | suppressed |
| 5 | 20478 | 20478 | 0 | 0 | 0.000000 |

## Primary tests for two and three visible banks; longer counts descriptive

| visible | n | banks | mean_square | MS_lo99 | MS_hi99 | TV_gain_over_visible_shape_lo99 | TV_gain_over_visible_shape_hi99 | meets_numeric_gates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 162341 | 2915 | 99.592167 | 98.381773 | 100.813641 | 0.000000 | 0.000000 | True |
| 3 | 4794 | 674 | 98.877138 | 92.609066 | 104.910412 | 0.049678 | 0.098754 | False |

## Six-bin total variation and 99% first-path-bank resampling intervals

| visible | model | TV | low | high |
| --- | --- | --- | --- | --- |
| 2 | fixed Gamma(2,5) | 0.001435 | 0.000490 | 0.004401 |
| 2 | matched exponential | 0.061114 | 0.058394 | 0.064477 |
| 2 | matched normal | 0.077587 | 0.074224 | 0.080307 |
| 2 | shape = visible count | 0.001435 | 0.000490 | 0.004401 |
| 3 | fixed Gamma(2,5) | 0.014069 | 0.003902 | 0.033231 |
| 3 | matched exponential | 0.076230 | 0.056248 | 0.094542 |
| 3 | matched normal | 0.062471 | 0.044159 | 0.083735 |
| 3 | shape = visible count | 0.095533 | 0.080412 | 0.111265 |

## One-second bins through 40 seconds, then 41+; descriptive

| visible | model | TV |
| --- | --- | --- |
| 2 | fixed Gamma(2,5) | 0.005751 |
| 2 | matched exponential | 0.068899 |
| 2 | matched normal | 0.078755 |
| 2 | shape = visible count | 0.005751 |
| 3 | fixed Gamma(2,5) | 0.027578 |
| 3 | matched exponential | 0.081586 |
| 3 | matched normal | 0.066357 |
| 3 | shape = visible count | 0.096140 |

## Absolute difference distribution; small tail cells masked

| visible | seconds | event_count | observed_share | model_share |
| --- | --- | --- | --- | --- |
| 2 | 0 | 8140 | 0.050141 | 0.049836 |
| 2 | 1–5 | 70562 | 0.434653 | 0.433912 |
| 2 | 6–10 | 43055 | 0.265213 | 0.265006 |
| 2 | 11–20 | 32343 | 0.199229 | 0.200644 |
| 2 | 21–40 | 7995 | 0.049248 | 0.049067 |
| 2 | 41+ | 246 | 0.001515 | 0.001535 |
| 3 | 0 | 231 | 0.048185 | 0.049836 |
| 3 | 1–5 | 2026 | 0.422612 | 0.433912 |
| 3 | 6–10 | 1313 | 0.273884 | 0.265006 |
| 3 | 11–20 | 986 | 0.205674 | 0.200644 |
| 3 | 21–40 | 236 | 0.049228 | 0.049067 |
| 3 | 41+ | <100 | suppressed | 0.001535 |

## Controls with at least 100 pairs and 100 first visible banks

| visible | group | n | banks | mean_square | p50/p90/p99 seconds | differences_over_100s |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | All paired rows | 162341 | 2915 | 99.592167 | [6, 16, 30] | 0 |
| 2 | Different senders and receivers | 127187 | 2519 | 99.706071 | [6, 16, 30] | 0 |
| 2 | Only one payment has a placeholder | 15366 | 1575 | 101.301250 | [6, 17, 30] | 0 |
| 2 | Both Direct | 162341 | 2915 | 99.592167 | [6, 16, 30] | 0 |
| 2 | Pair mean below 100 s | 97913 | 1379 | 99.016474 | [6, 16, 30] | 0 |
| 2 | Pair mean from 100 to below 1,000 s | 29062 | 1103 | 101.340169 | [6, 16, 30] | 0 |
| 2 | Pair mean at least 1,000 s | 35366 | 1806 | 99.749590 | [6, 16, 30] | 0 |
| 3 | All paired rows | 4794 | 674 | 98.877138 | [6, 17, 29] | 0 |
| 3 | Different senders and receivers | 3698 | 572 | 100.372093 | [6, 17, 30] | 0 |
| 3 | Only one payment has a placeholder | 823 | 298 | 101.744836 | [6, 16, 30] | 0 |
| 3 | Both Indirect | 4017 | 616 | 97.909883 | [6, 16, 29] | 0 |
| 3 | Both Covered | 777 | 134 | 103.877735 | [6, 17, 31] | 0 |
| 3 | Pair mean below 100 s | 1754 | 311 | 103.472634 | [6, 17, 29] | 0 |
| 3 | Pair mean from 100 to below 1,000 s | 1669 | 329 | 94.517675 | [6, 16, 29] | 0 |
| 3 | Pair mean at least 1,000 s | 1371 | 289 | 98.304887 | [6, 17, 30] | 0 |

## Overall two and three visible-bank decision

| pass |
| --- |
| False |
