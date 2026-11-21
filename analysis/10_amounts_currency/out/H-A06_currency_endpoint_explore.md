# H-A06: Endpoint currency association

May/June and earlier bit-0 training; July explore scoring. Freeze: ''.
Prior Phase 0, Round 1 and A03/A05 reused-population exposure applies.
Modal categorical currency predictor. A country with fewer than 100 training payments falls back to the global mode.
Each percentage uses all rows in the displayed July subgroup, including fallbacks.

| route | sender_agrees | receiver_agrees | payments | senders | receivers | global_pct | declared_send_pct | declared_receive_pct | path_send_pct | path_receive_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | All | All | 749066 | 91004 | 277916 | 30.465 | 89.307 | 30.697 | 93.321 | 30.727 |
| All | false | false | 1641 | 1402 | 1479 | 32.115 | 9.202 | 31.932 | 93.723 | 32.602 |
| All | false | true | 34100 | 15437 | 22454 | 32.317 | 9.252 | 32.449 | 93.364 | 32.443 |
| All | true | false | 33654 | 15154 | 21747 | 31.09 | 93.398 | 30.852 | 93.398 | 31.39 |
| All | true | true | 679671 | 86813 | 255179 | 30.337 | 93.314 | 30.599 | 93.314 | 30.603 |
| Covered | All | All | 32334 | 10144 | 19189 | 32.573 | 88.068 | 33.59 | 91.913 | 33.68 |
| Direct | All | All | 473855 | 72650 | 192399 | 29.892 | 90.555 | 30.144 | 94.664 | 30.174 |
| Indirect | All | All | 242877 | 51359 | 112661 | 31.303 | 87.036 | 31.392 | 90.887 | 31.411 |

## 99% ordering-bank cluster sensitivity intervals

| statistic | low | high |
| --- | --- | --- |
| path sender accuracy | 0.9299846069541198 | 0.9362325336944977 |
| lift vs declared sender | 0.03927864194904156 | 0.04111384779523963 |
| lift vs path receiver | 0.5835062152754172 | 0.6692109760289261 |

All practical criteria met: True.
Eligible senders / receivers / declared ordering banks: (91004, 277916, 5748).
Same-role sender / receiver / ordering-bank overlap with training: (71655, 102533, 5600).
Other cross-role accounts and path banks may overlap; no independent-holdout inference.
