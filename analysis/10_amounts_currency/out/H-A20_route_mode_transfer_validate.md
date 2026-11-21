# H-A20 — Currency mode transfer across training routes

Freeze: a045ce3340ccc00df5e8aee0918d719f1d0474a2.
512MB; one thread; no disk spill. Aggregates only.
Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## July route coverage

| route | n | two_mapped | multi_mapped | joint_mapped |
| --- | --- | --- | --- | --- |
| Covered | 27765 | 27625 | 27570 | 27570 |
| Direct | 442037 | 440406 | 439703 | 439703 |
| Indirect | 229801 | 228713 | 228199 | 228199 |

## FX count errors on jointly mapped rows

| route | n | senders | receivers | banks | two_errors | multi_errors | disagreement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Covered | 27570 | 9737 | 17616 | 1903 | 0 | 0 | 0 |
| Direct | 439703 | 70548 | 186196 | 5312 | 0 | 0 | 0 |
| Indirect | 228199 | 49850 | 109508 | 4778 | 0 | 0 | 0 |

## Routing coverage sensitivity and decision

| route | joint_coverage | scoped_ordering_banks | coverage_low99 | coverage_high99 | pass |
| --- | --- | --- | --- | --- | --- |
| Covered | 0.9929767693138843 | 1944 | 0.9888246066141759 | 0.9954385094524393 | True |
| Direct | 0.9947198990129785 | 5408 | 0.9926959014652255 | 0.9962582844412482 | True |
| Indirect | 0.9930287509627895 | 4874 | 0.9910828244654514 | 0.9946435434484335 | True |

Training uses payment currencies and first visible countries, without FX labels. Route categories in scoring are supplied labels. Training categories use visible path length. Joint support prevents coverage differences from distorting accuracy.
