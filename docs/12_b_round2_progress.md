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

Both plans and scripts are ready to freeze. July outcomes for these particular
estimands have not been queried. The prior outcome exposure recorded for B01–B10
makes July an internal test. Publication is to the existing Round 2 research PR.
