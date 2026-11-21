# H-B21 Exact reversed paths with the same interior bank

- **Status:** exploratory, insufficient support
- **Command:** `uv run python analysis/20_routing_time/H-B21_reversed_path_penalty.py --phase explore`

Test how much of a complete three-bank path's directional median gap is
explained by the same endpoints' Direct gap versus the sum of matching
adjacent Direct gaps. Use unlabelled May–June declared endpoint-bank parity
0/0, no placeholders, three distinct visible banks, at least three records
in each exact path direction and consistent observed labels. Direct
medians require ten records in each orientation. The outer Direct pair
must have a shorter median below 100 seconds. Also compare zero gap and
adding both directional signals.

Fewer than 100 exact reversed three-bank paths have the required support,
and none meets all Direct controls. The report suppresses the small count.
The experiment cannot decide among the proposed timing explanations. B23
uses a distinct design that calibrates a common baseline and uses
separate Direct witnesses for each pair without requiring reverse
multibank paths.

Phase 0 and B01–B19 expose related routing and duration outcomes.
Exploration also used May–June data for B20. There is no July outcome or
frozen claim. [Aggregate support audit](../../analysis/20_routing_time/out/H-B21_reversed_path_penalty_explore.md).
