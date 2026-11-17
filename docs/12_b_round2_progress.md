# Investigator B: Round2 progress and handoff

Started16November2026, branch `codex/r2-b-routing-generation`, isolated R2-B worktree.
Read AGENTS, shared protocol, Round1 B findings and original Rules PDF. Used local pinned
DuckDB/NumPy and Codex assistance; pypdf only to read the organiser PDF. No external data.
User research cutoff18November2026 20:00MYT; no new exploration afterward. The user is
unavailable17November18:00â€“21:00MYT; routine work does not wait for feedback.

| Hypothesis/question | Mechanism and current evidence | Validation | Evidence strength | Blocker / submission impact |
| --- | --- | --- | --- | --- |
| H-B04 bank-specific Covered stability | July bank probabilities reduce Brier error33.9% vs global and31.9% vs composition; calibration error .93points | Frozen internal test passed, f0259aa | Supported but not independently confirmed | Reused population exposure precludes independent holdout label; could materially explain rejected B03 coin |
| H-B05 joint endpoint disagreement | July mismatches 5.0485% ordering, 5.0402% beneficiary, 0.2547% jointly. Covered ordering reaches 5.8502%. | Frozen internal criteria passed at 1c4580b after audit-only syntax fix. Original freeze 4cec50a stopped before writing results. | Supported but not independently confirmed | Explains the pooled discrepancy rates. Route heterogeneity, signal direction and bank selection remain unresolved. |
| Endpoint disagreement explains Covered | Covered and Indirect endpoint agreement both about95%; simple mismatch interpretation inadequate | Exploratory aggregate screen only | Unresolved | No recovered mismatch mechanism; low priority |
| B01 duration transfer / B03 global coin | Round1 rejection remains intact | No retuning or replacement | Rejected | Useful methodological lesson, not a confirmed mechanism |

Round1 B04 population aggregate exposure and the rejected stricter pilot criterion are
fully disclosed in the hypothesis record. No wholly unseen data assertion is possible.
New helper/script uses512MB, one thread, no spill; no sponsor records or bank IDs exported.
Frozen scripts/evidence from Round1 remain unchanged.

## Freeze and validation log

Frozen at `f0259aa156723f60943dca219b8153532dca9860`, recorded before querying July B04 predictive errors/calibration. Exact scripts and criteria are preserved in that commit.

## Next step

July internal validation completed unchanged and passed all frozen criteria. Full safe
results are in the hypothesis record and `out/H-B04_covered_bank_stability_confirm.md`.
`uv run pytest`:69 passed in31.57s; four new invented-data tests passed. Independent
methodological review and an independent implementation remain outstanding. After that,
consider a separate fresh bank-selection/duration hypothesis, never relabel a tuned B01.
## Reproduce the rejected endpoint-mismatch shortcut screen

This is exploration only; all source reads must include the endpoint-bit0/0 predicate.
The statement can run locally through DuckDB in the existing pinned environment. It
returns route-level aggregates only, not individual records. No claim about the cause
or independence of mismatch events follows.

```sql
SELECT TRANSACTION_TYPE_CODE AS route, count(*) AS n,
  avg((ORDERING_BIC8=string_split(BIC8_PATH,';')[1])::INT) AS ordering_agreement,
  avg((BENEFICIARY_BIC8=string_split(BIC8_PATH,';')[-1])::INT) AS beneficiary_agreement
FROM read_parquet('dataset/payments.parquet')
WHERE ANOMALY_TYPE IS NULL
  AND (('0x'||substr(md5(ORDERING_BIC8),1,8))::UBIGINT%2)=0
  AND (('0x'||substr(md5(BENEFICIARY_BIC8),1,8))::UBIGINT%2)=0
GROUP BY 1;
```

## Current handoff / submission impact

B04 adds a materially useful interpretation beyond rejected B03: the near10% row share
conceals persistent known-bank routing propensities. It is an internally tested probability
approximation, not the exact Covered-selection mechanism or independent replication.
Use only after independent methodological review. No blocker to review; source-stage ordering,
corridor confounding and new-bank transfer remain unresolved. No new duration claim.
The next research pass can examine a separately planned bank-selection or duration mechanism;
freeze it separately and disclose all exposure here rather than tune B01 under its old label.
Do not merge this stacked Round2 PR until parent integration approval. Round1 scripts,
hypotheses and evidence were not modified. Parent coordinator controls the continuing
16–18November schedule and final cutoff inventory; this is the completed first B wave.

Second wave completed with H-B05 at retry freeze `1c4580bac192eac0d76727648796a6c2b14c9279`. The initial freeze `4cec50a611750402ace7a72e1d4602dbc6325ba1` failed in its final overlap audit because the pinned DuckDB rejects arrow lambda syntax. No result file or metrics were surfaced. The one-expression audit syntax correction preserved the data split, primary formulas, and all criteria. The regression test reproduces the original binding failure with invented data. The full suite passed 71 tests. The original Parquet SHA-256 remains `474ac30afd6378253fabd40c1f3ecd704ef5cd839947050b03bd1cf61fc2def3`.

For production, B04 can accompany the rejected B03 coin as a narrower known-bank approximation. B05 can accompany the endpoint disagreement issue as a pooled 5% per-role signature with a Covered subgroup exception. Each claim is conditional on the described population and needs independent methodological review before inclusion. Neither identifies the order of generator stages. See the hypothesis records for reproduction and exact overlap audits. The next B wave may test a separate timing or duration hypothesis if still before the research cutoff.

## H-B06 calendar timing screen

**Exploratory.** On 1,593,042 May–June endpoint-bit-0/0 unlabelled payments, UTC daytime share is 62.0435% weekdays versus 54.2453% weekends. Matching within ordering bank, route, party pair and month yields −6.9699 points, with 270 supported banks and about half the calendar cohorts retained. Simple minute/hour boundary piling is weak. Covered has inadequate separately matched bank support. Local scheduling, account/corridor composition and inference across dates remain unresolved. Phase 0, Round 1 and B04/B05 expose components of the population. A July check would be internal validation only. No validation queried or acceptance criteria frozen. See [H-B06](../findings/hypotheses/H-B06_calendar_timing.md) for exact scope and reproduction. Discovery-only mode applies through the research cutoff.

Follow-up: May and June, Saturday and Sunday, and all nine leave-one-week-out contrasts remained negative. The weekday-only placebo was +0.0590 points. Exact beneficiary-country, country/currency, beneficiary-bank and sender refinements could not reach the 100-bank gate. Same-country routes also lacked separate support. Freeze `9e737f1d1e1e028b634b318624360902e3b99715` preceded the unchanged July run. All four criteria passed. The matched contrast is −5.3911 points on 275 banks, covering 47,954/92,009 weekend and 285,728/558,659 weekday payments. Six week omissions span −6.2506 to −4.8242 points and the weekday-only placebo is −0.2520 points. Evidence is **Supported but not independently confirmed** because July records are reused. No causal, local-time or account-scheduling claim follows.

## H-B07 conditional placeholder placement

**Exploratory, confirmation-ready.** One gap is nearly uniformly located across internal path slots. With two gaps, v3/v4 adjacency is .677095/.518313, near the uniform weak-composition values .666667/.500000 and above independent slot allocation .500000/.333333. The original v3–5/two-gap pilot failed uncertainty criteria at v5 and is preserved. Before July shape outcomes, primary two-gap scope narrowed to v3/v4 while v5 stays descriptive. One-gap scope remains v3–5. Exchangeable ordered events conditional on counts and direct composition draws are observationally compatible. Phase 0/B02 previously exposed gap and adjacent-gap totals, including July, and other Round 1/2 analyses exposed records. Any frozen July result is internal only. Full criteria and source code are in H-B07, with no exact-implementation or source-stage-order claim.

H-B07 frozen result at `f28120d22534ea09b8a1015ac910dca4545b6ce3`: **Rejected** under the scoped conjunction. July v4/two-gap TV99 upper .074385 exceeds .06 and v5/one-gap .040449 exceeds .03. Point two-gap shape evidence still favors uniform weak compositions over iid per-gap slot allocation in v3/v4, but it cannot rescue the failed precision requirement. All July shape outcomes are now explicitly exposed. Full negative results and descriptive controls remain committed with unchanged scripts.

## H-B08 simple-path falsification

**Rejected in exploration.** May–June bit0/0 unlabelled displayed paths can repeat visible banks: 1,966/370,978 three-bank paths and 2,225/137,022 four-bank paths. Endpoints differ throughout the supported displayed cohorts. Candidate intermediate-bank sampling and endpoint exclusion remain unresolved. The script removes placeholders before testing visible adjacency, retains safe counts and has no validation mode. See [H-B08](../findings/hypotheses/H-B08_simple_paths.md). New precise sampling hypotheses require a separate freeze and exposure record. No independent-holdout, original-source-code or causal claim follows.

## H-B09 bank-associated short-duration exclusion

Exploratory and confirmation-ready. May Direct exposure identifies 1,061 supported visible banks, 440 with zero observed duration<100. In June, all-visible-bank-supported paths cover 646,066/891,959 v2-5 payments. All 209,343 containing an exclusion bank have duration>=100, whereas 86.5803% of other supported paths are fast. An exposure-bin label permutation gives 41.4656% fast among its exclusion paths. Supported route/length controls also have zero fast exceptions. A broad unnest/grouping query exceeded 512MB before results, replaced by fixed-position joins. A latent bank group/attribute remains among alternatives. Earlier exposure includes B06 July timing and B07 shapes. July B09 outcomes remain unexamined before freeze.

B09 passed its unchanged July internal test at freeze 399a3dd62f9cbcac3e0869585cb2a49c10f7d578. Evidence is Supported but not independently confirmed. Among462,931/638,824 eligible paths (72.4661%), all150,010 with a May exclusion bank have duration>=100. Other supported paths are86.5819% fast and the exposure-bin permutation cohort41.3393% fast. The primary cohort spans1,325 ordering banks,32,968 senders,69,913 receivers; known-bank/entity overlap limits the bank-bound interpretation. Literal service delays and source aggregation order remain unresolved.

## H-B10 country-class falsification

Rejected in May-only exploration. Of1,061 supported banks in142 countries,71 countries contain both observed May duration labels. Country-majority assignment misclassifies34.8728% of training banks, or39.5284% on the721 banks in countries with>=10 supported banks. Country alone cannot determine those observed labels, while probabilistic geography/latent classes remain open. No B10 validation claim.

## B11 and B12 follow-up

[B11](../findings/hypotheses/H-B11_same_path_duration_noise.md) isolates a small
timing component by pairing payments on the same ordered visible path. The May–June
mean squared difference is 100.35 s² at two banks and 98.82 s² at three. Their
90th-percentile differences are both 16 seconds. A discretised Gamma(2,5) shock
is compatible with that shape. At three banks, a fixed-scale shock count growing with
visible bank count fits worse. The fine-bin pilot missed a three-bank precision gate.
Its result is preserved alongside the discovery-informed coarse-bin plan.

[B12](../findings/hypotheses/H-B12_directed_endpoint_route_class.md) conditions
Covered versus Indirect on the directed first and last visible banks. May lookup
has zero June errors on 233,973 paths with known endpoints and unseen complete
visible sequences. Declared endpoints and reversing direction both give errors.
Direct payments can coexist on those directed pairs, so visible count is still
needed when considering all three route labels.

Both tests were frozen at `9489c1a051237433c0a6fbbbd260e602b2e27521`, committed
16 November 2026 at 21:46:08 MYT, before the specific July outcomes were queried.
The prior outcome exposure recorded for B01–B10 makes July an internal test.

- B11's joint test failed. At two banks, 162,341 July same-path pairs meet the
  frozen criteria. The 90th-percentile difference is 16 seconds and fitted-law
  discrepancy is small (TV .001435). The three-bank component missed both the
  5,000-pair minimum (4,794 observed) and the .020 upper TV gate (.033231).
- B12 passed. All 167,205 novel paths through May-supported directed endpoints
  match their May label. Coverage is 73.50% of July v3–5 unlabelled bit-0/0 rows.
  Reversing the pair gives 19.64% errors on jointly supported trials. The use of
  known endpoints and reuse of July records limit transport claims.

[B13](../findings/hypotheses/H-B13_symmetric_direct_duration.md) rejects a
symmetric Direct duration center. Among 905 supported bidirectional corridors,
31.05% have directional mean gaps above 100 seconds, versus zero of 2,040
same-direction May–June comparisons. A currency and FX matched subset still has
gaps. This exploration-only result provides a constraint on any model of the
stable route duration level.

[B14](../findings/hypotheses/H-B14_intermediate_bank_sampling.md) extends the
repeat-path investigation to the two interior positions of four-bank paths.
May rates from three-bank paths predict 0.6088% bank collisions, versus June's
0.5916% and a uniform-pool expectation of 0.0242%. The specific July collision
and joint-country results were unqueried before freeze
`b1dbe22f6712359081a4577de1643f032e9866ae` on 16 November 2026 at 21:53:11 MYT.
The unchanged July internal test passed. Across 55,865 four-bank paths, 0.6229%
repeat the interior bank and the pooled joint country TV is .016403. The estimate
is compatible with a shared weighted pool. It covers the tested collision and
country summaries and leaves exact identity weights and conditional dependence
unresolved.

## B15 supported three-bank duration decomposition

Exploratory, confirmation-ready. On 7,335/211,787 June three-visible-bank paths, May directed adjacent-edge medians plus a June −14.5s offset give MAE 7.5419s and 96.13% within20s. Equally calibrated maximum-edge comparison gives MAE21.6437s. This narrow coverage and shared edges limit transport and causal interpretations. B01 remains rejected. The new July B15 residual outcomes remain unqueried before freeze and reuse previously analysed records.

B15 was frozen at `44a4a5afa7959ad79e4bfe9058882a0a1f52e142` on
17 November 2026 at 03:15:34 MYT before opening its July errors.

## B16 currency and duration location

Exploration on 418 recurring Direct visible paths with at least ten payments in
each of two supported currencies covers 113,279 payments and 249 first visible
banks. No within-path currency mean range exceeds20 seconds. Median and99th
percentile ranges are1.1644 and5.4124 seconds. The same-path/currency month
reference has median mean drift .8659 seconds across1,900 cells. Higher currency-cell
support lacks adequate path/bank coverage. Large currency-specific shifts cannot
explain the observed locations on this subset. Other rare combinations and
account composition remain unresolved. The script is exploration only.

B15 frozen July test passed on5,219/151,146 payments (3.4530%).
Sum MAE7.323913s, maximum MAE21.820368s, ratio .335646 and96.148687% within20s.
Coverage stays narrow. Shorter-edge paths show similar sum/max errors.
July B15 outcomes are exposed. Known edges and shared entities limit interpretation.

## B17–B19 Direct duration and the directed Covered state

May–June exploration rejects a bank-score difference as the full explanation
for stable Direct duration asymmetry. In B17, 35.67% of 28,016 supported
triangles fail closure by more than 100 seconds, including 31.56% or more
after deleting any one bank. No split-month reference cycle exceeds 100
seconds. B18 finds approximately uniform 20–600-second gaps in 511 supported
asymmetric short-median corridors. A triangular difference-of-two-shocks
comparator fits worse.

B19 links the gap to a directed multibank label learned on different
payments. In exploration, 504 of 521 one-Covered pairs are slower in
the Covered direction by over 20 seconds. None of the 2,569 both-Indirect
pairs has a gap over 20 seconds. A shared directed corridor state could
generate the Covered label and a stable extra duration. The July outcomes
for B17–B19's specific contrasts are unqueried before freeze.

The three unchanged July checks ran after freeze `1979ad17f1431755e99d54a4579ade48eb35c71d`
at 03:27:59 MYT on 17 November 2026. All met their declared criteria.
These specific outcomes are now exposed.

- B17 rejected directional bank scores. 2,065 of 3,846 triangles fail
  closure by over 100 seconds. The failure share stays above 48.05% after
  any single-bank deletion. The split-period drift control has zero
  failures among 1,805 triangles.
- B18 supports the bounded conditional gap shape on 289 pairs and 127
  canonical first banks. TV is .036630 for a single uniform and .257841
  for the triangular comparator. The median directional gap is 318
  seconds, versus 3 seconds of split-period gap drift on eligible pairs.
- B19 links that asymmetry to earlier multibank route labels. The
  Covered direction is slower by over 20 seconds on 284 of 293
  one-Covered pairs, with zero reverse large gaps. There are zero large
  gaps across 643 both-Indirect pairs. The agreeing-endpoint control
  yields the same contrast. The labels and timing use separate payments
  but share known corridors and reused July data.

The next open question is what determines the directed Covered state,
including its relationship with bank support and pairs with no early
multibank witnesses. The observed rules do not determine assignment
for new corridors or identify the original sequence of generator stages.

## Round 3 discovery and exposure checkpoint

Resumed 17 November 2026 in the isolated B worktree from
`5cd77221d2b1769fbe16f700ed579fc47798da8a`. The organiser's original
Rules and Regulations section 3.3 restricts access to substantive work
to registered team members. Round 3 research remains local while the
GitHub destination is public. All earlier freezes and failures are
preserved. May–June queries preceded the new July outcomes.

| Hypothesis | Evidence and status |
| --- | --- |
| [B20](../findings/hypotheses/H-B20_unseen_corridor_propensities.md) | Frozen internal test passed on 3,384 of 5,008 novel repeated July corridors. Origin-only Brier .025336 versus .029565 global, .029831 receiver and .029426 directed country pair. The smallest 99% conditional lower gain is 5.38%. Receiver odds did not demonstrate incremental improvement over origin alone. |
| [B21](../findings/hypotheses/H-B21_reversed_path_penalty.md) | Exploration lacks matched support. Fewer than 100 exact reversed three-bank sequences, and none with all required Direct controls. No July query. |
| [B22](../findings/hypotheses/H-B22_covered_long_corridors.md) | Exploration lacks 100 pairs where both Direct direction medians are at least 100 seconds. No test of B19's transfer to slow baselines. |
| [B23](../findings/hypotheses/H-B23_edge_delay_propagation.md) | Frozen internal test passed. 3,111 of 151,146 July paths matched, 1,099 marked. Adjacent-only MAE 7.263 s, zero excess 244.262 s, outer only 289.970 s, both 132.056 s. Lowest 99% lower lift across controls and roles is 91.21%. |
| [B24](../findings/hypotheses/H-B24_origin_structural_zero.md) | Exploration rejects a literal zero-witness gate. Among 706 corridors from origins without May Covered witnesses, 1.13% are Covered in June. A graded origin rate beats the two-rate model on the whole 5,487-corridor comparison. |

B20 and B23 froze at `af07496a8a81d970bbb30531c1a4f484ec03fa55` on
17 November at 10:44:59 MYT. The unchanged `--phase confirm --freeze`
commands ran successfully and both July decision rows read True. These
outcomes are now exposed. B20 excludes both scored pair orientations
from May fitting, while every scored endpoint has May role support.
B23 uses separate May Direct and June calibration records and July
three-bank scoring. The evaluated July records and likely shared
accounts, banks, corridors, countries and dates limit both results to
internal tests. Separate bank-role resampling does not remove those
dependencies. Reproduction commands and denominators are in the records.

The current mechanism question is why origin propensities vary across
known banks. B20 and B24 constrain a candidate assignment function.
B23 shows that on supported three-bank paths the duration surcharge
transfers along adjacent pairs. The actual draw for the Covered state,
the higher-baseline timing process and longer path transfer remain open.
`uv run --locked pytest` passed 76 checks for this wave.

[B25](../findings/hypotheses/H-B25_covered_reciprocity.md) then tested
reciprocity in May–June exploration. Among 5,502 supported unordered pairs
and 88,634 payments, both directions are Covered on .800% of pairs versus
.438% estimated with calibrated independent origin rates. A 99% first-bank
interval for the gap excludes zero, while the second-bank interval spans
−.116 to .946 percentage points. Shared pair effects remain a possibility,
with no designated July outcome or frozen claim.
