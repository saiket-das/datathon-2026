# H-B02_route_gap_process: confirm

Freeze: 0607592078394baacf5454c6a1737916ea9b84c6.
DuckDB 2.0.0; 2GB; two threads; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% ordering-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Unlabelled population support and fixed event estimates

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 2730400 | 151586 | 784772 | 3990 | 0.349351 | 0.050133 | 0.600515 | 0.122243 | 0.077084 | 0.005943 |

## Frozen primary statistics and 99% bank-cluster sensitivity intervals

| statistic | estimate | low | high |
| --- | --- | --- | --- |
| visible_event | 0.349351 | 0.348792 | 0.349862 |
| gap_event | 0.050133 | 0.049894 | 0.050374 |
| finish_event | 0.600515 | 0.599938 | 0.601102 |
| covered_given_multibank | 0.122243 | 0.073593 | 0.185989 |
| joint_TV | 0.000967 | 0.000424 | 0.001778 |
| TV_ratio_to_independence | 0.027911 | 0.012471 | 0.050228 |

## Frozen primary decision

| pass | TV_ceiling | TV_ratio_ceiling | clusters |
| --- | --- | --- | --- |
| True | 0.010000 | 0.500000 | 3990 |

## Joint count distribution; fixed law versus independence baseline

| cell | n | observed_share | fixed_model_share | independent_baseline_share |
| --- | --- | --- | --- | --- |
| V=2; G=0 | 1640079 | 0.600674 | 0.600000 | 0.583161 |
| V=2; G=1 | 82290 | 0.030138 | 0.030000 | 0.044629 |
| V=2; G=2+ | 4305 | 0.001577 | 0.001579 | 0.003761 |
| V=3; G=0 | 572018 | 0.209500 | 0.210000 | 0.214883 |
| V=3; G=1 | 57426 | 0.021032 | 0.021000 | 0.016445 |
| V=3; G=2+ | 4572 | 0.001674 | 0.001687 | 0.001386 |
| V=4; G=0 | 200426 | 0.073405 | 0.073500 | 0.079381 |
| V=4; G=1 | 30173 | 0.011051 | 0.011025 | 0.006075 |
| V=4; G=2+ | 3393 | 0.001243 | 0.001202 | 0.000512 |
| V=5; G=0 | 69796 | 0.025563 | 0.025725 | 0.029052 |
| V=5; G=1 | 13837 | 0.005068 | 0.005145 | 0.002223 |
| V=5; G=2+ | 1993 | 0.000730 | 0.000714 | 0.000187 |
| V=6; G=0 | 24518 | 0.008980 | 0.009004 | 0.010721 |
| V=6; G=1 | 6087 | 0.002229 | 0.002251 | 0.000820 |
| V=6; G=2+ | 989 | 0.000362 | 0.000381 | 0.000069 |
| V=7+; G=0 | 13093 | 0.004795 | 0.004848 | 0.006181 |
| V=7+; G=1 | 4430 | 0.001622 | 0.001585 | 0.000473 |
| V=7+; G=2+ | 975 | 0.000357 | 0.000355 | 0.000040 |

## Structural exceptions and concentration

| n | endpoint_gaps | visible_count_mismatch | direct_mismatch | adjacent_placeholder_paths | largest_ordering_bank_share | largest_sender_share |
| --- | --- | --- | --- | --- | --- | --- |
| 2730400 | 0 | 0 | 0 | 10826 | 0.029638 | 0.014582 |

## Equal ordering-bank weighting

| clusters | visible_event | gap_event | finish_event |
| --- | --- | --- | --- |
| 3990 | 0.323900 | 0.048449 | 0.627651 |

## Equal ordering-bank weighting; >=100 unlabelled payments

| clusters | visible_event | gap_event | finish_event |
| --- | --- | --- | --- |
| 1623 | 0.347858 | 0.050370 | 0.601772 |

## Predeclared sensitivity (composition may differ): Party pair

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BB | 624767 | 46002 | 186905 | 3472 | 0.349307 | 0.050198 | 0.600495 | 0.119078 | 0.077102 | 0.006031 |
| BC | 1530497 | 63498 | 451666 | 3840 | 0.349347 | 0.050029 | 0.600624 | 0.121900 | 0.076957 | 0.005880 |
| CB | 167418 | 43578 | 65490 | 2296 | 0.350019 | 0.050278 | 0.599703 | 0.125180 | 0.077447 | 0.005955 |
| CC | 407718 | 69094 | 155605 | 2520 | 0.349162 | 0.050367 | 0.600471 | 0.127172 | 0.077382 | 0.006038 |

## Predeclared sensitivity (composition may differ): Route

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Covered | 122698 | 19088 | 55786 | 1845 | 0.581840 | 0.049842 | 0.368318 | 1.000000 | 0.122496 | 0.011850 |
| Direct | 1726674 | 127044 | 546293 | 3860 | 0.000000 | 0.050126 | 0.949874 | None | 0.050151 | 0.002493 |
| Indirect | 881028 | 96972 | 321402 | 3609 | 0.582088 | 0.050180 | 0.367732 | 0.000000 | 0.123543 | 0.011882 |

## Predeclared sensitivity (composition may differ): Calendar month

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-04 | 1467 | 1172 | 1335 | 437 | 0.353108 | 0.050792 | 0.596099 | 0.090416 | 0.077028 | 0.007498 |
| 2023-05 | 830371 | 92563 | 304453 | 3621 | 0.349596 | 0.050021 | 0.600382 | 0.122954 | 0.076956 | 0.005933 |
| 2023-06 | 1106209 | 105328 | 383535 | 3695 | 0.348856 | 0.050099 | 0.601045 | 0.122409 | 0.077017 | 0.005894 |
| 2023-07 | 792353 | 90670 | 293109 | 3555 | 0.349778 | 0.050298 | 0.599924 | 0.121325 | 0.077312 | 0.006019 |

## Predeclared sensitivity (composition may differ): File block

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 272190 | 53209 | 123813 | 3095 | 0.350123 | 0.049981 | 0.599896 | 0.122989 | 0.076799 | 0.006014 |
| 1 | 273071 | 53028 | 124204 | 3118 | 0.349601 | 0.050459 | 0.599940 | 0.121757 | 0.077332 | 0.006306 |
| 2 | 273068 | 53225 | 124169 | 3158 | 0.348719 | 0.050229 | 0.601052 | 0.122996 | 0.077204 | 0.005911 |
| 3 | 273279 | 53161 | 124582 | 3101 | 0.349716 | 0.049252 | 0.601032 | 0.121965 | 0.075681 | 0.005782 |
| 4 | 272860 | 52938 | 124004 | 3127 | 0.349242 | 0.050472 | 0.600286 | 0.120655 | 0.077633 | 0.005985 |
| 5 | 273761 | 53195 | 124464 | 3144 | 0.350671 | 0.050146 | 0.599184 | 0.122445 | 0.077345 | 0.005972 |
| 6 | 273452 | 53228 | 124215 | 3118 | 0.349443 | 0.049891 | 0.600666 | 0.121816 | 0.076796 | 0.005844 |
| 7 | 273065 | 53331 | 124408 | 3139 | 0.348399 | 0.050098 | 0.601503 | 0.123212 | 0.076872 | 0.005936 |
| 8 | 272920 | 53190 | 123866 | 3128 | 0.348798 | 0.049966 | 0.601237 | 0.122294 | 0.076707 | 0.005925 |
| 9 | 272734 | 53376 | 123952 | 3139 | 0.348794 | 0.050841 | 0.600365 | 0.122306 | 0.078472 | 0.005757 |

## Predeclared sensitivity (composition may differ): Endpoint agreement

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 267717 | 53402 | 125583 | 3175 | 0.349579 | 0.050027 | 0.600394 | 0.118115 | 0.077040 | 0.005838 |
| true | 2462683 | 144607 | 715113 | 3875 | 0.349327 | 0.050145 | 0.600528 | 0.122690 | 0.077089 | 0.005954 |

## Predeclared sensitivity (composition may differ): FX count

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 300861 | 33972 | 109259 | 2436 | 0.082972 | 0.050253 | 0.866775 | 0.164015 | 0.054816 | 0.002985 |
| 1 | 1609134 | 126455 | 514494 | 3832 | 0.093614 | 0.050051 | 0.856335 | 0.122746 | 0.055261 | 0.003017 |
| 2 | 548178 | 77326 | 219914 | 3445 | 0.510762 | 0.050262 | 0.438976 | 0.121814 | 0.105466 | 0.008477 |
| 3 | 272227 | 54036 | 124539 | 3106 | 0.695919 | 0.050090 | 0.253990 | 0.118831 | 0.173539 | 0.021405 |

## Labelled payments pooled (descriptive sensitivity only)

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 1747 | 1061 | 960 | 537 | 0.358342 | 0.043165 | 0.598493 | 0.069697 | 0.059531 | 0.008014 |

## Drop largest sending account (sensitivity)

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 2690584 | 151585 | 776895 | 3990 | 0.349396 | 0.050147 | 0.600457 | 0.114913 | 0.077120 | 0.005940 |

## Eligible source coverage

| n | unlabelled_n | labelled_n | distinct_rows |
| --- | --- | --- | --- |
| 2732147 | 2730400 | 1747 | 2732147 |

## Unlabelled population overlap with exploration (explore phase overlaps itself)

| row_ids | either_role_accounts | endpoint_banks | visible_path_banks |
| --- | --- | --- | --- |
| 0 | 11558 | 0 | 6708 |
