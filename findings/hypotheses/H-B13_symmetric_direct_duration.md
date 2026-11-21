# H-B13: Direct route duration centers can depend on direction

- **Owner:** B
- **Status:** rejected in exploration
- **Exploration:** `uv run python analysis/20_routing_time/H-B13_symmetric_direct_duration.py`
- **Evidence:** [aggregate report](../../analysis/20_routing_time/out/H-B13_symmetric_direct_duration_explore.md).

## Candidate and falsification

A common location for an unordered two-bank path predicts that reversing the
visible endpoints leaves the underlying mean duration unchanged. Allow a
100-second difference in estimated means for sampling noise and test whether
at most 1% of supported bidirectional corridors exceed it. Use unlabelled
May–June 2023 endpoint-bit-0/0 payments with two visible banks, at least 25
payments in each direction. The unit is an unordered corridor. Compare the
absolute difference of directional means to the May-to-June mean difference
within unchanged ordered paths. The latter provides a same-direction reference
for how much drift and sampling variation can move the estimated centers.

## Discovery evidence

Of 905 bidirectional corridors containing 117,640 payments, 31.0497% exceeded
a 100-second directional mean gap. Their median gap was 1.91 seconds and the 90th
percentile 440.58 seconds. The mixture of small and large gaps matters for
mechanism claims. The 99% cluster sensitivity interval for the share exceeding
100 seconds is [25.6383%,37.7412%], with 152 clusters grouped by the lexicographically
first path bank, whose identity stays local. Other-bank and account dependencies
can invalidate independent-bank inference.

In 832 corridors where visible and declared endpoints agree throughout the
compared rows, 31.6106% exceed 100 seconds. Exact matching on currency and FX
count retains 161 corridor-currency-FX cells across 22,477 payments and 41.6149%
exceed 100 seconds. This control lacks support for a 100-cluster interval.
The comparison population changes under matching. A same-direction reference
with 2,040 May–June recurring paths and at least 25 records per month has median
mean drift .86 seconds and 90th-percentile drift 2.37 seconds. Zero paths exceed
100 seconds of mean drift.

Across pooled reversals, 30.4972% of directional means straddle 100 seconds,
which illustrates that the same visible pair can generate very different timing
levels across directions. It does not estimate a change in B09 exclusion class,
which uses observed fast payments per supported bank.

## Exposure, uncertainty and assessment

The probe was attempted after Phase 0, Round 1 and B04–B10 results were exposed.
May–June reverse-pair duration summaries and B11/B12 discovery were exposed before
this reproducible screen. B11/B12 July internal tests also completed before the
final B13 exploration report was reviewed. The B13 script reads only May–June.
The symmetry candidate was falsified in discovery, so there is no validation
run or validation claim. A refined directional model needs its own identifier
and frozen validation test.

The supported sample contains many frequent corridors. Route direction can
proxy for party or bank role, conversion direction, a directional lookup or
other unobserved state. Endpoint mismatch or differences in the exact currency
and FX count cannot explain all the observed gaps. A fixed service time
contribution for each bank summed identically in both directions cannot account
for these counterexamples without additional terms. This comparison leaves the
generating duration location unresolved.
