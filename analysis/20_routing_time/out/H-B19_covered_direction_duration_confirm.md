# H-B19_covered_direction_duration: confirm

Freeze: 1979ad17f1431755e99d54a4579ade48eb35c71d.
DuckDB 2.0.0; 768MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% canonical first-visible-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Eligibility

| all_direct | supported_pairs | short_pairs | both_labels_known | one_covered | both_indirect |
| --- | --- | --- | --- | --- | --- |
| 411335 | 973 | 942 | 942 | 293 | 643 |

## Primary contrast

| covered_directions | n | banks | payments | large_gap_share | covered_slower_share | absolute_gap_seconds |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 643 | 109 | 27737 | 0.000000 | None | [2.0, 4.5, 8.0] |
| 1 | 293 | 128 | 18024 | 0.969283 | 0.969283 | [311.0, 531.4000000000001, 592.78] |

## Declared endpoints agree

| covered_directions | n | banks | payments | large_gap_share | covered_slower_share | absolute_gap_seconds |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 578 | 101 | 24555 | 0.000000 | None | [2.0, 5.0, 8.115000000000009] |
| 1 | 283 | 124 | 16954 | 0.971731 | 0.971731 | [310.0, 526.1, 591.27] |

## Primary practical gates and sign exceptions

| canonical_first_banks | one_covered_slower_fraction | one_covered_lower99 | both_indirect_large_gap_fraction | both_indirect_upper99 | one_covered_large_gaps | large_gap_points_toward_indirect |
| --- | --- | --- | --- | --- | --- | --- |
| 149 | 0.969283 | 0.939046 | 0.000000 | 0.000000 | 284 | 0 |

## Frozen decision

| pass |
| --- |
| True |
