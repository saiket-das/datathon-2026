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

## Round2

[Progress and exposure](../../docs/12_b_round2_progress.md).
[H-B04](../../findings/hypotheses/H-B04_covered_bank_stability.md) tests known-bank
Covered-propensity transfer across months with safe aggregates.
Run `uv run python analysis/20_routing_time/H-B04_covered_bank_stability.py --phase explore`
or `--phase confirm --freeze SHA` after freezing. This reuses Round1-exposed records
and cannot establish independent confirmation. Tests: `test_covered_stability.py`.

[H-B05](../../findings/hypotheses/H-B05_endpoint_mismatch.md) tests the joint frequency
of declared-versus-path endpoint disagreement. Run
`uv run python analysis/20_routing_time/H-B05_endpoint_mismatch.py --phase explore`
or use the recorded freeze for July internal validation.

[H-B06](../../findings/hypotheses/H-B06_calendar_timing.md) screens the UTC weekday/weekend timing contrast within bank, route, party pair and month. Run `uv run python analysis/20_routing_time/H-B06_calendar_timing.py` for May–June exploration or add `--phase confirm --freeze SHA` for the frozen July internal test.

[H-B07](../../findings/hypotheses/H-B07_gap_placement.md) tests conditional internal placeholder placement against uniform weak compositions and iid slot allocation. Run `uv run python analysis/20_routing_time/H-B07_gap_placement.py --phase explore` or the recorded frozen July command. The broad v5/two-gap pilot failure is preserved.

[H-B08](../../findings/hypotheses/H-B08_simple_paths.md) rejects selection of all visible banks without replacement in the exploration partition. Run `uv run python analysis/20_routing_time/H-B08_simple_paths.py`; output preserves supported aggregate counterexamples.

[H-B09](../../findings/hypotheses/H-B09_bank_duration_exclusion.md) tests a persistent visible-bank-associated exclusion of sub-100-second durations. Run the matching script with --phase explore, or use its frozen internal July command.

[H-B10](../../findings/hypotheses/H-B10_country_bank_class.md) falsifies a country-determined explanation of the May bank-duration witness classes. Run the matching script for aggregate-only exploration.

[H-B11](../../findings/hypotheses/H-B11_same_path_duration_noise.md) compares duration
differences on the same ordered visible path with fixed noise laws.
Run `uv run python analysis/20_routing_time/H-B11_same_path_duration_noise.py --phase explore`.

[H-B12](../../findings/hypotheses/H-B12_directed_endpoint_route_class.md) tests
whether Covered and Indirect follow the directed visible endpoints on novel paths.
Run `uv run python analysis/20_routing_time/H-B12_directed_endpoint_route_class.py --phase explore`.
Both records provide the frozen July internal validation command.

[H-B13](../../findings/hypotheses/H-B13_symmetric_direct_duration.md) compares
the duration of supported Direct paths in opposite directions. Run
`uv run python analysis/20_routing_time/H-B13_symmetric_direct_duration.py`.

[H-B14](../../findings/hypotheses/H-B14_intermediate_bank_sampling.md) compares
the two interior positions with draws from a weighted bank catalogue.
Run `uv run python analysis/20_routing_time/H-B14_intermediate_bank_sampling.py --phase explore`.

[H-B15](../../findings/hypotheses/H-B15_edge_duration.md) tests shifted directed-edge sums for supported three-visible-bank durations. See the record for the pilot and frozen command.

[H-B16](../../findings/hypotheses/H-B16_currency_duration_location.md) screens
currency-specific mean durations within recurring Direct paths.
Run `uv run python analysis/20_routing_time/H-B16_currency_duration_location.py`.

[H-B17](../../findings/hypotheses/H-B17_directional_triangle.md) checks whether
Direct direction gaps cancel around bank triangles.
[H-B18](../../findings/hypotheses/H-B18_bounded_directional_gap.md) compares
short-median corridor gaps with bounded distributions.
[H-B19](../../findings/hypotheses/H-B19_covered_direction_duration.md) tests
whether earlier multibank labels locate the slower Direct direction.
The records link the exact commands and frozen tests.

[H-B29](../../findings/hypotheses/H-B29_institution_prefix_transfer.md)
screens whether other banks with the same institution prefix explain an
origin's Covered propensity. [H-B30](../../findings/hypotheses/H-B30_same_country_corridor.md)
tests the bank-country relationship within origins. Run their matching
scripts from the repository root.

[H-B31](../../findings/hypotheses/H-B31_timing_origin_state.md) screens
timing-derived origin groups on unseen corridors. Run its matching
script for exploration-only evidence.

[H-B32](../../findings/hypotheses/H-B32_country_novelty_support.md) audits
geographic matching support on May-unseen June pairs. Run its matching
script for exploration-only support counts.

## Round 3

- [H-B20](../../findings/hypotheses/H-B20_unseen_corridor_propensities.md)
  compares endpoint propensities on ordered corridors with no May witness in either orientation.
- [H-B21](../../findings/hypotheses/H-B21_reversed_path_penalty.md) screens
  exact reversed three-bank paths for sufficient timing support.
- [H-B22](../../findings/hypotheses/H-B22_covered_long_corridors.md) screens
  Covered versus Indirect duration asymmetry when both Direct directions are slow.
- [H-B23](../../findings/hypotheses/H-B23_edge_delay_propagation.md) compares
  adjacent-edge and outer-endpoint duration components using fixed May and June fits.
- [H-B24](../../findings/hypotheses/H-B24_origin_structural_zero.md) compares
  binary origin activity and graded origin propensities.
- [H-B25](../../findings/hypotheses/H-B25_covered_reciprocity.md) compares
  reciprocal Covered labels with a calibrated independent-direction model.

- [H-B26](../../findings/hypotheses/H-B26_origin_penalty.md) screens a fixed
  Covered-origin duration increment on selected repeated-origin corridors.
- [H-B27](../../findings/hypotheses/H-B27_nested_receiver_rank.md) falsifies
  exact shared receiver ranks using alternating Covered/Indirect labels.
  Both are May–June exploration screens; run their matching Python scripts
  without phase arguments. Their negative results do not open July outcomes.

- [H-B28](../../findings/hypotheses/H-B28_placeholder_duration.md) tests
  a one-second equivalence bound for matched Direct duration with versus
  without placeholders. Run its script with `--phase explore`, or the
  recorded frozen `--phase confirm --freeze SHA` command. This new contrast
  reuses B11's duration populations and is an internal test.
