# H-A11 — Single-transition FX residuals concentrate on sparsely observed pairs

- **Owner:** A
- **Status at freeze:** ready for reused-account internal validation
- **Command:** `uv run python analysis/10_amounts_currency/H-A11_fx_transition_residuals.py`

## Proposed rule and scope

On unlabelled July multibank payments with exactly one H-A03 class change
and all visible country classes mapped, the recorded count equals one
whenever the directed country pair at that change has sufficient two-bank
support. Unsupported directed pairs should have a nontrivial zero-FX rate.
Exactly one transition gives an unambiguous candidate edge. This does not
identify residual causes on paths with multiple class changes.

## Test plan

- Retain the H-A03 account-bit-0 graph fitted across all dates. Define
  directed support as at least 100 unlabelled pre-July bit-0 two-visible-bank
  payments with the literal ordered countries of the sole scored
  transition. The reference group has fewer than 100 such payments.
- Score eligible unlabelled July multibank bit-1 records with exactly
  one learned transition. Exclude labelled, cross-bit and unmapped rows
  and paths outside that scope. Develop on bit-0 only.
- Acceptance requires at least 80% of scoped paths with supported
  transitions, zero supported FX counts different from one, zero counts
  above one in scope, at least a 1% zero-count rate among unsupported
  transitions and at least 100 senders, receivers and ordering banks
  in the unsupported group. Any failed condition rejects the frozen
  claim as stated. These are finite-population criteria.
- The comparator is the same H-A03 count on unsupported transitions,
  keeping predicted FX at one. Also show the transferred pre-July
  observed two-bank zero rate in supported pairs and descriptive
  route strata at the report's support floor. No bank or country-pair
  identity is exported. Positive event counts below 100 are masked.
- Preserve the executable and both helper versions in the freeze.
  Routing composition, within-class country heterogeneity and missing
  edges in the training graph remain possible explanations. Support
  is not a randomized factor. No adjustment to the upper bound follows.

## Discovery and prior exposure

July bit-0 has 41,071 scoped records with 102 residuals. Supported
transitions account for 36,621 payments with zero errors. The other 4,450
payments have a 2.29% zero-count rate and involve 3,021 senders, 3,582
receivers and 1,220 ordering banks. The supported group's transferred
two-bank zero rate is zero. Route cells overlap the primary results.
These findings select this narrow population and threshold.

Phase 0 and A01/A02 revealed full-data structure and reused account outcomes.
A03/A05 revealed count errors and their one-sided sign on the same bit-1
multibank data. A04 tested gaps in exploration. A06/A08 revealed July bit-1
currency and path associations and A07 tested alternatives in bit-0.
A09/A10 covered amount scaling. None of those reports cross-tabulated
this directed support flag and the zero residual on July bit-1.
Dates, country pairs, banks and callbacks between network entities can
overlap. This is a frozen internal outcome comparison on reused records.

## Confirmation and robustness results

Frozen at `33bb0c0f921719c2f04bfc5debc18aad043ade8a` on 16 November 2026
at 21:38:27 MYT. Run the script with `--phase validate --freeze` and that SHA.
The unchanged test passed every criterion. Among 39,086 scoped July
bit-1 payments, 34,714 had a supported transition (88.81%) and each
recorded exactly one conversion. All 100 zero-count residuals occurred
among the 4,372 unsupported payments (2.29%). This latter population
contains 3,163 senders, 3,698 receivers and 1,253 declared ordering banks.
There were zero counts above one. The [aggregate report](../../analysis/10_amounts_currency/out/H-A11_fx_transition_residuals_validate.md)
retains descriptive route groups and masks positive small cells.

## Assessment

The support split identifies where the upper bound is loose in this
single-transition July population. Rare support can reflect under-learned
class equivalence, unmeasured route attributes or a reporting rule.
Class changes on more complex paths still have unresolved residuals.
