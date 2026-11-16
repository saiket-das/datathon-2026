# H-A01: roughly two log units per business party

- **Owner:** A
- **Status:** confirmation-ready
- **Script / exact command / commit:** `uv run python analysis/10_amounts_currency/H-A01_amount_kernel.py`; frozen version is the commit introducing this plan. Confirmation: append `--phase confirm --freeze <SHA>`.
- **Chart:** `analysis/10_amounts_currency/out/H-A01_amount_kernel_confirm.png`

## Proposed rule and scope

For positive, unlabelled payments, changing the counterpart's type from consumer to business is associated with an approximately **2-unit increase in mean log USD amount**, holding the focal account and payment currency fixed. This is an approximately `exp(2)=7.389` geometric scale factor, not a deterministic payment-level multiplier, arithmetic-mean ratio, or identified causal intervention.

Two complementary estimands: beneficiary-type contrast within ordering account/currency, and ordering-type contrast within beneficiary account/currency. An account/currency cell must contain both counterpart types. Compute its difference of mean `ln(USD_AMOUNT)`; average eligible currency contrasts equally within each focal account; then average focal accounts equally. Account types are not changed or pooled across roles. Unlabelled is a selection condition, not a claim of legitimacy. No primary anomaly-class claim is made.

## Test plan (freeze before confirmation)

- **Comparator / effect:** consumer counterpart in the same focal account/currency. Both primary mean log contrasts must lie in **[1.85, 2.15]**, and both two-sided **97.5% account-summary intervals** must lie wholly inside that band. The interval is mean +/- `2.241403 * sample_sd(account contrast)/sqrt(accounts)` (Bonferroni across the two primary contrasts). This corresponds to a practical geometric factor of 6.36–8.58. Report failure if either primary requirement fails; do not shift the band.
- **Uncertainty:** these intervals describe variation across account summaries under account independence. Shared counterparties, banks and generator state can create residual dependence. They are not a network-independent confidence guarantee or proof of the original code. The finite sample contrasts are directly measured regardless of this interval assumption.
- **Controls / alternatives:** compare transaction weighting of matched cell contrasts with equal-account weighting. Focal account controls its stable type, repeated-customer scale and one endpoint's geography; currency controls the USD-normalisation mixture. Separately hold both endpoint-bank countries fixed; this tests whether counterpart country composition explains the association. It does not equate bank country to residence.
- **Falsification / exceptions:** report negative account contrasts and the share farther than one log unit from 2; do not suppress heterogeneous or reversed accounts. If the mean replicates but geography controls overturn it, retain only the narrower account/currency association. No lognormal distribution, exact common variance or 2-unit individual-account law is predeclared.
- **Partition:** shared `partition_sql('accounts')`: bit of an identifier is `(('0x'||substr(md5(identifier),1,8))::UBIGINT % 2)`. Explore iff both ordering and beneficiary bits are 0; confirm iff both are 1; crossing bits excluded. No reroll. SHA-256 of local Parquet: `474ac30afd6378253fabd40c1f3ecd704ef5cd839947050b03bd1cf61fc2def3`.
- **Coverage / audit:** shared scientific audit: 2,579,943 explore, 2,416,730 confirm, 5,003,327 excluded; zero shared record IDs or account strings in either role; 6,873 shared endpoint banks and 7,343 shared visible path banks. Currency TV 0.053469, party-pair TV 0.011575, route TV 0.003858; calendar/file-block and anomaly support reviewed in the shared report. These describe candidate partition composition, not target confirmation effects.
- **Eligible discovery support:** 2,578,169 positive unlabelled exploration payments; 153,991 ordering and 741,137 beneficiary accounts. Primary beneficiary contrast covers 65,319 senders and 2,325,234 matched payments (90.19% of unlabelled explore); ordering contrast covers 44,881 receivers and 1,248,585 matched payments (48.43%). Supports overlap and must not be added.
- **Primary confirmation:** run the committed script unchanged on account-bit-one data, with `--freeze <SHA>`; report eligible support and both fixed acceptance flags. The script verifies the scripts match the freeze commit and both hypothesis plans exist in it.
- **Separate robustness:** remove the busiest 1% of ordering accounts, ranked by unlabelled volume (identifier breaks ties locally); rerun both contrasts. Also rerun within each of May, June, July; within Direct, Indirect, Covered; and within focal account/currency/endpoint-country corridor. These are subsets of the primary account partition, not alternate independent holdouts. Primary thresholds are descriptive benchmarks for these sensitivity results, not additional adjusted confirmatory tests. No full time- or bank-scheme outcomes will be queried.
- **Freeze time / prior exposure:** prepared 16 Nov 2026, Malaysia time; exact SHA/time will be recorded immediately after committing and before confirmation. Phase 0 and the shared foundation already exposed full-data party-pair medians, whole-amount frequency, account consistency, structural FX comparisons, partition coverage and composition. No investigator B/C branch, PR or provisional finding was read. Only selected exploration rows informed this rule.

## Discovery evidence

All SQL, denominators, comparisons and exceptions: [exploration report](../../analysis/10_amounts_currency/out/H-A01_amount_kernel_explore.md).

- Unlabelled pair median USD amounts: BB 22,834.77; BC 3,103.76; CB 3,242.05; CC 469.305. These alone are confounded by currency and entity mix.
- Primary equal-account contrasts: beneficiary business **2.011733** (97.5% interval 1.994602–2.028864; **7.476x**); ordering business **1.959472** (1.935386–1.983558; **7.096x**).
- Matched transaction-weighted contrasts: 1.997937 and 1.947393. After fixing endpoint-country corridor: equal-account contrasts 2.001570 and 1.988216. Removing top-volume senders: 2.011740 and 1.938607. All planned discovery sensitivity intervals fit the band.
- Individual-account counterexamples are substantial: **12.59% / 16.64%** have negative contrasts, and **52.89% / 58.71%** differ from 2 by more than 1. Reject the stronger deterministic individual-account interpretation. Sampling noise and heterogeneous customer behaviour remain alternatives.

### Search ledger

Initial broad comparisons: party-pair log quantiles, currency/pair means and variances, repeated amount masses. Pooled log SD is about 2.29 and within-currency SD often about 2.1; currency mixing matters. Moved to within-account/currency comparisons and then checked country corridor, concentration, month and routing. No confirmation outcomes or alternate-scheme robustness outcomes informed these choices. The original generator's distribution family remains untested.

## Confirmation and robustness results

Pending frozen commit and unchanged test. Append results without changing the plan above.

## Assessment

Exploratory evidence supports an approximate mean-log scale rule. No causal direction, exact generator code or payment-level guarantee is established. Confirmation remains conditional on known full-data exposure.

## Real-world explanation (interpretation, not evidence)

Business invoices may have larger typical scale than household transfers. An alternative is currency/country composition or a few large customers; matching and concentration checks address parts of those explanations. A fixed factor near `e^2` may simply be a synthetic design parameter rather than an economic constant.
