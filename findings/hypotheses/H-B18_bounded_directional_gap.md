# H-B18 bounded directional gaps on selected Direct corridors

- **Status:** bounded gap shape supported in frozen internal validation
- **Command:** `uv run python analysis/20_routing_time/H-B18_bounded_directional_gap.py --phase explore`.
- **Internal test:** replace the phase with `--phase confirm --freeze 1979ad17f1431755e99d54a4579ade48eb35c71d`.

## Candidate and frozen test

A stable extra cost on one direction of some otherwise short corridors could
produce a broad, roughly uniform gap. Compare opposite direction medians
within each visible Direct bank pair. Use unlabelled payments with both
declared endpoint MD5 bits zero and require ten payments per direction.
Keep pairs whose shorter median is below 100 seconds and whose gap exceeds
20 seconds. The latter condition excludes near-symmetric corridors and is
part of the estimand. Each eligible pair contributes one absolute gap.

Compare bin probabilities from a single Uniform(0,600 seconds) draw,
conditioned on the gap exceeding 20 seconds, against the absolute difference
of two independent Uniform(0,600) draws with the same truncation. The latter
produces a decreasing triangular density. Bin at (20,120], (120,240],
(240,360], (360,480], (480,600], and above 600 seconds. The threshold and
support endpoint were chosen during May–June exploration. No parameters are
fitted on the July test.

Require at least 150 eligible pairs and 100 first banks under a canonical
lexicographic orientation. Resample these bank groups 1,000 times using seed
20261116. Require upper 99% percentile TV to the single uniform ≤.15, lower
99% TV advantage over the triangular comparator ≥.02 and upper 99% fraction
above 620 seconds ≤.025. The 620-second gate allows small median deviations
around the candidate 600-second bound. For skewed TV the upper resampling
percentile is a practical sensitivity gate. Shared partner banks and accounts
can weaken it. A zero empirical resampling tail gives no unseen-exception bound.

Repeat the summary among agreeing declared endpoints and compare the absolute
change in the same pair's directional gap across May and June, or July halves.
The temporal comparison requires at least five observations per direction and
half. It serves as a small-error reference. Neither control rescues a failed
criterion. More complex selection rules can approximate the same conditional
histogram, and conditioning on the observed shorter median limits which
underlying models can be distinguished.

## Exploration and exposure

The May–June cohort has 511 of 3,196 supported bidirectional pairs, covering
57,861 payments and 170 canonical first banks. Median gap is 314 seconds and
p99 is 589.95 seconds. Single-uniform TV is .023821, triangular TV .241691,
and the 99% lower advantage is .142254. The single-uniform TV upper bound is
.075668. None exceed 620 seconds, but positive counts above 600 exist and
are masked at low support. The median absolute change in the signed
directional gap across months is 2.5 seconds in 463 pairs with block support.
Under endpoint agreement, median gap remains 317 seconds across 501 pairs.

Phase 0 and B01–B16 results were exposed before discovery, including previous
July duration and path summaries. B17 and B18 shared May–June pilot queries.
The July gap histogram and comparison metrics were unqueried before freeze.
Any pass is internal validation. The test does not identify an exact penalty
law, which direction gets a penalty, or its rate among all pairs.

## Frozen July result

The unchanged test from freeze `1979ad17f1431755e99d54a4579ade48eb35c71d`
passed on 289 of 973 supported pairs across 127 canonical first banks,
covering 18,169 payments. The median gap was 318 seconds and p99 was 592.92
seconds. No observed gap exceeded 600 seconds. Uniform TV was .036630
with upper resampling bound .116289. The triangular alternative had TV
.257841 and the lower bound on the improvement was .111180. The empirical
upper bound for the share above 620 seconds was zero.

Declared endpoint agreement retained 280 pairs and a median gap of
316.75 seconds. The 209 pairs with enough observations to compare both July
halves had median absolute directional gap drift of 3 seconds. The
comparison supports a near-uniform conditional shape, with B19 providing
evidence about the direction of large gaps on separately labelled pairs.
Selection on gap size and duration still limits model identification.
These July gap outcomes are now exposed. [July aggregate report](../../analysis/20_routing_time/out/H-B18_bounded_directional_gap_confirm.md).
