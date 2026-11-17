# H-A16 — FX support gaps and map-only transfer

Freeze: 319f6d2f25bf9bc62911a37e58b495809ee8e43a.
512MB; one thread; no disk spill. Aggregates only.
Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Support and observed outcomes

| support_group | n | senders | receivers | banks | mode_eligible | mode_errors | class_errors | weak_eligible | weak_errors | outside_partial_bounds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| All | 257566 | 53583 | 121053 | 4995 | 256843 | 0 | 1036 | within 100 of n | 0 | 0 |
| Currency mode only | 2909 | 2093 | 2484 | 891 | 2909 | 0 | 0 | 2909 | 0 | 0 |
| Jointly supported | 253934 | 52571 | 119287 | 4838 | 253934 | 0 | 1036 | 253934 | 0 | 0 |
| Neither map | 723 | 432 | 630 | 288 | 0 | 0 | 0 | within 100 of n | 0 | 0 |

## Ordering-bank sensitivity

| measure | low99 | high99 |
| --- | --- | --- |
| coverage | 0.995335329169607 | 0.9982261771299508 |
| fraction newly scored | 0.00955216963107444 | 0.013313260619513588 |

## Prespecified decision

| scoped | mode_eligible | mode_only | mode_excluded | all_criteria_met |
| --- | --- | --- | --- | --- |
| 257566 | 256843 | 2909 | 723 | True |

Partial bounds count changes on supported edges and allow zero or one per edge with an unknown endpoint. They do not solve joint constraints across adjacent unknown edges. Weak modes are a diagnostic below the 100-payment support floor. Positive small cells are masked and undisplayed small groups remain in the pooled total.
