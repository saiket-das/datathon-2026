# H-A18 — USD decimal-place and significant-digit heaping

- **Owner:** A
- **Status:** exploratory. A single universal one-digit rounding rule is inadequate.
- **Command:** `uv run python analysis/10_amounts_currency/H-A18_usd_heaping_shape.py`

## Proposed mechanism and checks

Whole-dollar heaping might arise from a common significant-digit rule or
from distinct levels of quantization. Count integer amounts, noninteger
half dollars and amounts compatible with one or two significant digits by
USD magnitude and party pair. The amount-dependent place uses the observed
positive amount. Use grouped calculations with at least 2,000 payments
and 100 distinct senders and receivers. USD avoids the inferred conversion
scale. The half-dollar comparison is a descriptive terminal-digit control.

## Exploration and limits

July unlabelled both-account bit-0 provides 129,847 positive USD payments,
22,229 senders and 64,869 receivers. Pooled displayed decades from $10
through under $10 million cover 129,002 rows. For $1,000 through under
$100,000, whole-dollar shares are 38.31% and 38.04%, while one-digit
shares are 12.93% and 12.49%, and two-digit shares 16.48% and 15.72%.
Half-dollar shares are 0.65% and 0.60%. Within the $1,000 decade, the
displayed party-pair integer shares range from 37.30% to 40.55%.

The wide separation of the nested predicates is inconsistent with every
payment coming from a single one- or two-significant-digit rule. Chance
alignment, native integer rounding, rounding to other significant digits
or a mixture can all contribute. The estimates condition on the observed
decade, which rounding itself can change. No formal model, uncertainty
or new validation claim. A02 and A10 already exposed strong rounding
and some magnitude summaries. This experiment adds paired party strata
and count denominators on the previously explored bit-0 population.
[Full aggregate evidence](../../analysis/10_amounts_currency/out/H-A18_usd_heaping_shape_explore.md).
