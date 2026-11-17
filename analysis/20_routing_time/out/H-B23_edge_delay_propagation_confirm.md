# H-B23_edge_delay_propagation: confirm

Freeze: af07496a8a81d970bbb30531c1a4f484ec03fa55.
DuckDB 2.0.0; 600MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% separate bank-role cluster resampling sensitivity intervals, not proof of independent banks.

## Matched support

| scoped | matched | marked | origin_banks | receiver_banks | outer_corridors | middle_banks | june_baseline_shift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 151146 | 3111 | 1099 | 159 | 148 | 1810 | 135 | -13.0 |

## Observed delay by prior edge state

| adjacent_state | outer_state | n | banks | receivers | outer_corridors | covered_share | adjacent_delay | outer_delay | median_excess_seconds | baseline_mae | adjacent_mae | outer_mae | both_mae |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | All | 3111 | 159 | 148 | 1810 | 0.162006 | 87.479910 | 45.663934 | 4.500000 | 91.300868 | 7.683703 | 107.528930 | 51.962231 |
| suppressed | suppressed | 199 | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed |
| Edge marked | Outer unmarked | 645 | 110 | 111 | 538 | 0.038760 | 311.165891 | 1.161240 | 310.000000 | 310.172093 | 7.093023 | 309.010853 | 7.514729 |
| suppressed | suppressed | 255 | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed | suppressed |
| Edge unmarked | Outer unmarked | 2012 | 147 | 118 | 1317 | 0.012425 | 1.957505 | 1.043986 | 0.000000 | 7.750249 | 7.913519 | 7.875746 | 8.212972 |

## Primary marked paths

| n | banks | receivers | interior_banks | outer_corridors | baseline_mae | adjacent_mae | outer_mae | both_mae | adjacent_within20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1099 | 114 | 130 | 109 | 733 | 244.261601 | 7.262966 | 289.969518 | 132.056415 | 0.958144 |

## Bank sensitivity on marked paths

| cluster_role | clusters | lift_vs_base_low99 | lift_vs_base_high99 | lift_vs_outer_low99 | lift_vs_outer_high99 | lift_vs_both_low99 | lift_vs_both_high99 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Origin | 114 | 0.966349 | 0.973877 | 0.972478 | 0.977732 | 0.912121 | 0.954781 |
| Receiver | 130 | 0.966053 | 0.974771 | 0.971458 | 0.978025 | 0.930165 | 0.954591 |
| Interior | 109 | 0.958072 | 0.976252 | 0.966538 | 0.979410 | 0.923199 | 0.962015 |

## Frozen decision

| all_criteria_met |
| --- |
| True |
