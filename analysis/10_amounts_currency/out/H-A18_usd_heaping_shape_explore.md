# H-A18 — USD decimal place versus significant digit heaping

Freeze: exploration.
512MB; one thread; no disk spill. Aggregates only.
Both-account bit-0 only. Phase 0 and A01–A17 prior exposure applies.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## July bit-0 positive unlabelled USD

| n | senders | receivers |
| --- | --- | --- |
| 129847 | 22229 | 64869 |

## Magnitude and party groups

| parties | magnitude | n | senders | receivers | integer_share | half_only_share | one_digit | two_digit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | 1 | 5361 | 3862 | 4255 | 0.40291 | 0.00653 | 0.18112 | 0.40291 |
| All | 2 | 22696 | 10112 | 15239 | 0.3958 | 0.00617 | 0.14584 | 0.19929 |
| All | 3 | 44829 | 12353 | 27060 | 0.38306 | 0.00645 | 0.12927 | 0.16483 |
| All | 4 | 38749 | 9156 | 24154 | 0.38037 | 0.00604 | 0.12488 | 0.15719 |
| All | 5 | 14943 | 4648 | 10382 | 0.37656 | 0.00683 | 0.12521 | 0.15399 |
| All | 6 | 2424 | 1405 | 1994 | 0.375 | 0.00784 | 0.12954 | 0.15718 |
| BB | 3 | 6644 | 3000 | 4421 | 0.40548 | 0.00647 | 0.14916 | 0.18904 |
| BB | 4 | 12593 | 4070 | 7662 | 0.37846 | 0.00596 | 0.12896 | 0.16112 |
| BB | 5 | 8481 | 3105 | 5484 | 0.3759 | 0.00649 | 0.1264 | 0.15493 |
| BC | 1 | 2222 | 1499 | 1909 | 0.41179 | 0.00495 | 0.19442 | 0.41179 |
| BC | 2 | 13079 | 4648 | 9096 | 0.40011 | 0.00589 | 0.15139 | 0.20506 |
| BC | 3 | 29279 | 6339 | 17906 | 0.3801 | 0.00615 | 0.12688 | 0.16169 |
| BC | 4 | 22146 | 5073 | 14329 | 0.38025 | 0.00605 | 0.12115 | 0.15317 |
| BC | 5 | 5736 | 2437 | 4474 | 0.37535 | 0.0075 | 0.12169 | 0.15185 |
| CB | 3 | 3019 | 2250 | 2286 | 0.37297 | 0.00629 | 0.12454 | 0.16032 |
| CB | 4 | 2235 | 1752 | 1764 | 0.37897 | 0.00716 | 0.12796 | 0.16197 |
| CC | 1 | 2753 | 2094 | 2279 | 0.39884 | 0.00763 | 0.16854 | 0.39884 |
| CC | 2 | 6867 | 4390 | 5187 | 0.38095 | 0.00743 | 0.12684 | 0.17912 |
| CC | 3 | 5887 | 3773 | 4506 | 0.37761 | 0.00798 | 0.12111 | 0.15543 |

Significant digit predicates mean divisible by the decimal place inferred from the observed amount, allowing USD-floating representation error. They do not identify how many digits were rounded before output. Displayed groups overlap and omit small group cells.
