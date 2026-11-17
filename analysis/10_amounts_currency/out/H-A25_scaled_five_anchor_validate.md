# H-A25 — Scaled preferred mantissa-five screen

Freeze: ee8a5c55b97d31404ff3a28d444a4eca9c36abcf.
512MB; one thread; no disk spill. Aggregates only.
Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Amount-window scope

| currency | scoped | selected | senders | receivers | dates |
| --- | --- | --- | --- | --- | --- |
| CHF | 108456 | 14466 | 1766 | 9893 | 72 |
| EUR | 488287 | 68535 | 17481 | 38737 | 91 |
| GBP | 111916 | 15650 | 3950 | 11017 | 73 |
| USD | 226053 | 76319 | 17819 | 43076 | 90 |

## Complete supported anchor families

| currency | digit | n | points | point_senders | point_receivers | background | background_senders | background_receivers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHF | 4 | 3208 | 286 | 170 | 279 | 2922 | 734 | 2498 |
| CHF | 5 | 4322 | 1755 | 503 | 1569 | 2567 | 656 | 2169 |
| CHF | 6 | 2544 | 266 | 164 | 260 | 2278 | 651 | 1959 |
| CHF | 7 | 2286 | 227 | 144 | 222 | 2059 | 600 | 1819 |
| CHF | 8 | 2106 | 182 | 113 | 181 | 1924 | 547 | 1706 |
| EUR | 4 | 15435 | 1297 | 1016 | 1200 | 14138 | 6650 | 10364 |
| EUR | 5 | 20441 | 8299 | 4332 | 6522 | 12142 | 5965 | 9032 |
| EUR | 6 | 12081 | 1168 | 945 | 1101 | 10913 | 5455 | 8288 |
| EUR | 7 | 10829 | 982 | 816 | 915 | 9847 | 5026 | 7581 |
| EUR | 8 | 9749 | 885 | 728 | 840 | 8864 | 4533 | 6900 |
| GBP | 4 | 3632 | 296 | 245 | 289 | 3336 | 1523 | 2854 |
| GBP | 5 | 4728 | 1907 | 1049 | 1718 | 2821 | 1350 | 2429 |
| GBP | 6 | 2758 | 266 | 217 | 257 | 2492 | 1255 | 2160 |
| GBP | 7 | 2389 | 202 | 172 | 194 | 2187 | 1153 | 1930 |
| GBP | 8 | 2143 | 189 | 171 | 189 | 1954 | 1073 | 1742 |
| USD | 4 | 18138 | 1277 | 1050 | 1182 | 16861 | 7430 | 12252 |
| USD | 5 | 23129 | 8880 | 4678 | 7105 | 14249 | 6604 | 10582 |
| USD | 6 | 13354 | 1194 | 1009 | 1111 | 12160 | 5836 | 9203 |
| USD | 7 | 11396 | 912 | 790 | 865 | 10484 | 5275 | 8070 |
| USD | 8 | 10302 | 854 | 742 | 818 | 9448 | 4977 | 7435 |

## Mantissa-five point-background odds relative to four and six

| currency | five_ratio_or_support | five_low99 | five_high99 | seven_control | seven_low99 | seven_high99 | pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHF | 6.440439694449619 | 5.738377475641605 | 7.366367596095835 | 1.0340642995906473 | 0.8398560066764996 | 1.2436375013182412 | True |
| EUR | 6.946142352680568 | 6.5259715200300725 | 7.417916544848842 | 0.9606805853870106 | 0.8671159655905621 | 1.0770483282451229 | True |
| GBP | 7.010206874975558 | 6.039557322920277 | 7.944562457237981 | 0.902527924750147 | 0.6997322959151535 | 1.126374954619091 | True |
| USD | 7.319277398438065 | 6.760537454966595 | 7.889593106291431 | 0.9178092808088516 | 0.8315047767205771 | 1.0061513439366496 | True |

Anchor fitting amounts are at least USD10,000 and evaluation under USD9,000. Scale inference can alias denominations. Cent compatibility creates chance point hits. No iid interval or exact rounding operator follows from these odds.
