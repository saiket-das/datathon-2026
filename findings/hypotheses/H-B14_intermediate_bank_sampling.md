# H-B14: Interior banks are consistent with draws from a shared weighted pool

- **Owner:** B
- **Status:** confirmation-ready
- **Exploration:** `uv run python analysis/20_routing_time/H-B14_intermediate_bank_sampling.py --phase explore`
- **Internal validation:** same command with `--phase confirm --freeze <full SHA>`.
- **Evidence:** [discovery report](../../analysis/20_routing_time/out/H-B14_intermediate_bank_sampling_explore.md).

## Proposed rule and scope

Estimate bank weights from the single interior bank in May unlabelled paths with
three visible banks. For paths with four visible banks, compare the two interior
positions with independent draws from those same weights, with replacement.
The proposed sampler predicts the chance of coinciding banks as the sum of
squared bank weights. It predicts same-country coincidence as the sum of squared
country weights and gives an outer product for the joint country distribution.
The endpoints are outside the two draws. This explains repeat counts without
requiring uniformly likely banks or treating all visible path positions alike.

## Frozen internal validation plan

- **Population and exposure.** Unlabelled payments with both declared endpoint-bank
  MD5 parity bits zero, using the shared rule. Remove placeholders for positions.
  Fit May 2023 UTC three-bank payments only. June four-bank paths are exploration.
  Evaluate July four-bank paths, UTC `[2023-07-01,2023-08-01)`, with no outcome
  filtering and no refit. Month and length prevent record overlap. Bank identities,
  and potentially endpoint pairs and accounts, are reused.
- **Comparator and controls.** Compare the bank collision expectation with the
  uniform-with-replacement rate `1/M` for the May catalogue of M interior banks.
  A sampler without replacement for the interior draws has zero collisions.
  Score the two-country joint distribution with May's ten most frequent countries
  by weight, tied by country code, plus the remainder. Same-country collision
  uses the full country codes internally, including differences within the pooled
  bin. Assess coverage of bank identities in the May catalogue and report control
  strata by route, gap presence and whether endpoint countries match. Compare
  reuse of either endpoint in the first interior slot with the sum of its May
  endpoint weights. These metrics cannot rule out all conditional sampling laws.
- **Acceptance and uncertainty.** Require at least 10,000 target paths, 100 first
  visible banks, 100 distinct senders, 100 distinct receivers and 98% of paths
  with both interior identities in the fitted catalogue. Resample first-visible-bank
  clusters 1,000 times using seed 20261116. Require the entire 99% interval for
  observed minus expected bank collision within ±.0015 and same-country
  collision within ±.006. Require the 99% resampled joint TV upper bound ≤.035.
  Percentiles measure sensitivity to cluster resampling. TV is nonnegative and
  resampling adds variation to its distance from a fixed reference, so the upper
  bound is a practical gate. Neither it nor the collision intervals correct for
  shared intermediary or receiving banks. Compare marginal TVs descriptively.
  The conjunction fails on any miss. No subgroup can rescue it.
- **Prior exposure.** Phase 0, Round 1 and B04–B13 are exposed. B08 exposed repeated
  banks during discovery. B07 exposed July path shapes and B11 evaluated July
  repeated exact paths and timing, including a repeat-bank control. B12 exposed
  July route classes and novel exact path counts. May–June probes compared previous-month
  marginals with endpoint and middle-slot repeat rates by route and candidate strata.
  Specific July two-interior-bank collision and joint country results are still
  unqueried before freeze. The evidence is an internal test on reused records.

## Discovery evidence

May uses 159,191 three-visible-bank payments and 4,138 middle-bank identities.
June contains 78,427 four-bank payments and 3,234 first visible banks. In 98.69%
of paths, both middle banks occur in the May catalogue. The bank collision
prediction is 0.6088%, compared with 0.5916% observed and 0.0242% under uniform
draws. Country coincidence is 6.5067% observed and 6.5458% expected. The joint
TV is .013471 with resampling upper percentile .022428. Route and gap controls
are available in the aggregate report. The June observations guided tolerances.

## Internal validation and assessment

Pending the frozen July test. A repeatable weighted bank mix is compatible with
selection from a shared pool of potential correspondents. Conditional mixtures
and dependencies can have similar coarse summaries. This test does not identify
the exact original bank weights, independence conditional on every endpoint pair,
catalogue maintenance, generator ordering or eligibility rules.
