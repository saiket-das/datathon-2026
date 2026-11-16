# H-B03: Covered is not an independent 10% payment-level coin

- **Owner:** B
- **Status:** rejected
- **Script / exact command / commit:** `uv run python analysis/20_routing_time/H-B03_covered_coin.py`; exploration only, recorded with the B01/B02 freeze commit.
- **Chart:** not selected for a headline chart; safe tables in `analysis/20_routing_time/out/H-B03_covered_coin_explore.md`.

## Proposed rule and scope

Candidate: after choosing V>2, assign Covered independently to each payment with probability
.10, otherwise Indirect. Population: unlabelled multibank payments in bank exploration.
The approximate 10% row share and similar length distributions suggested this candidate;
those facts alone do not imply independent label draws.

## Test plan (freeze before confirmation)

This candidate was falsified during discovery and **not selected for confirmation**.
No independent-confirmation claim is made. For each ordering bank with >=100 eligible
payments, compare Covered-share dispersion and zero-Covered banks with the independent
Binomial(n,.10) prediction. A bank-shared route propensity is an alternative.
Exploration predicate: both declared endpoint-bank MD5 bits zero, exactly as H-B02.
No confirmation/robustness partition was inspected for this question. Phase 0 had already
exposed full-data route totals and structural meanings; no other investigator's work was read.

## Discovery evidence

998 supported banks cover 774,238 unlabelled multibank payments. Their row-weighted
Covered share is .101305, but 91 banks have zero Covered payments versus an expected
.001089 banks under the proposed coin. Across supported banks, mean squared deviation
of Covered share from .10 is .034074 versus expected .000336 under independent draws
(about 101 times larger). Bank-share 10th/50th/90th percentiles are
.002216/.018534/.196451. No identities or small-group extracts are reported.

The candidate compound B02 law initially included a 10% Covered component. Its discovery
bank-resampling interval [.065434,.139413] failed the intended [.09,.11] tolerance.
The candidate was split out and rejected **before B02 was frozen**; the final B02 test
does not include this label claim. This change was not based on confirmation.

## Confirmation and robustness results

Not run: an exploratory candidate that has already failed does not need confirmation
to be reported as rejected. A revised bank-dependent label rule would need a fresh plan.

## Assessment

Reject independent payment-level .10 assignment. Covered propensity is concentrated
by declared ordering bank, but the actual bank/corridor/other selection mechanism remains
unresolved. Bank association does not establish causal direction. No inference about
Covered being a data error, a particular bank category or a universal deterministic function.

## Real-world explanation (interpretation, not evidence)

Institutions might choose different routing arrangements. Alternatively, bank identity
could proxy for currency, corridor or a shared synthetic group; this exploration does
not distinguish those possibilities.
