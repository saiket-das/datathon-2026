# Amounts and currencies (owner A)

Columns: `USD_AMOUNT`, `CURRENCY_CODE`, `ORDERING_TYPE`, `BENEFICIARY_TYPE`, `CURRENCY_CONVERSION_COUNT`.

Starting questions:
- What distribution does the amount follow for each sender/receiver type pair, and does currency change it once the pair is held fixed?
- Are round amounts round in USD or in the original currency?
- What decides how many currency conversions a payment has?

## Independent A investigation

| Hypothesis | Script and evidence |
|---|---|
| [H-A01: approximate business-party amount factor](../../findings/hypotheses/H-A01_amount_kernel.md) | `H-A01_amount_kernel.py`; `out/H-A01_amount_kernel_explore.md`, `out/H-A01_amount_kernel_confirm.md` and confirmation PNG |
| [H-A02: EUR daily scaling and rounding](../../findings/hypotheses/H-A02_usd_rounding.md) | `H-A02_usd_rounding.py`; `out/H-A02_usd_rounding_explore.md`, `out/H-A02_usd_rounding_confirm.md` and PNGs |

Default commands run exploration only. Confirmation requires `--phase confirm --freeze <SHA>`.
Exact plans, partition restrictions, prior exposure, failed alternatives and results belong in
the hypothesis records. `test_value_mechanisms.py` uses invented data only; run `uv run pytest`.

## Round 2

[H-A03: latent country classes and FX steps](../../findings/hypotheses/H-A03_fx_country_classes.md)
uses `H-A03_fx_country_classes.py --phase explore`; internal validation requires
`--phase validate --freeze SHA`. Reports are `out/H-A03_fx_country_classes_*.md`.
[Progress and limitations](../../docs/11_a_round2_progress.md). Round 1 files remain unchanged.

[H-A04: FX residuals and path gaps](../../findings/hypotheses/H-A04_fx_gap_residuals.md) is exploration only. Run H-A04_fx_gap_residuals.py for grouped signed errors and gap comparisons.

[H-A05: tighter FX upper bound](../../findings/hypotheses/H-A05_fx_repeat_classes.md) tests the H-A03 class-change count as a bound and records the failed repeat-class alternative.

[H-A06: endpoint currency association](../../findings/hypotheses/H-A06_currency_endpoint.md) compares country-specific modal currency predictors on the same score rows, with paired bank-cluster sensitivity.

[H-A07: currency exceptions](../../findings/hypotheses/H-A07_currency_exceptions.md) is an exploration-only comparison of receiving-country alternatives within first-path-country modal errors.

[H-A08: visible-path currency set](../../findings/hypotheses/H-A08_path_currency_set.md) uses exact-set currency-frequency and shifted-map controls before its frozen internal test.

[H-A09: modal scale co-movement](../../findings/hypotheses/H-A09_modal_scale_coherence.md) records the weak common-factor candidate.

[H-A10: cross-denomination scaling](../../findings/hypotheses/H-A10_cross_denomination.md) evaluates CHF and GBP grids learned from large amounts on small amounts.

[H-A11: FX transition support](../../findings/hypotheses/H-A11_fx_transition_residuals.md) compares supported and sparse directed pairs on one-transition paths.

[H-A12: conditional log-amount shape](../../findings/hypotheses/H-A12_log_shape.md) compares trained standardization against equal-variance reference shapes.

[H-A13: reciprocal daily scale updates](../../findings/hypotheses/H-A13_daily_scale_updates.md) tests a bounded update approximation across separate account samples on shared dates.

[H-A14: adjacent currency-mode changes](../../findings/hypotheses/H-A14_currency_class_disagreement.md) tests an FX count based on pre-July currency modes.

[H-A15: recorded currency as an endpoint state](../../findings/hypotheses/H-A15_payment_currency_insertion.md) records failed endpoint alternatives on exploration data.

## Round 3

- [H-A16: FX support gaps](../../findings/hypotheses/H-A16_fx_support_gaps.md) audits exclusions and compares strong, weak and partial mode coverage.
- [H-A17: fractional denomination grids](../../findings/hypotheses/H-A17_fractional_denominations.md) compares aligned tenth-unit rates with shifted dates and translated phases.
- [H-A18: USD heaping shape](../../findings/hypotheses/H-A18_usd_heaping_shape.md) checks whole-dollar and significant-digit overlap by amount and party type.
- [H-A19: UTC scale boundary](../../findings/hypotheses/H-A19_utc_scale_boundary.md) compares neighboring date scales near UTC midnight.
- [H-A20: cross-route mode transfer](../../findings/hypotheses/H-A20_route_mode_transfer.md) tests maps learned separately on two-bank and multibank payments.

[H-A21: country amount context](../../findings/hypotheses/H-A21_country_amount_context.md) compares a first-path-country residual correction with currency/party, receiver and rotated-country baselines.

[H-A22: USD quantization levels](../../findings/hypotheses/H-A22_usd_quantization_levels.md) screens nested grids and preferred decimal mantissas without assuming mixture weights.

[H-A23: preferred USD five anchor](../../findings/hypotheses/H-A23_preferred_five_anchor.md) tests a local-density-normalized point-mass constraint with a matched neighboring-anchor control.

[H-A24: party-type scale transfer](../../findings/hypotheses/H-A24_party_scale_transfer.md) preserves the failed stringent EUR re-extraction threshold and factor-five ambiguity.

[H-A25: scaled preferred five](../../findings/hypotheses/H-A25_scaled_five_anchor.md) tests preferred denominations in CHF, EUR and GBP with fitted scales, disjoint amount ranges and neighboring-anchor controls.
