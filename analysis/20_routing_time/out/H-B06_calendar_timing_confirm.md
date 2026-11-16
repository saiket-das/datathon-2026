# H-B06: UTC calendar timing confirm

UTC period [2023-07-01, 2023-08-01). Unlabelled endpoint bit 0/0.
Frozen internal validation: 9e737f1d1e1e028b634b318624360902e3b99715. July records have earlier aggregate exposure.
512MB, one thread, no spill. Daytime denotes 06:00–17:59 UTC.

650,668 payments, 31 dates and 3,504 ordering banks.

| Alignment | Observed share | Uniform within-hour reference |
| --- | ---: | ---: |
| 5 seconds | 20.056311% | 20.000000% |
| Minute | 1.676431% | 1.666667% |
| Hour | 0.028279% | 0.027778% |

| Calendar | Payments | Dates | Ordering banks | Mean payments/day | UTC daytime share |
| --- | ---: | ---: | ---: | ---: | ---: |
| Weekday | 558,659 | 21 | 3,451 | 26,602.81 | 61.9841% |
| Weekend | 92,009 | 10 | 2,572 | 9,200.90 | 55.6011% |

Matched calendar contrast within ordering bank, route, party pair and month.
Each stratum has at least 30 payments of each calendar type. Weights are the smaller count.
Route rows with fewer than 100 supported ordering banks are suppressed.

| Route | Strata | Banks | Weekend payments | Weekday payments | Weighted delta (pp) | Equal-stratum delta (pp) | Strata with negative delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| All | 669 | 275 | 47,954 | 285,728 | -5.3911 | -5.1850 | 71.5994% |
| Direct | 434 | 275 | 33,742 | 201,312 | -5.0749 | -4.7298 | 69.3548% |
| Indirect | 220 | 157 | 13,028 | 76,927 | -5.8214 | -5.8721 | 75.0000% |

## Frozen decision

- Primary support: PASS
- Primary contrast at most −3 points: PASS
- Week omission support and direction: PASS
- Placebo within 3 points: PASS

Overall: PASS.

## Primary and weekday placebo contrasts

Positive contrast means a higher UTC daytime share in the first calendar group.
All estimates use smaller-group weights. Matched rows require 100 ordering banks.
Coverage denominators are the corresponding calendar groups before support filtering.
Suppressed rows have inadequate bank support. Date, bank and account composition can still differ.

| Contrast | Banks | Strata | Group 1 payments | Group 2 payments | Group 1 coverage | Group 2 coverage | Difference (pp) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Primary | 275 | 669 | 47,954 | 285,728 | 52.12% | 51.15% | -5.3911 |
| Placebo: Mon-Tue vs Wed-Fri | 530 | 1,554 | 155,943 | 232,573 | 69.91% | 69.30% | -0.2520 |

## Leave-one-UTC-week-out sensitivities

Remove all included dates in each Monday-start block, then recompute matching and support.
This range measures sensitivity to observed calendar blocks, without a confidence interval.

| Omitted week starting | Banks | Strata | Weekend payments | Weekday payments | Weekend coverage | Weekday coverage | Difference (pp) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-06-26 00:00:00 | 213 | 487 | 31,541 | 249,099 | 45.61% | 44.59% | -5.7131 |
| 2023-07-03 00:00:00 | 246 | 571 | 38,781 | 219,034 | 48.86% | 47.76% | -5.1618 |
| 2023-07-10 00:00:00 | 233 | 537 | 36,372 | 204,143 | 47.52% | 46.45% | -4.8242 |
| 2023-07-17 00:00:00 | 220 | 508 | 33,782 | 185,956 | 46.34% | 45.49% | -4.9238 |
| 2023-07-24 00:00:00 | 214 | 485 | 31,865 | 164,172 | 45.48% | 44.43% | -6.2506 |
| 2023-07-31 00:00:00 | 275 | 669 | 47,954 | 285,468 | 52.12% | 51.15% | -5.4363 |
