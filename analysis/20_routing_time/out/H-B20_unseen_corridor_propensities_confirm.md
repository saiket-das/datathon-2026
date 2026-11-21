# H-B20_unseen_corridor_propensities: confirm

Freeze: af07496a8a81d970bbb30531c1a4f484ec03fa55.
DuckDB 2.0.0; 512MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% separate origin- or receiver-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Record coverage

| cohort | corridors | payments | mixed_corridors | pure_repeat_corridors |
| --- | --- | --- | --- | --- |
| May training | 84121 | 239427 | 0 | 31420 |
| Score month | 81372 | 227489 | 0 | 30112 |

## Previously unseen corridor coverage

| novel_repeated_corridors | payments | without_role_support |
| --- | --- | --- |
| 5008 | 11581 | 1624 |

## Equal corridor comparisons

| n | payments | banks | receivers | covered_share | global_p | origin_p | receiver_p | country_p | combined_p | global_brier | origin_brier | receiver_brier | country_brier | combined_brier | payment_weighted_combined | payment_weighted_origin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3384 | 7907 | 408 | 732 | 0.030142 | 0.048359 | 0.040149 | 0.043324 | 0.048402 | 0.035459 | 0.029565 | 0.025336 | 0.029831 | 0.029426 | 0.026256 | 0.029176 | 0.028138 |

## Origin calibration

| probability_band | n | banks | receivers | predicted_share | observed_share |
| --- | --- | --- | --- | --- | --- |
| suppressed | 680 | suppressed | suppressed | suppressed | suppressed |
| 1–5% | 2280 | 271 | 676 | 0.023891 | 0.012719 |
| suppressed | 165 | suppressed | suppressed | suppressed | suppressed |
| suppressed | 259 | suppressed | suppressed | suppressed | suppressed |

## Bank resampling sensitivity

| cluster_role | clusters | global_low99 | receiver_low99 | country_low99 | combined_low99 | global_high99 | receiver_high99 | country_high99 | combined_high99 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Origin bank | 408 | 0.060051 | 0.063726 | 0.069590 | -0.020334 | 0.252618 | 0.258743 | 0.243960 | 0.073884 |
| Receiver bank | 732 | 0.058150 | 0.062267 | 0.053773 | -0.008141 | 0.217489 | 0.228490 | 0.208981 | 0.080015 |

## Secondary both-bank lift over origin only

| cluster_role | low99 | high99 |
| --- | --- | --- |
| Origin bank | -0.079778 | 0.019928 |
| Receiver bank | -0.086975 | 0.008075 |

## Frozen decision

| all_criteria_met |
| --- |
| True |
