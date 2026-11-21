# H-B09 bank-duration exclusion: explore

Freeze: exploration only. May training, month 6 evaluation.
Unlabelled endpoint-bit0/0, visible counts2–5.512MB, one thread, no spill.
Phase0/Round1/Round2 duration/path/calendar exposure applies. Reused populations are internal.
Training: 1,061 supported banks, 440 zero-fast banks.
Evaluation: 891,959 payments, 646,066 supported paths (72.4323%).

| Model | Any exclusion bank | Payments | Ordering banks | Senders | Receivers | Duration<100 count | Share |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| May bank labels | False | 436,723 | 1,686 | 53,956 | 169,061 | 378,116 | 86.580281% |
| May bank labels | True | 209,343 | 1,354 | 39,718 | 91,304 | 0 | 0.000000% |
| Exposure-bin permutation | False | 396,206 | 1,542 | 52,514 | 155,940 | 274,510 | 69.284665% |
| Exposure-bin permutation | True | 249,860 | 1,535 | 44,645 | 109,040 | 103,606 | 41.465621% |

Affected ordering-bank fraction99% upper: 0.00339538.
Criteria PASS (pilot only).
The binomial bound assumes independent ordering-bank clusters. Shared path banks can violate this assumption.
An exposure-matched bank-label permutation is a falsification control, not an exchangeable randomisation test.

## Route and visible-count controls

| Route | Visible | Payments | Ordering banks | Fast count | Fast share |
| --- | --- | ---: | ---: | ---: | ---: |
| Covered | 3 | 3,840 | 359 | 0 | 0.000000% |
| Covered | 4 | 1,058 | 235 | 0 | 0.000000% |
| Covered | 5 | 293 | 108 | 0 | 0.000000% |
| Direct | 2 | 151,987 | 1,257 | 0 | 0.000000% |
| Indirect | 3 | 38,684 | 1,041 | 0 | 0.000000% |
| Indirect | 4 | 10,664 | 914 | 0 | 0.000000% |
| Indirect | 5 | 2,817 | 714 | 0 | 0.000000% |

## Entity overlap audit

Whole eligible evaluation cohort versus full May Direct training records. No source rows overlap across months.
| Shared same-role senders | Shared same-role receivers | Shared declared ordering banks | Used May-fitted visible banks |
| ---: | ---: | ---: | ---: |
| 42,230 | 51,777 | 1,836 | 1,061 |
All eligible visible banks are May-fitted by construction. Either-role account, intermediary and text dependencies remain.
