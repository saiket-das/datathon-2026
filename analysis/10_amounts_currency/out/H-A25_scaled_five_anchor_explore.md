# H-A25 — Scaled preferred mantissa-five screen

Freeze: exploration.
512MB; one thread; no disk spill. Aggregates only.
Both-account bit-0 only. Phase 0 and A01–A24 exposure applies.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Amount-window scope

| currency | scoped | selected | senders | receivers | dates |
| --- | --- | --- | --- | --- | --- |
| CHF | 118916 | 16185 | 1843 | 10638 | 72 |
| EUR | 481734 | 68115 | 17706 | 38030 | 91 |
| GBP | 169603 | 23875 | 4129 | 15489 | 73 |
| USD | 244318 | 82510 | 18199 | 44435 | 90 |

## Complete supported anchor families

| currency | digit | n | points | point_senders | point_receivers | background | background_senders | background_receivers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHF | 4 | 3602 | 337 | 190 | 317 | 3265 | 766 | 2667 |
| CHF | 5 | 4823 | 2026 | 537 | 1727 | 2797 | 697 | 2327 |
| CHF | 6 | 2902 | 282 | 159 | 275 | 2620 | 644 | 2197 |
| CHF | 7 | 2577 | 209 | 135 | 200 | 2368 | 614 | 2004 |
| CHF | 8 | 2281 | 201 | 127 | 193 | 2080 | 573 | 1794 |
| EUR | 4 | 15250 | 1300 | 1043 | 1181 | 13950 | 6793 | 9944 |
| EUR | 5 | 20567 | 8409 | 4505 | 6419 | 12158 | 6060 | 8827 |
| EUR | 6 | 12063 | 1165 | 928 | 1074 | 10898 | 5495 | 8123 |
| EUR | 7 | 10568 | 949 | 788 | 860 | 9619 | 5040 | 7288 |
| EUR | 8 | 9667 | 849 | 732 | 789 | 8818 | 4743 | 6792 |
| GBP | 4 | 5424 | 433 | 235 | 411 | 4991 | 1625 | 4027 |
| GBP | 5 | 7248 | 2864 | 1065 | 2446 | 4384 | 1485 | 3569 |
| GBP | 6 | 4169 | 394 | 226 | 376 | 3775 | 1305 | 3165 |
| GBP | 7 | 3700 | 314 | 203 | 303 | 3386 | 1194 | 2856 |
| GBP | 8 | 3334 | 264 | 150 | 254 | 3070 | 1137 | 2620 |
| USD | 4 | 19472 | 1549 | 1224 | 1397 | 17923 | 7705 | 12601 |
| USD | 5 | 24695 | 9622 | 4786 | 7298 | 15073 | 6676 | 10756 |
| USD | 6 | 14430 | 1303 | 1060 | 1199 | 13127 | 6079 | 9636 |
| USD | 7 | 12642 | 1082 | 886 | 996 | 11560 | 5564 | 8581 |
| USD | 8 | 11271 | 898 | 775 | 828 | 10373 | 5052 | 7805 |

## Mantissa-five point-background odds relative to four and six

| currency | five_ratio_or_support | five_low99 | five_high99 | seven_control | seven_low99 | seven_high99 | pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHF | 6.886567248661877 | 6.130364397375268 | 8.147491243757653 | 0.8588460354764702 | 0.6753099139920017 | 1.1071915610619034 | True |
| EUR | 6.971989561376962 | 6.563278472647615 | 7.441390908229107 | 0.9658187468880122 | 0.8662899221625892 | 1.0757867021727763 | True |
| GBP | 6.924659529210319 | 6.220843737938999 | 7.66613639544448 | 0.964695501052968 | 0.8089413232540988 | 1.1843657504030276 | True |
| USD | 6.9498868945326295 | 6.5734389641212365 | 7.371320953559808 | 0.999349147682164 | 0.8994103579483146 | 1.1171431281058959 | True |

Anchor fitting amounts are at least USD10,000 and evaluation under USD9,000. Scale inference can alias denominations. Cent compatibility creates chance point hits. No iid interval or exact rounding operator follows from these odds.
