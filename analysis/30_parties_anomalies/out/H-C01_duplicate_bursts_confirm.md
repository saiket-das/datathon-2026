# H-C01_duplicate_bursts: confirm

DuckDB 2.0.0; 2GB; one thread; UTC; no disk spill.
Freeze: `bd61bc32dc61f4985c757244051404fb6622a71b`.
Sender MD5 parity split; whole sender clusters retained. Phase 0 full-data exposure applies.
No bank/time repartition is an independent holdout. Unlabelled does not mean legitimate.
Cohorts below 100 rows are suppressed; entity counts below 100 are masked.

## Partition and six-label baseline

| label | n | senders | receivers | amount_median | duration_median | business_sender_share | business_receiver_share |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACCOUNT_REPLACEMENT_SCAM | 312 | 301 | 253 | 4366.91 | 587.5 | 0.788462 | 0.221154 |
| CEO_SCAM | 465 | 442 | 367 | 16284 | 836 | 1 | 0.307527 |
| CUSTOMER_RECALL | 155 | 152 | 152 | 2738.93 | 48 | 0.774194 | 0.264516 |
| DUPLICATE_PAYMENT | 367 | 100 | 100 | 4875.43 | 389 | 0.841962 | 0.26158 |
| FAT_FINGER_MISTAKE | 993 | 901 | 958 | 233042 | 55 | 0.789527 | 0.287009 |
| ROMANCE_SCAM | 1154 | 236 | 200 | 117.865 | 1123 | 0 | 0.261698 |
| UNLABELLED | 4898616 | 194678 | 1449040 | 3718.18 | 57 | 0.793781 | 0.288421 |

## Broad repeat comparator without source-order or context conditions

| label | n | repeated_rows | repeat_share | median_family_size |
| --- | --- | --- | --- | --- |
| ACCOUNT_REPLACEMENT_SCAM | 312 | 0 | 0 | 1 |
| CEO_SCAM | 465 | 0 | 0 | 1 |
| CUSTOMER_RECALL | 155 | 0 | 0 | 1 |
| DUPLICATE_PAYMENT | 367 | 367 | 1 | 4 |
| FAT_FINGER_MISTAKE | 993 | 0 | 0 | 1 |
| ROMANCE_SCAM | 1154 | 12 | 0.0103986 | 1 |
| UNLABELLED | 4898616 | 2508 | 0.000511981 | 1 |

## Signature against every label (not a legitimacy classifier)

| label | n | hits | coverage | senders | receivers |
| --- | --- | --- | --- | --- | --- |
| ACCOUNT_REPLACEMENT_SCAM | 312 | 0 | 0 | 301 | 253 |
| CEO_SCAM | 465 | 0 | 0 | 442 | 367 |
| CUSTOMER_RECALL | 155 | 0 | 0 | 152 | 152 |
| DUPLICATE_PAYMENT | 367 | 367 | 1 | 100 | 100 |
| FAT_FINGER_MISTAKE | 993 | 0 | 0 | 901 | 958 |
| ROMANCE_SCAM | 1154 | 12 | 0.0103986 | 236 | 200 |
| UNLABELLED | 4898616 | 0 | 0 | 194678 | 1449040 |

## Candidate-family structure; target label used only for assessment

| label | n | families | target_rows | signature_rows | fully_labelled_family_share | smallest_family | largest_family | median_span | max_span | fixed_context_share | monotone_share | median_family_growth | mean_family_backwards_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| other | <100 | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed |
| target-containing | 367 | 100 | 367 | 367 | 1 | 2 | 5 | 4028 | 6980 | 1 | 0.15 | 1 | 0.555833 |

## Party-pair control

| stratum | label | n | coverage | senders |
| --- | --- | --- | --- | --- |
| BB | UNLABELLED | 1124807 | 0 | 60499 |
| BB | other-label | 457 | 0 | 425 |
| BB | target | <100 | suppressed | suppressed |
| BC | UNLABELLED | 2763623 | 0 | 80046 |
| BC | other-label | 1158 | 0 | 1034 |
| BC | target | 215 | 1 | <100 |
| CB | UNLABELLED | 288059 | 0 | 60200 |
| CB | other-label | 383 | 0 | 138 |
| CB | target | <100 | suppressed | suppressed |
| CC | UNLABELLED | 722127 | 0 | 92656 |
| CC | other-label | 1081 | 0.0111008 | 399 |
| CC | target | <100 | suppressed | suppressed |

## Calendar sensitivity within the same sender split

| stratum | label | n | coverage | senders |
| --- | --- | --- | --- | --- |
| 2023-04 | UNLABELLED | 3025 | 0 | 2154 |
| 2023-05 | UNLABELLED | 1492057 | 0 | 125266 |
| 2023-05 | other-label | 974 | 0.00205339 | 621 |
| 2023-05 | target | <100 | suppressed | suppressed |
| 2023-06 | UNLABELLED | 1983785 | 0 | 140355 |
| 2023-06 | other-label | 1158 | 0.00518135 | 813 |
| 2023-06 | target | 165 | 1 | <100 |
| 2023-07 | UNLABELLED | 1419749 | 0 | 122465 |
| 2023-07 | other-label | 947 | 0.00422386 | 617 |
| 2023-07 | target | 105 | 1 | <100 |

## Source-file block sensitivity (zero-based million-row blocks)

| stratum | label | n | coverage | senders |
| --- | --- | --- | --- | --- |
| 0 | UNLABELLED | 490066 | 0 | 75151 |
| 0 | other-label | 680 | 0.00588235 | 310 |
| 0 | target | <100 | suppressed | suppressed |
| 1 | UNLABELLED | 489374 | 0 | 74769 |
| 1 | other-label | 688 | 0.00290698 | 261 |
| 1 | target | <100 | suppressed | suppressed |
| 2 | UNLABELLED | 490054 | 0 | 75060 |
| 2 | other-label | 356 | 0.0168539 | 228 |
| 2 | target | <100 | suppressed | suppressed |
| 3 | UNLABELLED | 489929 | 0 | 74889 |
| 3 | other-label | 185 | 0 | 183 |
| 3 | target | <100 | suppressed | suppressed |
| 4 | UNLABELLED | 489882 | 0 | 75135 |
| 4 | other-label | 183 | 0 | 177 |
| 4 | target | <100 | suppressed | suppressed |
| 5 | UNLABELLED | 489997 | 0 | 74708 |
| 5 | other-label | 193 | 0 | 187 |
| 5 | target | <100 | suppressed | suppressed |
| 6 | UNLABELLED | 490087 | 0 | 75008 |
| 6 | other-label | 213 | 0 | 210 |
| 6 | target | <100 | suppressed | suppressed |
| 7 | UNLABELLED | 488663 | 0 | 74889 |
| 7 | other-label | 198 | 0 | 192 |
| 7 | target | <100 | suppressed | suppressed |
| 8 | UNLABELLED | 490661 | 0 | 75031 |
| 8 | other-label | 189 | 0 | 188 |
| 8 | target | <100 | suppressed | suppressed |
| 9 | UNLABELLED | 489903 | 0 | 75070 |
| 9 | other-label | 194 | 0 | 192 |
| 9 | target | <100 | suppressed | suppressed |

## Predeclared coverage decision and uncertainty

| rows | senders | row_coverage | sender_mean_coverage | sender_bootstrap_low | sender_bootstrap_high | all_success_sender_lower_97_5 | largest_sender_share | receivers | receiver_mean_coverage | largest_receiver_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 367 | 100 | 1 | 1 | 1 | 1 | 0.963783 | 0.013624 | 100 | 1 | 0.013624 |

Unlabelled signature share: 0.00000000. Decision: PASS.
Joint acceptance: row and equal-sender coverage >=95%; exact one-sided 97.5% lower bound
for an all-success sender >=90%; unlabelled signature share <=0.1%.
Two co-primary signatures use Bonferroni allocation (0.025 each) for the sender bound.
Bootstrap intervals are descriptive; all-success samples yield degenerate intervals.
Shared receivers/banks/text prevent a claim of globally independent entity replication.
