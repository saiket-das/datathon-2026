# H-A11 — Single-transition FX residuals

Freeze: 33bb0c0f921719c2f04bfc5debc18aad043ade8a.
512MB; one thread; no disk spill. Aggregates only.
Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## July multibank residuals by pre-July directed two-bank evidence

| training | route | n | senders | receivers | banks | residuals | residual_share | above_class | transferred_two_bank_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | All | 39086 | 15866 | 24770 | 3056 | 100 | 0.002558460829964693 | 0 | 0.0 |
| No zero FX in two-bank training | All | 34714 | 14122 | 22058 | 2757 | 0 | 0.0 | 0 | 0.0 |
| No zero FX in two-bank training | Covered | 3580 | 1984 | 2959 | 582 | 0 | 0.0 | 0 | 0.0 |
| No zero FX in two-bank training | Indirect | 31134 | 13179 | 20132 | 2683 | 0 | 0.0 | 0 | 0.0 |
| Unsupported | All | 4372 | 3163 | 3698 | 1253 | 100 | 0.022872827081427266 | 0 | None |
| Unsupported | Indirect | 3991 | 2953 | 3400 | 1202 | <100 | None | 0 | None |

## Frozen decision and support

| support_share | unsupported_senders | unsupported_receivers | unsupported_banks | all_criteria_met |
| --- | --- | --- | --- | --- |
| 0.8881440925139437 | 3163 | 3698 | 1253 | True |

The existing H-A03 graph uses all bit-0 two-bank dates. Only the directed two-bank rates in this diagnostic use pre-July dates. Undisplayed small cells remain in the pooled denominator. No country pair or bank identity is exported.
