# H-A22 — USD quantization levels and preferred mantissas

Owner A. Exploratory only; no validation query or mixture fit.

Command: `uv run --locked python analysis/10_amounts_currency/H-A22_usd_quantization_levels.py`.

## Question and population

A18 ruled out a universal one- or two-significant-digit quantizer. Inspect
nested grid increments and leading-digit point masses to determine whether
a more precise rounding constraint is worth testing. Select positive,
unlabelled July USD payments in both-account bit-0. Scope129,847 payments,
22,229 senders and64,869 receivers. Select observed decades2 through6:
123,641 payments; exclude6,206 outside those decades. All published digit
families pass100-payment and100-entity support checks, including their
non-point-mass complements. No small digit family is selectively printed.

## Evidence and alternatives

Across observed decades3,4,5, one-significant-digit compatibility remains
12.53–12.93%, while whole-dollar compatibility is37.66–38.31%. Additional
second-significant-digit compatibility is2.88–3.56%. These overlapping
grid fractions do not identify mixture probabilities.

The pooled selected decades have4,116 exact one-significant-digit values
in the leading-5 bin (12,404 total), versus685/10,819 in leading4 and
569/7,489 in leading6. Leading1 has7,682/40,575. A preferred mantissa5
is a promising explanatory constraint. However, those bins place point
masses at the lower boundary and have unequal smooth density; decimal
boundary crossings particularly affect mantissa1. They do not yet test
a specific quantizer. Fixed standard values, preferred rounding anchors,
amount-dependent rounding and latent mixture components remain alternatives.

Next evidence: compare exact mantissa5 mass with nearby non-point mass
on symmetric windows and neighboring anchors4/6; use7 versus6/8 as a
negative comparison. Freeze a new complete design before bit-1 scoring.
Do not tune A21 after its failed criterion.

## Exposure and confidentiality

Phase0/Round1 full-data summaries and A02/A10/A18 rounding outcomes are
already exposed. A19 examined UTC daily alignment, A09/A13 rate movement,
and A21 amount-country prediction. This screen is bit-0 only and adds no
independent holdout. USD requires no inferred rate or date scaling here.
The script uses512MB, one thread, no spill, and exports grouped counts
and compatibility shares without identifiers. The original script's
initial parser error was corrected before its first successful output;
it did not query any validation population.

[Full aggregate screen](../../analysis/10_amounts_currency/out/H-A22_usd_quantization_levels_explore.md).
