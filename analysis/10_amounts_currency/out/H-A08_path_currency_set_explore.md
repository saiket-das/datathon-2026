# H-A08: Currency membership in visible path-country modes

Phase explore; freeze not frozen. Pre-July bit-0 country modes score July.
Only paths with all country modes supported enter membership comparisons.
The wrong map circularly shifts seven sorted supported countries, preserving country-level mode frequencies.
Five visible banks and four distinct currencies denote their capped upper groups. Phase 0, Round 1 and A03-A07 exposure applies.

## Coverage

| scoped | eligible | senders | receivers |
| --- | --- | --- | --- |
| 749066 | 747835 | 90726 | 277364 |

## Membership and controls

| route | visible_banks | distinct_currencies | gap | n | senders | receivers | first_share | last_share | endpoint_share | path_share | wrong_path_share | union_frequency_baseline | unexplained |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | All | All | All | 747835 | 90726 | 277364 | 0.93377 | 0.185851 | 0.971499 | 0.986974 | 0.224424 | 0.290105 | 9741 |
| All | All | All | false | 690238 | 87296 | 260032 | 0.934596 | 0.186018 | 0.972447 | 0.98687 | 0.222512 | 0.286854 | 9063 |
| All | All | All | true | 57597 | 21752 | 34512 | 0.923868 | 0.183846 | 0.960137 | 0.988229 | 0.247339 | 0.329068 | 678 |
| Covered | 3 | All | All | 20514 | 7452 | 13198 | 0.928342 | 0.23735 | 0.960174 | 0.989373 | 0.263284 | 0.334848 | 218 |
| Covered | 4 | All | All | 7461 | 3614 | 5560 | 0.915025 | 0.225975 | 0.943707 | 0.992226 | 0.303042 | 0.40548 | <100 |
| Covered | 5 | All | All | 4290 | 2405 | 3478 | 0.885315 | 0.229837 | 0.914685 | 0.992075 | 0.361072 | 0.479822 | <100 |
| Direct | 2 | All | All | 473207 | 72459 | 192081 | 0.947222 | 0.188336 | 0.985224 | 0.985224 | 0.195823 | 0.243814 | 6992 |
| Indirect | 3 | All | All | 152993 | 39620 | 77661 | 0.919003 | 0.176551 | 0.957599 | 0.988784 | 0.251998 | 0.333799 | 1716 |
| Indirect | 4 | All | All | 56417 | 21477 | 33679 | 0.900597 | 0.17165 | 0.938192 | 0.990747 | 0.292022 | 0.403347 | 522 |
| Indirect | 5 | All | All | 32953 | 15092 | 21568 | 0.87989 | 0.170789 | 0.9167 | 0.9939 | 0.331593 | 0.479433 | 201 |

## Set cardinality control

| distinct_currencies | n | senders | receivers | path_share | wrong_path_share | union_frequency_baseline |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 78852 | 18453 | 38285 | 0.986735 | 0.388043 | 0.230508 |
| 2 | 469174 | 72853 | 190731 | 0.985696 | 0.192856 | 0.259738 |
| 3 | 146336 | 39313 | 74969 | 0.989237 | 0.226656 | 0.358882 |
| 4 | 53473 | 21302 | 32658 | 0.992351 | 0.254016 | 0.456213 |

## Bank-cluster sensitivity

| statistic | low99 | high99 |
| --- | --- | --- |
| membership | 0.9862613737941569 | 0.9876380235849548 |
| lift vs union frequency | 0.690600255976843 | 0.7032755942647522 |
| lift vs shifted map | 0.7288246927165075 | 0.7914201200913632 |
| multibank lift vs endpoints | 0.04034672101101127 | 0.04414007341654535 |

## Practical decision

| all_criteria_met | ordering_banks |
| --- | --- |
| True | 5700 |
