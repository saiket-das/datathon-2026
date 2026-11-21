# H-A16 — FX support gaps and map-only transfer

Freeze: exploration.
512MB; one thread; no disk spill. Aggregates only.
July both-account bit-0 evaluation only.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Support and observed outcomes

| support_group | n | senders | receivers | banks | mode_eligible | mode_errors | class_errors | weak_eligible | weak_errors | outside_partial_bounds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | 275211 | 54714 | 124331 | 5055 | 274628 | 0 | 1051 | within 100 of n | 0 | 0 |
| Currency mode only | 3452 | 2306 | 2803 | 954 | 3452 | 0 | 0 | 3452 | 0 | 0 |
| Jointly supported | 271176 | 53625 | 122429 | 4904 | 271176 | 0 | 1051 | 271176 | 0 | 0 |
| Neither map | 583 | 469 | 514 | 299 | 0 | 0 | 0 | within 100 of n | 0 | 0 |

## Ordering-bank sensitivity

| measure | low99 | high99 |
| --- | --- | --- |
| coverage | 0.9974150784849305 | 0.9983099568770348 |
| fraction newly scored | 0.010474725815873972 | 0.014880947288597181 |

## Prespecified decision

| scoped | mode_eligible | mode_only | mode_excluded | all_criteria_met |
| --- | --- | --- | --- | --- |
| 275211 | 274628 | 3452 | 583 | True |

Partial bounds count changes on supported edges and allow zero or one per edge with an unknown endpoint. They do not solve joint constraints across adjacent unknown edges. Weak modes are a diagnostic below the 100-payment support floor. Positive small cells are masked and undisplayed small groups remain in the pooled total.
