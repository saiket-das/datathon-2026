# H-B19_covered_direction_duration: explore

Freeze: not yet frozen.
DuckDB 2.0.0; 768MB; one thread; UTC; no spill.
No identifiers or payment records are exported. Counts below 100 are suppressed.
Any reported intervals are 99% canonical first-visible-bank cluster resampling sensitivity intervals, not proof of independent banks.

## Eligibility

| all_direct | supported_pairs | short_pairs | both_labels_known | one_covered | both_indirect |
| --- | --- | --- | --- | --- | --- |
| 1005689 | 3196 | 3103 | 3098 | 521 | 2569 |

## Primary contrast

| covered_directions | n | banks | payments | large_gap_share | covered_slower_share | absolute_gap_seconds |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2569 | 186 | 156098 | 0.000000 | None | [1.5, 4.0, 7.0] |
| 1 | 521 | 170 | 57833 | 0.967370 | 0.967370 | [303.0, 529.0, 589.9] |

## Declared endpoints agree

| covered_directions | n | banks | payments | large_gap_share | covered_slower_share | absolute_gap_seconds |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2411 | 181 | 144227 | 0.000000 | None | [1.5, 4.0, 7.5] |
| 1 | 512 | 169 | 54829 | 0.966797 | 0.966797 | [306.25, 529.0, 589.9449999999999] |

## Primary practical gates and sign exceptions

| canonical_first_banks | one_covered_slower_fraction | one_covered_lower99 | both_indirect_large_gap_fraction | both_indirect_upper99 | one_covered_large_gaps | large_gap_points_toward_indirect |
| --- | --- | --- | --- | --- | --- | --- |
| 200 | 0.967370 | 0.946805 | 0.000000 | 0.000000 | 504 | 0 |

## Frozen decision

| pass |
| --- |
| True |
