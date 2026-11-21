# H-B12: Covered versus Indirect follows directed visible endpoints

- **Owner:** B
- **Status:** supported in frozen internal validation
- **Exploration:** `uv run python analysis/20_routing_time/H-B12_directed_endpoint_route_class.py --phase explore`
- **Internal validation:** same command with `--phase confirm --freeze 9489c1a051237433c0a6fbbbd260e602b2e27521`.
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

Freeze `9489c1a051237433c0a6fbbbd260e602b2e27521` was committed on
16 November 2026 at 21:46:08 MYT. The unchanged
[July test](../../analysis/20_routing_time/out/H-B12_directed_endpoint_route_class_confirm.md)
passed every criterion. On 167,205 of 227,489 July payments (73.50%) with known
directed endpoints and a new complete visible path, the May rule made zero errors.
These observations span 39,761 directed endpoint pairs, 164,380 visible paths,
2,741 first visible banks, 39,984 senders and 81,171 receivers. There are 19,173
Covered and 148,032 Indirect payments. The 99% upper affected-bank fraction is
.001679 under the stated cluster independence assumption.

The declared-endpoint comparator errs on .6387% of 159,706 jointly supported
payments and the reversed-pair comparator on 19.6384% of 73,504 jointly supported
payments. Within July, 0 of 30,112 repeated directed visible endpoint groups mix
both labels. Using unordered visible endpoints produces 909 mixed groups, and using
declared directed bank fields produces 1,154.

There are also zero observed errors in supported subgroups with 3, 4 or 5
visible banks, the 19,610 payments with gaps, the 10,805 with a new currency for
the directed pair, and the 11,437 with an endpoint disagreement. Of the target
population, 50,012 have no supported May directed pair and 10,272 have a visible
path already seen in May. There are 38,004 July Direct payments on visible
endpoint pairs also used by Covered routes and 280,090 on pairs also used by
Indirect routes. This bounds the rule to the multibank classification.

A fixed directional correspondent arrangement is compatible with the pattern.
Latent corridor attributes or a shared route catalogue could also determine path
and label together. Novel visible paths and stable labels distinguish the result
from exact path memorization. Shared banks, corridors and possibly accounts and
reused July exposure limit inference beyond the selected population. Assignment
for new directed pairs and the order of generator stages remain unresolved.
July classification, exception and subgroup outcomes are now exposed.
