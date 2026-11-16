# H-C03: immediate source-neighbour edit candidate

- **Owner:** C
- **Status:** Rejected in exploration for the three supported labels. CUSTOMER_RECALL remains unresolved.
- **Reproduce:** `uv run python analysis/30_parties_anomalies/H-C03_adjacent_edit.py`
- **Evidence:** [Safe aggregate table](../../analysis/30_parties_anomalies/out/H-C03_adjacent_edit.md)

## Proposed rule and scope

A labelled transaction could be an edit of its immediate predecessor or successor
in source order, retaining at least one role-specific account. This is narrower
than a candidate edit mechanism with arbitrary distance or replacement of both accounts.

## Exploration design and results

Use only profiles whose sending account maps to sender MD5 bit 0, including the
candidate neighbour. Compare exact literal role-specific account equality at
ROW_ID offsets -1 and +1. Each displayed cell requires 100 pairs and 100 target
senders. The partition filter limits eligible neighbour coverage.

ACCOUNT_REPLACEMENT_SCAM contributes 172 and 166 pairs by offset, CEO_SCAM 261
and 250, and FAT_FINGER_MISTAKE 470 and 483. Both the sender and the receiver
match counts are zero in every displayed cell. CUSTOMER_RECALL cells lack support.
These observations reject a prevalent immediate-neighbour copy retaining an
account among the eligible pairs. Copies placed at another location, edits of both
accounts and neighbours outside the eligible population remain unresolved.

## Validation and exposure

Rejected during discovery. The test has no validation run. Phase 0 structural
aggregates and Round 1 label/cohort summaries and C01/C02 adjacency outcomes were
available before this search. The current pattern does not explain generation of
the four unresolved labels and has no role as a fraud detector.