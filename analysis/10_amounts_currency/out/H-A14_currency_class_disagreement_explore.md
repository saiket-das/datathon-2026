# H-A14 — FX-class versus currency-mode changes

Freeze: exploration only.
512MB; one thread; no disk spill. Aggregates only.
Both-account bit-0 exploration only. Phase 0 and A01–A13 exposure applies.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Coverage

| scoped | eligible | senders | receivers |
| --- | --- | --- | --- |
| 275211 | 271176 | 53625 | 122429 |

## Missed equivalence and counterexamples

| category | n | senders | receivers | class_errors | mode_errors | repaired | broken | above_mode_bound | first_mode_match |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | 271176 | 53625 | 122429 | 1051 | 0 | 1051 | 0 | 0 | 0.9107111248783079 |
| Equal counts | 270125 | 53494 | 121998 | 0 | 0 | 0 | 0 | 0 | 0.9106709856547894 |
| Fewer currency-mode changes | 1051 | 798 | 889 | 1051 | 0 | 1051 | 0 | 0 | 0.9210275927687916 |

## Ordering-bank sensitivity

| ordering_banks | lift_low99 | lift_high99 | all_criteria_met |
| --- | --- | --- | --- |
| 4904 | 0.003120936031688817 | 0.004997197998830074 | True |

Country modes use currency outcomes while classes use two-bank FX counts. Both can encode shared metadata. Neither map identifies legal native currencies.
