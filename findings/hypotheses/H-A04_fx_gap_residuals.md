# H-A04: Do path gaps concentrate FX-count residuals?

- **Owner:** A
- **Status:** exploratory. The gap explanation lacked support in the displayed comparison groups.
- **Reproduce:** `uv run python analysis/10_amounts_currency/H-A04_fx_gap_residuals.py`
- **Evidence:** [Aggregate exploration report](../../analysis/10_amounts_currency/out/H-A04_fx_gap_residuals_explore.md)

## Proposed rule and scope

If removing placeholders obscures opportunities to count FX transitions, gapped
paths should show materially more errors than gap-free paths of comparable route
and visible-bank count. The population is unlabelled multibank payments with
both account bits zero. H-A03's learned country groups, eligibility and predicted
FX count are reused unchanged. A gap is a positive prepared gap count.

## Test plan (freeze before confirmation)

The current executable is exploration only. It compares signed errors by gap
within route and visible-bank count (3, 4, 5+), with pooled results for context.
This comparison partly controls the number of opportunities to accumulate error.
Route composition, true hidden bank count, bank mix, and count recording rules
remain alternatives. Displayed subgroups require 1,000 payments and 100 distinct
senders and receivers. Positive error counts below 100 are masked.

The investigator already saw Phase 0 full-data structural summaries, Round 1
amount/rounding exploration and account-confirmation outcomes, and H-A03's
exploration and internal-validation aggregate outcomes. This run queried only
both-account exploration records. Future tests on previously used records require
explicit reuse disclosure and cannot be described as independent confirmation.
Before any validation, commit a new comparator, practical tolerance, fit/score
population, negative controls and overlap audit. None has been frozen here.

## Discovery evidence

Of 947,930 multibank payments, 934,229 were eligible. Exactly 3,594 predictions
disagreed, all overpredictions. The pooled error rate was 0.4060% with a gap
(465/114,528) and 0.3817% without (3,129/819,701). Within supported Indirect
length groups, the rates with versus without gaps were respectively
0.2978% vs 0.3201%, 0.4642% vs 0.4668%, and 0.6269% vs 0.6287%.
Covered gap cells had too few errors to display the corresponding rates.

## Confirmation and robustness results

No validation outcome was queried. The earlier H-A03 frozen failure stands.

## Assessment

The displayed within-length Indirect comparisons do not support the proposed
gap concentration. Suppressed groups and the absence of an uncertainty analysis
limit this check. The one-sided errors are an exploratory clue. A follow-on
question could test whether a context-dependent suppression rule or missing
country equivalences explain them. No revised generating rule is accepted.

## Real-world explanation (interpretation, not evidence)

A payment can cross currency regions without a conversion at every step.
Alternatively, the inferred classes may split actual shared-currency groups,
or the FX-count field may follow a recording convention. The current comparison
cannot distinguish these explanations.
