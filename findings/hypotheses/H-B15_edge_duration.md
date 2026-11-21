# H-B15 shifted directed-edge duration on supported paths

- **Owner:** B
- **Status:** supported in frozen internal validation
- **Evidence level:** Supported on a narrow reused population
- **Command:** `uv run python analysis/20_routing_time/H-B15_edge_duration.py --phase explore`
- **Frozen command:** replace the phase with `--phase confirm --freeze SHA`

## Candidate and population

For an unlabelled three-visible-bank path, approximate total duration as the sum of the May Direct medians of its two consecutive directed visible bank pairs, plus a constant estimated in June. Remove placeholder strings only to obtain the visible sequence. Use a directed edge median only when there are at least ten May two-visible-bank witnesses. All training, calibration and evaluation records have both declared endpoint-bank MD5 parity bits zero. Restrict the analysis to UTC May–July 2023. May provides every edge median, June calibrates the common offsets, and July provides the internal evaluation.

Compare the sum with a bottleneck model that uses the larger of the same two edge medians. Give both models the median signed residual on the same June cohort as their own offset. Describe a third comparator using the May Direct median of the path's first-to-last visible bank pair where supported. Its June residual median calibrates its offset on the endpoint-supported subset. Comparisons against the endpoint model use only jointly supported records for interpretation. No raw bank identity, path, payment, or fitted individual edge median is reported.

This is an empirical edge-centre decomposition on a selected population. The offset could combine stable path timing, overlapping bank contributions, duration noise and selection effects. No literal service-time interpretation, unique source-code discovery, or transport across unseen directed edges follows. The broader B01 bank-effect failure stays rejected.

## Development and selection

May fit 7,236 directed pairs from 212,230 witnesses. The exploratory June denominator is 211,787 three-visible-bank payments. Only 7,335 (3.4634%) have both edges supported, comprising 361 declared ordering banks, 3,986 senders and 5,366 receivers. June offsets are −14.5 seconds for edge sum, +7 for max edge and +14 for endpoint. June was used for calibration, so these estimates are pilot evidence. Earlier descriptive probes used a rounded +8 offset for the maximum before implementing equal calibration for the two models.

Pilot sum MAE is 7.5419 seconds, max MAE 21.6437 seconds, ratio .34846, sum p90 error 15.5 seconds and within-20 share 96.1282%. The pilot one-sided order-bank bounds are 8.4971s for sum MAE, .45472 for ratio, and .95568 for within-20 share. On 4,878 jointly supported endpoint-comparison paths, MAEs are 7.8719s for sum, 23.0205s for max and 163.7927s for endpoint. On paths where the shorter edge is below100 seconds, shifted max MAE is 7.9754 seconds versus 7.2096 seconds for the sum. This subgroup illustrates that the pooled contrast should not be described as a universal large gain. Alternative bank-country, pair-state or reused path centres may explain the selected fit. Covered and other small cohorts are subject to a reporting gate.

Independent initial exploration found substantial same-pair variation in some cases, and large differences between visible and declared endpoint medians and between directed and undirected relationships. They motivated using visible directed edges. No model takes coefficients from July. The eligible edge support is sparse and disproportionately represents recurrent paths. Full-stage selection coverage is a frozen criterion, without making extrapolation beyond supported rows.

## Frozen internal gates

Run the exact frozen executable for July. Require all gates to pass:

1. At least 2% of July unlabelled bit0/0 three-visible-bank payments are supported, with at least 1,000 paths and 100 ordering banks, senders and receivers.
2. Ordering-bank bootstrap one-sided 99% upper bound for shifted-sum MAE is at most 12 seconds.
3. The analogous upper bound on sum-to-maximum MAE ratio is at most .75. Pair the comparisons on exactly the same scored payments and bank draws.
4. Bootstrap one-sided 99% lower bound for the share within20 seconds is at least .90, and observed p90 absolute error is at most25 seconds.

Resample whole declared ordering-bank groups 1,000 times with seed20261116. Bounds are conditional sensitivities because path banks and customers can recur and timing outcomes share earlier training inputs. The tolerances allow practical drift from June yet require a clear improvement on the supported cohort. Route, shorter-edge and endpoint-comparator sections are descriptive. Uncertainty and support must be reported at their actual denominators. A suppressed or favorable subgroup cannot rescue a failed conjunction.

## Prior exposure

Phase 0 structural, Round 1 B01 additive duration results, B02 paths and other outcomes, and B04–B14 routing/duration/temporal aggregates were already available. In particular B09 used July durations for its exclusion signature, B11 used July within-path duration differences and B13 used May–June directed pairs. The specific July B15 edge-sum errors remain uninspected before freeze. July is reused internal evaluation, and every scored edge was seen during May. Other selections and higher visible counts are unresolved. A pass can only support the stated narrow empirical rule without independent confirmation.

## Frozen July result

Freeze 44a4a5afa7959ad79e4bfe9058882a0a1f52e142 was committed on
17 November 2026 at 03:15:34 MYT. The unchanged executable passed all gates.
Reproduce with the recorded command, --phase confirm and --freeze followed by that SHA.

July supports 5,219/151,146 three-visible-bank payments (3.4530%), across 331
ordering banks, 3,055 senders and 3,977 receivers. Sum MAE is 7.323913s,
maximum MAE 21.820368s, ratio .335646, p90 error 15.5s and within20s share 96.148687%.
One-sided99% resampling bounds are 7.629742s for sum MAE, .482308 for the MAE
ratio and 95.545228% for the within20s share. June-calibrated offsets stayed fixed.

On 3,493 paths with the endpoint comparator, sum MAE 7.435585s contrasts with
endpoint MAE 160.668194s. On 4,936 paths with shorter edge below100s, sum MAE
7.218497s and max MAE 7.860920s are close. Covered and both-long-edge subgroups
lack display entity support. These restrictions limit extrapolation of the pooled effect.

The -14.5s shift and directed-edge fit provide an empirical decomposition.
Possible explanations include edge-associated states, shared node contributions
counted in both edge medians, or stable path centers. Noise and selection also
enter the medians. Physical processing costs remain unresolved. B01 remains
failed. July B15 residual outcomes are now exposed.
