# H-B28 Matched mean duration with and without placeholders

- **Status:** confirmation-ready
- **Explore:** `uv run python analysis/20_routing_time/H-B28_placeholder_duration.py --phase explore`
- **Frozen internal test:** same command with `--phase confirm --freeze SHA`.

## Proposed narrow rule

On repeated Direct visible paths, placeholder-bearing records have a
matched average duration within one second of placeholder-free records.
This tests whether a meaningful common added timing increment accompanies
the omitted path positions. A fixed positive increment of at least one
second is the substantive comparator; the equivalence interval is [-1,1]
seconds. Equality, stochastic independence, absence of hidden hops and
original generator stage ordering are stronger claims and are not tested.
Positive and negative subgroup effects can cancel in the average.

## Frozen population, estimator and decision

1. Use only unlabelled Direct records with exactly two visible bank
   occurrences and both declared endpoint-bank MD5 parity bits zero.
   Strip `...` placeholders to identify the exact ordered visible path.
   The binary exposure is `gap_count>0`. No outcome-dependent exclusions.
2. Exploration is UTC May–June 2023. The designated internal test is UTC
   July 2023, `[2023-07-01,2023-08-01)`, read only after committing this
   complete plan and executable. Match by exact visible path, UTC calendar
   month and route type. Retain cells with at least five records both with
   and without placeholders. Each retained cell has equal weight, regardless
   of payment volume. The contrast is mean duration with placeholders minus
   mean duration without placeholders. Scope excludes unsupported paths
   and all longer visible paths.
3. Require at least 200 retained cells, 200 distinct visible paths and
   100 distinct banks in each endpoint role. For each role separately,
   resample whole bank groups with replacement 1,000 times using NumPy
   seed 20261117. Recompute the equal-cell mean from group sums/counts.
   Both 99% percentile intervals (quantiles .005/.995) must be fully within
   [-1,1] seconds. All support and interval gates must pass jointly. No
   subgroup or alternative estimator can rescue failure.
4. Descriptive controls use UTC weeks instead of months; add exact currency
   to the monthly match; or require declared endpoints to equal visible
   endpoints. Each control retains the same five-record-per-group rule.
   Export a control only with at least 100 cells, paths and banks per role.
   Also report median contrast, mean squared cell contrast and the average
   estimated sampling variance `s_gap²/n_gap+s_no_gap²/n_no_gap`. These do not
   enter acceptance or establish homogeneous effects.
5. Report scoped and retained population counts. Audit eligible July
   accounts in either role and visible endpoint banks against all scoped
   May–June Direct records, including cross-role matches. Suppress small
   overlap counts or complements. No identities or row-level data leave
   local memory. Data are not altered, uploaded or copied.

## Exploration evidence and alternatives

The May–June primary has 1,047 cells, 764 paths, 414 first banks, 305 last
banks and 168,673 payments, including 9,946 with placeholders. The mean
contrast is -.090970 seconds. First- and last-bank intervals are
[-.284381,.119768] and [-.278721,.102929]. Weekly, currency-matched and
endpoint-agreement means are .026980, -.090998 and -.096021 seconds.
Mean squared primary contrast is 7.809446 s² versus estimated sampling
variance 7.338612 s². This comparison is descriptive, with uncertain
path-specific mean differences and dependent estimates.

Path matching controls the visible endpoint pair and its bank geography,
but not all account, date, selection or latent state differences. Month
matching may mask date interactions; the weekly control probes a narrower
time scale. Sparse gap-bearing paths fail eligibility and selection may
limit transport to all Direct payments. Shared accounts and banks persist
across rows, paths and periods. Separate role bootstrap intervals condition
on these populations and are sensitivity checks, not proof of independence
or causal confidence intervals. A near-zero mean does not prove that every
placeholder lacks a duration contribution.

## Prior exposure and provenance

Phase 0 and Round 1 full-data summaries, B01 and Round 2/3 duration outcomes
are exposed. B11 already compared same-path July duration differences,
including a descriptive control containing placeholders. B07 exposed July
placeholder shapes and B09/B15/B19/B23 exposed other July duration outcomes.
Thus the chosen July records are reused and cannot be an independent
holdout. The specific matched placeholder-versus-no-placeholder mean and
equivalence intervals have not been queried in July before this freeze.
This is a new internal contrast, not a repaired claim of B11's failed joint
noise hypothesis. That rejection remains unchanged.

Initial exploratory scratch queries failed on reserved alias `month`, then
an incorrect duration column name, before the successful source query used
`total_duration`. Neither failed query produced a result. The complete
executable and safe [exploration report](../../analysis/20_routing_time/out/H-B28_placeholder_duration_explore.md)
preserve the chosen estimator; no confirmation threshold will be retuned.
