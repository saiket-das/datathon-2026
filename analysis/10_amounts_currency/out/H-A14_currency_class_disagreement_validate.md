# H-A14 — FX-class versus currency-mode changes

Freeze: 7bd948fa5a5663bb9fc3d57ebd35bb567f4ab38f.
512MB; one thread; no disk spill. Aggregates only.
Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Coverage

| scoped | eligible | senders | receivers |
| --- | --- | --- | --- |
| 257566 | 253934 | 52571 | 119287 |

## Missed equivalence and counterexamples

| category | n | senders | receivers | class_errors | mode_errors | repaired | broken | above_mode_bound | first_mode_match |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | 253934 | 52571 | 119287 | 1036 | 0 | 1036 | 0 | 0 | 0.9119889420085534 |
| Equal counts | 252898 | 52446 | 118903 | 0 | 0 | 0 | 0 | 0 | 0.9118458825297155 |
| Fewer currency-mode changes | 1036 | 754 | 876 | 1036 | 0 | 1036 | 0 | 0 | 0.946911196911197 |

## Ordering-bank sensitivity

| ordering_banks | lift_low99 | lift_high99 | all_criteria_met |
| --- | --- | --- | --- |
| 4838 | 0.003246504101314346 | 0.005206107963378436 | True |

Country modes use currency outcomes while classes use two-bank FX counts. Both can encode shared metadata. Neither map identifies legal native currencies.
