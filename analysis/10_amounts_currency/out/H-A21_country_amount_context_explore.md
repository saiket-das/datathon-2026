# H-A21: Country context in log payment amounts

Phase explore. Freeze exploration only. Pre-July bit-0 fit, selected July score. Phase0 and A01-A20 exposure applies.
Country effects are simple training residual averages after a currency/party mean. Both fitted countries required.
No causal, wealth or original implementation interpretation is assigned.

Scoped July / currency-party fits / sender-country fits / receiver-country fits: (749066, 144, 126, 185).

## Same-row predictive metrics

| n | senders | receivers | baseline_mse | send_mse_ratio | receive_mse_ratio | wrong_mse_ratio | additive_mse_ratio | baseline_bias | additive_bias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 705162 | 76955 | 263424 | 4.62439 | 0.96097 | 0.994971 | 1.274787 | 0.965367 | 0.003075 | -0.002021 |

## Party controls

| parties | n | senders | receivers | additive_mse_ratio |
| --- | --- | --- | --- | --- |
| BB | 158089 | 23759 | 61819 | 0.962674 |
| BC | 403029 | 37558 | 154961 | 0.964256 |
| CB | 38758 | 15059 | 19384 | 0.968736 |
| CC | 105286 | 29220 | 52024 | 0.972612 |

## Equal-sender predictive metrics

| sender_groups | baseline_mse | send_mse_ratio | receiver_mse_ratio | wrong_mse_ratio |
| --- | --- | --- | --- | --- |
| 76955 | 4.858428 | 0.966796 | 1.001085 | 1.112163 |

## Bank-cluster sensitivity

| statistic | low99 | high99 |
| --- | --- | --- |
| row model/baseline | 0.9387276475580912 | 0.9795154407835022 |
| row model/receiver | 0.9466423807578181 | 0.9806520679228271 |
| equal-sender model/baseline | 0.9541989772001729 | 0.9781596167519787 |

## Decision

| ordering_banks | shared_training_banks | all_criteria_met |
| --- | --- | --- |
| 5301 | 5196 | True |
