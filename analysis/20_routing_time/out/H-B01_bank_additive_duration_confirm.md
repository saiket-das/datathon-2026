# H-B01_bank_additive_duration: confirm

Freeze: 0607592078394baacf5454c6a1737916ea9b84c6.
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
| Covered | 122698 | 64856 | 0.528582 | 19088 | 55786 | 1845 | 0.149073 |
| Direct | 1726674 | 720884 | 0.417499 | 127044 | 546293 | 3860 | 0.029647 |
| Indirect | 881028 | 285426 | 0.323969 | 96972 | 321402 | 3609 | 0.012987 |

## Primary: unlabelled eligible non-Direct

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 350282 | 42080 | 131367 | 1854 | 0.900205 | 182.755311 | 122.487919 | -11.651668 | 0.044379 |

## Route comparison (Direct exploration is in-sample)

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Covered | 64856 | 9717 | 29575 | 859 | 0.817138 | 240.852300 | 179.586101 | -57.344310 | 0.089233 |
| Direct | 720884 | 59214 | 232679 | 2291 | 0.757934 | 132.586331 | 76.470415 | -8.426893 | 0.046760 |
| Indirect | 285426 | 39637 | 112995 | 1772 | 0.917564 | 166.755557 | 109.513769 | -1.269145 | 0.035840 |

## Primary 99% bank-cluster sensitivity intervals

| statistic | low | high |
| --- | --- | --- |
| R2 | 0.880433 | 0.920206 |
| MSE ratio | 0.033854 | 0.055850 |
| bias seconds | -24.598693 | 1.033643 |

## Equal ordering-bank weighting

| clusters | mse_ratio | mean_bank_bias |
| --- | --- | --- |
| 1854 | 0.034037 | -3.096197 |

## Frozen primary decision

| pass | eligible_share | r2_floor | mse_ratio_ceiling | absolute_bias_ceiling |
| --- | --- | --- | --- | --- |
| False | 0.348982 | 0.950000 | 0.100000 | 60 |

## Predeclared sensitivity: Party pair

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BB | 82077 | 12888 | 31764 | 1063 | 0.901245 | 180.933015 | 121.098123 | -10.511474 | 0.043295 |
| BC | 197340 | 18795 | 76756 | 1506 | 0.901146 | 182.070720 | 122.422772 | -10.978326 | 0.044080 |
| CB | 20989 | 9102 | 10359 | 568 | 0.896556 | 185.784438 | 123.105632 | -14.406398 | 0.046062 |
| CC | 49876 | 16112 | 24927 | 844 | 0.896327 | 187.105686 | 124.772809 | -15.032894 | 0.046659 |

## Predeclared sensitivity: Gap presence

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 308542 | 39519 | 118680 | 1785 | 0.898966 | 181.361750 | 121.437145 | -11.227188 | 0.044348 |
| true | 41740 | 12763 | 23256 | 801 | 0.907281 | 192.744253 | 130.255240 | -14.789422 | 0.044587 |

## Predeclared sensitivity: FX count

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 9917 | 3914 | 6234 | 396 | 0.848969 | 189.270729 | 127.143555 | -30.405445 | 0.058749 |
| 1 | 61907 | 15319 | 30990 | 933 | 0.856597 | 187.201331 | 125.511145 | -21.281380 | 0.056360 |
| 2 | 196611 | 31735 | 83328 | 1565 | 0.900772 | 164.891192 | 108.373674 | -3.753790 | 0.040748 |
| 3 | 81847 | 19363 | 40764 | 1122 | 0.912423 | 216.287258 | 153.542044 | -21.067799 | 0.043564 |

## Predeclared sensitivity: Visible banks

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 235229 | 34430 | 95531 | 1636 | 0.891432 | 162.642094 | 106.843306 | -5.223405 | 0.042625 |
| 4 | 77469 | 18610 | 38655 | 1102 | 0.901765 | 201.089206 | 140.683476 | -18.112487 | 0.045239 |
| 5 | 25223 | 9360 | 15272 | 626 | 0.897736 | 235.010088 | 170.595249 | -31.863558 | 0.048729 |
| 6 | 12361 | 5739 | 8376 | 449 | 0.909962 | 277.401398 | 208.003970 | -52.246779 | 0.048026 |

## Predeclared sensitivity: Endpoint agreement

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false | 42125 | 16351 | 25277 | 1854 | 0.951495 | 174.451066 | 115.052121 | -6.316863 | 0.034229 |
| true | 308157 | 34554 | 115418 | 177 | 0.884209 | 183.861362 | 123.504391 | -12.380935 | 0.046060 |

## Predeclared sensitivity: Calendar month

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-04 | 190 | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed |
| 2023-05 | 106899 | 22174 | 50427 | 1257 | 0.898770 | 183.749036 | 123.309549 | -12.109404 | 0.044929 |
| 2023-06 | 141482 | 26186 | 63242 | 1345 | 0.900725 | 181.632554 | 121.936016 | -10.725443 | 0.043873 |
| 2023-07 | 101711 | 21871 | 48355 | 1235 | 0.900991 | 183.294388 | 122.408977 | -12.473838 | 0.044522 |

## Labelled payments pooled (descriptive sensitivity only)

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 150 | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed |

## Drop largest sending account (sensitivity)

| group | n | senders | receivers | banks | r2 | rmse | mae | bias | mse_ratio_to_route_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 342335 | 42079 | 129391 | 1854 | 0.902438 | 180.876716 | 120.804461 | -10.082726 | 0.043245 |

## Eligible population identity and path-bank support

| n | distinct_rows | senders | receivers | banks |
| --- | --- | --- | --- | --- |
| 350282 | 350282 | 42080 | 131367 | 1854 |

## Eligible visible path banks shared with training

| shared_path_banks |
| --- |
| 1827 |

## Eligible population overlap with unlabelled exploration (explore phase overlaps itself)

| row_ids | either_role_accounts | endpoint_banks | visible_path_banks |
| --- | --- | --- | --- |
| 0 | 2164 | 0 | 1827 |
