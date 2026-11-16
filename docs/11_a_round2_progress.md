# A Round 2 progress register

Updated 16 November 2026. Worktree: `datathon-2026-R2-A`; branch `codex/r2-a-amount-generation`.
Research cutoff: 18 November 2026, 20:00 MYT. No new exploratory hypotheses after cutoff.
No automatic merge; final PDFs need user approval. Round 1 evidence remains unchanged.

| Hypothesis | Mechanism | Validation | Evidence strength | Blocker | Submission impact |
| --- | --- | --- | --- | --- | --- |
| H-A03 | Learned country equivalence classes predict FX counts over visible paths | Frozen internal validation completed. 99.5940% agreement vs 81.2848% baseline, with 98.5875% eligible coverage. | Rejected at the near-exact threshold. Comparative gain supported but not independently confirmed. | 99% bank-cluster lower bound 99.4690% vs required 99.5%. Round 1 reuse and 6,530 shared training banks. | High for approximate FX-count reconstruction with the rejected threshold displayed. |
| H-A04 | Do path gaps concentrate H-A03 errors? | Bit-0 exploration only. All 3,594 errors overpredict. Gap rates slightly lower within displayed Indirect length groups. | Exploratory signed-error clue. No support for broad gap concentration. | Covered gap strata have sparse errors. Phase 0, Round 1 and A03 exposure retained. | Negative comparison narrows the FX-count question; residual mechanism unresolved. |
| H-A05 | Learned class changes tighten the empirical FX upper bound | Frozen reused-population internal test passed. 0 violations in 876,388 eligible payments and 161,137 (18.3865%) tighter than country changes. | Supported but not independently confirmed. | Phase 0, Round 1, A03 unsigned error and A04 sign exposures documented. | Narrows the FX reconstruction. A03 exactness failure and the unresolved signed residual mechanism remain. |
| H-A06 | First visible path-country modal currency | Frozen internal July bit-1 test passed. 93.367% vs 89.408% declared sender. | Supported but not independently confirmed. | Prior currency/FX records exposed. Bank and country overlap, bank/corridor selection remain. | Explains which location is most associated with payment currency and much declared-path disagreement. |
| H-A07 | Receiving-country alternatives within currency exceptions | July bit-0 residual screen only. 28,220 of 49,548 match a sending-trained currency map applied to receiver country. | Exploratory. | Conditioning and EUR/USD prevalence confound interpretation. No frozen rule or validation. | Narrows currency-choice follow-up toward consistently learned endpoint/path maps. |
| H-A08 | Payment currency in visible-path country-mode set | Frozen internal test passed on 697,868 eligible July bit-1 rows. 98.7488% membership, 97.2536% endpoints, 24.2718% shifted-map and 29.3716% exact-set frequency controls. | Supported but not independently confirmed. | 8,732 outside-set currencies, prior A06 outcomes, shared banks/countries and route selection. | Extends first-country association to a controlled path-set compatibility relationship. |

## Completed and exposure

Read AGENTS, competition brief, the original case-study PDF, existing scientific helper and
A01/A02 code/records. Used Ponytail for minimal code. All pre-freeze queries used both-account exploration. The complete plan and executable were
committed at `2196f80cc3ab647ce67e7eb493aeed23cc190628` (16 November 17:31:22 MYT). Phase 0 and Round 1
aggregate exposure is disclosed in H-A03. No Round 2 colleague developing work was read.
Sponsor data remain a local ignored hard link; no rows or identifiers are printed/exported.
Initial materialisation hit the 512MB cap; switched to lazy streaming views without spill.

## Next wave

1. Audit discrepancies only as a new exploratory question with honest exposure disclosure;
   do not repair H-A03 and label it the same frozen success.
2. Consider further amount-tail/rounding and multi-currency mechanisms after reviewing this
   wave's submission value. No precise mixture weight follows from Round 1 grid shares.
3. Maintain new frozen records and register outcomes, then independent methodological review.

## Handoff

Goal: explanatory Round 2 value/FX mechanisms, no new infrastructure. New files are H-A03
script, invented-aggregate tests and hypothesis record, this register, and matching aggregate
reports. `uv run pytest` passed 68 tests. Frozen executable and helper matched the commit.
The original Parquet hash matched setup. Use the H-A03 record and its reported denominators
for independent review and production. The user is unavailable on 17 November 18:00-21:00 MYT.