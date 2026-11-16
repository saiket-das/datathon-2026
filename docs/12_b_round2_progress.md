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
