# H-A07: Currency exceptions

Exploration only. Both-account bit-0 July; modes trained pre-July on bit-0.
Only rows where both endpoint-country maps are supported enter this conditional screen.
Phase 0, Round 1 and A03-A06 exposure applies. This is new exploratory conditioning.

## Coverage and receiver alternative

| n | senders | receivers | matches_receiver | matches_receiver_sendertrained | usd_or_eur |
| --- | --- | --- | --- | --- | --- |
| 49548 | 20435 | 29718 | 27531 | 28220 | 40252 |

## Residual currencies with broad entity support

| currency | n | senders | receivers | receiver_match_share | receiver_sendertrained_share |
| --- | --- | --- | --- | --- | --- |
| EUR | 27778 | 13326 | 17675 | 0.988336 | 0.610051 |
| USD | 12474 | 6716 | 9151 | 0.005932 | 0.532949 |
| GBP | 3195 | 2320 | 2269 | 0.000313 | 0.639124 |
| CHF | 1651 | 1409 | 1246 | 0.001211 | 0.569958 |
| CNY | 1176 | 939 | 1112 | 0.0 | 0.534864 |

## Route and shared endpoint-mode controls

| route | same_endpoint_mode | n | senders | receivers | receiver_match_share | receiver_sendertrained_share | usd_or_eur_share |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Covered | False | 2197 | 1292 | 1887 | 0.614929 | 0.395084 | 0.85025 |
| Direct | False | 21880 | 10957 | 14631 | 0.641179 | 0.730439 | 0.861974 |
| Direct | True | 3099 | 1871 | 2631 | 0.0 | 0.645692 | 0.56373 |
| Indirect | False | 19253 | 10191 | 13501 | 0.631122 | 0.429336 | 0.835298 |
| Indirect | True | 2718 | 1700 | 2333 | 0.0 | 0.359088 | 0.546726 |
