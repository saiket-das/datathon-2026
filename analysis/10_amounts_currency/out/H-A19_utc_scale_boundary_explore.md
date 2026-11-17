# H-A19 — Effective UTC date of implied scales

Freeze: exploration.
512MB; one thread; no disk spill. Aggregates only.
Both-account bit-0 only. Phase 0 and A01–A18 prior exposure applies.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Coverage

| currency | scoped | eligible |
| --- | --- | --- |
| CHF | 45646 | 28216 |
| EUR | 201796 | 197714 |
| GBP | 72198 | 45080 |

## UTC hour-window comparison

| currency | utc_window | n | n_dates | senders | receivers | current_share | previous_share | next_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHF | 02–21 | 26730 | 45 | 2884 | 15968 | 0.40867938645716423 | 0.006921062476618032 | 0.00909090909090909 |
| EUR | 00–01 | 5707 | 89 | 3862 | 4281 | 0.4128263536008411 | 0.008936393902225337 | 0.010338181181005782 |
| EUR | 02–21 | 183171 | 89 | 33704 | 84056 | 0.40438715735569497 | 0.008997057394456547 | 0.008751385317544809 |
| EUR | 22–23 | 8836 | 89 | 5184 | 6204 | 0.3939565414214577 | 0.010072430964237211 | 0.009053870529651425 |
| GBP | 00–01 | 1160 | 47 | 610 | 1054 | 0.38448275862068965 | 0.005172413793103448 | 0.01206896551724138 |
| GBP | 02–21 | 41799 | 47 | 6143 | 24123 | 0.4074738630110768 | 0.008445178114308954 | 0.01000023924017321 |
| GBP | 22–23 | 2121 | 47 | 933 | 1872 | 0.3927392739273927 | 0.007072135785007072 | 0.007543611504007544 |

## EUR boundary tests versus union of adjacent-date hits

| window | n | dates | own_share | lift | lift_low99 | lift_high99 | pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 00–01 | 5707 | 89 | 0.4128263536008411 | 0.3937270019274575 | 0.3812226592409357 | 0.40628664326150027 | True |
| 22–23 | 8836 | 89 | 0.3939565414214577 | 0.3749434133091897 | 0.3636927428637414 | 0.38691944033807363 | True |

The same rows are scored with the previous, current and next calendar date's rate. All three anchors must be supported. EUR is primary. CHF and GBP hour windows are descriptive.
