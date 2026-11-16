# H-B04_covered_bank_stability: explore

Freeze: not frozen; pilot only.
512MB; one thread; no spill. UTC. Bank-bit-0/0 unlabelled multibank payments only.
Prior Phase 0 and Round 1 aggregates include these records; this is not an independent holdout.
Training uses May / May-June; evaluation uses June / July for explore / confirm.

## Support and predictive error

| all_n | n | senders | receivers | banks | covered_share | bank_brier | global_brier | composition_brier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 335391 | 276038 | 43737 | 126152 | 497 | 0.10240981 | 0.06263350 | 0.09192846 | 0.08958861 |

## Primary bank-cluster uncertainty

| statistic | estimate | low_99 | high_99 |
| --- | --- | --- | --- |
| bank/global Brier ratio | 0.68132867 | 0.60602756 | 0.77668097 |
| bank/composition Brier ratio | 0.69912344 | 0.61738885 | 0.78659723 |
| row-weighted bank calibration absolute error | 0.00848810 | 0.00733402 | 0.00959338 |

## Decision

Frozen internal-validation criteria pass: False. Coverage: 0.82303341.
Brier scores are predictive errors, not fraud-classification or recovered generator code.
Intervals resample ordering banks only; shared counterparties/path banks can induce residual dependence.

## Descriptive sensitivity: party pair

| group_name | n | senders | receivers | banks | covered_share | brier_ratio |
| --- | --- | --- | --- | --- | --- | --- |
| BB | 63070 | 13559 | 30397 | 497 | 0.10172824 | 0.70403741 |
| BC | 156449 | 20998 | 73593 | 497 | 0.10662261 | 0.68984955 |
| CB | 15985 | 8126 | 9679 | 477 | 0.09546450 | 0.72143853 |
| CC | 40534 | 15411 | 24139 | 485 | 0.08994918 | 0.72297901 |

## Descriptive sensitivity: visible count

| group_name | n | senders | receivers | banks | covered_share | brier_ratio |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 174227 | 34188 | 86831 | 497 | 0.10220574 | 0.70065005 |
| 4 | 64653 | 19392 | 38415 | 497 | 0.10267118 | 0.69568029 |
| 5 | 37158 | 13866 | 24159 | 497 | 0.10291189 | 0.69801232 |

## Descriptive sensitivity: currency

| group_name | n | senders | receivers | banks | covered_share | brier_ratio |
| --- | --- | --- | --- | --- | --- | --- |
| AED | 1521 | 363 | 1183 | 135 | 0.18080210 | 0.41503654 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| AUD | 4725 | 924 | 3711 | 183 | 0.07661376 | 0.85779254 |
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
| CAD | 1701 | 533 | 1395 | 139 | 0.02763081 | 0.98651161 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| CHF | 25690 | 2047 | 16413 | 425 | 0.13647334 | 0.68825355 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| CNY | 13666 | 8709 | 10246 | 350 | 0.22903556 | 0.71723166 |
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
| EUR | 93069 | 16716 | 50747 | 497 | 0.10599663 | 0.68321309 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| GBP | 21171 | 3549 | 13969 | 455 | 0.05687025 | 0.80286266 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| HKD | 7457 | 717 | 5423 | 208 | 0.05672522 | 0.73371852 |
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
| JPY | 3595 | 1336 | 2680 | 223 | 0.06147427 | 0.85781389 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| KRW | 2966 | 860 | 2459 | 120 | 0.04416723 | 0.99771906 |
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
| SAR | 640 | 267 | 521 | 112 | 0.25000000 | 0.46199953 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| SGD | 12359 | 996 | 8057 | 304 | 0.08018448 | 0.44309474 |
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
| UAH | 3002 | 973 | 2639 | 110 | 0.16722185 | 0.99566257 |
| suppressed | <100 | suppressed | suppressed | suppressed | suppressed | suppressed |
| USD | 44766 | 10697 | 27707 | 494 | 0.10583925 | 0.71419720 |
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

## Aggregate entity overlap (not identifiers)

| shared_senders | shared_receivers | shared_ordering_banks | shared_beneficiary_banks |
| --- | --- | --- | --- |
| 31722 | 32634 | 2866 | 2806 |
