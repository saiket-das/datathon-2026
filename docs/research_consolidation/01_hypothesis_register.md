# Phase 2 — hypothesis classification register

**Role:** coordinator/research synthesis, read-only scientific audit. **Date:** 18 Nov 2026 MYT.

This index is reconciled against the original publicly visible A/B/C branch progress records and branch change inventories, **not** against a fresh local Parquet run or an individual code-level rereview of each of the 63 plans. Individual freeze details, controls, denominators and exceptions remain authoritative in the linked original records. This CSV/Markdown is a derivative classification index, not independent confirmation.

Source branches: `codex/r2-a-amount-generation`, `codex/r2-b-routing-generation`, `codex/r2-c-entity-mechanisms`. Their histories are unmerged and unchanged. Machine-readable register: [CSV](01_hypothesis_register.csv).

**Evidence meanings**: `INTERNAL_PASS` means original investigator reports a passed internal/reused-population criterion; not independent. `FROZEN_FAILURE` means at least one frozen criterion failed (never rescue conjunction). `EXPLORATORY` includes unvalidated negative screens and missing support.

## A (26 entries; 15 internal passes, 3 frozen failures, 8 exploratory)
| ID | Topic | Status | Original hypothesis |
|---|---|---|---|
| H-A01 | amount kernel | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A01_amount_kernel.md) |
| H-A02 | usd rounding | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A02_usd_rounding.md) |
| H-A03 | fx country classes | FROZEN_FAILURE | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A03_fx_country_classes.md) |
| H-A04 | fx gap residuals | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A04_fx_gap_residuals.md) |
| H-A05 | fx repeat classes | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A05_fx_repeat_classes.md) |
| H-A06 | currency endpoint | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A06_currency_endpoint.md) |
| H-A07 | currency exceptions | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A07_currency_exceptions.md) |
| H-A08 | path currency set | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A08_path_currency_set.md) |
| H-A09 | modal scale coherence | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A09_modal_scale_coherence.md) |
| H-A10 | cross denomination | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A10_cross_denomination.md) |
| H-A11 | fx transition residuals | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A11_fx_transition_residuals.md) |
| H-A12 | log shape | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A12_log_shape.md) |
| H-A13 | daily scale updates | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A13_daily_scale_updates.md) |
| H-A14 | currency class disagreement | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A14_currency_class_disagreement.md) |
| H-A15 | payment currency insertion | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A15_payment_currency_insertion.md) |
| H-A16 | fx support gaps | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A16_fx_support_gaps.md) |
| H-A17 | fractional denominations | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A17_fractional_denominations.md) |
| H-A18 | usd heaping shape | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A18_usd_heaping_shape.md) |
| H-A19 | utc scale boundary | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A19_utc_scale_boundary.md) |
| H-A20 | route mode transfer | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A20_route_mode_transfer.md) |
| H-A21 | country amount context | FROZEN_FAILURE | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A21_country_amount_context.md) |
| H-A22 | usd quantization levels | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A22_usd_quantization_levels.md) |
| H-A23 | preferred five anchor | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A23_preferred_five_anchor.md) |
| H-A24 | party scale transfer | FROZEN_FAILURE | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A24_party_scale_transfer.md) |
| H-A25 | scaled five anchor | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A25_scaled_five_anchor.md) |
| H-A26 | sender scale persistence | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A26_sender_scale_persistence.md) |

## B (32 entries; 15 internal passes, 3 frozen failures, 14 exploratory)
| ID | Topic | Status | Original hypothesis |
|---|---|---|---|
| H-B01 | bank additive duration | FROZEN_FAILURE | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B01_bank_additive_duration.md) |
| H-B02 | route gap process | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B02_route_gap_process.md) |
| H-B03 | covered coin | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B03_covered_coin.md) |
| H-B04 | covered bank stability | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B04_covered_bank_stability.md) |
| H-B05 | endpoint mismatch | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B05_endpoint_mismatch.md) |
| H-B06 | calendar timing | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B06_calendar_timing.md) |
| H-B07 | gap placement | FROZEN_FAILURE | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B07_gap_placement.md) |
| H-B08 | simple paths | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B08_simple_paths.md) |
| H-B09 | bank duration exclusion | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B09_bank_duration_exclusion.md) |
| H-B10 | country bank class | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B10_country_bank_class.md) |
| H-B11 | same path duration noise | FROZEN_FAILURE | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B11_same_path_duration_noise.md) |
| H-B12 | directed endpoint route class | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B12_directed_endpoint_route_class.md) |
| H-B13 | symmetric direct duration | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B13_symmetric_direct_duration.md) |
| H-B14 | intermediate bank sampling | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B14_intermediate_bank_sampling.md) |
| H-B15 | edge duration | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B15_edge_duration.md) |
| H-B16 | currency duration location | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B16_currency_duration_location.md) |
| H-B17 | directional triangle | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B17_directional_triangle.md) |
| H-B18 | bounded directional gap | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B18_bounded_directional_gap.md) |
| H-B19 | covered direction duration | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B19_covered_direction_duration.md) |
| H-B20 | unseen corridor propensities | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B20_unseen_corridor_propensities.md) |
| H-B21 | reversed path penalty | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B21_reversed_path_penalty.md) |
| H-B22 | covered long corridors | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B22_covered_long_corridors.md) |
| H-B23 | edge delay propagation | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B23_edge_delay_propagation.md) |
| H-B24 | origin structural zero | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B24_origin_structural_zero.md) |
| H-B25 | covered reciprocity | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B25_covered_reciprocity.md) |
| H-B26 | origin penalty | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B26_origin_penalty.md) |
| H-B27 | nested receiver rank | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B27_nested_receiver_rank.md) |
| H-B28 | placeholder duration | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B28_placeholder_duration.md) |
| H-B29 | institution prefix transfer | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B29_institution_prefix_transfer.md) |
| H-B30 | same country corridor | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B30_same_country_corridor.md) |
| H-B31 | timing origin state | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B31_timing_origin_state.md) |
| H-B32 | country novelty support | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-b-routing-generation/findings/hypotheses/H-B32_country_novelty_support.md) |

## C remote (5 entries; 2 internal passes, 1 frozen combined failure, 2 exploratory)
| ID | Topic | Status | Original hypothesis |
|---|---|---|---|
| H-C01 | duplicate bursts | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-c-entity-mechanisms/findings/hypotheses/H-C01_duplicate_bursts.md) |
| H-C02 | romance bursts | INTERNAL_PASS | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-c-entity-mechanisms/findings/hypotheses/H-C02_romance_bursts.md) |
| H-C03 | adjacent edit | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-c-entity-mechanisms/findings/hypotheses/H-C03_adjacent_edit.md) |
| H-C04 | literal linebreak | EXPLORATORY | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-c-entity-mechanisms/findings/hypotheses/H-C04_literal_linebreak.md) |
| H-C05 | scam endpoint agreement | FROZEN_FAILURE | [original](https://github.com/saiket-das/datathon-2026/blob/codex/r2-c-entity-mechanisms/findings/hypotheses/H-C05_scam_endpoint_agreement.md) |

## Counts and scope

**63 indexed remote A/B/C records: 32 internally passed, 7 frozen failures, 24 exploratory.** These counts must never be interpreted as a scientific accuracy, completeness, FDR or independent-replication score. The A01/A02 and C01/C02 round-one replicated signatures are classified using the original investigation and coordinator's stage record; do not imply complete independence.

**Exclusions**: C06–C48 are reported local-only and unavailable on remote C branch; E01–E04 locally recovered/replayed but original local sources were not fetched by this coordinator, E05 unexecuted; D remains isolated; F01–F03 private explorations, F04 proposal-only; G01 frozen with restricted private evidence not copied here, G02 unexecuted/unfrozen. These are explicitly **outside the 63**. See [source inventory](00_scope_and_source_inventory.md) and [audit](04_evidence_and_exposure_audit.md).

**Do not create** retrospective validation stamps, claim that split Parquet parts were independent, or merge investigator branches.
