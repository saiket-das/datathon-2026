# H-B01_bank_additive_duration: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 2GB; two threads; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% ordering-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Exploration-only training

| training_rows | model_banks | banks_support_ge100 | negative_effects_support_ge100 | iterations |
| --- | --- | --- | --- | --- |
| 1417991 | 6534 | 1844 | 240 | 45 |

## Coverage and support (no identifiers)

| group | n | eligible_n | eligible_share | senders | receivers | banks | largest_bank_share |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Covered | 82502 | 65661 | 0.795872 | 20981 | 41734 | 1813 | 0.099355 |
| Direct | 1417991 | 1336003 | 0.942180 | 119970 | 473684 | 3819 | 0.018207 |
| Indirect | 744759 | 586358 | 0.787312 | 88433 | 282987 | 3515 | 0.010480 |

## Primary: unlabelled eligible non-Direct

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 652019 | 80711 | 250366 | 2165 | 0.982510 | 157.024975 | 98.513758 | 3.835815 | 0.017338 |

## Route comparison (Direct exploration is in-sample)

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Covered | 65661 | 17317 | 34037 | 1229 | 0.963154 | 236.004644 | 179.552162 | 32.565393 | 0.036440 |
| Direct | 1336003 | 111609 | 443939 | 2476 | 0.993079 | 89.719846 | 43.586703 | -0.033453 | 0.006913 |
| Indirect | 586358 | 75138 | 229577 | 2105 | 0.984853 | 145.536247 | 89.438990 | 0.618645 | 0.015020 |

## Primary 99% bank-cluster sensitivity intervals

| statistic | low | high |
| --- | --- | --- |
| R2 | 0.978636 | 0.985843 |
| MSE ratio | 0.014166 | 0.020934 |
| bias seconds | -5.051396 | 11.130565 |

## Equal ordering-bank weighting

| clusters | mse_ratio | mean_bank_bias |
| --- | --- | --- |
| 2165 | 0.012559 | 13.114705 |

## Frozen primary decision

| pass | eligible_share | r2_floor | mse_ratio_ceiling | absolute_bias_ceiling |
| --- | --- | --- | --- | --- |
| True | 0.788166 | 0.950000 | 0.100000 | 60 |

## Predeclared sensitivity: Party pair

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BB | 148319 | 24877 | 60122 | 1737 | 0.982684 | 155.755377 | 97.970089 | 4.572529 | 0.017101 |
| BC | 366497 | 37713 | 144372 | 1964 | 0.981990 | 158.300170 | 99.571313 | 2.447863 | 0.017835 |
| CB | 39151 | 16500 | 19871 | 1412 | 0.983829 | 155.497569 | 97.102996 | 8.933917 | 0.016084 |
| CC | 98052 | 30331 | 49345 | 1579 | 0.983554 | 154.742237 | 95.946535 | 5.873668 | 0.016417 |

## Predeclared sensitivity: Gap presence

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 574859 | 75881 | 226138 | 2117 | 0.982747 | 155.454637 | 97.330586 | 4.395436 | 0.017100 |
| true | 77160 | 25026 | 43997 | 1690 | 0.980809 | 168.263651 | 107.328649 | -0.333492 | 0.019023 |

## Predeclared sensitivity: FX count

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 17030 | 6420 | 10612 | 867 | 0.982998 | 150.556740 | 93.695437 | -1.473560 | 0.016792 |
| 1 | 106894 | 27764 | 55532 | 1688 | 0.982670 | 146.163703 | 90.820267 | -0.647250 | 0.017017 |
| 2 | 373479 | 62306 | 160519 | 1988 | 0.985407 | 140.798756 | 85.806664 | 10.382451 | 0.014471 |
| 3 | 154616 | 38316 | 78399 | 1775 | 0.976196 | 197.042545 | 135.057692 | -8.293590 | 0.023231 |

## Predeclared sensitivity: Visible banks

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 438000 | 66468 | 181646 | 2027 | 0.986236 | 134.175528 | 81.332500 | 10.840793 | 0.013636 |
| 4 | 144088 | 36071 | 73632 | 1772 | 0.979188 | 177.021640 | 118.762739 | -3.688397 | 0.020369 |
| 5 | 46904 | 18299 | 29059 | 1613 | 0.972603 | 213.230786 | 151.323052 | -17.889459 | 0.026379 |
| 6 | 23027 | 11380 | 16017 | 1480 | 0.964670 | 258.905407 | 191.048129 | -38.072808 | 0.033240 |

## Predeclared sensitivity: Endpoint agreement

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 52884 | 20679 | 32670 | 2102 | 0.977464 | 162.692957 | 103.475647 | 0.402850 | 0.021439 |
| true | 599135 | 76289 | 231941 | 1601 | 0.982859 | 156.514820 | 98.075786 | 4.138833 | 0.017028 |

## Predeclared sensitivity: Calendar month

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-04 | 451 | 404 | 437 | 211 | 0.978301 | 178.510596 | 109.328252 | -3.639362 | 0.021965 |
| 2023-05 | 198578 | 43414 | 95802 | 1843 | 0.982473 | 157.005161 | 98.580449 | 3.636875 | 0.017368 |
| 2023-06 | 264355 | 50919 | 120503 | 1873 | 0.982731 | 156.644780 | 98.248961 | 3.978361 | 0.017139 |
| 2023-07 | 188635 | 42004 | 91699 | 1841 | 0.982244 | 157.522325 | 98.788786 | 3.863346 | 0.017579 |

## Labelled payments pooled (descriptive sensitivity only)

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 434 | 276 | 261 | 211 | 0.992438 | 131.901303 | 83.752017 | 24.196486 | 0.007069 |

## Drop largest sending account (sensitivity)

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 649099 | 80710 | 249748 | 2165 | 0.982534 | 157.090706 | 98.536311 | 3.780596 | 0.017321 |

## Eligible population identity and path-bank support

| n | distinct_rows | senders | receivers | banks |
| --- | --- | --- | --- | --- |
| 652019 | 652019 | 80711 | 250366 | 2165 |

## Eligible visible path banks shared with training

| shared_path_banks |
| --- |
| 1844 |

## Eligible population overlap with unlabelled exploration (explore phase overlaps itself)

| row_ids | either_role_accounts | endpoint_banks | visible_path_banks |
| --- | --- | --- | --- |
| 652019 | 289341 | 2349 | 1844 |
