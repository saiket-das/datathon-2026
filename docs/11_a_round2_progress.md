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

## Round 3 discovery, 17 November 2026

| Hypothesis | Status and evidence |
| --- | --- |
| H-A16 | Frozen internal pass. Class-filter removal scores 2,909 of A14's 3,632 exclusions without error. Strong mode map covers 256,843 of 257,566, or 99.72%. All 723 residual exclusions lack both strong maps. Weak modes and necessary edgewise bounds gave no observed contradiction. |
| H-A17 | Exploratory negative result. Same-day tenth-unit fits beat shifted dates after conditioning on the off-unit population. None clears the two opportunity-matched phase controls. |
| H-A18 | Exploratory. Whole-dollar, one-digit and two-digit heaping differ markedly in USD. A universal single one-digit rule would leave most observed amounts unexplained. Magnitude, party strata and weak half-dollar heaping are recorded. |
| H-A19 | Frozen internal pass. EUR fits current-date scales around 40% in the first and last two UTC hours, with paired lifts of 38.38 and 38.48 points against the union of neighboring rates. Date windows are reused and the exact switching instant remains open. |
| H-A20 | Frozen internal pass. Maps trained separately on two-bank and multibank payments each scored all 695,472 jointly mapped July rows without error. Each supplied route type met the 98% eligibility floor. |

H-A16 froze at `319f6d2f25bf9bc62911a37e58b495809ee8e43a`.
H-A19 froze at `5b6b952ed029696e0991df60d677998a64cc7c4c`.
H-A20 froze at `a045ce3340ccc00df5e8aee0918d719f1d0474a2`.
All three tests scored both-account bit-1 after freezing. H-A17 and H-A18
queried bit-0 only. Known May/June/July exposure, dependency limitations,
thresholds and reproduction commands are recorded in each hypothesis.
The repository remains public. Local research stays within the A worktree.
The unchanged frozen tests and all five exploration commands ran successfully.
`uv run --locked pytest`: 68 passed.

## Completed and exposure

### A22 — USD quantization levels, 17 November

Exploratory only. Command: `uv run --locked python analysis/10_amounts_currency/H-A22_usd_quantization_levels.py`.
129,847 scoped July bit-0 USD payments;123,641 selected observed decades2–6,
6,206 excluded. Preferred exact mantissa5 mass is a lead, not a verified
generator rule:4,116/12,404 leading-5 rows versus685/10,819 leading4 and
569/7,489 leading6. Leading1 also has a large mass but decimal boundary
crossing is a competing explanation. Existing A18 varied-grid results
remain intact. A symmetric local-density control is the next step.
No validation queried, no quantizer-mixture weight inferred. Prior
Phase0/Round1, rounding, UTC and rate exposures explicitly retained.

### A21 — country context, 17 November

Frozen all-criteria prediction claim rejected. Freeze
`b82670542b97fa295cf719d7cd48a978af035f55`; executable and helper unchanged.
Command: `uv run --locked python analysis/10_amounts_currency/H-A21_country_amount_context.py --phase validate --freeze b82670542b97fa295cf719d7cd48a978af035f55`.
The first-path-country residual correction reduces row MSE descriptively
by2.4768% on656,546/699,603 covered July bit-1 payments, but upper99
bank-cluster model/base ratio .984483 exceeds frozen .98. Other ratio
and support criteria pass. 75,374 senders,255,885 receivers,5,228 banks;
4,045 banks overlap training. A weaker conditional association remains
supported, without an independent holdout, causal wealth effect or
generator architecture claim. Receiver correction and rotated-country
negative controls remain in the complete aggregate report. Phase0,
Round1 and A01-A20 exposure applies. No raw data or identifiers exported.
Tests before freeze:68 passed; diff checks passed. A03 failure remains.
Next opportunity: explain previously observed USD rounding/heaping using
bit-0 exploration, without inferring mixture weights from compatibility.

Read AGENTS, competition brief, the original case-study PDF, existing scientific helper and
A01/A02 code/records. Used Ponytail for minimal code. All pre-freeze queries used both-account exploration. The complete plan and executable were
committed at `2196f80cc3ab647ce67e7eb493aeed23cc190628` (16 November 17:31:22 MYT). Phase 0 and Round 1
aggregate exposure is disclosed in H-A03. No Round 2 colleague developing work was read.
Sponsor data remain a local ignored hard link; no rows or identifiers are printed/exported.
Initial materialisation hit the 512MB cap; switched to lazy streaming views without spill.

## 17 November 16:00 continuation and publication

Recovered committed A21/A22 and uncommitted A23 instead of restarting their
experiments. A21's failed threshold was preserved. A23 froze at
`7581544b1917f567ffabf8d4b18796268f1fd62b` and passed unchanged on
25,967 selected July bit-1 USD payments. The five-anchor ratio was
7.4086 [6.7446,8.2617], control .9245 [.7618,1.1159].

A24 froze at `559bdce5a72fd02708fd4249c683df3fb956d086` and failed.
Only 72 of 73 common EUR dates met the near-identical-scale criterion,
below 99%, and every party-pair disagreement bound exceeded .002.
One ratio was approximately .2. No date, scale or threshold was changed
after scoring. A25 explores a shared preferred-denomination explanation
under the pre-existing whole-population rate fit as a distinct question.

A25 froze at `ee8a5c55b97d31404ff3a28d444a4eca9c36abcf`. CHF/EUR/GBP
all passed, with selected counts 14,466/68,535/15,650, preferred-five
ratios 6.4404/6.9461/7.0102 and full near-one seven-anchor controls.
This test selects whole untruncated local windows under the amount cutoff.
Dates and previous account outcomes overlap; no independent confirmation
or generator source-code claim is made. All scripts suppress source-valued
error details and export only aggregate tables. The A23/A24 frozen code
and helper comparisons were verified before their outcome runs.

Publication decision updated under the user's explicit temporary
authorisation to use the connected research branch for code and safe
aggregate evidence. Earlier public-visibility holds above describe their
historical decisions. Repository visibility remains public. Publication
includes no sponsor records, bank/account identifiers, daily rate tables
or credentials. Only dataset/README.md is tracked under dataset/.
The existing PR remains unmerged. The pre-publication local suite passed
68 tests in 29.41 seconds with uv --locked.

### A26 — sender residual persistence versus bank context

May-to-June bit-0 exploration only. On 8,545 matched cells across6,163
senders and958 banks (476,291 June payments), sender mean residuals
correlate .6372. Own-history error does not improve over a matched
bank/currency/party peer:ratio1.0370, nominal99% bank sensitivity
.9860–1.0880. The exploratory own-history screen fails. Separately
centering each month's bank/currency/party groups reduces the
correlation to .0190. That centering uses target outcomes and remains
a descriptive variance-structure diagnostic. No new bit-1 outcome
or July confirmation query was made. The next question is which
group attributes explain shared persistent amount scale, alongside
how preferred denominations produce the A24 factor-five alias.

The authorised A08–A25 research publication was verified on GitHub at
`59f5ba1a3f368e9febed356f870d1bb981139936`. PR8 remains open and unmerged.
Its Ubuntu and Windows CI checks passed. The earlier blanket public
visibility hold was superseded by the user's explicit temporary
publication authorisation for safe code and aggregates. No raw or
identifying sponsor extracts were added.

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
