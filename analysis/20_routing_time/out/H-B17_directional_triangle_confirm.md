# H-B17_directional_triangle: confirm

Freeze: 1979ad17f1431755e99d54a4579ade48eb35c71d.
DuckDB 2.0.0; 768MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Bank deletion ranges quantify concentration. Triangles share edges, banks, dates and payment entities.

## Coverage before forming triangles

| all_direct | supported_bidirectional_pairs | supported_payments |
| --- | --- | --- |
| 411335 | 973 | 50641 |

## Cycle sum and split-period reference

| group | triangles | breaks | break_fraction | residual_s | reference_triangles | reference_breaks | reference_s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All supported triangles | 3846 | 2065 | 0.536921 | [121.25, 488.0, 761.9750000000026] | 1805 | 0 | [5.5, 12.800000000000068, 21.980000000000018] |
| Declared endpoints agree | 3415 | 1877 | 0.549634 | [130.5, 491.5, 783.7200000000003] | 1571 | 0 | [5.5, 13.0, 21.5] |

## Leave out each bank across all triangle positions

| group | banks | low | high | largest_triangle_share |
| --- | --- | --- | --- | --- |
| All supported triangles | 135 | 0.480581 | 0.558350 | 0.189548 |
| Declared endpoints agree | 123 | 0.492634 | 0.570566 | 0.195022 |

## Frozen criteria for rejecting the bank-score model

| passes |
| --- |
| True |
