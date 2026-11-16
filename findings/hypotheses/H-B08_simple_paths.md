# H-B08: Do visible route paths always use distinct banks?

- **Owner:** B
- **Status:** rejected in exploration
- **Script:** `uv run python analysis/20_routing_time/H-B08_simple_paths.py`
- **Evidence:** [safe aggregate report](../../analysis/20_routing_time/out/H-B08_simple_paths_explore.md)

## Candidate and scope

Candidate: unlabelled routes select visible banks without replacement, producing a simple path with no repeated bank occurrences. Screen only May–June 2023 UTC, with both declared endpoint-bank MD5 bits zero, as in B04–B07 exploration. Remove placeholders before comparing bank identities. This bank-selection question concerns the displayed path, independently of declared endpoint disagreement.

## Exploration and falsification

The without-replacement candidate is false in supported cohorts. Among 370,978 three-visible-bank paths, 1,966 contain a repeated visible bank. Four-bank paths have 2,225 repeats among 137,022. At five banks the repeat count is 1,635 of 50,120. For three-bank paths, every repeat is between adjacent visible occurrences. Longer paths contain both adjacent and non-adjacent repeated visible banks.

Visible adjacency is measured after removing placeholders. A placeholder may separate those bank strings in the stored path. The report suppresses positive counts below 100 and only shows cohorts with at least 100 payments, ordering banks, senders and receivers. It exports no identities or individual paths.

The first and last visible bank differ in every displayed supported cohort. This is an exploratory constraint. Its origin could include endpoint selection or another path-generation condition. A new test of endpoint exclusion or intermediate-bank draw probabilities needs its own plan. These aggregates do not identify uniform bank sampling, a distribution of bank weights or a unique selection algorithm.

## Exposure and validation

Phase 0 full-data structural observations, Round 1 B01/B02 path-related summaries, Round 2 B04–B07 mechanisms and the B06 July timing outcome were exposed before this screen. May–June bank-bit0/0 is the chosen exploration population. B07 conditional July shapes were opened while the B08 exploration wave ran. B08 repeated-bank outcomes were queried only on May–June.

No B08 validation population or threshold was opened or frozen. A rejected universal path constraint needs no additional validation to preserve its observed counterexamples. Any later endpoint-exclusion or sampling mechanism will disclose this evidence and reused populations.
