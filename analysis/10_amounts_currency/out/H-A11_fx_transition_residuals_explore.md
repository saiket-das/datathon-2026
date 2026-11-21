# H-A11 — Single-transition FX residuals

Freeze: exploration.
512MB; one thread; no disk spill. Aggregates only.
Both-account bit-0 exploration only. A03–A08 outcome exposure applies.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## July multibank residuals by pre-July directed two-bank evidence

| training | route | n | senders | receivers | banks | residuals | residual_share | above_class | transferred_two_bank_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | All | 41071 | 16041 | 25237 | 3033 | 102 | 0.0024835041756957462 | 0 | 0.0 |
| No zero FX in two-bank training | All | 36621 | 14489 | 22648 | 2797 | 0 | 0.0 | 0 | 0.0 |
| No zero FX in two-bank training | Covered | 4226 | 1988 | 3277 | 591 | 0 | 0.0 | 0 | 0.0 |
| No zero FX in two-bank training | Indirect | 32395 | 13541 | 20512 | 2728 | 0 | 0.0 | 0 | 0.0 |
| Unsupported | All | 4450 | 3021 | 3582 | 1220 | 102 | 0.02292134831460674 | 0 | None |
| Unsupported | Indirect | 4060 | 2802 | 3302 | 1174 | <100 | None | 0 | None |

## Frozen decision and support

| support_share | unsupported_senders | unsupported_receivers | unsupported_banks | all_criteria_met |
| --- | --- | --- | --- | --- |
| 0.8916510433152346 | 3021 | 3582 | 1220 | True |

The existing H-A03 graph uses all bit-0 two-bank dates. Only the directed two-bank rates in this diagnostic use pre-July dates. Undisplayed small cells remain in the pooled denominator. No country pair or bank identity is exported.
