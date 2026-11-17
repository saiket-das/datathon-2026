# H-A23 — Preferred USD mantissa-five anchor

Phase explore; freeze exploration only.
Positive unlabelled July USD, selected both-account bit. Magnitudes3–5; symmetric decimal-mantissa windows ±.4 around4–8.
Phase0/Round1 and A02/A10/A18/A22 exposure; A19 UTC and A09/A13 rates exposed. Reused bit-1 records are internal validation only.
512MB, one thread, no spill. Point mass tolerance USD1e-6; background is the rest of the same local window.

| scoped | selected | senders | receivers | banks | excluded |
| --- | --- | --- | --- | --- | --- |
| 129847 | 28553 | 8127 | 18567 | 1588 | 101294 |

| decade_group | digit | n | point_n | point_senders | point_receivers | background_n | background_senders | background_receivers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 4 | 3675 | 270 | 251 | 263 | 3405 | 2256 | 2891 |
| 3 | 5 | 4526 | 1634 | 1249 | 1480 | 2892 | 1963 | 2485 |
| 3 | 6 | 2707 | 221 | 211 | 214 | 2486 | 1775 | 2170 |
| 4-5 | 4 | 3949 | 236 | 220 | 229 | 3713 | 2114 | 3101 |
| 4-5 | 5 | 4049 | 1276 | 979 | 1156 | 2773 | 1743 | 2436 |
| 4-5 | 6 | 2199 | 154 | 148 | 152 | 2045 | 1398 | 1807 |
| All | 4 | 7624 | 506 | 449 | 485 | 7118 | 3565 | 5598 |
| All | 5 | 8575 | 2910 | 1893 | 2502 | 5665 | 3029 | 4628 |
| All | 6 | 4906 | 375 | 335 | 360 | 4531 | 2651 | 3755 |
| All | 7 | 3986 | 270 | 254 | 263 | 3716 | 2291 | 3122 |
| All | 8 | 3462 | 233 | 219 | 230 | 3229 | 2012 | 2754 |

| contrast | odds_ratio | low99 | high99 |
| --- | --- | --- | --- |
| 5 vs4/6 | 6.792127216424408 | 6.0983573409613685 | 7.55461414366481 |
| 7 vs6/8 control | 0.9273553906294261 | 0.7441377802117974 | 1.1524493326817287 |

| decade_group | 5 vs4/6 |
| --- | --- |
| 3 | 6.778932260636125 |
| 4-5 | 6.793723358021952 |

All frozen criteria met: True.

Whole declared ordering-bank bootstrap1000, seed20261117, .005/.995 percentiles. Shared countries/corridors, receivers and previous exposure remain. Preferred fixed values, rounding anchors and different latent mixtures are observational alternatives; this test does not recover a rounding operator or mixture probability.
