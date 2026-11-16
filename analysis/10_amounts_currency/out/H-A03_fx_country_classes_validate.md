# H-A03: validate country-class FX transitions

Freeze: 2196f80cc3ab647ce67e7eb493aeed23cc190628.
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
| 888944 | 876388 | 0.9858753757267049 | 99617 | 328292 |

## Primary eligible multibank comparisons

| n | senders | receivers | exact_matches | exact_share | country_baseline | wrong_mapping | mean_absolute_error | largest_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 876388 | 97364 | 323316 | 872830 | 0.9959401543608538 | 0.8128477341086369 | 0.8033382474429134 | 0.004363364172033392 | 3 |

## 99% ordering-bank cluster sensitivity intervals

| statistic | low | high |
| --- | --- | --- |
| exact match | 0.9946903088567686 | 0.996804861891838 |
| lift over country transitions | 0.1736909028471477 | 0.19534702647908442 |

## Frozen practical decision

| passes | coverage_floor | exact_lower_floor | lift_lower_floor |
| --- | --- | --- | --- |
| False | 0.9 | 0.995 | 0.02 |

## Route sensitivity

| route | n | senders | receivers | exact_share | country_baseline |
| --- | --- | --- | --- | --- | --- |
| Covered | 94933 | 21314 | 47833 | 0.9972928275731305 | 0.8058525486395669 |
| Indirect | 781455 | 92181 | 295232 | 0.9957758284226219 | 0.8136975257692382 |

## Eligible identity and overlap audit

| n | distinct_rows | visible_banks | shared_training_banks |
| --- | --- | --- | --- |
| 876388 | 876388 | 7110 | 6530 |

## Month sensitivity

| period | n | senders | receivers | exact_share |
| --- | --- | --- | --- | --- |
| 4 | 545 | 485 | 521 | 0.9871559633027523 |
| 5 | 266942 | 53857 | 124100 | 0.9958343010841306 |
| 6 | 354967 | 62775 | 156344 | 0.9960475199103015 |
| 7 | 253934 | 52571 | 119287 | 0.9959201997369396 |
