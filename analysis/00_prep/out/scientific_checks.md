# Scientific foundation: executed aggregate checks

Run: `uv run python analysis/00_prep/scientific_checks.py`

DuckDB 2.0.0; 2GB memory limit; two threads; UTC; no disk spill.
Measurements are full-data descriptions, not independent confirmation or causal rules.
Subgroups with fewer than 100 records are suppressed; small entity-support counts are masked.

## Source coverage

| records | distinct_row_ids | missing_required | start_utc | end_utc |
| --- | --- | --- | --- | --- |
| 10000000 | 10000000 | 0 | 2023-04-30 11:22:26 | 2023-07-31 09:56:01 |

## Structural counts (whole dataset)

| records | helper_path_bad | helper_gap_bad | helper_time_bad | helper_country_bad | participants_vs_entries | participants_vs_visible | direct_iff_two_bad | continuity_bad | fx_exceeds_links | fx_vs_country_changes | fx_exceeds_country_changes | ordering_endpoint_mismatch | beneficiary_endpoint_mismatch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10000000 | 0 | 0 | 0 | 0 | 767204 | 0 | 0 | 0 | 0 | 1209536 | 0 | 498399 | 499265 |

## Account consistency: ORDERING

| accounts | reused_accounts | multi_type | multi_bank |
| --- | --- | --- | --- |
| 391132 | 260873 | 0 | 0 |

## Visible details to tokens: ORDERING

| inconsistent_detail_groups | affected_rows |
| --- | --- |
| 324 | 3274 |

## Account consistency: BENEFICIARY

| accounts | reused_accounts | multi_type | multi_bank |
| --- | --- | --- | --- |
| 2590877 | 567583 | 0 | 61606 |

## Visible details to tokens: BENEFICIARY

| inconsistent_detail_groups | affected_rows |
| --- | --- |
| 41432 | 317832 |

## Cross-role identity consistency

| identifiers_in_both_roles | type_disagreement | bank_disagreement |
| --- | --- | --- |
| 253120 | 127584 | 984 |

## sender: coverage and baseline stability

| split | n | pct | amount_median | duration_median | business_sender_share | direct_share |
| --- | --- | --- | --- | --- | --- | --- |
| confirm | 4902062 | 49.0206 | 3717.62 | 57.0 | 0.793616 | 0.63211 |
| excluded | 0 | suppressed | suppressed | suppressed | suppressed | suppressed |
| explore | 5097938 | 50.9794 | 3610.3 | 55.0 | 0.781548 | 0.632538 |

## sender: overlap audit

| row_ids | sender_ids | account_ids_either_role | endpoint_bank_ids | visible_path_bank_ids |
| --- | --- | --- | --- | --- |
| 0 | 0 | 388309 | 7838 | 8017 |

## sender: anomaly support (all label values allowlisted)

| split | label | n | senders | receivers | support |
| --- | --- | --- | --- | --- | --- |
| confirm | ACCOUNT_REPLACEMENT_SCAM | 312 | 301 | 253 | displayable; power not assessed |
| excluded | ACCOUNT_REPLACEMENT_SCAM | 0 | suppressed | suppressed | absent |
| explore | ACCOUNT_REPLACEMENT_SCAM | 337 | 321 | 284 | displayable; power not assessed |
| confirm | CEO_SCAM | 465 | 442 | 367 | displayable; power not assessed |
| excluded | CEO_SCAM | 0 | suppressed | suppressed | absent |
| explore | CEO_SCAM | 480 | 449 | 378 | displayable; power not assessed |
| confirm | CUSTOMER_RECALL | 155 | 152 | 152 | displayable; power not assessed |
| excluded | CUSTOMER_RECALL | 0 | suppressed | suppressed | absent |
| explore | CUSTOMER_RECALL | 162 | 154 | 160 | displayable; power not assessed |
| confirm | DUPLICATE_PAYMENT | 367 | 100 | 100 | displayable; power not assessed |
| excluded | DUPLICATE_PAYMENT | 0 | suppressed | suppressed | absent |
| explore | DUPLICATE_PAYMENT | 312 | <100 | <100 | limited |
| confirm | FAT_FINGER_MISTAKE | 993 | 901 | 958 | displayable; power not assessed |
| excluded | FAT_FINGER_MISTAKE | 0 | suppressed | suppressed | absent |
| explore | FAT_FINGER_MISTAKE | 947 | 839 | 912 | displayable; power not assessed |
| confirm | OTHER_LABEL | 0 | suppressed | suppressed | absent |
| excluded | OTHER_LABEL | 0 | suppressed | suppressed | absent |
| explore | OTHER_LABEL | 0 | suppressed | suppressed | absent |
| confirm | ROMANCE_SCAM | 1154 | 236 | 200 | displayable; power not assessed |
| excluded | ROMANCE_SCAM | 0 | suppressed | suppressed | absent |
| explore | ROMANCE_SCAM | 1322 | 264 | 230 | displayable; power not assessed |
| confirm | UNLABELLED | 4898616 | 194678 | 1449040 | displayable; power not assessed |
| excluded | UNLABELLED | 0 | suppressed | suppressed | absent |
| explore | UNLABELLED | 5094378 | 196047 | 1481991 | displayable; power not assessed |

## sender: composition distance for CURRENCY_CODE

| total_variation |
| --- |
| 0.050678 |

## sender: composition distance for TRANSACTION_TYPE_CODE

| total_variation |
| --- |
| 0.003202 |

## sender: composition distance for ORDERING_TYPE||BENEFICIARY_TYPE

| total_variation |
| --- |
| 0.012068 |

## sender: stability by strftime(ts_utc,'%Y-%m')

| split | block | n | amount_median | labelled |
| --- | --- | --- | --- | --- |
| confirm | 2023-04 | 3025 | 2944.9 | 0 |
| explore | 2023-04 | 3136 | 2850.13 | <100 |
| confirm | 2023-05 | 1493128 | 3719.36 | 1071 |
| explore | 2023-05 | 1551272 | 3593.64 | 1027 |
| confirm | 2023-06 | 1985108 | 3721.66 | 1323 |
| explore | 2023-06 | 2065052 | 3620.53 | 1455 |
| confirm | 2023-07 | 1420801 | 3712.47 | 1052 |
| explore | 2023-07 | 1478478 | 3615.21 | 1075 |

## sender: stability by (ROW_ID-1)//1000000

| split | block | n | amount_median | labelled |
| --- | --- | --- | --- | --- |
| confirm | 0 | 490788 | 3712.07 | 722 |
| explore | 0 | 509212 | 3595.23 | 739 |
| confirm | 1 | 490120 | 3700.38 | 746 |
| explore | 1 | 509880 | 3600.0 | 778 |
| confirm | 2 | 490456 | 3720.63 | 402 |
| explore | 2 | 509544 | 3593.94 | 463 |
| confirm | 3 | 490133 | 3701.17 | 204 |
| explore | 3 | 509867 | 3601.91 | 215 |
| confirm | 4 | 490098 | 3723.27 | 216 |
| explore | 4 | 509902 | 3623.68 | 237 |
| confirm | 5 | 490217 | 3725.27 | 220 |
| explore | 5 | 509783 | 3634.11 | 218 |
| confirm | 6 | 490327 | 3706.64 | 240 |
| explore | 6 | 509673 | 3631.27 | 234 |
| confirm | 7 | 488902 | 3745.26 | 239 |
| explore | 7 | 511098 | 3619.12 | 200 |
| confirm | 8 | 490903 | 3732.08 | 242 |
| explore | 8 | 509097 | 3594.75 | 235 |
| confirm | 9 | 490118 | 3710.81 | 215 |
| explore | 9 | 509882 | 3606.98 | 241 |

## accounts: coverage and baseline stability

| split | n | pct | amount_median | duration_median | business_sender_share | direct_share |
| --- | --- | --- | --- | --- | --- | --- |
| confirm | 2416730 | 24.1673 | 3692.41 | 58.0 | 0.793172 | 0.631887 |
| excluded | 5003327 | 50.0333 | 3671.76 | 56.0 | 0.787732 | 0.632548 |
| explore | 2579943 | 25.7994 | 3614.87 | 54.0 | 0.781597 | 0.632314 |

## accounts: overlap audit

| row_ids | sender_ids | account_ids_either_role | endpoint_bank_ids | visible_path_bank_ids |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 6873 | 7343 |

## accounts: anomaly support (all label values allowlisted)

| split | label | n | senders | receivers | support |
| --- | --- | --- | --- | --- | --- |
| confirm | ACCOUNT_REPLACEMENT_SCAM | 174 | 171 | 135 | displayable; power not assessed |
| excluded | ACCOUNT_REPLACEMENT_SCAM | 296 | 289 | 250 | displayable; power not assessed |
| explore | ACCOUNT_REPLACEMENT_SCAM | 179 | 170 | 152 | displayable; power not assessed |
| confirm | CEO_SCAM | 215 | 206 | 170 | displayable; power not assessed |
| excluded | CEO_SCAM | 497 | 480 | 385 | displayable; power not assessed |
| explore | CEO_SCAM | 233 | 223 | 190 | displayable; power not assessed |
| confirm | CUSTOMER_RECALL | <100 | suppressed | suppressed | limited |
| excluded | CUSTOMER_RECALL | 170 | 169 | 168 | displayable; power not assessed |
| explore | CUSTOMER_RECALL | <100 | suppressed | suppressed | limited |
| confirm | DUPLICATE_PAYMENT | 188 | <100 | <100 | limited |
| excluded | DUPLICATE_PAYMENT | 319 | <100 | <100 | limited |
| explore | DUPLICATE_PAYMENT | 172 | <100 | <100 | limited |
| confirm | FAT_FINGER_MISTAKE | 510 | 473 | 492 | displayable; power not assessed |
| excluded | FAT_FINGER_MISTAKE | 953 | 898 | 921 | displayable; power not assessed |
| explore | FAT_FINGER_MISTAKE | 477 | 445 | 457 | displayable; power not assessed |
| confirm | OTHER_LABEL | 0 | suppressed | suppressed | absent |
| excluded | OTHER_LABEL | 0 | suppressed | suppressed | absent |
| explore | OTHER_LABEL | 0 | suppressed | suppressed | absent |
| confirm | ROMANCE_SCAM | 547 | 115 | <100 | limited |
| excluded | ROMANCE_SCAM | 1287 | 255 | 211 | displayable; power not assessed |
| explore | ROMANCE_SCAM | 642 | 130 | 120 | displayable; power not assessed |
| confirm | UNLABELLED | 2415020 | 151189 | 724650 | displayable; power not assessed |
| excluded | UNLABELLED | 4999805 | 304594 | 1465244 | displayable; power not assessed |
| explore | UNLABELLED | 2578169 | 153991 | 741137 | displayable; power not assessed |

## accounts: composition distance for CURRENCY_CODE

| total_variation |
| --- |
| 0.053469 |

## accounts: composition distance for TRANSACTION_TYPE_CODE

| total_variation |
| --- |
| 0.003858 |

## accounts: composition distance for ORDERING_TYPE||BENEFICIARY_TYPE

| total_variation |
| --- |
| 0.011575 |

## accounts: stability by strftime(ts_utc,'%Y-%m')

| split | block | n | amount_median | labelled |
| --- | --- | --- | --- | --- |
| confirm | 2023-04 | 1507 | 2539.43 | 0 |
| excluded | 2023-04 | 3070 | 3098.89 | <100 |
| explore | 2023-04 | 1584 | 2881.14 | <100 |
| confirm | 2023-05 | 736596 | 3682.83 | 520 |
| excluded | 2023-05 | 1522847 | 3667.35 | 1047 |
| explore | 2023-05 | 784957 | 3604.72 | 531 |
| confirm | 2023-06 | 978481 | 3707.64 | 647 |
| excluded | 2023-06 | 2027852 | 3673.03 | 1399 |
| explore | 2023-06 | 1043827 | 3625.21 | 732 |
| confirm | 2023-07 | 700146 | 3682.06 | 543 |
| excluded | 2023-07 | 1449558 | 3676.7 | 1075 |
| explore | 2023-07 | 749575 | 3613.86 | 509 |

## accounts: stability by (ROW_ID-1)//1000000

| split | block | n | amount_median | labelled |
| --- | --- | --- | --- | --- |
| confirm | 0 | 241801 | 3711.0 | 350 |
| excluded | 0 | 500337 | 3656.06 | 727 |
| explore | 0 | 257862 | 3589.94 | 384 |
| confirm | 1 | 241876 | 3688.95 | 344 |
| excluded | 1 | 500420 | 3645.72 | 798 |
| explore | 1 | 257704 | 3615.96 | 382 |
| confirm | 2 | 241658 | 3701.48 | 241 |
| excluded | 2 | 500532 | 3653.09 | 430 |
| explore | 2 | 257810 | 3618.53 | 194 |
| confirm | 3 | 241988 | 3697.22 | <100 |
| excluded | 3 | 499944 | 3637.18 | 213 |
| explore | 3 | 258068 | 3634.11 | 109 |
| confirm | 4 | 241719 | 3700.0 | 113 |
| excluded | 4 | 500104 | 3678.33 | 214 |
| explore | 4 | 258177 | 3632.88 | 126 |
| confirm | 5 | 241115 | 3689.06 | 107 |
| excluded | 5 | 501047 | 3694.21 | 224 |
| explore | 5 | 257838 | 3636.8 | 107 |
| confirm | 6 | 241776 | 3674.11 | 109 |
| excluded | 6 | 500187 | 3682.4 | 230 |
| explore | 6 | 258037 | 3636.48 | 135 |
| confirm | 7 | 240884 | 3712.2 | 126 |
| excluded | 7 | 500168 | 3704.61 | 226 |
| explore | 7 | 258948 | 3595.2 | <100 |
| confirm | 8 | 242111 | 3691.97 | 113 |
| excluded | 8 | 500395 | 3681.74 | 234 |
| explore | 8 | 257494 | 3591.16 | 130 |
| confirm | 9 | 241802 | 3656.87 | 110 |
| excluded | 9 | 500193 | 3686.05 | 226 |
| explore | 9 | 258005 | 3595.23 | 120 |

## banks: coverage and baseline stability

| split | n | pct | amount_median | duration_median | business_sender_share | direct_share |
| --- | --- | --- | --- | --- | --- | --- |
| confirm | 2732147 | 27.3215 | 3777.21 | 58.0 | 0.789206 | 0.632382 |
| excluded | 5020872 | 50.2087 | 3651.93 | 55.0 | 0.786359 | 0.632641 |
| explore | 2246981 | 22.4698 | 3550.86 | 57.0 | 0.787813 | 0.631563 |

## banks: overlap audit

| row_ids | sender_ids | account_ids_either_role | endpoint_bank_ids | visible_path_bank_ids |
| --- | --- | --- | --- | --- |
| 0 | 0 | 11565 | 0 | 6709 |

## banks: anomaly support (all label values allowlisted)

| split | label | n | senders | receivers | support |
| --- | --- | --- | --- | --- | --- |
| confirm | ACCOUNT_REPLACEMENT_SCAM | 183 | 176 | 152 | displayable; power not assessed |
| excluded | ACCOUNT_REPLACEMENT_SCAM | 303 | 298 | 242 | displayable; power not assessed |
| explore | ACCOUNT_REPLACEMENT_SCAM | 163 | 158 | 135 | displayable; power not assessed |
| confirm | CEO_SCAM | 228 | 215 | 185 | displayable; power not assessed |
| excluded | CEO_SCAM | 486 | 469 | 380 | displayable; power not assessed |
| explore | CEO_SCAM | 231 | 223 | 177 | displayable; power not assessed |
| confirm | CUSTOMER_RECALL | <100 | suppressed | suppressed | limited |
| excluded | CUSTOMER_RECALL | 158 | 157 | 156 | displayable; power not assessed |
| explore | CUSTOMER_RECALL | <100 | suppressed | suppressed | limited |
| confirm | DUPLICATE_PAYMENT | 157 | <100 | <100 | limited |
| excluded | DUPLICATE_PAYMENT | 347 | <100 | <100 | limited |
| explore | DUPLICATE_PAYMENT | 175 | <100 | <100 | limited |
| confirm | FAT_FINGER_MISTAKE | 516 | 482 | 495 | displayable; power not assessed |
| excluded | FAT_FINGER_MISTAKE | 984 | 916 | 949 | displayable; power not assessed |
| explore | FAT_FINGER_MISTAKE | 440 | 419 | 426 | displayable; power not assessed |
| confirm | OTHER_LABEL | 0 | suppressed | suppressed | absent |
| excluded | OTHER_LABEL | 0 | suppressed | suppressed | absent |
| explore | OTHER_LABEL | 0 | suppressed | suppressed | absent |
| confirm | ROMANCE_SCAM | 585 | 115 | 103 | displayable; power not assessed |
| excluded | ROMANCE_SCAM | 1252 | 252 | 220 | displayable; power not assessed |
| explore | ROMANCE_SCAM | 639 | 133 | 116 | displayable; power not assessed |
| confirm | UNLABELLED | 2730400 | 151586 | 784772 | displayable; power not assessed |
| excluded | UNLABELLED | 5017342 | 302762 | 1465752 | displayable; power not assessed |
| explore | UNLABELLED | 2245252 | 144821 | 682154 | displayable; power not assessed |

## banks: composition distance for CURRENCY_CODE

| total_variation |
| --- |
| 0.143729 |

## banks: composition distance for TRANSACTION_TYPE_CODE

| total_variation |
| --- |
| 0.009021 |

## banks: composition distance for ORDERING_TYPE||BENEFICIARY_TYPE

| total_variation |
| --- |
| 0.003192 |

## banks: stability by strftime(ts_utc,'%Y-%m')

| split | block | n | amount_median | labelled |
| --- | --- | --- | --- | --- |
| confirm | 2023-04 | 1468 | 2893.07 | <100 |
| excluded | 2023-04 | 3150 | 2672.73 | <100 |
| explore | 2023-04 | 1543 | 3190.58 | <100 |
| confirm | 2023-05 | 830851 | 3753.51 | 480 |
| excluded | 2023-05 | 1528676 | 3637.92 | 1130 |
| explore | 2023-05 | 684873 | 3573.4 | 488 |
| confirm | 2023-06 | 1106950 | 3799.48 | 741 |
| excluded | 2023-06 | 2033825 | 3657.6 | 1309 |
| explore | 2023-06 | 909385 | 3549.03 | 728 |
| confirm | 2023-07 | 792878 | 3772.92 | 525 |
| excluded | 2023-07 | 1455221 | 3660.22 | 1090 |
| explore | 2023-07 | 651180 | 3533.4 | 512 |

## banks: stability by (ROW_ID-1)//1000000

| split | block | n | amount_median | labelled |
| --- | --- | --- | --- | --- |
| confirm | 0 | 272552 | 3779.75 | 362 |
| excluded | 0 | 502461 | 3630.66 | 740 |
| explore | 0 | 224987 | 3554.44 | 359 |
| confirm | 1 | 273451 | 3762.43 | 380 |
| excluded | 1 | 501818 | 3616.3 | 771 |
| explore | 1 | 224731 | 3592.93 | 373 |
| confirm | 2 | 273251 | 3796.35 | 183 |
| excluded | 2 | 501346 | 3639.81 | 437 |
| explore | 2 | 225403 | 3531.73 | 245 |
| confirm | 3 | 273372 | 3755.97 | <100 |
| excluded | 3 | 501978 | 3651.79 | 211 |
| explore | 3 | 224650 | 3532.02 | 115 |
| confirm | 4 | 272974 | 3766.28 | 114 |
| excluded | 4 | 503094 | 3659.6 | 242 |
| explore | 4 | 223932 | 3580.35 | <100 |
| confirm | 5 | 273894 | 3810.73 | 133 |
| excluded | 5 | 501289 | 3661.78 | 202 |
| explore | 5 | 224817 | 3558.5 | 103 |
| confirm | 6 | 273572 | 3785.56 | 120 |
| excluded | 6 | 501920 | 3674.31 | 241 |
| explore | 6 | 224508 | 3522.43 | 113 |
| confirm | 7 | 273185 | 3803.87 | 120 |
| excluded | 7 | 502093 | 3666.98 | 212 |
| explore | 7 | 224722 | 3556.89 | 107 |
| confirm | 8 | 273048 | 3776.09 | 128 |
| excluded | 8 | 502952 | 3653.88 | 241 |
| explore | 8 | 224000 | 3536.24 | 108 |
| confirm | 9 | 272848 | 3730.65 | 114 |
| excluded | 9 | 501921 | 3667.48 | 233 |
| explore | 9 | 225231 | 3545.42 | 109 |

## time: coverage and baseline stability

| split | n | pct | amount_median | duration_median | business_sender_share | direct_share |
| --- | --- | --- | --- | --- | --- | --- |
| confirm | 2896968 | 28.9697 | 3659.06 | 56.0 | 0.787323 | 0.632431 |
| excluded | 8472 | 0.0847 | 3295.69 | 51.0 | 0.789778 | 0.632436 |
| explore | 7094560 | 70.9456 | 3663.54 | 56.0 | 0.787518 | 0.632286 |

## time: overlap audit

| row_ids | sender_ids | account_ids_either_role | endpoint_bank_ids | visible_path_bank_ids |
| --- | --- | --- | --- | --- |
| 0 | 202503 | 461216 | 7958 | 8039 |

## time: anomaly support (all label values allowlisted)

| split | label | n | senders | receivers | support |
| --- | --- | --- | --- | --- | --- |
| confirm | ACCOUNT_REPLACEMENT_SCAM | 203 | 200 | 172 | displayable; power not assessed |
| excluded | ACCOUNT_REPLACEMENT_SCAM | 0 | suppressed | suppressed | absent |
| explore | ACCOUNT_REPLACEMENT_SCAM | 446 | 433 | 351 | displayable; power not assessed |
| confirm | CEO_SCAM | 263 | 256 | 223 | displayable; power not assessed |
| excluded | CEO_SCAM | <100 | suppressed | suppressed | limited |
| explore | CEO_SCAM | 681 | 645 | 501 | displayable; power not assessed |
| confirm | CUSTOMER_RECALL | <100 | suppressed | suppressed | limited |
| excluded | CUSTOMER_RECALL | 0 | suppressed | suppressed | absent |
| explore | CUSTOMER_RECALL | 228 | 223 | 224 | displayable; power not assessed |
| confirm | DUPLICATE_PAYMENT | 198 | <100 | <100 | limited |
| excluded | DUPLICATE_PAYMENT | 0 | suppressed | suppressed | absent |
| explore | DUPLICATE_PAYMENT | 481 | 133 | 133 | displayable; power not assessed |
| confirm | FAT_FINGER_MISTAKE | 587 | 552 | 568 | displayable; power not assessed |
| excluded | FAT_FINGER_MISTAKE | <100 | suppressed | suppressed | limited |
| explore | FAT_FINGER_MISTAKE | 1349 | 1242 | 1292 | displayable; power not assessed |
| confirm | OTHER_LABEL | 0 | suppressed | suppressed | absent |
| excluded | OTHER_LABEL | 0 | suppressed | suppressed | absent |
| explore | OTHER_LABEL | 0 | suppressed | suppressed | absent |
| confirm | ROMANCE_SCAM | 785 | 159 | 142 | displayable; power not assessed |
| excluded | ROMANCE_SCAM | 0 | suppressed | suppressed | absent |
| explore | ROMANCE_SCAM | 1691 | 341 | 282 | displayable; power not assessed |
| confirm | UNLABELLED | 2894843 | 245689 | 973785 | displayable; power not assessed |
| excluded | UNLABELLED | 8467 | 6165 | 7171 | displayable; power not assessed |
| explore | UNLABELLED | 7089684 | 347276 | 1979401 | displayable; power not assessed |

## time: composition distance for CURRENCY_CODE

| total_variation |
| --- |
| 0.002944 |

## time: composition distance for TRANSACTION_TYPE_CODE

| total_variation |
| --- |
| 0.000195 |

## time: composition distance for ORDERING_TYPE||BENEFICIARY_TYPE

| total_variation |
| --- |
| 0.000449 |

## time: stability by strftime(ts_utc,'%Y-%m')

| split | block | n | amount_median | labelled |
| --- | --- | --- | --- | --- |
| excluded | 2023-04 | 6161 | 2902.42 | <100 |
| explore | 2023-05 | 3044400 | 3655.02 | 2098 |
| explore | 2023-06 | 4050160 | 3669.88 | 2778 |
| confirm | 2023-07 | 2896968 | 3659.06 | 2125 |
| excluded | 2023-07 | 2311 | 5000.0 | <100 |

## time: stability by (ROW_ID-1)//1000000

| split | block | n | amount_median | labelled |
| --- | --- | --- | --- | --- |
| confirm | 0 | 289795 | 3667.36 | 454 |
| excluded | 0 | 893 | 3583.26 | <100 |
| explore | 0 | 709312 | 3643.78 | 1006 |
| confirm | 1 | 290286 | 3619.6 | 445 |
| excluded | 1 | 859 | 3118.11 | 0 |
| explore | 1 | 708855 | 3662.81 | 1079 |
| confirm | 2 | 289958 | 3632.0 | 254 |
| excluded | 2 | 849 | 3428.54 | 0 |
| explore | 2 | 709193 | 3665.73 | 611 |
| confirm | 3 | 289221 | 3650.0 | 159 |
| excluded | 3 | 831 | 3161.54 | <100 |
| explore | 3 | 709948 | 3652.45 | 257 |
| confirm | 4 | 289380 | 3669.5 | 132 |
| excluded | 4 | 864 | 3330.65 | 0 |
| explore | 4 | 709756 | 3672.6 | 321 |
| confirm | 5 | 290238 | 3718.79 | 136 |
| excluded | 5 | 826 | 3047.41 | <100 |
| explore | 5 | 708936 | 3662.26 | 301 |
| confirm | 6 | 289121 | 3644.02 | 145 |
| excluded | 6 | 846 | 3943.9 | 0 |
| explore | 6 | 710033 | 3676.74 | 329 |
| confirm | 7 | 289221 | 3661.2 | 120 |
| excluded | 7 | 822 | 3325.77 | 0 |
| explore | 7 | 709957 | 3687.16 | 319 |
| confirm | 8 | 290511 | 3673.94 | 144 |
| excluded | 8 | 879 | 3134.72 | 0 |
| explore | 8 | 708610 | 3655.29 | 333 |
| confirm | 9 | 289237 | 3661.25 | 136 |
| excluded | 9 | 803 | 3095.32 | 0 |
| explore | 9 | 709960 | 3654.07 | 320 |
