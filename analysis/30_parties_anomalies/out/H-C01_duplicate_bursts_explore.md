# H-C01_duplicate_bursts: explore

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
| CEO_SCAM | 480 | 0 | 0 | 1 |
| CUSTOMER_RECALL | 162 | 0 | 0 | 1 |
| DUPLICATE_PAYMENT | 312 | 312 | 1 | 4 |
| FAT_FINGER_MISTAKE | 947 | 0 | 0 | 1 |
| ROMANCE_SCAM | 1322 | 10 | 0.0075643 | 1 |
| UNLABELLED | 5094378 | 3040 | 0.000596736 | 1 |

## Signature against every label (not a legitimacy classifier)

| label | n | hits | coverage | senders | receivers |
| --- | --- | --- | --- | --- | --- |
| ACCOUNT_REPLACEMENT_SCAM | 337 | 0 | 0 | 321 | 284 |
| CEO_SCAM | 480 | 0 | 0 | 449 | 378 |
| CUSTOMER_RECALL | 162 | 0 | 0 | 154 | 160 |
| DUPLICATE_PAYMENT | 312 | 312 | 1 | <100 | <100 |
| FAT_FINGER_MISTAKE | 947 | 0 | 0 | 839 | 912 |
| ROMANCE_SCAM | 1322 | 8 | 0.00605144 | 264 | 230 |
| UNLABELLED | 5094378 | 0 | 0 | 196047 | 1481991 |

## Candidate-family structure; target label used only for assessment

| label | n | families | target_rows | signature_rows | fully_labelled_family_share | smallest_family | largest_family | median_span | max_span | fixed_context_share | monotone_share | median_family_growth | mean_family_backwards_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| other | <100 | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed |
| target-containing | 312 | <100 | 312 | 312 | 1 | 2 | 5 | 3959 | 7043 | 1 | 0.188235 | 1 | 0.478431 |

## Party-pair control

| stratum | label | n | coverage | senders |
| --- | --- | --- | --- | --- |
| BB | UNLABELLED | 1145078 | 0 | 60516 |
| BB | other-label | 451 | 0 | 420 |
| BB | target | <100 | suppressed | suppressed |
| BC | UNLABELLED | 2837342 | 0 | 80162 |
| BC | other-label | 1176 | 0 | 1014 |
| BC | target | 178 | 1 | <100 |
| CB | UNLABELLED | 321703 | 0 | 60850 |
| CB | other-label | 439 | 0.00911162 | 149 |
| CB | target | <100 | suppressed | suppressed |
| CC | UNLABELLED | 790255 | 0 | 93800 |
| CC | other-label | 1182 | 0.00338409 | 393 |
| CC | target | <100 | suppressed | suppressed |

## Calendar sensitivity within the same sender split

| stratum | label | n | coverage | senders |
| --- | --- | --- | --- | --- |
| 2023-04 | UNLABELLED | 3133 | 0 | 2196 |
| 2023-04 | other-label | <100 | suppressed | suppressed |
| 2023-05 | UNLABELLED | 1550245 | 0 | 125891 |
| 2023-05 | other-label | 945 | 0 | 611 |
| 2023-05 | target | <100 | suppressed | suppressed |
| 2023-06 | UNLABELLED | 2063597 | 0 | 141128 |
| 2023-06 | other-label | 1318 | 0.00151745 | 802 |
| 2023-06 | target | 137 | 1 | <100 |
| 2023-07 | UNLABELLED | 1477403 | 0 | 123284 |
| 2023-07 | other-label | 982 | 0.00610998 | 609 |
| 2023-07 | target | <100 | suppressed | suppressed |

## Source-file block sensitivity (zero-based million-row blocks)

| stratum | label | n | coverage | senders |
| --- | --- | --- | --- | --- |
| 0 | UNLABELLED | 508473 | 0 | 75628 |
| 0 | other-label | 717 | 0.0055788 | 282 |
| 0 | target | <100 | suppressed | suppressed |
| 1 | UNLABELLED | 509102 | 0 | 75053 |
| 1 | other-label | 737 | 0.00542741 | 286 |
| 1 | target | <100 | suppressed | suppressed |
| 2 | UNLABELLED | 509081 | 0 | 75451 |
| 2 | other-label | 417 | 0 | 230 |
| 2 | target | <100 | suppressed | suppressed |
| 3 | UNLABELLED | 509652 | 0 | 75172 |
| 3 | other-label | 187 | 0 | 172 |
| 3 | target | <100 | suppressed | suppressed |
| 4 | UNLABELLED | 509665 | 0 | 75090 |
| 4 | other-label | 209 | 0 | 203 |
| 4 | target | <100 | suppressed | suppressed |
| 5 | UNLABELLED | 509565 | 0 | 75243 |
| 5 | other-label | 191 | 0 | 186 |
| 5 | target | <100 | suppressed | suppressed |
| 6 | UNLABELLED | 509439 | 0 | 75373 |
| 6 | other-label | 200 | 0 | 189 |
| 6 | target | <100 | suppressed | suppressed |
| 7 | UNLABELLED | 510898 | 0 | 75568 |
| 7 | other-label | 190 | 0 | 181 |
| 7 | target | <100 | suppressed | suppressed |
| 8 | UNLABELLED | 508862 | 0 | 75244 |
| 8 | other-label | 186 | 0 | 178 |
| 8 | target | <100 | suppressed | suppressed |
| 9 | UNLABELLED | 509641 | 0 | 75437 |
| 9 | other-label | 214 | 0 | 208 |
| 9 | target | <100 | suppressed | suppressed |

## Predeclared coverage decision and uncertainty

| rows | senders | row_coverage | sender_mean_coverage | sender_bootstrap_low | sender_bootstrap_high | all_success_sender_lower_97_5 | largest_sender_share |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 312 | <100 | 1 | 1 | 1 | 1 | 0.956529 | 0.025641 |

Unlabelled signature share: 0.00000000. Decision: PASS.
Joint acceptance: row and equal-sender coverage >=95%; exact one-sided 97.5% lower bound
for an all-success sender >=90%; unlabelled signature share <=0.1%.
Two co-primary signatures use Bonferroni allocation (0.025 each) for the sender bound.
Bootstrap intervals are descriptive; all-success samples yield degenerate intervals.
Shared receivers/banks/text prevent a claim of globally independent entity replication.
