# H-A03: explore country-class FX transitions

Freeze: not frozen; exploration only.
512MB; one thread; no disk spill. Aggregates only.
Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Training graph support

| supported_countries | learned_groups |
| --- | --- |
| 158 | 131 |

## Coverage

| n | eligible_n | eligible_share | senders | receivers |
| --- | --- | --- | --- | --- |
| 947930 | 934229 | 0.9855464011055669 | 101679 | 335798 |

## Primary eligible multibank comparisons

| n | senders | receivers | exact_matches | exact_share | country_baseline | wrong_mapping | mean_absolute_error | largest_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 934229 | 99409 | 330699 | 930635 | 0.9961529774819664 | 0.8164871781972086 | 0.8069349163855971 | 0.0041649317244487165 | 2 |

## 99% ordering-bank cluster sensitivity intervals

| statistic | low | high |
| --- | --- | --- |
| exact match | 0.9950535378254892 | 0.9968986655177526 |
| lift over country transitions | 0.17098708531521412 | 0.18902324064467066 |

## Frozen practical decision

| passes | coverage_floor | exact_lower_floor | lift_lower_floor |
| --- | --- | --- | --- |
| True | 0.9 | 0.995 | 0.02 |

## Route sensitivity

| route | n | senders | receivers | exact_share | country_baseline |
| --- | --- | --- | --- | --- | --- |
| Covered | 110177 | 21808 | 51022 | 0.9968686749503073 | 0.81039599916498 |
| Indirect | 824052 | 93984 | 300493 | 0.996057287646896 | 0.8173015780557538 |
