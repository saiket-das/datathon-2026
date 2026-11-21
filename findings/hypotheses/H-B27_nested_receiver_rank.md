# H-B27 Shared receiver ranking with origin thresholds

- **Status:** rejected as an exact deterministic assignment mechanism in exploration.
- **Command:** `uv run python analysis/20_routing_time/H-B27_nested_receiver_rank.py`

## Mechanistic implication and falsification

A single receiver score with one Covered threshold for each origin implies
nested Covered receiver sets. Two origins cannot each cover a receiver that
the other leaves Indirect. Such an alternating two-origin/two-receiver
checkerboard falsifies exact shared ranking, regardless of unknown scores
or thresholds. This is an exploratory implication check, not a fitted model
or a frozen confirmation test. Origin propensities alone do not imply this
mechanism. Probabilistic thresholds or pair-specific attributes are alternatives.

## Population and controls

Use unlabelled May–June 2023 payments with three to five visible bank
occurrences and declared endpoint MD5 parity 0/0. Group by ordered first/last
visible bank. Keep pure Covered-versus-Indirect labels only, including singleton
observations in the primary screen. Retain origins with at least 100 such
corridors, and origin pairs with at least 20 shared receivers. Weight each
ordered corridor once. Repeat after requiring declared endpoints to agree
with visible endpoints, and after requiring at least two payment witnesses
per corridor. Cohorts with fewer than 100 supported banks in either
canonical comparison role are suppressed.

The primary supported graph has 95,742 corridors, 249 origins and 4,332
receivers. Of 30,171 eligible origin pairs, 14,829 (49.149846%) contain
checkerboards, with 1,179,238 alternating receiver-pair motifs. Declared
endpoint agreement retains 83,668 corridors, 225 origins and 3,098 receivers;
12,940 of 25,005 pairs (51.749650%) still violate exact nesting. See the
[report](../../analysis/20_routing_time/out/H-B27_nested_receiver_rank_explore.md)
for full aggregate denominators. The repeated-witness control retains
39,602 corridors, 168 origins and 1,834 receivers; 8,250 of 13,886 origin
pairs violate nesting, with a 1.266570% pairwise minimum editing fraction.

## Interpretation and limitations

Exact shared ranking is inconsistent with these observed labels. Approximate
ranking remains possible: the sum of pairwise minimum flips divided by
repeated shared-receiver comparisons is only .965146% in the primary screen,
and .934984% under endpoint agreement. Those are local editing summaries,
not the global minimum matrix edits. Rare Covered labels, support selection
and pure-label filtering influence the fractions. Motifs and origin pairs
overlap heavily; neither is an independent sample count and no precision
claim follows from their large totals. No original assignment code is recovered.

Phase 0/Round 1 full-data aggregates and prior Round 2/3 Covered labels,
origin propensities and July outcomes are exposed. Reused May–June records
provide internal falsification only. No new July outcome was queried, and
no hypothesis was revised using a newly opened confirmation result.
