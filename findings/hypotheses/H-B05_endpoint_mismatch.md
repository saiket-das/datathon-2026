# H-B05: Approximate joint 5% endpoint disagreement law

- **Owner:** B
- **Status:** confirmation-ready
- **Evidence level:** Exploratory before frozen temporal validation.
- **Script:** `uv run python analysis/20_routing_time/H-B05_endpoint_mismatch.py --phase explore`.
- **Validation:** replace `--phase explore` with `--phase confirm --freeze <SHA>`.

## Proposed rule and scope

In the selected unlabelled population, the two indicators comparing declared endpoint banks with the first and last visible path entries approximately follow two independent Bernoulli(.05) draws at the pooled payment level. The four predicted probabilities for neither, ordering only, beneficiary only, and both are .9025, .0475, .0475, and .0025. The hypothesis concerns the observed distribution of the two flags. Which representation changed, the identity selection process, subgroup homogeneity, and generator ordering remain open.

## Test plan (freeze before validation)

- Population: records without an anomaly label and with both declared endpoint bank MD5 bits zero, where bit is `(('0x'||substr(md5(bank),1,8))::UBIGINT % 2)`. Compare the first and last semicolon-delimited BIC8_PATH entries to the two declared banks. Validate on July 2023. Develop on May–June 2023. April falls outside both windows.
- All criteria must pass: at least 100 validation sender accounts, receiver accounts and declared ordering banks, no unscorable endpoint comparisons, both flag marginal 99% cluster intervals wholly within [.045,.055], 99% interval for excess joint rate (joint minus product of observed marginal rates) wholly within [-.00075,.00075], and total variation from the fixed four-cell law with 99% upper bound ≤.0075. These are practical tolerances. Successful pooled results do not establish exact probabilities or conditional independence.
- Bootstrap 1,000 whole declared ordering-bank count vectors with the existing deterministic seed 20261116. The interval is a bank-sampling sensitivity under possible shared receiver, intermediary bank and account dependence. Audit actual month-to-month overlap in distinct same-role senders, receivers, both-role account strings, declared endpoint banks and visible path banks. Months exclude common source rows by construction.
- Show descriptive sensitivities by route and party pair with aggregate support. Do not use subgroup results to rescue a failed primary test. Contrast joint count with a disjoint single-endpoint error model which predicts zero joint events. Inside mismatch subsets, report same-country and opposite-path-endpoint equality only with 100 or more records and senders and receivers. Those comparisons constrain within-country remapping and endpoint swapping as sole explanations, but do not identify how source BIC values were generated.
- Pilot alternatives: quick tests for conspicuous duration rounding showed roughly 20% durations divisible by five in all three routes, too weak a lead to select over endpoint disagreement. UTC hour/day summary differed by day and party type, but requires explicit calendar/composition work.

## Discovery evidence and prior exposure

Before selecting the test, May–June bit0/0 rates were 5.0163% ordering and 5.0176% beneficiary on 1,005,689 Direct payments, joint 0.25117%. For 528,669 Indirect payments the corresponding rates were 4.9876%, 4.9674%, and 0.23852%. For 58,684 Covered they were 5.6898%, 5.0167%, and 0.27776%. Covered ordering disagrees more often than the common 5% rule suggests. The primary claim is pooled, and subgroup heterogeneity remains visible. Mismatched banks kept the path endpoint country only about 4.7–5.7% of the time and equalled the opposite endpoint only about 0.2–1.1% of the time in this screen.

The executable exploration report pools 1,593,042 payments. Ordering and beneficiary mismatch are .05031569 and .05000873, the joint rate is .00247953 across 3,950 payments, and fixed-law total variation is .00036535. These estimates informed selection of the model. Conditioning on both declared bank bits can change bank composition and the apparent mismatch law. Generalisation to other partitions is unresolved.

Phase 0 and Round 1 exposed full-data and partition summaries, including endpoint disagreement and route composition. B04's all-period exploratory endpoint summaries also include July within this same bank subset, so July records and marginal information were previously exposed. The July-only joint table and B05 uncertainty were not examined before freeze. A successful unchanged test is **Supported but not independently confirmed**. Neither month holds out banks or accounts.

## Confirmation and assessment

Pending. Retain failed criteria and limitations without tuning.

## Real-world explanation (interpretation only)

A representation process could introduce disagreement independently at each endpoint, or both representations could carry different bank identities by construction. The joint flag law does not resolve direction or mandate a specific replacement draw.
