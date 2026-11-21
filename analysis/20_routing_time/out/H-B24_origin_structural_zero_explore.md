# H-B24_origin_structural_zero: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 512MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% separate bank-role cluster resampling sensitivity intervals, not proof of independent banks.

## Two-state versus graded transfer

| n | banks | receivers | two_rate_brier | graded_brier | global_brier |
| --- | --- | --- | --- | --- | --- |
| 5487 | 437 | 759 | 0.029147 | 0.025279 | 0.029172 |

## Previously inactive versus active origins

| cohort | n | banks | receivers | covered_directions | observed | two_rate_predicted | graded_predicted | two_rate_brier | graded_brier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| No May Covered direction | 706 | 131 | 353 | <100 | 0.011331 | 0.000000 | 0.007477 | 0.011331 | 0.011180 |
| Any May Covered direction | 4781 | 306 | 754 | 155 | 0.032420 | 0.052649 | 0.043203 | 0.031778 | 0.027361 |

## Bank-role sensitivity

| cluster_role | clusters | graded_lift_low99 | graded_lift_high99 |
| --- | --- | --- | --- |
| Origin | 437 | 0.039652 | 0.227419 |
| Receiver | 759 | 0.068976 | 0.188916 |
