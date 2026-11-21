# H-A15 — Payment currency as an endpoint path state

- **Owner:** A
- **Status:** exploration only. Tested endpoint substitutions fail.
- **Command:** `uv run python analysis/10_amounts_currency/H-A15_payment_currency_insertion.py`

## Proposed mechanism and alternatives

When recorded currency differs from the first path-country mode, consider
three observable models for how it enters the FX count. Substitute recorded
currency for the first mode, substitute it for the last mode, or prepend it
to the visible currency-mode path. Compare errors against adjacent mode
changes without substitution. These models do not cover all ways recorded
currency might influence unobserved states or route selection.

## Discovery evidence

Learn modal currencies from unlabelled pre-July both-account bit-0 data
by first visible country with at least 100 training payments. Select the
lexically first currency on a tie. Score unlabelled July bit-0 paths with
at least two visible banks and all countries mapped. Of 749,066 scoped
payments, 747,835 were mapped and 49,529 differed from their first-country
mode. The latter included 20,426 senders, 29,718 receivers and 3,473 declared
ordering banks. The geography count made zero observed errors. First
substitution made 31,444 errors, last substitution 10,173, and prepending
49,529. First substitution repaired zero rows. Direct, Indirect and Covered
strata show the same ordering of geography versus the alternatives.
[Aggregate report](../../analysis/10_amounts_currency/out/H-A15_payment_currency_insertion_explore.md).

## Exposure and assessment

Phase 0, A03/A05/A11 and A06/A08/A14 already exposed related path, FX and
currency outcomes. The screen uses the previously explored July population
and an overlapping map, so there is no frozen confirmation or uncertainty
claim. It gives finite-sample counterexamples to treating payment currency
as a mechanically substituted endpoint state. How payment currency and
route geography are jointly assigned remains open.
