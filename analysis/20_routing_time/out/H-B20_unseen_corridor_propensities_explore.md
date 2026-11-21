# H-B20_unseen_corridor_propensities: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 512MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% separate origin- or receiver-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Record coverage

| cohort | corridors | payments | mixed_corridors | pure_repeat_corridors |
| --- | --- | --- | --- | --- |
| May training | 84121 | 239427 | 0 | 31420 |
| Score month | 100498 | 318693 | 0 | 39655 |

## Previously unseen corridor coverage

| novel_repeated_corridors | payments | without_role_support |
| --- | --- | --- |
| 8283 | 19957 | 2796 |

## Equal corridor comparisons

| n | payments | banks | receivers | covered_share | global_p | origin_p | receiver_p | country_p | combined_p | global_brier | origin_brier | receiver_brier | country_brier | combined_brier | payment_weighted_combined | payment_weighted_origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5487 | 13459 | 437 | 759 | 0.029707 | 0.048359 | 0.038606 | 0.043035 | 0.047835 | 0.033930 | 0.029172 | 0.025279 | 0.029314 | 0.029254 | 0.025765 | 0.029152 | 0.028432 |

## Origin calibration

| probability_band | n | banks | receivers | predicted_share | observed_share |
| --- | --- | --- | --- | --- | --- |
| suppressed | 1078 | suppressed | suppressed | suppressed | suppressed |
| 1–5% | 3741 | 285 | 731 | 0.024374 | 0.017108 |
| suppressed | 228 | suppressed | suppressed | suppressed | suppressed |
| suppressed | 440 | suppressed | suppressed | suppressed | suppressed |

## Bank resampling sensitivity

| cluster_role | clusters | global_low99 | receiver_low99 | country_low99 | combined_low99 | global_high99 | receiver_high99 | country_high99 | combined_high99 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Origin bank | 437 | 0.038272 | 0.039446 | 0.050926 | -0.013314 | 0.228712 | 0.235136 | 0.231307 | 0.041691 |
| Receiver bank | 759 | 0.070316 | 0.071732 | 0.071118 | -0.010253 | 0.191786 | 0.194858 | 0.192546 | 0.047246 |

## Secondary both-bank lift over origin only

| cluster_role | low99 | high99 |
| --- | --- | --- |
| Origin bank | -0.043505 | 0.013139 |
| Receiver bank | -0.049589 | 0.010149 |

## Frozen decision

| all_criteria_met |
| --- |
| True |
