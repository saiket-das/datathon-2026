# H-B03_covered_coin: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 2GB; two threads; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Intervals are 99% ordering-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Banks with >=100 unlabelled multibank payments

| banks | rows | banks_with_no_covered | banks_with_only_covered | expected_no_covered_under_coin | expected_only_covered_under_coin | bank_share_quantiles | row_weighted_covered_share |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 998 | 774238 | 91 | 0 | 0.001089 | 0.000000 | [0.002216348507097406, 0.018533584023333452, 0.19645066906675662] | 0.101305 |

## Within-bank versus independent-coin variance

| banks | mean_squared_share_deviation | expected_under_independent_coin |
| --- | --- | --- |
| 998 | 0.034074 | 0.000336 |
