# H-B05_endpoint_mismatch: explore

Freeze: not yet frozen

Endpoint bit0/0, unlabelled payments. 512MB, one thread, no spill, UTC.
Phase 0 and Round 1 priors are exposed. July is internal temporal validation.

Payments: 1,593,042. Senders: 125,980. Receivers: 519,939. Ordering banks: 3,838.
Unscorable comparisons: 0. Both mismatch: 3,950.
A disjoint single-endpoint error comparator predicts zero joint cases.
Fixed-law practical criteria pass: True.

| Statistic | Pooled estimate | 99% lower | 99% upper |
| --- | ---: | ---: | ---: |
| ordering mismatch | 0.05031569 | 0.04917804 | 0.05158284 |
| beneficiary mismatch | 0.05000873 | 0.04895092 | 0.05121708 |
| both mismatch | 0.00247953 | 0.00237682 | 0.00260445 |
| joint excess | -0.00003669 | -0.00014936 | 0.00006799 |
| fixed-law TV | 0.00036535 | 0.00006502 | 0.00260166 |

## Route sensitivity
| Group | Payments | Ordering mismatch | Beneficiary mismatch | Joint rate | Excess joint | TV |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Covered | 58,684 | 0.05689796 | 0.05016700 | 0.00277759 | -0.00007681 | 0.00689796 |
| Direct | 1,005,689 | 0.05016262 | 0.05017555 | 0.00251171 | -0.00000523 | 0.00032647 |
| Indirect | 528,669 | 0.04987620 | 0.04967380 | 0.00238524 | -0.00009231 | 0.00033523 |

## Party pair sensitivity
| Group | Payments | Ordering mismatch | Beneficiary mismatch | Joint rate | Excess joint | TV |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BB | 360,919 | 0.04970090 | 0.04955683 | 0.00245484 | -0.00000817 | 0.00069712 |
| BC | 894,635 | 0.05044404 | 0.04996563 | 0.00246693 | -0.00005354 | 0.00047711 |
| CB | 96,078 | 0.05054227 | 0.05002186 | 0.00239389 | -0.00013433 | 0.00077635 |
| CC | 241,410 | 0.05066899 | 0.05083882 | 0.00259724 | 0.00002129 | 0.00141057 |

## Mismatch comparisons
| Role | Mismatches | Same country share | Equals opposite path endpoint share |
| --- | ---: | ---: | ---: |
| ordering | 80,155 | 0.04783232 | 0.00406712 |
| beneficiary | 79,666 | 0.05582055 | 0.00391635 |
