# H-A06: Endpoint currency association

May/June and earlier bit-0 training; July validate scoring. Freeze: 3fb8c1dcd842bdb20ccafeb2ee2f44dfec15f357.
Prior Phase 0, Round 1 and A03/A05 reused-population exposure applies.
Modal categorical currency predictor. A country with fewer than 100 training payments falls back to the global mode.
Each percentage uses all rows in the displayed July subgroup, including fallbacks.

| route | sender_agrees | receiver_agrees | payments | senders | receivers | global_pct | declared_send_pct | declared_receive_pct | path_send_pct | path_receive_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | All | All | 699603 | 89167 | 270945 | 33.385 | 89.408 | 33.515 | 93.367 | 33.528 |
| All | false | false | 1559 | 1360 | 1445 | 34.06 | 10.904 | 33.675 | 93.329 | 34.573 |
| All | false | true | 31878 | 14958 | 21521 | 33.133 | 10.393 | 33.368 | 93.262 | 33.34 |
| All | true | false | 31257 | 14822 | 20971 | 33.644 | 93.4 | 33.324 | 93.4 | 33.788 |
| All | true | true | 634909 | 85151 | 248934 | 33.383 | 93.371 | 33.532 | 93.371 | 33.522 |
| Covered | All | All | 27765 | 9839 | 17752 | 40.436 | 88.323 | 40.94 | 92.246 | 40.99 |
| Direct | All | All | 442037 | 71216 | 187365 | 32.902 | 90.669 | 33.058 | 94.685 | 33.069 |
| Indirect | All | All | 229801 | 50315 | 110314 | 33.462 | 87.112 | 33.499 | 90.968 | 33.509 |

## 99% ordering-bank cluster sensitivity intervals

| statistic | low | high |
| --- | --- | --- |
| path sender accuracy | 0.9294326238880523 | 0.937553247137504 |
| lift vs declared sender | 0.03857744967601556 | 0.04077595128151892 |
| lift vs path receiver | 0.5460359479560066 | 0.6474299489949215 |

All practical criteria met: True.
Eligible senders / receivers / declared ordering banks: (89167, 270945, 5696).
Same-role sender / receiver / ordering-bank overlap with training: (0, 0, 4414).
Other cross-role accounts and path banks may overlap; no independent-holdout inference.
