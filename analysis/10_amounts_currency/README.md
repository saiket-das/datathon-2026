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
