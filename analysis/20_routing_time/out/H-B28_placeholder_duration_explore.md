# H-B28_placeholder_duration: explore

Freeze: not yet frozen.
Unlabelled Direct, two visible banks, declared endpoint MD5 parity0/0.
512MB, one thread, no spill. Exact visible path and UTC period/route matched.
Each cell needs five payments with and without placeholders; equal cell weights.
Intervals: separate first/last-bank resampling, 1000 draws, seed20261117; conditional, not independent banks.
No identifiers or small-support cell values exported. Phase0/Round1/Round2/3 records and duration outcomes are exposed.

Scoped source: 1,005,689 payments, 192,851 visible paths, 5,580 first banks and 5,441 last banks.

| Match/control | Cells | Paths | First banks | Last banks | Payments | Gap-bearing payments | Mean contrast seconds | Median contrast | Mean squared contrast | Expected sampling variance | First-bank99% interval | Last-bank99% interval |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Month: primary | 1,047 | 764 | 414 | 305 | 168,673 | 9,946 | -0.090970 | -0.244444 | 7.809446 | 7.338612 | [-0.284381,0.119768] | [-0.278721,0.102929] |
| Week | 424 | 170 | 140 | 112 | 49,090 | 3,201 | 0.026980 | -0.167152 | 7.711071 | 8.416330 | [-0.331139,0.346991] | [-0.350216,0.377009] |
| Month + currency | 981 | 707 | 394 | 292 | 155,464 | 9,204 | -0.090998 | -0.264313 | 7.846554 | 7.445622 | [-0.285676,0.120179] | [-0.264233,0.079799] |
| Month + declared endpoints agree | 976 | 713 | 399 | 294 | 155,302 | 9,217 | -0.096021 | -0.289685 | 7.726068 | 7.301101 | [-0.330127,0.126219] | [-0.290789,0.108763] |

Primary equivalence/support conjunction: True.
A passed internal test bounds the matched equal-cell average contrast; it does not prove zero effect on every path, independence, missing-hop absence, causality or generator stage ordering.
Controls do not rescue a failed primary criterion. Paths with insufficient repeats and longer paths are outside scope.
Previously exposed records and shared banks/accounts prevent an independent holdout interpretation.
