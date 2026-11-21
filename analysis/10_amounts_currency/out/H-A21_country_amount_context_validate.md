# H-A21: Country context in log payment amounts

Phase validate. Freeze b82670542b97fa295cf719d7cd48a978af035f55. Pre-July bit-0 fit, selected July score. Phase0 and A01-A20 exposure applies.
Country effects are simple training residual averages after a currency/party mean. Both fitted countries required.
No causal, wealth or original implementation interpretation is assigned.

Scoped July / currency-party fits / sender-country fits / receiver-country fits: (699603, 144, 126, 185).

## Same-row predictive metrics

| n | senders | receivers | baseline_mse | send_mse_ratio | receive_mse_ratio | wrong_mse_ratio | additive_mse_ratio | baseline_bias | additive_bias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 656546 | 75374 | 255885 | 4.575395 | 0.975232 | 1.000448 | 1.315288 | 0.976804 | 0.010433 | -0.014365 |

## Party controls

| parties | n | senders | receivers | additive_mse_ratio |
| --- | --- | --- | --- | --- |
| BB | 147571 | 23272 | 61117 | 0.980408 |
| BC | 382257 | 37081 | 152100 | 0.978568 |
| CB | 33010 | 14420 | 17950 | 0.962832 |
| CC | 93708 | 28470 | 48225 | 0.969008 |

## Equal-sender predictive metrics

| sender_groups | baseline_mse | send_mse_ratio | receiver_mse_ratio | wrong_mse_ratio |
| --- | --- | --- | --- | --- |
| 75374 | 4.836638 | 0.96973 | 1.001069 | 1.113042 |

## Bank-cluster sensitivity

| statistic | low99 | high99 |
| --- | --- | --- |
| row model/baseline | 0.9654608230515028 | 0.9844825433471801 |
| row model/receiver | 0.9650730152777861 | 0.9840964969857502 |
| equal-sender model/baseline | 0.9582151128035318 | 0.9795330455403463 |

## Decision

| ordering_banks | shared_training_banks | all_criteria_met |
| --- | --- | --- |
| 5228 | 4045 | False |
