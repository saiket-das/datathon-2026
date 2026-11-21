# H-B09 bank-duration exclusion: confirm

Freeze: 399a3dd62f9cbcac3e0869585cb2a49c10f7d578. May training, month 7 evaluation.
Unlabelled endpoint-bit0/0, visible counts2–5.512MB, one thread, no spill.
Phase0/Round1/Round2 duration/path/calendar exposure applies. Reused populations are internal.
Training: 1,061 supported banks, 440 zero-fast banks.
Evaluation: 638,824 payments, 462,931 supported paths (72.4661%).

| Model | Any exclusion bank | Payments | Ordering banks | Senders | Receivers | Duration<100 count | Share |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| May bank labels | False | 312,921 | 1,527 | 45,745 | 129,307 | 270,933 | 86.581917% |
| May bank labels | True | 150,010 | 1,325 | 32,968 | 69,913 | 0 | 0.000000% |
| Exposure-bin permutation | False | 283,939 | 1,397 | 44,715 | 119,871 | 196,939 | 69.359616% |
| Exposure-bin permutation | True | 178,992 | 1,445 | 36,958 | 82,706 | 73,994 | 41.339278% |

Affected ordering-bank fraction99% upper: 0.00346957.
Criteria PASS (frozen internal test).
The binomial bound assumes independent ordering-bank clusters. Shared path banks can violate this assumption.
An exposure-matched bank-label permutation is a falsification control, not an exchangeable randomisation test.

## Route and visible-count controls

| Route | Visible | Payments | Ordering banks | Fast count | Fast share |
| --- | --- | ---: | ---: | ---: | ---: |
| Covered | 3 | 2,836 | 321 | 0 | 0.000000% |
| Covered | 4 | 723 | 193 | 0 | 0.000000% |
| Direct | 2 | 109,032 | 1,232 | 0 | 0.000000% |
| Indirect | 3 | 27,541 | 1,008 | 0 | 0.000000% |
| Indirect | 4 | 7,651 | 876 | 0 | 0.000000% |
| Indirect | 5 | 2,029 | 628 | 0 | 0.000000% |

## Entity overlap audit

Whole eligible evaluation cohort versus full May Direct training records. No source rows overlap across months.
| Shared same-role senders | Shared same-role receivers | Shared declared ordering banks | Used May-fitted visible banks |
| ---: | ---: | ---: | ---: |
| 38,348 | 45,484 | 1,725 | 1,061 |
All eligible visible banks are May-fitted by construction. Either-role account, intermediary and text dependencies remain.
