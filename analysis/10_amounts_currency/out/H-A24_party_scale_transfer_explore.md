# H-A24 — Party-specific scale extraction

Freeze: exploration only.
512MB; one thread; no disk spill. Aggregates only.
Unlabelled both-account bit-0 only. A01–A23 and Phase 0 outcome exposure applies.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Date support and scale comparison

| currency | dates | min_consumer_base | max_consumer_base | near_equal | large_ratio | minimum_ratio | maximum_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHF | 26 | 1000.0 | 10000.0 | 1.0 | 0.0 | 0.9999963100789799 | 1.000003937658983 |
| EUR | 71 | 1000.0 | 10000.0 | 1.0 | 0.0 | 0.9999956286446176 | 1.0000040695811794 |
| GBP | 14 | 1000.0 | 1000.0 | 1.0 | 0.0 | 0.9999962142721938 | 1.0000030196883682 |
| USD | 51 | 1000.0 | 10000.0 | 1.0 | 0.0 | 1.0 | 1.0 |

## Common support by scored party pair

| currency | pair | n | senders | receivers | dates | business_fit | consumer_fit | different_fit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHF | BC | 8889 | 1141 | 6307 | 26 | 0.4076949038137023 | 0.40803239959500504 | 0.0003374957813027337 |
| CHF | CB | 1036 | 375 | 809 | 26 | 0.4063706563706564 | 0.40733590733590735 | 0.0009652509652509653 |
| CHF | CC | 9035 | 1004 | 6227 | 26 | 0.39081350304371887 | 0.39092418372993915 | 0.00011068068622025456 |
| EUR | BB | 10046 | 4481 | 6300 | 71 | 0.43579534142942467 | 0.4359944256420466 | 0.00019908421262193908 |
| EUR | BC | 103806 | 15202 | 49360 | 71 | 0.40912856674951353 | 0.40921526694025395 | 8.670019074041963e-05 |
| EUR | CB | 11544 | 5974 | 7182 | 71 | 0.4095634095634096 | 0.40965003465003463 | 8.662508662508663e-05 |
| EUR | CC | 62545 | 16528 | 33036 | 71 | 0.3908705731873051 | 0.390902550163882 | 3.197697657686466e-05 |
| GBP | BB | 1043 | 418 | 851 | 14 | 0.4467881112176414 | 0.4467881112176414 | 0.0 |
| GBP | BC | 10754 | 1633 | 7410 | 14 | 0.41947182443741865 | 0.41993676771433885 | 0.00046494327692021576 |
| GBP | CB | 1011 | 552 | 849 | 14 | 0.40158259149357073 | 0.40158259149357073 | 0.0 |
| GBP | CC | 5048 | 1815 | 3926 | 14 | 0.38252773375594296 | 0.3829239302694136 | 0.0003961965134706815 |
| USD | BB | 3297 | 2080 | 2471 | 51 | 0.4346375492872308 | 0.4346375492872308 | 0.0 |
| USD | BC | 36329 | 8637 | 21435 | 51 | 0.4101681851963996 | 0.4101681851963996 | 0.0 |
| USD | CB | 3820 | 2787 | 2852 | 51 | 0.4028795811518325 | 0.4028795811518325 | 0.0 |
| USD | CC | 23344 | 10245 | 14564 | 51 | 0.38669465387251545 | 0.38669465387251545 | 0.0 |

## Small-amount coverage

| currency | scoped | covered |
| --- | --- | --- |
| CHF | 45646 | 19507 |
| EUR | 201796 | 187941 |
| GBP | 72198 | 17856 |
| USD | 91173 | 66790 |

## EUR paired date-block sensitivity

| pair | n | disagreement | low99 | high99 | pass |
| --- | --- | --- | --- | --- | --- |
| BB | 10046 | 0.00019908421262193908 | 0.0 | 0.0008120624460840634 | True |
| BC | 103806 | 8.670019074041963e-05 | 1.7194464933934236e-05 | 0.00021223040737009276 | True |
| CB | 11544 | 8.662508662508663e-05 | 0.0 | 0.0003777805212604838 | True |
| CC | 62545 | 3.197697657686466e-05 | 0.0 | 0.00010199850113777083 | True |

## EUR primary decision

| all_criteria_met |
| --- |
| True |

B and C training groups have separate source records but share dates and currencies. Unknown latent denomination can multiply a modal scale. Own-date cent tolerance uses each trained anchor's magnitude. No hypothesis acceptance follows from compatibility alone.
