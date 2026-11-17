# H-B29_institution_prefix_transfer: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 512MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% ordering-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Existing B20 June cohort and prefix eligibility

| original_corridors | n | banks | receivers | prefix_groups | payments | observed | prefix_rate | prefix_brier | global_brier | origin_brier | country_brier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5487 | 3812 | 308 | 740 | 131 | 9284 | 0.025446 | 0.044803 | 0.026743 | 0.025323 | 0.022124 | 0.025624 |

## Within-May bank-level similarity, excluding own bank from prefix

| banks | prefixes | correlation | mean_absolute_gap | gap_quantiles |
| --- | --- | --- | --- | --- |
| 329 | 136 | -0.061902 | 0.028506 | [0.0030831994506660965, 0.017528939286557996, 0.04789488864028878] |
