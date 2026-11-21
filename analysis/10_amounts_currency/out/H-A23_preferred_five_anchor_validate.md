# H-A23 — Preferred USD mantissa-five anchor

Phase validate; freeze 7581544b1917f567ffabf8d4b18796268f1fd62b.
Positive unlabelled July USD, selected both-account bit. Magnitudes3–5; symmetric decimal-mantissa windows ±.4 around4–8.
Phase0/Round1 and A02/A10/A18/A22 exposure; A19 UTC and A09/A13 rates exposed. Reused bit-1 records are internal validation only.
512MB, one thread, no spill. Point mass tolerance USD1e-6; background is the rest of the same local window.

| scoped | selected | senders | receivers | banks | excluded |
| --- | --- | --- | --- | --- | --- |
| 119382 | 25967 | 7782 | 17748 | 1566 | 93415 |

| decade_group | digit | n | point_n | point_senders | point_receivers | background_n | background_senders | background_receivers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 4 | 3430 | 236 | 225 | 232 | 3194 | 2150 | 2809 |
| 3 | 5 | 4279 | 1559 | 1199 | 1435 | 2720 | 1899 | 2444 |
| 3 | 6 | 2346 | 183 | 175 | 181 | 2163 | 1563 | 1946 |
| 4-5 | 4 | 3596 | 202 | 191 | 198 | 3394 | 2011 | 2900 |
| 4-5 | 5 | 3631 | 1169 | 891 | 1094 | 2462 | 1574 | 2167 |
| 4-5 | 6 | 1963 | 131 | 129 | 130 | 1832 | 1274 | 1627 |
| All | 4 | 7026 | 438 | 400 | 427 | 6588 | 3388 | 5367 |
| All | 5 | 7910 | 2728 | 1795 | 2448 | 5182 | 2878 | 4363 |
| All | 6 | 4309 | 314 | 295 | 309 | 3995 | 2378 | 3405 |
| All | 7 | 3619 | 241 | 225 | 239 | 3378 | 2158 | 2950 |
| All | 8 | 3103 | 217 | 207 | 215 | 2886 | 1894 | 2524 |

| contrast | odds_ratio | low99 | high99 |
| --- | --- | --- | --- |
| 5 vs4/6 | 7.408630118987987 | 6.744609994813424 | 8.261721838526169 |
| 7 vs6/8 control | 0.9245160053029517 | 0.7618345680831804 | 1.1158995580393118 |

| decade_group | 5 vs4/6 |
| --- | --- |
| 3 | 7.3279894356310535 |
| 4-5 | 7.451636038963415 |

All frozen criteria met: True.

Whole declared ordering-bank bootstrap1000, seed20261117, .005/.995 percentiles. Shared countries/corridors, receivers and previous exposure remain. Preferred fixed values, rounding anchors and different latent mixtures are observational alternatives; this test does not recover a rounding operator or mixture probability.
