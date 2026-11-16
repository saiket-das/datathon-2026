# H-C02_romance_bursts: explore

DuckDB 2.0.0; 2GB; one thread; UTC; no disk spill.
Freeze: `not yet frozen; discovery only`.
Sender MD5 parity split; whole sender clusters retained. Phase 0 full-data exposure applies.
No bank/time repartition is an independent holdout. Unlabelled does not mean legitimate.
Cohorts below 100 rows are suppressed; entity counts below 100 are masked.

## Partition and six-label baseline

| label | n | senders | receivers | amount_median | duration_median | business_sender_share | business_receiver_share |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACCOUNT_REPLACEMENT_SCAM | 337 | 321 | 284 | 3693.39 | 525 | 0.777448 | 0.305638 |
| CEO_SCAM | 480 | 449 | 378 | 25376.4 | 694 | 1 | 0.247917 |
| CUSTOMER_RECALL | 162 | 154 | 160 | 3561.81 | 84.5 | 0.777778 | 0.271605 |
| DUPLICATE_PAYMENT | 312 | <100 | <100 | 2259.02 | 54 | 0.75641 | 0.246795 |
| FAT_FINGER_MISTAKE | 947 | 839 | 912 | 296596 | 50 | 0.801478 | 0.275607 |
| ROMANCE_SCAM | 1322 | 264 | 230 | 103.26 | 1268 | 0 | 0.274584 |
| UNLABELLED | 5094378 | 196047 | 1481991 | 3611 | 55 | 0.781728 | 0.287922 |

## Broad repeat comparator without source-order or context conditions

| label | n | repeated_rows | repeat_share | median_family_size |
| --- | --- | --- | --- | --- |
| ACCOUNT_REPLACEMENT_SCAM | 337 | 0 | 0 | 1 |
| CEO_SCAM | 480 | 1 | 0.00208333 | 1 |
| CUSTOMER_RECALL | 162 | 39 | 0.240741 | 1 |
| DUPLICATE_PAYMENT | 312 | 312 | 1 | 4 |
| FAT_FINGER_MISTAKE | 947 | 222 | 0.234424 | 1 |
| ROMANCE_SCAM | 1322 | 1322 | 1 | 6 |
| UNLABELLED | 5094378 | 1240388 | 0.243482 | 1 |

## Signature against every label (not a legitimacy classifier)

| label | n | hits | coverage | senders | receivers |
| --- | --- | --- | --- | --- | --- |
| ACCOUNT_REPLACEMENT_SCAM | 337 | 0 | 0 | 321 | 284 |
| CEO_SCAM | 480 | 0 | 0 | 449 | 378 |
| CUSTOMER_RECALL | 162 | 0 | 0 | 154 | 160 |
| DUPLICATE_PAYMENT | 312 | 0 | 0 | <100 | <100 |
| FAT_FINGER_MISTAKE | 947 | 0 | 0 | 839 | 912 |
| ROMANCE_SCAM | 1322 | 1322 | 1 | 264 | 230 |
| UNLABELLED | 5094378 | 0 | 0 | 196047 | 1481991 |

## Candidate-family structure; target label used only for assessment

| label | n | families | target_rows | signature_rows | fully_labelled_family_share | smallest_family | largest_family | median_span | max_span | fixed_context_share | monotone_share | median_family_growth | mean_family_backwards_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| other | 1528 | <100 | 0 | 0 | 0 | 2 | 541 | 4727.5 | 7809552 | 0.755556 | 0.166667 | 1 | 0.467683 |
| target-containing | 1322 | 264 | 1322 | 1322 | 1 | 2 | 8 | 1060.5 | 3812 | 1 | 1 | 1.4954 | 0 |

## Party-pair control

| stratum | label | n | coverage | senders |
| --- | --- | --- | --- | --- |
| BB | UNLABELLED | 1145078 | 0 | 60516 |
| BB | other-label | 509 | 0 | 436 |
| BC | UNLABELLED | 2837342 | 0 | 80162 |
| BC | other-label | 1354 | 0 | 1049 |
| CB | UNLABELLED | 321703 | 0 | 60850 |
| CB | other-label | <100 | suppressed | suppressed |
| CB | target | 363 | 1 | <100 |
| CC | UNLABELLED | 790255 | 0 | 93800 |
| CC | other-label | 280 | 0 | 215 |
| CC | target | 959 | 1 | 190 |

## Calendar sensitivity within the same sender split

| stratum | label | n | coverage | senders |
| --- | --- | --- | --- | --- |
| 2023-04 | UNLABELLED | 3133 | 0 | 2196 |
| 2023-04 | other-label | <100 | suppressed | suppressed |
| 2023-05 | UNLABELLED | 1550245 | 0 | 125891 |
| 2023-05 | other-label | 663 | 0 | 553 |
| 2023-05 | target | 364 | 1 | <100 |
| 2023-06 | UNLABELLED | 2063597 | 0 | 141128 |
| 2023-06 | other-label | 901 | 0 | 729 |
| 2023-06 | target | 554 | 1 | 108 |
| 2023-07 | UNLABELLED | 1477403 | 0 | 123284 |
| 2023-07 | other-label | 671 | 0 | 551 |
| 2023-07 | target | 404 | 1 | <100 |

## Source-file block sensitivity (zero-based million-row blocks)

| stratum | label | n | coverage | senders |
| --- | --- | --- | --- | --- |
| 0 | UNLABELLED | 508473 | 0 | 75628 |
| 0 | other-label | 203 | 0 | 181 |
| 0 | target | 536 | 1 | 108 |
| 1 | UNLABELLED | 509102 | 0 | 75053 |
| 1 | other-label | 221 | 0 | 186 |
| 1 | target | 557 | 1 | 109 |
| 2 | UNLABELLED | 509081 | 0 | 75451 |
| 2 | other-label | 234 | 0 | 195 |
| 2 | target | 229 | 1 | <100 |
| 3 | UNLABELLED | 509652 | 0 | 75172 |
| 3 | other-label | 215 | 0 | 178 |
| 4 | UNLABELLED | 509665 | 0 | 75090 |
| 4 | other-label | 237 | 0 | 212 |
| 5 | UNLABELLED | 509565 | 0 | 75243 |
| 5 | other-label | 218 | 0 | 193 |
| 6 | UNLABELLED | 509439 | 0 | 75373 |
| 6 | other-label | 234 | 0 | 197 |
| 7 | UNLABELLED | 510898 | 0 | 75568 |
| 7 | other-label | 200 | 0 | 183 |
| 8 | UNLABELLED | 508862 | 0 | 75244 |
| 8 | other-label | 235 | 0 | 190 |
| 9 | UNLABELLED | 509641 | 0 | 75437 |
| 9 | other-label | 241 | 0 | 214 |

## Predeclared coverage decision and uncertainty

| rows | senders | row_coverage | sender_mean_coverage | sender_bootstrap_low | sender_bootstrap_high | all_success_sender_lower_97_5 | largest_sender_share |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1322 | 264 | 1 | 1 | 1 | 1 | 0.986124 | 0.00605144 |

Unlabelled signature share: 0.00000000. Decision: PASS.
Joint acceptance: row and equal-sender coverage >=95%; exact one-sided 97.5% lower bound
for an all-success sender >=90%; unlabelled signature share <=0.1%.
Two co-primary signatures use Bonferroni allocation (0.025 each) for the sender bound.
Bootstrap intervals are descriptive; all-success samples yield degenerate intervals.
Shared receivers/banks/text prevent a claim of globally independent entity replication.
