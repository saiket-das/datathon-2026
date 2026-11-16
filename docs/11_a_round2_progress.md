# A Round 2 progress register

Updated 17 November 2026. Worktree: `datathon-2026-R2-A`; branch `codex/r2-a-amount-generation`.
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
| H-A09 | A common daily factor across stable modal scales | Bit-0 only. Three finite correlations range from .069 to .084. | Little support for dominant co-movement. | Sparse pair and date coverage and possible shifts in anchor denomination. | Led to a cross-denomination test within individual currencies. |
| H-A10 | Large-amount peaks identify a daily grid for small CHF and GBP payments | Frozen internal test passed. Daily grid 41.11% CHF and 40.36% GBP. Both controls at or below 1.27%. | Reused-account support for cross-denomination scaling. | SGD failed coverage and date support. Exact scale units and off-grid amounts unresolved. | Extends EUR rounding evidence across currencies and disjoint amount ranges. |
| H-A11 | Single-transition FX overprediction concentrates on sparsely observed directed country pairs | Frozen internal test passed. Zero residuals among 34,714 supported payments versus 100 among 4,372 unsupported. | Reused-account support, limited to one-transition July paths. | Route/edge selection and missing class links remain plausible. | Narrows the explanation for where the FX upper bound is loose. |

## Continuation and publication

A08 freeze `8bf80a9efd104bf2ebb200690a745443f02f4808` and results
`4b60bec204989675aae2f54a7701ba48e79b0188` were already local. The
unchanged frozen rerun reproduced the report byte for byte and exited 0.
Inspection found broad aggregate counts and cluster intervals. Account,
bank and country identifiers stay in local computation. Only the dataset
README is tracked under the dataset directory.

PR #8 was open at `256f6f5d474616e288a35b8c0f42299772077fb1`. GitHub
reported public visibility on 16 November. The original rules PDF,
section 3.3, limits substantive analyses and source code to the registered
team. A08 and the continuation remain local pending a verified team-only
destination. Earlier published material is already accessible on GitHub.

H-A10 froze at `f31764d04d8d4280281ace5f0e8c0dbc8cb1dff5` and H-A11
at `33bb0c0f921719c2f04bfc5debc18aad043ade8a`. Their records contain
the exact executable test, cutoffs, failed controls, reused-population
exposure and local reproduction commands.

## 17 November continuation

| Hypothesis | Outcome and qualification |
| --- | --- |
| H-A12 | Frozen internal test passed on 658,785 of 699,603 July bit-1 payments. Gaussian TV .007371 vs .038275 logistic and .082839 Laplace. Gaussian upper 99% TV .017461. No exact-tail or subgroup-law claim. |
| H-A13 | Frozen internal re-extraction passed on 208 CHF/EUR/GBP changes. Three direct-scale violations and zero reciprocal violations. Uniform fit advantage remains uncertain under seven-date blocks. |
| H-A14 | Frozen internal test repaired 1,036 class errors with zero new errors on 253,934 eligible July multibank payments. The maps cover 98.59% of scope. A03's frozen failure retains its original scope. |
| H-A15 | Bit-0 endpoint alternatives caused 31,444 first substitutions, 10,173 last substitutions and 49,529 prepend errors among 49,529 first-country exceptions. The geographic count made zero errors. |

H-A12 froze at `36627f0fda8e672ab279868b7807e83d48286acf`.
Its original plan is preserved, with a separate
[validation report](../analysis/10_amounts_currency/out/H-A12_log_shape_validate.md).
The lower 99% ordering-bank advantages were .020742 versus logistic
and .065301 versus Laplace. The test shares 4,156 of 5,356 banks with
training. H-A13/H-A14 froze at `7bd948fa5a5663bb9fc3d57ebd35bb567f4ab38f`.
Argon's methodological feedback informed exposure limits and dependence
checks. No new result is labelled an independent holdout.

GitHub still reported PUBLIC on 17 November. The additional commits remain
local under organiser rule 3.3. PR #8 is open and unmerged. The new FX rule
can next be probed on geography absent from the fitted map and the rate
update bound on currencies with competing anchor denominations.

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
