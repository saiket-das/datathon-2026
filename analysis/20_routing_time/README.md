# Routing and time (owner B)

Columns: `BIC8_PATH`, `ORDERING_BIC8`, `BENEFICIARY_BIC8`, `TRANSACTION_TYPE_CODE`, `PARTICIPANT_COUNT`, `CONTINUITY_QFLAG`, `TOTAL_DURATION`, `EPOCH_SECONDS`.

Starting questions:
- Which routing columns are exact functions of the path (definitions), and which are randomly drawn?
- What decides Direct vs Indirect vs Covered, and how many intermediary banks?
- Is duration explained by hops, conversions, route type or the time of day?
- Does payment volume follow the sender's local business hours?

## Independent investigation (16 November 2026)

Search history, official sources, freeze provenance and review handoff:
[docs/08_b_routing_investigation.md](../../docs/08_b_routing_investigation.md).

| Candidate | Reproduction from repository root | Record |
| --- | --- | --- |
| Bank-effect duration approximation | `uv run python analysis/20_routing_time/H-B01_bank_additive_duration.py --phase explore` | [H-B01](../../findings/hypotheses/H-B01_bank_additive_duration.md) |
| Joint route-length/gap count law | `uv run python analysis/20_routing_time/H-B02_route_gap_process.py --phase explore` | [H-B02](../../findings/hypotheses/H-B02_route_gap_process.md) |
| Independent Covered-label coin (rejected in discovery) | `uv run python analysis/20_routing_time/H-B03_covered_coin.py` | [H-B03](../../findings/hypotheses/H-B03_covered_coin.md) |

For B01/B02, replace `--phase explore` with `--phase confirm --freeze <SHA>` for
the unchanged frozen test. Read the freeze SHA in the investigation note. Scripts verify
that the executable and shared helper match that ancestor commit before opening confirmation.
Do not interpret outputs from a changed script as that frozen test.

`routing_common.py` reuses the foundation's MD5 bank partition and provides local-only
entity-overlap audits, cluster resampling and small-group suppression. No sponsor
records, model coefficients or bank identities are saved. Reports and PNG charts use
matching script stems with `_explore`/`_confirm` suffixes in [out/](out/).
Dataset-independent checks: `uv run pytest analysis/20_routing_time/test_routing_research.py`.
