# H-B07 conditional gap placement: explore

UTC period [2023-05-01, 2023-07-01); unlabelled endpoint bit 0/0; 512MB, one thread, no spill.
Freeze: exploration only. Prior Phase 0/Round 1/Round 2 exposure applies.
The July population has prior outcome exposure and shared entities. Only new shape outcomes were sealed.
Selected shape population: 64,102; endpoint placeholders: 0; visible-count mismatches: 0.

| Visible | Gaps | Payments | Banks | Senders | Receivers | TV uniform shapes | 99% upper | TV iid-slot | TV ratio | Ratio 99% upper | Adjacency share | Uniform adjacency | Iid adjacency |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | 1 | 33,000 | 2,079 | 15,071 | 22,087 | 0.001939 | 0.007434 | 0.001939 | — | — | — | — | — |
| 3 | 2 | 2,589 | 812 | 2,083 | 2,296 | 0.010429 | 0.032672 | 0.177095 | 0.058888 | 0.170219 | 0.677095 | 0.666667 | 0.500000 |
| 4 | 1 | 17,631 | 1,705 | 9,626 | 12,869 | 0.003800 | 0.012643 | 0.003800 | — | — | — | — | — |
| 4 | 2 | 1,802 | 684 | 1,513 | 1,643 | 0.018313 | 0.049750 | 0.184980 | 0.099000 | 0.241471 | 0.518313 | 0.500000 | 0.333333 |
| 5 | 1 | 8,077 | 1,309 | 5,347 | 6,441 | 0.004024 | 0.018305 | 0.004024 | — | — | — | — | — |
| 5 | 2 | 1,003 | 485 | 888 | 948 | 0.033998 | 0.079124 | 0.129860 | 0.261804 | 0.695493 | 0.379860 | 0.400000 | 0.250000 |

## Descriptive shape controls

Two-gap conditional shapes only. Require 250 payments and 100 banks, senders and receivers per cohort.
These controls share primary records and do not replace failed primary criteria.

| Control | Group | Visible | Payments | Banks | TV uniform | TV iid-slot | Adjacency |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| route | Covered | 3 | 272 | 127 | 0.024510 | 0.150735 | 0.650735 |
| route | Covered | 4 | Suppressed | — | — | — | — |
| route | Covered | 5 | Suppressed | — | — | — | — |
| route | Indirect | 3 | 2,317 | 760 | 0.014099 | 0.180190 | 0.680190 |
| route | Indirect | 4 | 1,634 | 643 | 0.015300 | 0.181967 | 0.515300 |
| route | Indirect | 5 | 899 | 453 | 0.030478 | 0.132647 | 0.382647 |
| month | 5 | 3 | 1,072 | 509 | 0.025808 | 0.185634 | 0.685634 |
| month | 5 | 4 | 758 | 400 | 0.034301 | 0.200967 | 0.534301 |
| month | 5 | 5 | 453 | 283 | 0.030464 | 0.138521 | 0.388521 |
| month | 6 | 3 | 1,517 | 613 | 0.005493 | 0.171061 | 0.671061 |
| month | 6 | 4 | 1,044 | 510 | 0.019157 | 0.173372 | 0.506705 |
| month | 6 | 5 | 550 | 325 | 0.045455 | 0.122727 | 0.372727 |

Practical criteria PASS (pilot only).
Uniform weak compositions give equal probability to each legal sorted gap-slot pattern conditional on counts.
Primary strata: one gap and 3–5 visible banks, or two gaps and 3–4 visible banks. Two gaps with five banks is descriptive.
This also follows from exchangeable ordered visible/placeholder sequences conditional on counts.
It distinguishes iid per-gap slot allocation without identifying unique source implementation or exact probabilities.
Ordering-bank bootstrap intervals measure sensitivity with dependence and prior exposure limitations.
