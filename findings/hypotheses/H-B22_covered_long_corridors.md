# H-B22 Covered directional gap when both Direct directions are slow

- **Status:** exploratory, insufficient support
- **Command:** `uv run python analysis/20_routing_time/H-B22_covered_long_corridors.py --phase explore`

Extend B19's label-to-duration association to bidirectionally slow
corridors whose shorter Direct median is at least 100 seconds. Use the
same May–June MD5 endpoint-bank parity 0/0 unlabelled cohort and at
least ten Direct records in each direction. Derive directed labels
from separate May–June v3–5 records with consistent Covered or Indirect
labels. Compare signed gaps over 20 seconds on one-Covered pairs with
absolute gaps on both-Indirect pairs. The executable checks whether the
long cohort supports the proposed cutoff of lower 99% covered-slower
share .80 and upper 99% both-Indirect gap share .03, requiring at least
100 pairs in each group and 100 first-bank clusters. Reported subgroup
statistics also require displayable receiver support.

The long regime has fewer than 100 pairs and the candidate misses its
support gate. Its sign and gap-size summaries are suppressed. The short
control recovers the already exposed B19 overlap by design. The experiment
does not falsify or extend the B19 duration rule to a higher baseline.

Phase 0 and B01–B21 expose related structural and timing aggregates,
including B18's short-center restriction and B19's primary comparison.
No July long-regime outcome or frozen validation was opened.
[Aggregate exploration](../../analysis/20_routing_time/out/H-B22_covered_long_corridors_explore.md).
