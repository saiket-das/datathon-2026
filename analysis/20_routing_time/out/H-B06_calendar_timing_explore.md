# H-B06: UTC calendar timing exploration

May and June unlabelled endpoint bit 0/0. No validation was opened.
512MB, one thread, no spill. Daytime denotes 06:00–17:59 UTC.

1,593,042 payments, 61 dates and 3,838 ordering banks.

| Alignment | Observed share | Uniform within-hour reference |
| --- | ---: | ---: |
| 5 seconds | 20.050507% | 20.000000% |
| Minute | 1.685329% | 1.666667% |
| Hour | 0.028938% | 0.027778% |

| Calendar | Payments | Dates | Ordering banks | Mean payments/day | UTC daytime share |
| --- | ---: | ---: | ---: | ---: | ---: |
| Weekday | 1,436,129 | 45 | 3,804 | 31,913.98 | 62.0435% |
| Weekend | 156,913 | 16 | 2,871 | 9,807.06 | 54.2453% |

Matched calendar contrast within ordering bank, route, party pair and month.
Each stratum has at least 30 payments of each calendar type. Weights are the smaller count.
Route rows with fewer than 100 supported ordering banks are suppressed.

| Route | Strata | Banks | Weekend payments | Weekday payments | Weighted delta (pp) | Equal-stratum delta (pp) | Strata with negative delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| All | 1,107 | 270 | 76,245 | 680,435 | -6.9699 | -6.4776 | 76.4228% |
| Direct | 736 | 270 | 54,452 | 487,444 | -6.8747 | -6.3242 | 75.2717% |
| Indirect | 347 | 155 | 19,783 | 175,018 | -7.0327 | -6.6777 | 78.3862% |
