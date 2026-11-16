# H-B15 supported directed-edge duration: confirm

Freeze: 44a4a5afa7959ad79e4bfe9058882a0a1f52e142. Unlabelled endpoint bit0/0, May edge fit and June calibration.
512MB, one thread, no spill. Prior Phase 0, Round 1 and Round 2 exposure applies.
May trained 7,236 directed edges from 212,230 two-visible-bank witnesses.
June offsets (seconds): sum -14.5, maximum 7.0, endpoint 14.0.
Scored month 7: 5,219/151,146 paths (3.4530%) across 331 ordering banks, 3,055 senders and 3,977 receivers.
Paths with shorter fitted edge at least100 seconds: 283.

| Shifted sum MAE | Shifted max MAE | MAE ratio | Sum p90 absolute error | Within20 seconds | Median unshifted sum residual |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 7.323913 | 21.820368 | 0.335646 | 15.500000 | 96.148687% | -14.500000 |

Ordering-bank 99% one-sided bounds: sum MAE upper 7.629742, ratio upper 0.482308, within20 lower 95.545228%.
Practical criteria PASS (unchanged frozen internal test).
Bank resampling is conditional and may retain path, repeated account and shared-intermediary dependencies.

## Descriptive controls

Each displayed cohort requires100 payments, ordering banks, senders and receivers. No control can rescue a failed primary result.

| Cohort | Payments | Banks | Sum MAE | Max MAE | Endpoint MAE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Indirect | 4,358 | 321 | 7.326411 | 17.535108 | 132.370405 |
| Covered | Suppressed | — | — | — | — |
| Shorter edge below100s | 4,936 | 320 | 7.218497 | 7.860920 | 143.932797 |
| Both edges at least100s | Suppressed | — | — | — | — |
| May endpoint comparator available | 3,493 | 267 | 7.435585 | 22.039937 | 160.668194 |
