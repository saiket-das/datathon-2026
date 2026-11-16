# H-B07: Conditional placement of internal path placeholders

- **Owner:** B
- **Status:** rejected
- **Evidence level:** Frozen conjunction rejected. Conditional point approximations remain supported but not independently confirmed.
- **Reproduce discovery:** `uv run python analysis/20_routing_time/H-B07_gap_placement.py --phase explore`
- **Reproduce internal validation:** same script with `--phase confirm --freeze SHA`

## Rule and mechanism scope

Conditional on v visible bank occurrences and exactly g internal placeholders, each legal weak composition of g indistinguishable placeholders into the v−1 internal slots has approximately equal probability. For one gap, this is uniform placement among the internal slots. For two gaps, sorted slot pairs including repeats have probability 1/choose(v,2). Consecutive placeholders then have probability 2/v. The comparator independently allocates the two gaps to uniform slots, predicting adjacency 1/(v−1) and twice the probability of a split pair compared with a repeated slot.

Uniform weak compositions can follow from an exchangeable ordered sequence of visible-bank and placeholder events conditional on counts. The same observed distribution can result from directly choosing a gap composition. These measurements distinguish the iid-slot comparator without determining a unique algorithm, execution order or exact probabilities. Visible count refers to occurrences, which may repeat bank identities.

## Discovery population and search ledger

Only unlabelled, May–June 2023 UTC payments whose two declared endpoint-bank MD5 parity bits are zero were queried. The primary scope is one placeholder with 3–5 visible banks, or two placeholders with 3–4 visible banks. Endpoints are audited for placeholders. Direct two-bank paths, more than two gaps, larger visible counts and labelled records lie outside this claim.

The first coarse screen inspected gap-start and gap-end shares for v3–7. Then full conditional shapes were compared for v3–5 and g1/2. The original pilot included every one of these six strata as primary and failed the v5/g2 uncertainty requirements. At 1,003 payments the two-gap v5 uniform-shape TV was .033998, 99% upper .079124 against intended ceiling .06. Its TV ratio upper bound was .695493 against .50. This pilot remains in `out/H-B07_gap_placement_pilot.md` with its false decision intact.

Before any July shape outcome, v5/g2 was moved to the explicitly descriptive scope. This is a discovery-informed scope restriction. The original ceilings for the remaining primary strata are retained. One-gap v3/v4/v5 TVs were .001939/.003800/.004024. Two-gap v3/v4 TVs were .010429/.018313 versus iid-slot .177095/.184980. Two-gap adjacency was .677095/.518313, near the composition references .666667/.500000 and above iid references .500000/.333333. Route and month summaries challenge the pooled shape explanation, with low-support cohorts suppressed. They do not replace primary outcomes.

## Frozen internal validation design

The primary confirmation population is July 2023 UTC, the same endpoint-bit0/0 and unlabelled filter, and the same five primary conditional strata. At least 250 payments and 100 declared ordering banks, senders and receivers are required per stratum. Failure in any primary stratum rejects the scoped conjunction.

- All selected v3–5/g1–2 shapes must have zero endpoint placeholders and zero mismatch between stored visible count and non-placeholder path entries.
- For every primary one-gap stratum, the 99th percentile ordering-bank bootstrap upper bound of TV to uniform shape is at most .03.
- For each primary two-gap stratum (v3/v4), that TV upper bound is at most .06 and the 99th percentile ratio of TV(uniform composition) / TV(iid slots) is at most .50.
- Whole ordering-bank resampling uses 1,000 multinomial replicates and deterministic seed 20261116+10v+g. These are conditional sampling sensitivities. Banks can share accounts, path banks and generator state. The per-stratum bounds do not constitute a formal simultaneous confidence guarantee over the search.
- Descriptive controls report month and route for two-gap v3–5 cohorts with the same 250-row/100-bank/sender/receiver gate. The v5/g2 result remains visible whether it fits or fails. No selected sensitivity rescues a failed primary.
- Preserve complete scripts, criteria and negative outcomes. Commit this plan before accessing the new July shape statistics. The program verifies the executable and confirmation-ready plan at the supplied ancestor SHA.

## Prior exposure

Phase 0 exposed full-data structural/count aggregates. B02 inspected gap counts and adjacent-placeholder counts, including July, so the new placement outcome is partly related to previously exposed results. B01/B03/B04/B05/B06 and coordinator Round 1 summaries also expose records or other outcomes in this same dataset. July is a reused population. Only the new conditional shape tables/TVs are unqueried before this freeze. Shared ordering/path banks and accounts prevent an independent holdout claim. Confirmation can at most produce **Supported but not independently confirmed** evidence.

## Confirmation results

Freeze `f28120d22534ea09b8a1015ac910dca4545b6ce3` preceded July conditional-shape queries. The unchanged executable produced a [failed internal result](../../analysis/20_routing_time/out/H-B07_gap_placement_confirm.md). No gate was relaxed afterward.

July has 650,668 source-population payments, 239,333 multibank payments and 49,974 paths with any placeholder. The selected v3–5/g1–2 shape population contains 26,211 payments. Endpoint placeholders and visible-count mismatches are both zero.

All five primary strata meet the minimum row/entity support, but two uniform-TV uncertainty criteria fail. The v4/two-gap upper bound .074385 exceeds .06, and the v5/one-gap upper bound .040449 exceeds .03. This rejects the conjunction even though the two-gap ratio bounds pass.

| Visible banks / gaps | Payments | Ordering banks | TV uniform | 99% upper | Primary decision |
| --- | ---: | ---: | ---: | ---: | --- |
| 3 / 1 | 13,702 | 1,572 | .002700 | .013649 | Pass |
| 3 / 2 | 1,015 | 482 | .013136 | .048945 | Pass |
| 4 / 1 | 7,060 | 1,223 | .009585 | .023502 | Pass |
| 4 / 2 | 680 | 373 | .025000 | .074385 | Fail |
| 5 / 1 | 3,318 | 903 | .021398 | .040449 | Fail |

Descriptively, v3/v4 two-gap adjacency is .662069/.508824 compared with uniform-composition .666667/.500000 and iid-slot .500000/.333333. Corresponding iid-slot TVs are .162069/.175490, with ratio upper bounds .347570/.441859. These conditional point patterns distinguish the simple iid-slot comparator but cannot rescue the failed broader precision claim. The v5/two-gap descriptive TV is .072477, with upper bound .139014. Complete route/month controls, including suppressed cohorts, remain in the report.

The finite cohort and bank-resampling uncertainty are material. No independent validation or exact conditional law is established. July now has explicit conditional-shape exposure for future B work.

## Alternatives and limitations

Bank/corridor composition, nonexchangeable event constructions with the same conditional distribution and direct shape sampling remain plausible. No unique source-code or causal-order claim follows. Small conditional cohorts and reused entities limit precision, as the v5/g2 pilot failure demonstrates.
