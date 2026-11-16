# H-B17 direction gaps and bank-score triangle closure

- **Status:** confirmation-ready
- **Command:** `uv run python analysis/20_routing_time/H-B17_directional_triangle.py --phase explore`.
- **Internal test:** replace the phase with `--phase confirm --freeze <full SHA>`.

## Candidate and frozen test

If a bank's sending and receiving roles each contribute a fixed term and the
pair's remaining effect is symmetric, then the gap between opposite directed
path medians equals a difference of bank scores. Even a nonzero symmetric
corridor effect cancels. For three banks A, B and C with both directions
observed on every edge, the directional gaps must sum to zero around the cycle.
This constraint is distinct from fitting the full additive duration model in B01.

Use unlabelled Direct paths with two visible banks, both declared endpoint MD5
bits zero, and at least ten observations in each direction for each pair.
Take direction medians and orient the contrast by lexicographic bank order.
Use all supported three-bank triangles once. Report the proportion whose
absolute cycle sum exceeds 100 seconds, a tolerance much larger than observed
same-path timing noise. A fresh July test supports rejection of the bank-score
explanation if at least 500 triangles span at least 100 distinct participating
banks and the failure fraction is at least .20 after every single-bank deletion.
This is a practical gate, without an independent-triangle sampling assumption.
Each deletion drops all triangles containing that bank in any position.

Repeat with only records whose two declared endpoints agree with the visible
path. As a negative control, take the change in directional gaps between
May and June, or between 1–15 and 16–31 July in the frozen run. Require five
observations per direction in each time block for this control. Evaluate cycle
sums of those changes. They measure temporal drift and estimation error and
need not equal the cycle sums of the underlying stable locations. Neither
control rescues the primary decision. Triangles reuse constituent edges,
banks, dates and potentially accounts. Bank deletions quantify sensitivity to
concentration rather than uncertainty under independent sampling.

## Exploration and exposure

May–June has 3,196 supported bidirectional pairs and 230,724 of 1,005,689
Direct payments on those pairs. Of 28,016 triangles across 211 participating
banks, 9,992 fail closure by over 100 seconds (35.67%). The failure share after
single-bank deletion ranges from 31.56% to 36.57%. With agreeing declared
endpoints, 9,302 of 25,357 triangles fail. Zero of 16,530 temporal reference
cycles exceed 100 seconds, and the 99th percentile is 19 seconds. Preliminary
exploration also raised per-direction support to 25 and 50. These narrower
populations had larger closure failures, while the primary test retains the
larger ten-payment cohort.

This can distinguish bank scores from directional corridor or interaction
effects. It cannot distinguish a directional lookup from other latent
context tied to the observed corridor. The result has no physical interpretation
as a bank processing time.

Phase 0, B01–B16 results and May–June triangle and gap-shape probes were exposed
before freeze. B11, B13, B15 and B16 cover related duration outcomes. Exact
July cycle outcomes were unqueried before freeze, but records and entities are
reused. Pending frozen internal evaluation.
