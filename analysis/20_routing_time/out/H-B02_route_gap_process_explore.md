# H-B02_route_gap_process: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 2GB; two threads; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% ordering-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Unlabelled population support and fixed event estimates

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 2245252 | 144821 | 682154 | 3948 | 0.349848 | 0.049865 | 0.600288 | 0.099729 | 0.076621 | 0.005956 |

## Frozen primary statistics and 99% bank-cluster sensitivity intervals

| statistic | estimate | low | high |
| --- | --- | --- | --- |
| visible_event | 0.349848 | 0.349222 | 0.350445 |
| gap_event | 0.049865 | 0.049597 | 0.050137 |
| finish_event | 0.600288 | 0.599640 | 0.600996 |
| covered_given_multibank | 0.099729 | 0.065434 | 0.139413 |
| joint_TV | 0.000571 | 0.000394 | 0.001464 |
| TV_ratio_to_independence | 0.016913 | 0.011648 | 0.044436 |

## Frozen primary decision

| pass | TV_ceiling | TV_ratio_ceiling | clusters |
| --- | --- | --- | --- |
| True | 0.010000 | 0.500000 | 3948 |

## Joint count distribution; fixed law versus independence baseline

| cell | n | observed_share | fixed_model_share | independent_baseline_share |
| --- | --- | --- | --- | --- |
| V=2; G=0 | 1347263 | 0.600050 | 0.600000 | 0.583161 |
| V=2; G=1 | 67206 | 0.029932 | 0.030000 | 0.044629 |
| V=2; G=2+ | 3522 | 0.001569 | 0.001579 | 0.003761 |
| V=3; G=0 | 471921 | 0.210186 | 0.210000 | 0.214883 |
| V=3; G=1 | 46737 | 0.020816 | 0.021000 | 0.016445 |
| V=3; G=2+ | 3843 | 0.001712 | 0.001687 | 0.001386 |
| V=4; G=0 | 165593 | 0.073753 | 0.073500 | 0.079381 |
| V=4; G=1 | 24699 | 0.011001 | 0.011025 | 0.006075 |
| V=4; G=2+ | 2728 | 0.001215 | 0.001202 | 0.000512 |
| V=5; G=0 | 57647 | 0.025675 | 0.025725 | 0.029052 |
| V=5; G=1 | 11399 | 0.005077 | 0.005145 | 0.002223 |
| V=5; G=2+ | 1595 | 0.000710 | 0.000714 | 0.000187 |
| V=6; G=0 | 20058 | 0.008934 | 0.009004 | 0.010721 |
| V=6; G=1 | 5123 | 0.002282 | 0.002251 | 0.000820 |
| V=6; G=2+ | 888 | 0.000396 | 0.000381 | 0.000069 |
| V=7+; G=0 | 10737 | 0.004782 | 0.004848 | 0.006181 |
| V=7+; G=1 | 3497 | 0.001558 | 0.001585 | 0.000473 |
| V=7+; G=2+ | 796 | 0.000355 | 0.000355 | 0.000040 |

## Structural exceptions and concentration

| n | endpoint_gaps | visible_count_mismatch | direct_mismatch | adjacent_placeholder_paths | largest_ordering_bank_share | largest_sender_share |
| --- | --- | --- | --- | --- | --- | --- |
| 2245252 | 0 | 0 | 0 | 8989 | 0.018223 | 0.004224 |

## Equal ordering-bank weighting

| clusters | visible_event | gap_event | finish_event |
| --- | --- | --- | --- |
| 3948 | 0.321223 | 0.047162 | 0.631615 |

## Equal ordering-bank weighting; >=100 unlabelled payments

| clusters | visible_event | gap_event | finish_event |
| --- | --- | --- | --- |
| 1528 | 0.349287 | 0.049931 | 0.600782 |

## Predeclared sensitivity (composition may differ): Party pair

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BB | 508624 | 45205 | 163269 | 3387 | 0.349948 | 0.049856 | 0.600197 | 0.101111 | 0.076764 | 0.005847 |
| BC | 1260659 | 63808 | 392096 | 3769 | 0.349888 | 0.049695 | 0.600417 | 0.102874 | 0.076330 | 0.005925 |
| CB | 135599 | 37549 | 55351 | 2284 | 0.350117 | 0.050036 | 0.599847 | 0.093160 | 0.076815 | 0.006150 |
| CC | 340370 | 62262 | 136199 | 2544 | 0.349441 | 0.050438 | 0.600121 | 0.088623 | 0.077407 | 0.006152 |

## Predeclared sensitivity (composition may differ): Route

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Covered | 82502 | 20981 | 41734 | 1813 | 0.581754 | 0.049827 | 0.368419 | 1.000000 | 0.121924 | 0.012157 |
| Direct | 1417991 | 119970 | 473684 | 3819 | 0.000000 | 0.049871 | 0.950129 | None | 0.049879 | 0.002484 |
| Indirect | 744759 | 88433 | 282987 | 3515 | 0.582161 | 0.049864 | 0.367975 | 0.000000 | 0.122517 | 0.011879 |

## Predeclared sensitivity (composition may differ): Calendar month

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-04 | 1542 | 1166 | 1408 | 447 | 0.343984 | 0.047732 | 0.608284 | 0.100870 | 0.072633 | 0.004540 |
| 2023-05 | 684385 | 86383 | 264572 | 3535 | 0.349818 | 0.049969 | 0.600212 | 0.099876 | 0.076742 | 0.005997 |
| 2023-06 | 908657 | 98783 | 332353 | 3638 | 0.350225 | 0.049729 | 0.600045 | 0.099940 | 0.076405 | 0.005986 |
| 2023-07 | 650668 | 84156 | 254069 | 3504 | 0.349364 | 0.049948 | 0.600688 | 0.099276 | 0.076804 | 0.005874 |

## Predeclared sensitivity (composition may differ): File block

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 224628 | 48711 | 107598 | 3045 | 0.350989 | 0.050150 | 0.598861 | 0.097861 | 0.077212 | 0.006077 |
| 1 | 224358 | 48245 | 107396 | 3050 | 0.347733 | 0.049551 | 0.602716 | 0.099547 | 0.075696 | 0.006084 |
| 2 | 225158 | 48635 | 107738 | 3091 | 0.350207 | 0.050050 | 0.599743 | 0.100544 | 0.076928 | 0.005996 |
| 3 | 224535 | 48456 | 107420 | 3071 | 0.350427 | 0.049557 | 0.600016 | 0.099832 | 0.076153 | 0.005946 |
| 4 | 223835 | 48313 | 107379 | 3059 | 0.347684 | 0.049709 | 0.602608 | 0.097613 | 0.076302 | 0.005750 |
| 5 | 224714 | 48489 | 107619 | 3081 | 0.349844 | 0.050413 | 0.599743 | 0.101307 | 0.077454 | 0.005994 |
| 6 | 224395 | 48546 | 107179 | 3064 | 0.350093 | 0.050388 | 0.599519 | 0.100240 | 0.077662 | 0.005945 |
| 7 | 224615 | 48819 | 107134 | 3032 | 0.351400 | 0.049494 | 0.599106 | 0.100115 | 0.076268 | 0.005837 |
| 8 | 223892 | 48226 | 107228 | 3057 | 0.350411 | 0.049957 | 0.599633 | 0.100179 | 0.076783 | 0.005985 |
| 9 | 225122 | 48390 | 107735 | 3057 | 0.349656 | 0.049373 | 0.600971 | 0.100035 | 0.075750 | 0.005943 |

## Predeclared sensitivity (composition may differ): Endpoint agreement

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 220010 | 49504 | 108348 | 3131 | 0.350149 | 0.049245 | 0.600607 | 0.106483 | 0.075837 | 0.005686 |
| true | 2025242 | 137364 | 621299 | 3851 | 0.349815 | 0.049932 | 0.600253 | 0.098995 | 0.076706 | 0.005985 |

## Predeclared sensitivity (composition may differ): FX count

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 233628 | 31570 | 90566 | 2326 | 0.082827 | 0.050124 | 0.867049 | 0.132013 | 0.054681 | 0.002996 |
| 1 | 1330398 | 118269 | 448801 | 3767 | 0.090982 | 0.049758 | 0.859260 | 0.089499 | 0.054710 | 0.003020 |
| 2 | 455185 | 72017 | 191558 | 3367 | 0.510116 | 0.049769 | 0.440115 | 0.101324 | 0.103967 | 0.008449 |
| 3 | 226041 | 49530 | 108726 | 3077 | 0.695450 | 0.050084 | 0.254466 | 0.099349 | 0.173190 | 0.021270 |

## Labelled payments pooled (descriptive sensitivity only)

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 1729 | 1008 | 880 | 525 | 0.329619 | 0.048886 | 0.621495 | 0.026230 | 0.077501 | 0.001157 |

## Drop largest sending account (sensitivity)

| group | n | senders | receivers | banks | visible_event | gap_event | finish_event | covered_given_multibank | gap_path_share | multiple_gap_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 2235769 | 144820 | 680799 | 3948 | 0.349841 | 0.049860 | 0.600299 | 0.099986 | 0.076618 | 0.005950 |

## Eligible source coverage

| n | unlabelled_n | labelled_n | distinct_rows |
| --- | --- | --- | --- |
| 2246981 | 2245252 | 1729 | 2246981 |

## Unlabelled population overlap with exploration (explore phase overlaps itself)

| row_ids | either_role_accounts | endpoint_banks | visible_path_banks |
| --- | --- | --- | --- |
| 2245252 | 739625 | 4156 | 7543 |
