# Investigator B: Round2 progress and handoff

Started16November2026, branch `codex/r2-b-routing-generation`, isolated R2-B worktree.
Read AGENTS, shared protocol, Round1 B findings and original Rules PDF. Used local pinned
DuckDB/NumPy and Codex assistance; pypdf only to read the organiser PDF. No external data.
User research cutoff18November2026 20:00MYT; no new exploration afterward. The user is
unavailable17November18:00–21:00MYT; routine work does not wait for feedback.

| Hypothesis/question | Mechanism and current evidence | Validation | Evidence strength | Blocker / submission impact |
| --- | --- | --- | --- | --- |
| H-B04 bank-specific Covered stability | May-to-June bank probabilities reduce Brier error versus global and composition rates; calibration error <1point | Plan/script ready to freeze before July predictive outcomes | Exploratory | Reused population exposure precludes independent holdout label; could materially explain rejected B03 coin |
| Endpoint disagreement explains Covered | Covered and Indirect endpoint agreement both about95%; simple mismatch interpretation inadequate | Exploratory aggregate screen only | Unresolved | No recovered mismatch mechanism; low priority |
| B01 duration transfer / B03 global coin | Round1 rejection remains intact | No retuning or replacement | Rejected | Useful methodological lesson, not a confirmed mechanism |

Round1 B04 population aggregate exposure and the rejected stricter pilot criterion are
fully disclosed in the hypothesis record. No wholly unseen data assertion is possible.
New helper/script uses512MB, one thread, no spill; no sponsor records or bank IDs exported.
Frozen scripts/evidence from Round1 remain unchanged.

## Freeze and validation log

Pending commit; record full SHA here before querying July B04 error/calibration.

## Next step

Commit exact B04 script and plan, record SHA, then run the unchanged July validation with
`--phase confirm --freeze SHA`. Preserve failure if any criterion fails. Independent
methodological review and an independent implementation remain outstanding. After that,
consider a separate fresh bank-selection/duration hypothesis, never relabel a tuned B01.