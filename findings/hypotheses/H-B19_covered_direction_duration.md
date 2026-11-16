# H-B19 multibank Covered state and Direct directional duration

- **Status:** confirmation-ready
- **Command:** `uv run python analysis/20_routing_time/H-B19_covered_direction_duration.py --phase explore`.
- **Internal test:** replace the phase with `--phase confirm --freeze <full SHA>`.

## Candidate and frozen test

The directed relation that predicts Covered versus Indirect on multibank
payments in B12 may also mark a directional duration penalty, visible even
on Direct payments. This is an association between different payment
populations sharing visible endpoints. A shared latent corridor state is an
alternative to the route class itself causing the timing difference.

Fit the label from unlabelled May–June v3–5 payments when all observed
multibank labels for an ordered pair agree, using visible first and last
banks and declared endpoint MD5 bits both zero. Keep unlabelled Direct
payments in that same bank partition, ten or more per direction, and require
the shorter direction median below 100 seconds. Apply the May–June labels to
July Direct durations. Both labels must be available. Direct timing and
multibank route labels come from distinct payments. Exploration Direct
durations used May–June. Training labels and July durations share some
corridors and potentially banks and payment entities.

The primary comparisons are the fraction of one-Covered pairs whose Covered
direction is slower by over 20 seconds, and the fraction of both-Indirect
pairs with an absolute gap over 20 seconds. Require ≥100 unordered pairs in
each primary group and ≥100 pooled canonical first banks. Resample those
bank groups with 1,000 draws and seed 20261116. Require the lower end of
the central 99% covered-slows interval ≥.85 and the upper end of the
both-Indirect large-gap interval ≤.02. Record sign reversals, the number
of selected pairs with both labels, and unsupported cases. Both-Covered
comparisons are descriptive where support permits. Group results require at
least 100 pairs and first banks to display. As a control, re-estimate
the Direct medians using only records with agreeing declared endpoints.
No descriptive control rescues a failed gate.

The bank resampling is conditional. Canonical first banks can share the
same opposite banks, corridors or accounts and a zero resampled error
rate does not bound the chance of future exceptions. The label lookup
evaluates known corridors and does not discover labels for new pairs.

## Exploration and exposure

Among 3,103 supported short-median pairs, 3,098 have a known multibank label
in both directions. On 2,569 both-Indirect pairs covering 156,098 Direct
payments, no absolute gap exceeds 20 seconds. Of 521 one-Covered pairs
covering 57,833 Direct payments, 504 have a large gap and all 504 are slower
in the Covered direction. The slower-share estimate is 96.74%, with
99% lower resampling bound 94.68%. Median absolute gap is 303 seconds.
In the agreeing-endpoint control the slower share is 96.68% on 512 pairs.
The both-Covered cohort lacks reporting support.

Phase 0 and B01–B16 were exposed. B17 and B18 May–June exploration motivated
the location gap and scale. The B19 exploratory join was run before freezing
any of the three new tests. Figures for these July cross-payment association
outcomes remain unqueried before freeze. Prior July duration and route results
and reused entities limit the test to internal validation. Pending July.
