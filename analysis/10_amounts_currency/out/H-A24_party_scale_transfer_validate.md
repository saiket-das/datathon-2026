# H-A24 — Party-specific scale extraction

Freeze: 559bdce5a72fd02708fd4249c683df3fb956d086.
512MB; one thread; no disk spill. Aggregates only.
Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Date support and scale comparison

| currency | dates | min_consumer_base | max_consumer_base | near_equal | large_ratio | minimum_ratio | maximum_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHF | 10 | 1000.0 | 1000.0 | 1.0 | 0.0 | 0.9999962233221907 | 1.0000038589058033 |
| EUR | 73 | 1000.0 | 10000.0 | 0.9863013698630136 | 0.0136986301369863 | 0.20000013793840704 | 1.0000040695811794 |
| GBP | 3 | 1000.0 | 1000.0 | 1.0 | 0.0 | 0.9999962142721938 | 1.0000028859590497 |
| USD | 55 | 1000.0 | 10000.0 | 1.0 | 0.0 | 1.0 | 1.0 |

## Common support by scored party pair

| currency | pair | n | senders | receivers | dates | business_fit | consumer_fit | different_fit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHF | BC | 3599 | 629 | 2885 | 10 | 0.42428452347874407 | 0.4245623784384551 | 0.0002778549597110308 |
| CHF | CC | 2791 | 578 | 2291 | 10 | 0.3862414905051953 | 0.3862414905051953 | 0.0 |
| EUR | BB | 9896 | 4416 | 6530 | 73 | 0.4413904607922393 | 0.440784155214228 | 0.0014147130153597412 |
| EUR | BC | 105595 | 15468 | 51619 | 73 | 0.4078507505090203 | 0.40722572091481607 | 0.0010417159903404517 |
| EUR | CB | 10948 | 5754 | 7072 | 73 | 0.40372670807453415 | 0.40272195834855684 | 0.001370113262696383 |
| EUR | CC | 62041 | 16288 | 32643 | 73 | 0.392675811157138 | 0.3918860108637836 | 0.0009832207733595525 |
| GBP | BC | 1546 | 654 | 1330 | 3 | 0.4055627425614489 | 0.4055627425614489 | 0.0 |
| USD | BB | 3162 | 2050 | 2445 | 55 | 0.43801391524351674 | 0.43801391524351674 | 0.0 |
| USD | BC | 35510 | 8958 | 21591 | 55 | 0.4086172909039707 | 0.4086172909039707 | 0.0 |
| USD | CB | 3991 | 2800 | 2891 | 55 | 0.4076672513154598 | 0.4076672513154598 | 0.0 |
| USD | CC | 23403 | 10497 | 15014 | 55 | 0.38627526385506133 | 0.38627526385506133 | 0.0 |

## Small-amount coverage

| currency | scoped | covered |
| --- | --- | --- |
| CHF | 39893 | 6905 |
| EUR | 200142 | 188480 |
| GBP | 48215 | 2777 |
| USD | 85304 | 66066 |

## EUR paired date-block sensitivity

| pair | n | disagreement | low99 | high99 | pass |
| --- | --- | --- | --- | --- | --- |
| BB | 9896 | 0.0014147130153597412 | 0.0 | 0.00434462375998513 | False |
| BC | 105595 | 0.0010417159903404517 | 5.159913911838014e-05 | 0.0037699053359072626 | False |
| CB | 10948 | 0.001370113262696383 | 0.0 | 0.00499462646004473 | False |
| CC | 62041 | 0.0009832207733595525 | 1.5113317151276567e-05 | 0.003881018661617595 | False |

## EUR primary decision

| all_criteria_met |
| --- |
| False |

B and C training groups have separate source records but share dates and currencies. Unknown latent denomination can multiply a modal scale. Own-date cent tolerance uses each trained anchor's magnitude. No hypothesis acceptance follows from compatibility alone.
