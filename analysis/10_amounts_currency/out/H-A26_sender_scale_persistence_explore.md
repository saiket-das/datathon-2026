# H-A26 — Persistent sender residual scale

Freeze: exploration.
512MB; one thread; no disk spill. Aggregates only.
Bit-zero May-to-June development only. Phase 0 and A01–A25 exposure applies.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Coverage

| scoped_target | baseline_covered | supported_cells | matched_cells | senders | banks | matched_target_rows |
| --- | --- | --- | --- | --- | --- | --- |
| 1043095 | 929549 | 10890 | 8545 | 6163 | 958 | 476291 |

## Equal-sender paired-month aggregates

| senders | month_correlation | baseline_mean_square | own_history_mean_square | peer_history_mean_square | own_vs_baseline | own_vs_peer |
| --- | --- | --- | --- | --- | --- | --- |
| 6163 | 0.6371671599904072 | 0.45996640012858825 | 0.38637572372334555 | 0.3725737031228708 | 0.8400085823993455 | 1.037045074530993 |

## Exploratory centering by bank, currency and party in each month

| senders | centred_month_correlation | baseline | own_history_error | peer_history_error | own_vs_centred_baseline | own_vs_centred_peer |
| --- | --- | --- | --- | --- | --- | --- |
| 6163 | 0.01900621833256246 | 0.14146198975762383 | 0.3098823568495217 | 0.2996431979612426 | 2.1905697592721807 | 1.0341711707722578 |

## Ordering-bank sensitivity

| comparison | low99 | high99 |
| --- | --- | --- |
| own/base | 0.7780978087424221 | 0.9029562816523259 |
| own/peer | 0.9859764329119175 | 1.087967766458526 |

## Prespecified decision

| all_criteria_met |
| --- |
| False |

Each supported sender/currency/party cell needs at least ten payments in both months. The peer is a deterministic different sender from the same bank/currency/party group. Repeated histories and grouped target means condition on the selected repeated customers.
