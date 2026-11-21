# H-B06: May–June exploratory composition checks

## Pre-validation challenges

Positive contrast means a higher UTC daytime share in the first calendar group.
All estimates use smaller-group weights. Matched rows require 100 ordering banks.
Coverage denominators are the corresponding calendar groups before support filtering.
Suppressed rows have inadequate bank support. Date, bank and account composition can still differ.

| Contrast | Banks | Strata | Group 1 payments | Group 2 payments | Group 1 coverage | Group 2 coverage | Difference (pp) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Primary | 270 | 1,107 | 76,245 | 680,435 | 48.59% | 47.38% | -6.9699 |
| May | 204 | 452 | 28,770 | 266,510 | 44.04% | 43.05% | -7.2779 |
| June | 269 | 655 | 47,475 | 413,925 | 51.84% | 50.66% | -6.7832 |
| Saturday vs weekdays | 230 | 838 | 26,233 | 581,590 | 43.71% | 40.50% | -9.7148 |
| Sunday vs weekdays | 340 | 1,459 | 53,396 | 758,981 | 55.10% | 52.85% | -5.9016 |
| Placebo: Mon-Tue vs Wed-Fri | 658 | 3,844 | 425,037 | 637,540 | 74.19% | 73.85% | 0.0590 |
| Minimum support 10 | 658 | 3,441 | 114,484 | 1,016,677 | 72.96% | 70.79% | -6.5803 |
| Minimum support 50 | 173 | 572 | 56,057 | 499,744 | 35.72% | 34.80% | -7.2551 |
| Also match beneficiary country | Suppressed | — | — | — | — | — | — |
| Also match beneficiary country and currency | Suppressed | — | — | — | — | — | — |
| Also match beneficiary bank | Suppressed | — | — | — | — | — | — |
| Also match ordering account | Suppressed | — | — | — | — | — | — |
| Same declared bank country | Suppressed | — | — | — | — | — | — |
| Different declared bank countries | 254 | 1,032 | 69,667 | 622,947 | 47.71% | 46.49% | -7.0442 |

## Leave-one-UTC-week-out sensitivities

Remove all included dates in each Monday-start block, then recompute matching and support.
This range measures sensitivity to observed calendar blocks, without a confidence interval.

| Omitted week starting | Banks | Strata | Weekend payments | Weekday payments | Weekend coverage | Weekday coverage | Difference (pp) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2023-05-01 00:00:00 | 269 | 941 | 64,169 | 575,753 | 46.30% | 44.73% | -7.1440 |
| 2023-05-08 00:00:00 | 269 | 998 | 68,003 | 609,080 | 47.08% | 45.58% | -6.8872 |
| 2023-05-15 00:00:00 | 269 | 991 | 67,291 | 607,077 | 46.85% | 45.43% | -6.7563 |
| 2023-05-22 00:00:00 | 269 | 913 | 62,222 | 560,087 | 45.86% | 44.23% | -7.0573 |
| 2023-05-29 00:00:00 | 224 | 946 | 61,398 | 558,227 | 45.11% | 44.11% | -7.1902 |
| 2023-06-05 00:00:00 | 229 | 952 | 62,391 | 567,262 | 45.24% | 44.10% | -6.9311 |
| 2023-06-12 00:00:00 | 229 | 944 | 60,755 | 556,171 | 45.01% | 43.92% | -6.7388 |
| 2023-06-19 00:00:00 | 212 | 864 | 55,040 | 505,336 | 43.31% | 42.20% | -7.5100 |
| 2023-06-26 00:00:00 | 270 | 1,107 | 76,245 | 584,661 | 48.59% | 46.89% | -6.9897 |
