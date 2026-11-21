# H-A19 — Effective UTC date of implied scales

Freeze: 5b6b952ed029696e0991df60d677998a64cc7c4c.
512MB; one thread; no disk spill. Aggregates only.
Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Coverage

| currency | scoped | eligible |
| --- | --- | --- |
| CHF | 39893 | 24595 |
| EUR | 200142 | 195974 |
| GBP | 48215 | 30021 |

## UTC hour-window comparison

| currency | utc_window | n | n_dates | senders | receivers | current_share | previous_share | next_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHF | 02–21 | 23286 | 45 | 2683 | 14490 | 0.41067594262647084 | 0.0078158550201838 | 0.007386412436657219 |
| EUR | 00–01 | 5151 | 89 | 3694 | 4191 | 0.4008930304795185 | 0.009512715977480102 | 0.007571345369831101 |
| EUR | 02–21 | 182795 | 89 | 33254 | 85237 | 0.4047101944801554 | 0.008835033781011515 | 0.008463032358653136 |
| EUR | 22–23 | 8028 | 89 | 5068 | 6226 | 0.4059541604384654 | 0.01245640259093174 | 0.008719481813652218 |
| GBP | 02–21 | 27848 | 47 | 5806 | 17910 | 0.40692329790290144 | 0.008366848606722207 | 0.009408216029876472 |
| GBP | 22–23 | 1386 | 47 | 871 | 1253 | 0.3874458874458874 | 0.007936507936507936 | 0.007215007215007215 |

## EUR boundary tests versus union of adjacent-date hits

| window | n | dates | own_share | lift | lift_low99 | lift_high99 | pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 00–01 | 5151 | 89 | 0.4008930304795185 | 0.38380896913220736 | 0.365179859388239 | 0.4017867488460686 | True |
| 22–23 | 8028 | 89 | 0.4059541604384654 | 0.38477827603388143 | 0.36714494185843166 | 0.4022025413419126 | True |

The same rows are scored with the previous, current and next calendar date's rate. All three anchors must be supported. EUR is primary. CHF and GBP hour windows are descriptive.
