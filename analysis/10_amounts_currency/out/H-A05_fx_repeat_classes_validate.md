# H-A05: FX bounds and repeat-class alternatives

Freeze: 54fe784a9ac96ba5fffd1f5bcbf172ad4018ac77.
512MB; one thread; no disk spill. Aggregates only.
Both-account bit-1 internal validation. Records, support and unsigned errors were previously exposed.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Primary scoped coverage and decision

| scoped | eligible | tightened | tightened_senders | tightened_receivers | tightened_ordering_banks | violations | all_criteria_met |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 888944 | 876388 | 161137 | 36148 | 78173 | 4248 | 0 | True |

## Bound violations and candidate corrections

| route | gap | reentry | n | senders | receivers | tighter_bound | above_country | above_class | above_shifted_class | below_class | repeat_repaired | repeat_broken | minus_one_repaired |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | All | All | 876388 | 97364 | 323316 | 161137 | 0 | 0 | 9002 | 3558 | 475 | 200290 | 3293 |
| All | All | false | 675313 | 88893 | 264926 | 133227 | 0 | 0 | 7622 | 2773 | 0 | 0 | 2768 |
| All | All | true | 201075 | 38653 | 90253 | 27910 | 0 | 0 | 1380 | 785 | 475 | 200290 | 525 |
| Covered | false | false | 58411 | 16096 | 32820 | 12609 | 0 | 0 | 672 | 159 | 0 | 0 | 159 |
| Covered | false | true | 24828 | 7815 | 14535 | 3126 | 0 | 0 | 161 | <100 | <100 | 24767 | <100 |
| Covered | true | false | 7394 | 3771 | 5718 | 1743 | 0 | 0 | <100 | <100 | 0 | 0 | <100 |
| Covered | true | true | 4300 | 2372 | 3362 | 743 | 0 | 0 | <100 | <100 | <100 | 4287 | <100 |
| Indirect | false | false | 540140 | 79626 | 221246 | 104342 | 0 | 0 | 5992 | 2289 | 0 | 0 | 2285 |
| Indirect | false | true | 145484 | 32209 | 69570 | 19211 | 0 | 0 | 959 | 588 | 368 | 144896 | 402 |
| Indirect | true | false | 69368 | 25197 | 41630 | 14533 | 0 | 0 | 866 | 301 | 0 | 0 | 300 |
| Indirect | true | true | 26463 | 11971 | 17546 | 4830 | 0 | 0 | 224 | 123 | <100 | 26340 | <100 |

See the H-A05 exposure audit for Phase 0, Round 1 and A03/A04 constraints.
