# H-A05: FX bounds and repeat-class alternatives

Freeze: exploration only.
512MB; one thread; no disk spill. Aggregates only.
Both-account bit-0 exploration only.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Primary scoped coverage and decision

| scoped | eligible | tightened | tightened_senders | tightened_receivers | tightened_ordering_banks | violations | all_criteria_met |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 947930 | 934229 | 168566 | 36428 | 79326 | 4316 | 0 | True |

## Bound violations and candidate corrections

| route | gap | reentry | n | senders | receivers | tighter_bound | above_country | above_class | above_shifted_class | below_class | repeat_repaired | repeat_broken | minus_one_repaired |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | All | All | 934229 | 99409 | 330699 | 168566 | 0 | 0 | 9655 | 3594 | 459 | 205706 | 3297 |
| All | All | false | 727721 | 90893 | 272049 | 140374 | 0 | 0 | 8153 | 2792 | 0 | 0 | 2787 |
| All | All | true | 206508 | 39097 | 91289 | 28192 | 0 | 0 | 1502 | 802 | 459 | 205706 | 510 |
| Covered | false | false | 71251 | 16507 | 35940 | 14665 | 0 | 0 | 697 | 224 | 0 | 0 | 224 |
| Covered | false | true | 25380 | 8027 | 14932 | 3131 | 0 | 0 | 206 | <100 | <100 | 25302 | <100 |
| Covered | true | false | 9136 | 4098 | 6534 | 2051 | 0 | 0 | 107 | <100 | 0 | 0 | <100 |
| Covered | true | true | 4410 | 2433 | 3415 | 770 | 0 | 0 | <100 | <100 | <100 | 4390 | <100 |
| Indirect | false | false | 573719 | 80966 | 225769 | 108537 | 0 | 0 | 6411 | 2249 | 0 | 0 | 2244 |
| Indirect | false | true | 149351 | 32500 | 69963 | 19354 | 0 | 0 | 1019 | 578 | 332 | 148773 | 369 |
| Indirect | true | false | 73615 | 25748 | 42730 | 15121 | 0 | 0 | 938 | 296 | 0 | 0 | 296 |
| Indirect | true | true | 27367 | 12200 | 17882 | 4937 | 0 | 0 | 234 | 126 | <100 | 27241 | <100 |

See the H-A05 exposure audit for Phase 0, Round 1 and A03/A04 constraints.
