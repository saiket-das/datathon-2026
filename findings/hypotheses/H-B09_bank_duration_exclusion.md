# H-B09: Persistent bank-associated exclusion of short durations

- **Owner:** B
- **Status:** supported but not independently confirmed
- **Evidence level:** Supported but not independently confirmed
- **Discovery command:** `uv run python analysis/20_routing_time/H-B09_bank_duration_exclusion.py --phase explore`
- **Internal validation:** same script with `--phase confirm --freeze SHA`

## Proposed rule and scope

Some visible banks have a persistent association with total durations of at least 100 seconds. Infer an exclusion-bank set from May Direct payments: a bank must appear at least 100 times and appear in zero payments with TOTAL_DURATION<100. Bank counts include each visible occurrence in a Direct path. Other banks with at least 100 appearances form the non-exclusion supported set.

For unlabelled payments with 2–5 visible occurrences and both declared endpoint-bank MD5 bits zero, evaluate only paths for which every visible bank is supported in May. The proposed near-exclusion signature predicts a duration below 100 seconds in at most 0.1% of eligible paths containing an exclusion bank. No converse requirement is made for paths using other banks. Placeholders are removed only for matching the visible-bank identities.

This signature could reflect a persistent bank attribute, bank group, geography, a shared generator label or another bank-associated state. The data do not establish that a literal service delay is caused by visiting a bank. The signature differs from rejected B01 mean-additive duration transfer and does not rehabilitate that frozen hypothesis.

## Exploration and alternatives

First, route-level log amount/log duration correlation was close to zero in May–June and no duration was zero or negative in the screened unlabelled routes. Fixed thresholds 100/600/1,800 seconds and visible counts showed substantial duration heterogeneity. A broad exploratory unnest-and-row-group aggregation exceeded the 512MB cap and produced no path-class results. Fixed-position joins then completed within the cap.

Initial narrower June screens used May Direct banks with at least 100 fast observations versus banks with no fast observations. Any no-fast-bank class had zero sub-100-second payments across the supported two- and three-bank cohorts. The final supported set uses all banks with >=100 May Direct appearances, and the no-fast requirement only for the exclusion set. This broader pilot is preserved in the report.

There are 1,061 supported May banks, of which 440 are exclusion banks. June evaluation has 891,959 v2–5 payments, with 646,066 eligible (72.4323%). Among the 209,343 eligible paths containing an exclusion bank, zero have duration<100. The 436,723 other eligible paths include 378,116 sub-100 durations (86.5803%). They show that absence of an exclusion bank does not force duration below 100 seconds.

A pre-validation bank-label permutation within May exposure bins [100,300), [300,1000), [1000,3000), [3000,10000), [10000,infinity), seed20261116, preserves the number of exclusion labels in each bin. Its 249,860 exclusion-labelled paths have a 41.4656% fast share. This is a falsification control for bank identity within coarse exposure support, without a randomisation-test interpretation. Correlated bank attributes and geography can still matter.

The zero-exception result holds in each supported route/visible-count cell. Source support and coverage change under this selection, and unsupported banks, labelled payments, v>5 and other partition schemes remain outside scope.

## Frozen internal test

Keep the May fit unchanged and evaluate July, with UTC half-open range [2023-07-01,2023-08-01). The whole dataset had earlier Phase0/other-investigator exposure. All criteria below are required before labelling the internal test supported:

1. May-supported paths retain at least 50% of the July v2–5 population.
2. At least 5,000 eligible exclusion paths, 100 declared ordering banks, 100 senders and 100 receivers.
3. At most .001 of eligible exclusion paths have TOTAL_DURATION<100.
4. The one-sided 99% Clopper–Pearson upper bound on the fraction of declared ordering banks with any fast exception is at most .03. The all-zero formula is 1−.01^(1/K). This bound assumes independent ordering-bank units and is reported with the known shared-visible-bank dependency limitation.
5. The exposure-bin permutation control also has at least 100 payments, ordering banks, senders and receivers, and its fast share exceeds the real-label fast share by at least .10.

Report the other supported-bank cohort, each adequately supported route/length subgroup and overlapping senders/receivers/ordering banks versus the full May Direct cohort. All eligible visible banks are training banks by construction. No subgroup may rescue a failed pooled test. The thresholds are practical discovery-informed requirements and do not establish exact exclusion outside the evaluated records. Freeze complete plan and executable before the new July bank-duration outcomes.

## Exposure and limitations

Phase0 full-data summaries, Round1 B01 duration outcomes and all other Round1 summaries were exposed. B04–B06 and B07 use reused July bank/account records or other outcomes; B07 conditional placement outcomes are now exposed. The June bank-duration pilot is development evidence. The new July exclusion-bank fast counts are unqueried before freeze, but July records and many duration statistics have already been examined. Only a reused-population internal test can follow.

Either-role accounts, currencies, counterparties, path banks and text can remain shared. The estimate cannot identify exact original code, a bank-delay distribution, source-stage order, a causal effect or unseen-bank transfer. A successful result would support a persistent bank-associated duration constraint. Retain B01's rejection and all pilot resource failures.

## Frozen internal result

Freeze `399a3dd62f9cbcac3e0869585cb2a49c10f7d578` preceded July B09 evaluation. The unchanged executable [passed all criteria](../../analysis/20_routing_time/out/H-B09_bank_duration_exclusion_confirm.md).

- July contains638,824 v2–5 population payments, of which462,931 have every visible bank supported in May (72.4661%).
- The150,010 eligible paths containing an exclusion bank have zero duration<100 observations, across1,325 declared ordering banks,32,968 senders and69,913 receivers. The one-sided affected-ordering-bank upper bound is.00346957 under its stated independence assumption.
- The remaining312,921 eligible paths have270,933 fast durations (86.5819%). Thus an all-other-bank path can still take at least100 seconds.
- The exposure-bin permutation has73,994 fast durations among178,992 exclusion-labelled paths (41.3393%), a41.3393-point difference from real bank labels.
- Every supported displayed route/length cell has zero fast exceptions. The script omits a route/length cell when row or entity support is inadequate. Omission is not evidence that a route is absent.
- Full eligible evaluation versus May Direct shares38,348 same-role senders,45,484 same-role receivers and1,725 declared ordering banks. All1,061 fitted visible banks recur, by construction.

This supports a persistent bank-associated duration exclusion on eligible reused records. The mechanism may reside in bank attributes or correlated generator state. It does not prove a literal service-delay floor or original duration aggregation rule. July bank-duration class outcomes are now exposed for later work.
