# H-B29 Institution-prefix transfer between origin banks

- **Status:** unsupported in exploration
- **Command:** `uv run python analysis/20_routing_time/H-B29_institution_prefix_transfer.py`.

## Candidate and comparison

The first four BIC characters identify an institution component. If B20's
origin propensities are mainly shared at that level, rates learned from
other banks with that prefix should help on an origin's unseen corridors.
Use B20's unlabelled bit0/0 May training and June test population with v3–5,
pure labels, two June observations per target corridor and neither orientation
in May. Both endpoint roles require 25 May corridors. Keep target origins
whose prefix has at least 25 May corridors at other banks. Exclude the
target origin entirely when computing the prefix rate. Smooth toward the
May global rate with ten pseudo-corridors, matching B20.

Compare Brier scores on identical target corridors, weighted once each.
The prefix comparison is exploration. No July evaluation or frozen test
is claimed. Code reuses the historical B20 loading and scoring functions.

## Results and limitations

Prefix eligibility retains 3,812/5,487 June B20 corridors, 9,284 payments,
308 origin banks, 740 receiving banks and 131 prefixes. Prefix Brier is
.026743, global .025323, own-origin .022124 and directed country pair
.025624. Prefix predicted share is 4.4803% versus 2.5446% observed.
On 329 May-supported origin banks in 136 prefixes, smoothed own-bank and
other-bank rates have correlation −.061902. Their average absolute
difference is 2.8506 percentage points. These support restrictions select
frequent origins and the reported correlation is descriptive.

The tested shared-prefix rate gives no benefit over the global comparator.
Prefix groups need not denote economically consistent entities in this
synthetic dataset. More detailed hierarchy and country interactions remain
possible. The screen neither rejects every institution-level influence nor
identifies a random bank-level parameter. Shared receivers and data-driven
selection limit independent inference.

## Exposure

Phase 0 and B01–B28 were exposed, including B20's July internal outcomes
and B28's existing frozen July aggregate. Only May and June were loaded
for this question. Initial syntax retries in scratch PowerShell produced
no scientific output. No individual bank, prefix or account is exported.
[Aggregate evidence](../../analysis/20_routing_time/out/H-B29_institution_prefix_transfer_explore.md).
