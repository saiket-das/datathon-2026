# H-B12: Covered versus Indirect follows directed visible endpoints

- **Owner:** B
- **Status:** confirmation-ready
- **Exploration:** `uv run python analysis/20_routing_time/H-B12_directed_endpoint_route_class.py --phase explore`
- **Internal validation:** same command with `--phase confirm --freeze <full SHA>`.
- **Evidence:** [discovery report](../../analysis/20_routing_time/out/H-B12_directed_endpoint_route_class_explore.md).

## Proposed rule and scope

Among unlabelled paths with three to five visible banks, a fixed label associated
with the ordered pair of first and last visible banks predicts Covered versus
Indirect, including when the exact ordered intermediate sequence is new. This is
a narrower conditioning set than declared ordering-bank probabilities in B04.
First and last visible banks come from the displayed path after removing placeholders.
Both declared bank fields are preserved and can disagree with the visible endpoints.
The target is the recorded route label, the unit is a payment and support is counted
over endpoint pairs, paths, accounts and first visible banks.

## Frozen internal validation plan

- **Population and partition.** Unlabelled endpoint-bit-0/0 using the shared MD5
  parity definition on both declared endpoint bank fields. Fit a binary route label
  per ordered visible endpoint pair on May 2023 UTC payments with 3–5 visible banks.
  A label is supported when at least one May observation exists and May is unanimous.
  June is discovery. Evaluate July 2023 UTC, half-open `[2023-07-01,2023-08-01)`.
  Primary trials require supported endpoints and an exact ordered visible path
  sequence absent from May. The novelty is in the path sequence rather than the
  endpoints. The fit and test months cannot share records.
- **Comparator and alternatives.** Compare May endpoint-label lookup with May majority
  conditioned on declared directed endpoints on the subset where both give a label.
  Reverse the visible endpoints as a second comparator where the reversed pair
  is also known in May. Count mixed-label directed, unordered and declared endpoint
  groups, restricted to groups with multiple target-month payments. Within each
  grouping, the minimum in-sample mistakes are the sum of minority-label counts.
  These comparators diagnose endpoints, geography and order as explanations.
- **Falsification.** Require zero mixed-label directed visible endpoints in May,
  at least 5,000 primary target payments and at least 50% of July v3–5 payments
  eligible. Require at least 100 first visible banks, directed corridors, senders,
  receivers and payments of each route label. Error rate must be at most .001, and
  the one-sided 99% Clopper–Pearson upper bound on first-visible-bank units with
  any error must be at most .02. The bound assumes independent units. Shared
  receiving banks and account dependencies can invalidate that assumption.
- **Controls and exceptions.** Report route label, visible count, gap presence,
  novel currency within the known endpoint pair and agreement with the declared
  endpoint fields, with support suppression. Report unsupported endpoints,
  repeated complete paths, and Direct payments in the same month on a visible
  pair also used by a multibank route. Direct has its own participant-count
  definition. The latter control tests whether the pair can determine all three
  route labels without knowing visible count. Controls cannot rescue a failed
  primary result.
- **Exposure.** Phase 0 and Round 1 exposed full-data QFlag, path and route
  aggregates, plus B01 performance by route. Round 2 B04 exposed known-bank
  Covered probabilities and July comparisons. B05–B10 exposed July endpoints,
  route-conditioned timing, path shapes and duration-exclusion results on reused
  records as applicable. This wave exposed May–June endpoint-label consistency
  and the B11 duration pairing controls. The new May-label/novel-path July
  classification outcomes were unqueried before freeze. July is internal validation.

## Discovery evidence

May labels covered 233,973 of 318,693 June v3–5 payments that also had novel
visible sequences (73.4164%). They span 45,199 directed endpoint pairs and 2,856
first visible banks. All 27,024 Covered and 206,949 Indirect primary predictions
agreed. The declared-endpoint classifier erred on .5967% of the 223,546 payments
with both predictors available, versus zero for visible endpoints. On 102,402
eligible rows with labels for both directions, reversing the pair gave 19.7584%
error. There were 1,052 mixed groups under unordered visible endpoints and
1,691 under declared directed endpoints. No visible directed group with multiple
June payments mixed labels.

The primary result persisted in the novel-currency and endpoint-disagreement
controls. June has 53,601 Direct payments on visible pairs that also have Covered
payments, and 409,876 Direct payments on visible pairs that also have Indirect
payments. The scope is Covered versus Indirect at v3–5, conditional on the known
corridor. It does not determine Direct eligibility or assign classes to unseen pairs.

## Internal validation and assessment

Pending frozen July execution. A fixed directional correspondent arrangement is
compatible with the pattern. Latent corridor attributes or a shared route catalogue
could also determine path and label together. The observation cannot establish
which attributes are generated first or how new directed pairs get assigned a label.
