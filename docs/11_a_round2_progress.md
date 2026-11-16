# A Round 2 progress register

Updated 16 November 2026. Worktree: `datathon-2026-R2-A`; branch `codex/r2-a-amount-generation`.
Research cutoff: 18 November 2026, 20:00 MYT. No new exploratory hypotheses after cutoff.
No automatic merge; final PDFs need user approval. Round 1 evidence remains unchanged.

| Hypothesis | Mechanism | Validation | Evidence strength | Blocker | Submission impact |
| --- | --- | --- | --- | --- | --- |
| H-A03 | Learned country equivalence classes predict FX counts over visible paths | Exploration complete; freeze and internal validation next | Exploratory | Round 1 reuse prevents independent-holdout claim | High if validated: explains most differences between FX count and country changes |

## Completed and exposure

Read AGENTS, competition brief, the original case-study PDF, existing scientific helper and
A01/A02 code/records. Used Ponytail for minimal code. All queries use only both-account
exploration until a complete new plan and executable are committed. Phase 0 and Round 1
aggregate exposure is disclosed in H-A03. No Round 2 colleague developing work was read.
Sponsor data remain a local ignored hard link; no rows or identifiers are printed/exported.
Initial materialisation hit the 512MB cap; switched to lazy streaming views without spill.

## Next wave

1. Freeze H-A03, record SHA/time, run unchanged internal validation and preserve failure if any.
2. Audit discrepancies only as a new exploratory question with honest exposure disclosure;
   do not repair H-A03 and label it the same frozen success.
3. Consider further amount-tail/rounding and multi-currency mechanisms after reviewing this
   wave's submission value. No precise mixture weight follows from Round 1 grid shares.
4. Maintain new frozen records and register outcomes, then independent methodological review.

## Handoff

Goal: explanatory Round 2 value/FX mechanisms, no new infrastructure. New files are H-A03
script, invented-aggregate tests and hypothesis record, this register, and matching aggregate
reports. Tests and final commit/PR links will be recorded after validation. Parent coordinator
handles parallel production and schedule. Routine progress must not block on user feedback
17 November 18:00-21:00 MYT.