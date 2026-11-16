# H-B11: Near-constant duration noise on the same visible path

- **Owner:** B
- **Status:** confirmation-ready
- **Exploration:** `uv run python analysis/20_routing_time/H-B11_same_path_duration_noise.py --phase explore`
- **Internal validation:** same command with `--phase confirm --freeze <full SHA>`.
- **Evidence:** [discovery report](../../analysis/20_routing_time/out/H-B11_same_path_duration_noise_explore.md) and [fine-bin pilot](../../analysis/20_routing_time/out/H-B11_same_path_duration_noise_pilot.md).

## Proposed rule and scope

Model durations on an ordered visible path as a path-specific location plus
integer-discretised Gamma noise with shape 2 and scale 5 seconds. If two payments on
that path have independent draws from this noise law, differencing durations cancels
the location. At both two and three visible banks, the predicted mean square of the
absolute difference is 100.165 s² and its 50th, 90th and 99th percentiles are 6, 16
and 30 seconds. A model with one exponential component per visible bank predicts a
mean square of 150.167 s² and a 90th percentile of 20 seconds at three banks.

The data test the distribution of the differences. An independent shock with this
Gamma law is one compatible construction. Other noise laws or dependencies can
produce similar differences, and the analysis does not recover the path location,
the noise mean or a lower bound on each bank's service time. This concerns within-path
variation and preserves B01's failed path-location approximation.

## Frozen internal validation plan

- **Population and pairing.** Unlabelled payments with both declared endpoint MD5
  parity bits zero. Take exact ordered visible paths, omitting placeholders. Within
  each path, sort by MD5 of decimal ROW_ID, breaking ties by ROW_ID. Pair successive
  records without replacement and drop an unpaired remainder. Absolute duration
  difference is the outcome. Primary scopes are exactly two and three visible banks.
  Four and five banks are descriptive, with small population cells masked.
- **Partition.** May–June 2023 UTC for discovery. July 2023 UTC, half-open
  `[2023-07-01,2023-08-01)`, for frozen internal validation. A path, sender or
  receiver can recur across months. The scripts report path counts, first-bank support
  and the fraction of payments with a partner at each length.
- **Comparator and test.** Sum the discrete autocorrelation of the one-draw mass
  function into absolute differences at 0, 1–5, 6–10, 11–20, 21–40 and 41+ seconds.
  Compare fixed Gamma(2,5) with matched-variance normal, matched-variance exponential,
  and Gamma(shape=visible count, scale=5). Fit no parameters to July. Use TV distance
  and mean square throughout and retain fine-grid TV as a descriptive comparison.
- **Acceptance.** Each primary length requires at least 5,000 pairs from at least
  100 first visible banks. Resample whole first-visible-bank histograms 1,000 times
  with NumPy seed 20261116. Both 99% percentile intervals for mean square must lie in
  [90,110] s², and both upper TV bounds must be at most .020 for the fixed Gamma
  model in the six-bin comparison. At three banks, the lower bound of the paired TV
  advantage over the per-visible-bank shape model must be at least .020. Any miss
  fails the joint primary claim. No subgroup can rescue a failure.
- **Controls and uncertainty.** Report pooled route types and strata with different
  same-role sender and receiver identifiers, a different month in exploration, one
  payment with placeholders, repeated visible banks, and center bands below 100,
  100–999.5 and at least 1,000 seconds. Bins with too few pairs or first banks are
  suppressed. Counts of differences over 100 seconds check large exceptions.
  Using center bands is descriptive because the centers use the paired outcomes.
  First-bank resampling does not separate shared counterparty or intermediary banks.
- **Exposure.** Phase 0 and Round 1 exposed full-data duration summaries and B01
  outcomes. Round 2 B04–B08 exposed route, calendar and placeholder measures in reused
  records. B09 exposed July bank-specific short-duration exclusion and B10 the May
  country screen. Earlier May–June probes for this wave also examined the count and
  position of exclusion banks, within-Direct-path quantile widths and signed residuals,
  as well as the B12 endpoint labels. No new July same-path difference histogram,
  model fit or uncertainty statistic was queried before freeze. The result is internal.

## Discovery evidence

Among 2,040 Direct paths with at least 25 payments in each of May and June, the
median June within-path 10th-to-90th percentile width was 16 seconds. Grouping by
May mean duration below 100, 100–999 and 1,000+ seconds gave median June standard
deviations of 6.88, 6.97 and 6.93 seconds. This encouraged comparison on the
seconds scale instead of assuming a common relative error. A separate bank-class
screen found a marked duration-level shift with the number and identities of
B09 exclusion banks. Such between-path effects can coexist with common noise
within a path.

To reproduce the Direct width screen, use the discovery predicate and visible
path expression in `build_pairs` with `visible=2`. Before pairing, independently
group each month's rows by exact visible path and retain groups with at least 25
payments. Join the two grouped months by path. Report the median June
`quantile_cont(d,.9)-quantile_cont(d,.1)` and June `stddev_samp(d)` summarized
within the May mean bands below 100, 100–999 and 1,000+ seconds. The path-level
subqueries stay local.

The exact-path differencing report reproduces the main discovery. The fine-bin
pilot used one-second bins and a .025 upper TV gate. The three-bank pilot failed
that gate with a 99% upper TV bound of .029287. Before validation, pooling bins
reduced the sampling sensitivity of the sparse three-bank histogram and retained
the tail, central mass and atom at zero. The discarded gate and its failed result
remain available. The new coarse-grid test is discovery-informed.

An early all-length pairing query exceeded 768MB before returning data. The tested
script processes lengths serially and uses 1536MB without spill. No individual row,
path or entity identity is emitted.

## Internal validation and assessment

Pending the frozen test. An economic interpretation is a stable route-specific
component with a small stochastic timing component, which could also be an artefact
of a synthetic table of per-path timing baselines. Differencing cannot distinguish
those mechanisms or identify the original random-number calls.
