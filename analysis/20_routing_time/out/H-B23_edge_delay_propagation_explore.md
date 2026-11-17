# H-B23_edge_delay_propagation: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 600MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% separate bank-role cluster resampling sensitivity intervals, not proof of independent banks.

## Matched support

| scoped | matched | marked | origin_banks | receiver_banks | outer_corridors | middle_banks | june_baseline_shift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 211787 | 4326 | 1521 | 164 | 152 | 2306 | 132 | -13.0 |

## Observed delay by prior edge state

| adjacent_state | outer_state | n | banks | receivers | outer_corridors | covered_share | adjacent_delay | outer_delay | median_excess_seconds | baseline_mae | adjacent_mae | outer_mae | both_mae |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | All | 4326 | 164 | 152 | 2306 | 0.165049 | 84.424411 | 48.035136 | 4.000000 | 88.350555 | 7.828826 | 106.162159 | 54.432386 |
| suppressed | suppressed | 285 | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed |
| Edge marked | Outer unmarked | 863 | 126 | 123 | 701 | 0.030127 | 307.333140 | 1.319235 | 297.000000 | 306.024913 | 7.661645 | 304.705678 | 8.235805 |
| suppressed | suppressed | 373 | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed |
| Edge unmarked | Outer unmarked | 2805 | 155 | 123 | 1698 | 0.010695 | 1.906061 | 1.022460 | 0.000000 | 7.658289 | 7.844920 | 7.852585 | 8.227807 |

## Primary marked paths

| n | banks | receivers | interior_banks | outer_corridors | baseline_mae | adjacent_mae | outer_mae | both_mae | adjacent_within20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1521 | 130 | 137 | 118 | 948 | 237.161736 | 7.799145 | 287.462853 | 139.642012 | 0.957922 |

## Bank sensitivity on marked paths

| cluster_role | clusters | lift_vs_base_low99 | lift_vs_base_high99 | lift_vs_outer_low99 | lift_vs_outer_high99 | lift_vs_both_low99 | lift_vs_both_high99 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Origin | 130 | 0.963632 | 0.970785 | 0.970078 | 0.976103 | 0.912595 | 0.954767 |
| Receiver | 137 | 0.963841 | 0.969989 | 0.969665 | 0.975385 | 0.930980 | 0.953157 |
| Interior | 118 | 0.953626 | 0.973946 | 0.966353 | 0.977016 | 0.920515 | 0.960672 |

## Frozen decision

| all_criteria_met |
| --- |
| True |
