# H-B28_placeholder_duration: confirm

Freeze: ddf5da4681cef5f163ad45966cb577f7d8fce31e.
Unlabelled Direct, two visible banks, declared endpoint MD5 parity0/0.
512MB, one thread, no spill. Exact visible path and UTC period/route matched.
Each cell needs five payments with and without placeholders; equal cell weights.
Intervals: separate first/last-bank resampling, 1000 draws, seed20261117; conditional, not independent banks.
No identifiers or small-support cell values exported. Phase0/Round1/Round2/3 records and duration outcomes are exposed.

Scoped source: 411,335 payments, 116,938 visible paths, 4,725 first banks and 4,604 last banks.

| Match/control | Cells | Paths | First banks | Last banks | Payments | Gap-bearing payments | Mean contrast seconds | Median contrast | Mean squared contrast | Expected sampling variance | First-bank99% interval | Last-bank99% interval |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Month: primary | 378 | 378 | 261 | 205 | 59,643 | 3,553 | 0.066669 | -0.153331 | 7.498822 | 7.592955 | [-0.282442,0.462346] | [-0.252486,0.515665] |
| Week | Suppressed: insufficient path/bank support | — | — | — | — | — | — | — | — | — | — | — |
| Month + currency | 348 | 347 | 245 | 196 | 54,478 | 3,261 | 0.070789 | -0.079136 | 6.989058 | 7.565009 | [-0.297978,0.425821] | [-0.318572,0.509718] |
| Month + declared endpoints agree | 350 | 350 | 251 | 197 | 54,678 | 3,259 | 0.112963 | -0.134112 | 8.105206 | 7.835697 | [-0.312527,0.542839] | [-0.255561,0.518405] |

## Eligible primary entity overlap with May–June scoped Direct records
Either account role and either visible endpoint role; all earlier scoped records, not just matched cells.
| Entity | Eligible distinct | Also in May–June |
| --- | ---: | ---: |
| Accounts, either role | 34980 | 22908 |
| Visible endpoint banks | 403 | 403 |

Primary equivalence/support conjunction: True.
A passed internal test bounds the matched equal-cell average contrast; it does not prove zero effect on every path, independence, missing-hop absence, causality or generator stage ordering.
Controls do not rescue a failed primary criterion. Paths with insufficient repeats and longer paths are outside scope.
Previously exposed records and shared banks/accounts prevent an independent holdout interpretation.
