# H-B17_directional_triangle: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 768MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Bank deletion ranges quantify concentration. Triangles share edges, banks, dates and payment entities.

## Coverage before forming triangles

| all_direct | supported_bidirectional_pairs | supported_payments |
| --- | --- | --- |
| 1005689 | 3196 | 230724 |

## Cycle sum and split-period reference

| group | triangles | breaks | break_fraction | residual_s | reference_triangles | reference_breaks | reference_s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All supported triangles | 28016 | 9992 | 0.356653 | [6.0, 443.0, 684.9249999999993] | 16530 | 0 | [4.5, 11.5, 19.0] |
| Declared endpoints agree | 25357 | 9302 | 0.366842 | [6.5, 446.5, 691.5] | 15142 | 0 | [4.5, 11.5, 19.0] |

## Leave out each bank across all triangle positions

| group | banks | low | high | largest_triangle_share |
| --- | --- | --- | --- | --- |
| All supported triangles | 211 | 0.315603 | 0.365720 | 0.095802 |
| Declared endpoints agree | 207 | 0.324767 | 0.376619 | 0.099539 |

## Frozen criteria for rejecting the bank-score model

| passes |
| --- |
| True |
