# H-B07 conditional gap placement: confirm

UTC period [2023-07-01, 2023-08-01); unlabelled endpoint bit 0/0; 512MB, one thread, no spill.
Freeze: f28120d22534ea09b8a1015ac910dca4545b6ce3. Prior Phase 0/Round 1/Round 2 exposure applies.
The July population has prior outcome exposure and shared entities. Only new shape outcomes were sealed.
Selected shape population: 26,211; endpoint placeholders: 0; visible-count mismatches: 0.
Source population: 650,668; multibank: 239,333; paths with any gaps: 49,974.

| Visible | Gaps | Payments | Banks | Senders | Receivers | TV uniform shapes | 99% upper | TV iid-slot | TV ratio | Ratio 99% upper | Adjacency share | Uniform adjacency | Iid adjacency |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | 1 | 13,702 | 1,572 | 8,009 | 10,275 | 0.002700 | 0.013649 | 0.002700 | — | — | — | — | — |
| 3 | 2 | 1,015 | 482 | 905 | 942 | 0.013136 | 0.048945 | 0.162069 | 0.081054 | 0.347570 | 0.662069 | 0.666667 | 0.500000 |
| 4 | 1 | 7,060 | 1,223 | 4,729 | 5,788 | 0.009585 | 0.023502 | 0.009585 | — | — | — | — | — |
| 4 | 2 | 680 | 373 | 626 | 644 | 0.025000 | 0.074385 | 0.175490 | 0.142458 | 0.441859 | 0.508824 | 0.500000 | 0.333333 |
| 5 | 1 | 3,318 | 903 | 2,597 | 2,904 | 0.021398 | 0.040449 | 0.021398 | — | — | — | — | — |
| 5 | 2 | 436 | 293 | 416 | 428 | 0.072477 | 0.139014 | 0.137615 | 0.526667 | 0.950748 | 0.385321 | 0.400000 | 0.250000 |

## Descriptive shape controls

Two-gap conditional shapes only. Require 250 payments and 100 banks, senders and receivers per cohort.
These controls share primary records and do not replace failed primary criteria.

| Control | Group | Visible | Payments | Banks | TV uniform | TV iid-slot | Adjacency |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| route | Covered | 3 | Suppressed | — | — | — | — |
| route | Covered | 4 | Suppressed | — | — | — | — |
| route | Covered | 5 | Suppressed | — | — | — | — |
| route | Indirect | 3 | 908 | 457 | 0.011747 | 0.165198 | 0.665198 |
| route | Indirect | 4 | 618 | 351 | 0.012945 | 0.171521 | 0.504854 |
| route | Indirect | 5 | 398 | 279 | 0.064824 | 0.137563 | 0.384422 |
| month | 7 | 3 | 1,015 | 482 | 0.013136 | 0.162069 | 0.662069 |
| month | 7 | 4 | 680 | 373 | 0.025000 | 0.175490 | 0.508824 |
| month | 7 | 5 | 436 | 293 | 0.072477 | 0.137615 | 0.385321 |

Practical criteria FAIL (unchanged frozen internal test).
Uniform weak compositions give equal probability to each legal sorted gap-slot pattern conditional on counts.
Primary strata: one gap and 3–5 visible banks, or two gaps and 3–4 visible banks. Two gaps with five banks is descriptive.
This also follows from exchangeable ordered visible/placeholder sequences conditional on counts.
It distinguishes iid per-gap slot allocation without identifying unique source implementation or exact probabilities.
Ordering-bank bootstrap intervals measure sensitivity with dependence and prior exposure limitations.
