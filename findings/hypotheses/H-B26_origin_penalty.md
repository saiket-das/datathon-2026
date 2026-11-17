# H-B26 A fixed Covered-origin duration increment

- **Status:** rejected as an exact description of selected exploration medians; not a frozen confirmation.
- **Command:** `uv run python analysis/20_routing_time/H-B26_origin_penalty.py`

## Question and comparison

Could a single duration increment for each Covered-origin bank explain
the direction differences previously associated with Covered labels?
Such a model implies constant Covered-minus-Indirect direction differences
across receiving banks, after assuming a symmetric pair baseline. Pair-specific
baseline asymmetry and sampling error provide alternative explanations.

## Population and observations

Use only May–June 2023 unlabelled records in the existing declared endpoint
MD5 parity 0/0 exploration partition. `duration_reversals.py` estimates
Direct medians with at least ten payments in each direction of an unordered
visible-endpoint pair. Select shorter median below 100 seconds and absolute
direction difference above 20 seconds. Pure Covered/Indirect labels come
from separate multibank payments with three to five visible bank occurrences;
require exactly one Covered direction. Orient the gap by that direction.

There are 504 selected pairs and 195 receiving banks. Actual Covered-origin
support is below 100 banks; the report therefore suppresses its exact count.
The repeated-origin groups contain 461 corridors. Every repeated-origin
group has a direction-gap range exceeding 20 seconds. These are descriptive
observed medians, not a formal rejection of every noisy bank-level model.
The selection conditions on large direction differences and short baselines.
It does not establish the distribution of increments over all corridors.

## Exposure and limitations

Phase 0 and Round 1 full-data aggregates, earlier Round 2/3 direction,
Covered-label and July internal outcomes are exposed. This screen uses
reused May–June records and opens no new July outcome. There is no freeze,
independent holdout, causal effect or original implementation claim.
In particular, actual Covered-origin support differs from B19's canonical
first/second-bank bootstrap roles. That bootstrap is not an actual-origin
independence audit. Pair baselines, bank concentration, median uncertainty
and dependencies across corridors remain limitations.

The [aggregate report](../../analysis/20_routing_time/out/H-B26_origin_penalty_explore.md)
preserves the negative result without bank identities or small-group values.
