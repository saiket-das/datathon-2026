# H-B04_covered_bank_stability: confirm

Freeze: f0259aa156723f60943dca219b8153532dca9860.
512MB; one thread; no spill. UTC. Bank-bit-0/0 unlabelled multibank payments only.
Prior Phase 0 and Round 1 aggregates include these records; this is not an independent holdout.
Training uses May / May-June; evaluation uses June / July for explore / confirm.

## Support and predictive error

| all_n | n | senders | receivers | banks | covered_share | bank_brier | global_brier | composition_brier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 239333 | 218479 | 42073 | 104342 | 840 | 0.10164364 | 0.06038437 | 0.09131520 | 0.08869949 |

## Primary bank-cluster uncertainty

| statistic | estimate | low_99 | high_99 |
| --- | --- | --- | --- |
| bank/global Brier ratio | 0.66127395 | 0.58981634 | 0.74504310 |
| bank/composition Brier ratio | 0.68077469 | 0.60324234 | 0.75861473 |
| row-weighted bank calibration absolute error | 0.00925026 | 0.00802591 | 0.01038991 |

## Decision

Frozen internal-validation criteria pass: True. Coverage: 0.91286617.
Brier scores are predictive errors, not fraud-classification or recovered generator code.
Intervals resample ordering banks only; shared counterparties/path banks can induce residual dependence.

## Descriptive sensitivity: party pair

| group_name | n | senders | receivers | banks | covered_share | brier_ratio |
| --- | --- | --- | --- | --- | --- | --- |
| BB | 49821 | 13072 | 25042 | 839 | 0.10493567 | 0.67902433 |
| BC | 123122 | 20792 | 60495 | 840 | 0.10472539 | 0.67380277 |
| CB | 13024 | 7252 | 8175 | 751 | 0.09505528 | 0.70790870 |
| CC | 32512 | 13948 | 20207 | 795 | 0.08756767 | 0.70339617 |

## Descriptive sensitivity: visible count

| group_name | n | senders | receivers | banks | covered_share | brier_ratio |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 137961 | 32682 | 71775 | 840 | 0.10246374 | 0.68521349 |
| 4 | 51090 | 17940 | 31614 | 840 | 0.09917792 | 0.67032122 |
| 5 | 29428 | 12707 | 19742 | 840 | 0.10207965 | 0.67768045 |

## Descriptive sensitivity: currency

| group_name | n | senders | receivers | banks | covered_share | brier_ratio |
| --- | --- | --- | --- | --- | --- | --- |
| AED | 1321 | 389 | 1071 | 128 | 0.18849357 | 0.49784654 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| AUD | 3580 | 829 | 2885 | 176 | 0.07541899 | 0.83610039 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| CAD | 1470 | 516 | 1185 | 119 | 0.05238095 | 0.57654996 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| CHF | 19155 | 1855 | 12895 | 523 | 0.13855390 | 0.64768114 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| CNY | 10395 | 7065 | 8100 | 388 | 0.22260702 | 0.70217969 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| EUR | 72647 | 15448 | 41264 | 836 | 0.10546891 | 0.66926280 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| GBP | 17078 | 3311 | 11609 | 587 | 0.05943319 | 0.81376570 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| HKD | 5703 | 638 | 4344 | 197 | 0.04997370 | 0.75211508 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| JPY | 3329 | 1449 | 2594 | 239 | 0.05286873 | 0.83592914 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| KRW | 2287 | 785 | 1961 | 125 | 0.03148229 | 1.01601246 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| SGD | 9705 | 873 | 6519 | 306 | 0.09294178 | 0.46469397 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| UAH | 2364 | 886 | 2104 | 100 | 0.13705584 | 0.99510023 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| USD | 35028 | 9876 | 22279 | 779 | 0.10508736 | 0.69336534 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |

## Aggregate entity overlap (not identifiers)

| shared_senders | shared_receivers | shared_ordering_banks | shared_beneficiary_banks |
| --- | --- | --- | --- |
| 35930 | 39334 | 2939 | 2874 |
