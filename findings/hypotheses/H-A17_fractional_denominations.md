# H-A17 — Fractional denomination grids after scaling

- **Owner:** A
- **Status:** exploratory. A broad tenth-unit component did not clear its controls.
- **Command:** `uv run python analysis/10_amounts_currency/H-A17_fractional_denominations.py`

## Proposed mechanism and tests

A second denomination regime might round to fractional units before
multiplying by the date-specific scale. Compare half-, quarter- and
tenth-unit grid fits outside the same-day whole-unit grid. Fit scales only
on unlabelled bit-0 amounts in [10,000, 2,000,000), using A10's highest
supported decade and exact mode. Evaluate amounts in [10,900) on dates
with rates available both then and seven supported dates later. CHF,
EUR and GBP are the scoped currencies.

Off-unit analysis pairs both rates on exactly the same eligible rows.
The first broad table includes unconditional fits for context. In
exploration, the shifted date produced fewer incremental tenth-unit
hits (7.04%, 7.84%, 6.81%) than own-day rates (9.14%, 9.31%, 9.53%;
22,505, 108,847, 36,434 off-unit payments respectively). A same-scale
half-step translation fits roughly 10% but includes ten points per
unit, compared with nine after excluding integers. The revised controls
delete either the .05 or the .95 phase to match opportunity at nine
points. The readout retains both the full translation and these
opportunity-matched controls.

## Falsification and limits

Against both matched phase controls the practical improvement criterion
was a 99% lower sensitivity bound of at least 0.5 points in each currency.
No currency cleared both controls. The .05-deletion lower bounds were
−0.56, −0.16, and −0.10 points (CHF, EUR and GBP). We used 1,000 circular
seven-observed-date blocks within each currency, seed 20261117, as
a sensitivity analysis rather than a formal interval on model parameters.
The date-shift advantage by itself cannot identify a tenth-unit regime.
Half- and quarter-unit fits also remain ambiguous. No confirmation ran.

This is exploratory bit-0 only. A02/A10 exposed known rounding geometry
and populations in both account sets. A13 exposed shared daily factors.
This does not isolate a fresh period, bank network or latent process.
[Full aggregate evidence](../../analysis/10_amounts_currency/out/H-A17_fractional_denominations_explore.md).
