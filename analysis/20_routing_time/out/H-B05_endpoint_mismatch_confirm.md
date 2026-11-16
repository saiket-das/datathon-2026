# H-B05_endpoint_mismatch: confirm

Freeze: 1c4580bac192eac0d76727648796a6c2b14c9279

Endpoint bit0/0, unlabelled payments. 512MB, one thread, no spill, UTC.
Phase 0 and Round 1 priors are exposed. July is internal temporal validation.

Payments: 650,668. Senders: 84,156. Receivers: 254,069. Ordering banks: 3,504.
Unscorable comparisons: 0. Both mismatch: 1,657.
A disjoint single-endpoint error comparator predicts zero joint cases.
Fixed-law practical criteria pass: True.

| Statistic | Pooled estimate | 99% lower | 99% upper |
| --- | ---: | ---: | ---: |
| ordering mismatch | 0.05048504 | 0.04920545 | 0.05178590 |
| beneficiary mismatch | 0.05040205 | 0.04919990 | 0.05159552 |
| both mismatch | 0.00254661 | 0.00237544 | 0.00270894 |
| joint excess | 0.00000206 | -0.00015791 | 0.00016910 |
| fixed-law TV | 0.00084047 | 0.00007717 | 0.00324862 |

## Route sensitivity
| Group | Payments | Ordering mismatch | Beneficiary mismatch | Joint rate | Excess joint | TV |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Covered | 23,760 | 0.05850168 | 0.05058923 | 0.00340909 | 0.00044954 | 0.00850168 |
| Direct | 411,335 | 0.05052086 | 0.05034339 | 0.00252835 | -0.00001504 | 0.00083591 |
| Indirect | 215,573 | 0.04953310 | 0.05049334 | 0.00248640 | -0.00001470 | 0.00050694 |

## Party pair sensitivity
| Group | Payments | Ordering mismatch | Beneficiary mismatch | Joint rate | Excess joint | TV |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BB | 147,369 | 0.05018016 | 0.04931159 | 0.00261249 | 0.00013803 | 0.00080090 |
| BC | 365,139 | 0.05032330 | 0.05067111 | 0.00250316 | -0.00004678 | 0.00099126 |
| CB | 39,423 | 0.05108693 | 0.05050351 | 0.00258732 | 0.00000725 | 0.00150312 |
| CC | 98,737 | 0.05129789 | 0.05099405 | 0.00259275 | -0.00002314 | 0.00219920 |

## Mismatch comparisons
| Role | Mismatches | Same country share | Equals opposite path endpoint share |
| --- | ---: | ---: | ---: |
| ordering | 32,849 | 0.04797711 | 0.00401839 |
| beneficiary | 32,795 | 0.05516085 | 0.00399451 |

## Distinct entities shared with May–June
| Entity set | Shared count |
| --- | ---: |
| sender | 65,380 |
| receiver | 92,216 |
| accounts across both roles | 128,589 |
| declared endpoint banks | 3,696 |
| visible path banks | 6,319 |
