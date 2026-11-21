# H-B15 supported directed-edge duration: explore

Freeze: exploration only. Unlabelled endpoint bit0/0, May edge fit and June calibration.
512MB, one thread, no spill. Prior Phase 0, Round 1 and Round 2 exposure applies.
May trained 7,236 directed edges from 212,230 two-visible-bank witnesses.
June offsets (seconds): sum -14.5, maximum 7.0, endpoint 14.0.
Scored month 6: 7,335/211,787 paths (3.4634%) across 361 ordering banks, 3,986 senders and 5,366 receivers.
Paths with shorter fitted edge at least100 seconds: 386.

| Shifted sum MAE | Shifted max MAE | MAE ratio | Sum p90 absolute error | Within20 seconds | Median unshifted sum residual |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 7.541922 | 21.643695 | 0.348458 | 15.500000 | 96.128153% | -14.500000 |

Ordering-bank 99% one-sided bounds: sum MAE upper 8.497065, ratio upper 0.454718, within20 lower 95.568000%.
Practical criteria PASS (pilot only).
Bank resampling is conditional and may retain path, repeated account and shared-intermediary dependencies.

## Descriptive controls

Each displayed cohort requires100 payments, ordering banks, senders and receivers. No control can rescue a failed primary result.

| Cohort | Payments | Banks | Sum MAE | Max MAE | Endpoint MAE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Indirect | 6,085 | 351 | 7.171980 | 17.555875 | 132.797580 |
| Covered | 1,250 | 101 | 9.342800 | 41.543200 | Suppressed |
| Shorter edge below100s | 6,949 | 347 | 7.209599 | 7.975392 | 143.878514 |
| Both edges at least100s | Suppressed | — | — | — | — |
| May endpoint comparator available | 4,878 | 288 | 7.871874 | 23.020500 | 163.792743 |
