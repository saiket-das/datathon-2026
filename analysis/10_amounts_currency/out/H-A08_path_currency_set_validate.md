# H-A08: Currency membership in visible path-country modes

Phase validate; freeze 8bf80a9efd104bf2ebb200690a745443f02f4808. Pre-July bit-0 country modes score July.
Only paths with all country modes supported enter membership comparisons.
The wrong map circularly shifts seven sorted supported countries, preserving country-level mode frequencies.
Five visible banks and four distinct currencies denote their capped upper groups. Phase 0, Round 1 and A03-A07 exposure applies.

## Coverage

| scoped | eligible | senders | receivers |
| --- | --- | --- | --- |
| 699603 | 697868 | 88886 | 270205 |

## Membership and controls

| route | visible_banks | distinct_currencies | gap | n | senders | receivers | first_share | last_share | endpoint_share | path_share | wrong_path_share | union_frequency_baseline | unexplained |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | All | All | All | 697868 | 88886 | 270205 | 0.934662 | 0.197199 | 0.972536 | 0.987488 | 0.242718 | 0.293716 | 8732 |
| All | All | All | false | 644506 | 85644 | 253479 | 0.935485 | 0.197084 | 0.973443 | 0.987386 | 0.240729 | 0.290654 | 8130 |
| All | All | All | true | 53362 | 21018 | 33220 | 0.924722 | 0.198587 | 0.961583 | 0.988719 | 0.266744 | 0.330697 | 602 |
| Covered | 3 | All | All | 17530 | 7191 | 12056 | 0.931546 | 0.280091 | 0.960297 | 0.988534 | 0.315231 | 0.338607 | 201 |
| Covered | 4 | All | All | 6427 | 3459 | 5088 | 0.919558 | 0.272289 | 0.946943 | 0.992843 | 0.355687 | 0.402018 | <100 |
| Covered | 5 | All | All | 3751 | 2322 | 3142 | 0.889629 | 0.290856 | 0.922154 | 0.994668 | 0.401493 | 0.473835 | <100 |
| Direct | 2 | All | All | 441025 | 71017 | 186893 | 0.947881 | 0.199732 | 0.985992 | 0.985992 | 0.213772 | 0.248781 | 6178 |
| Indirect | 3 | All | All | 144987 | 38776 | 75897 | 0.920772 | 0.182975 | 0.959396 | 0.98884 | 0.264713 | 0.335356 | 1618 |
| Indirect | 4 | All | All | 53265 | 21088 | 33086 | 0.899371 | 0.181939 | 0.938834 | 0.991157 | 0.307613 | 0.403957 | 471 |
| Indirect | 5 | All | All | 30883 | 14596 | 20876 | 0.882362 | 0.180067 | 0.918596 | 0.993589 | 0.356928 | 0.479894 | 198 |

## Set cardinality control

| distinct_currencies | n | senders | receivers | path_share | wrong_path_share | union_frequency_baseline |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 79125 | 18225 | 38350 | 0.987956 | 0.418224 | 0.238585 |
| 2 | 434718 | 71309 | 185270 | 0.986375 | 0.208618 | 0.264751 |
| 3 | 135221 | 38371 | 72511 | 0.989188 | 0.239815 | 0.360712 |
| 4 | 48804 | 20842 | 31299 | 0.991927 | 0.269957 | 0.455482 |

## Bank-cluster sensitivity

| statistic | low99 | high99 |
| --- | --- | --- |
| membership | 0.986755038093397 | 0.9882410942974384 |
| lift vs union frequency | 0.6853638504471314 | 0.7014499021690278 |
| lift vs shifted map | 0.706372651584477 | 0.7777472928873161 |
| multibank lift vs endpoints | 0.03852352620417398 | 0.042882765471904755 |

## Practical decision

| all_criteria_met | ordering_banks | shared_training_ordering_banks |
| --- | --- | --- |
| True | 5651 | 4380 |
