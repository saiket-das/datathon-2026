# Phase 2 — provenance, validation independence and disclosure audit

**P2 coordinator:** Scientific evidence auditor / synthesis only.  
**Scientific cutoff:** 18 Nov 2026, 20:00 Asia/Kuala_Lumpur.  
**What was executed:** source and repository metadata review only; no new empirical investigation.  
**What was NOT executed:** raw Parquet SHA-256 computation in this Chat, frozen reruns, bank-disjoint revalidation or original external coordinator logs.

## A. What is actually verified?

| Claim | Evidence accessible to this coordinator | Decision |
|---|---|---|
| Official use/redistribution restrictions | original rules text read | **Documented**: no third-party dataset redistribution, team-only substantive work |
| Dataset structure | uploaded `dataset_manifest.json` | **Manifest-declared** 10,000,000 rows, five 2M consecutive parts, 26 physical columns |
| Actual uploaded source bytes equal manifest | local runtime unavailable for physical file hashing | **Not independently verified** by this coordinator |
| A/B/C existing hypothesis artifacts | remote branch/PR inventory and published progress source | **Indexed**, no fresh code-level or data-level reexecution |
| A/B/C numerical frozen passes/failures | investigator frozen/result reports and original progress summaries | **Investigator-reported internal evidence**, not independent validation |
| C06–C48 local progression | external handoff statements only, no original remote evidence | **Not audited** |
| E01–E04 isolated worktree and replay | prior operator's local attestation, no original files in remote audit | **Not audited from source**; E05 unexecuted |
| D separate investigator | protected teammate work, intentionally unopened | **Not reviewed; isolation preserved** |
| F01–F03 empirical evidence | private handoff documents, F public protocol and research ledger | **Exploratory/private**; private execution provenance not independently verified |
| F04 | public proposal/implementation record | **Unexecuted**, no freeze/outcome |
| G01 | frozen public protocol plus private earlier aggregate report | **Restricted same-dataset test exists**; no independent confirmation, private publication barred |
| G02 | extensive public protocol and synthetic fixture/inference audit | **Unfrozen / no approved designated July test** |
| Repository consolidated into main | PR metadata | **No**: A/B/C and G PRs remain unmerged; consolidation branch kept separate |

## B. Dependence and prior exposure

1. **Phase 0 exposure:** full-data structural and anomaly-label aggregates were visible before later hypotheses.
2. **Entity reuse:** sender-MD5 splits remove literal same-role sender overlap but do not remove receivers, path banks, networks, text, or country/time state. Account-hash split also leaves banks and other dependencies.
3. **July reuse:** a July test on a reused dataset/entity network is *internal validation*, even when frozen before opening a specific designated outcome.
4. **Consecutive Parquet partitions:** five ordered parts are not independent random trials. `ROW_ID` can encode sequence/burst placement. Repartitioning them cannot manufacture independence.
5. **Model selection:** screening many ideas on May/June/July creates a selective reporting risk. Preserve unsuccessful attempts in the index and never compute a naive global success rate as if tests were i.i.d.
6. **Date semantics:** UTC is documented; bank-country is not a reliable individual timezone. Month/weekday stratification reuses social/bank context.
7. **Bank/path clustering:** bank resampling may ignore shared counterparties and correspondent structure; bank confidence limits should be stated as conditional sensitivities unless true exchangeability is justified.
8. **Rare anomaly labels:** entity/sequence family denominators matter, not just row counts. Label presence does not prove every unlabelled record is nonfraud.
9. **Hidden generator source:** statistical agreement cannot identify code, sampling order or a physical causal mechanism. Alternative samplers remain viable.

## C. Freeze verification policy for later private signoff

Before anyone marks a passed frozen hypothesis as verified, check:
- hypothesis ID and full exact claim; explicit eligibilities, exclusions, units and outcome;
- source branch full freeze SHA and *unchanged* executable and helper bytes;
- designated confirmation population first examined **after** freeze and exposure recorded;
- numerator, denominator, support, missing/unsupported strata, control groups and sensitivity intervals;
- each originally precommitted decision criterion, including conjunction and sample-size gates;
- source-mount dataset identity and immutable local checksum, with timestamp and exact command;
- shared bank/account/path/day reuse and adverse subsets;
- final verdict: exploratory / frozen internal pass / frozen failure / independently confirmed **only with genuine independent evidence**.

This P2 auditor did not run that checklist against every local private executable; the index is therefore a provenance-aware **handoff**, not a fully externally replicated audit.

## D. Private evidence review and non-publication

The coordinator separately inspected:
- A **private F03 exploratory report**. Its five *reported* partition SHA-256 strings match the uploaded manifest entries. That is a cross-document consistency check, **not a fresh byte-level SHA verification**. Its nested support populations change eligibility. It has no confirmatory freeze, confidence interval or causal conclusion. Exact report content, hashes, and small-cell-reconstructible combinations remain private.
- A **private G01 internal aggregate report** tied to a recorded public freeze protocol. Its directed-endpoint rule has a documented coverage limitation against the original acceptance gate. The supported zero-error component does not justify an unrestricted deterministic or independent-confirmation claim. The original report's data counts and controls are **not copied into the public branch**.
- A separate methodological review of A/B/C, which is *reviewer opinion*, not original validation output.

**Provenance reservation:** the private G report uses a local single-Parquet input, while the uploaded manifest describes five consecutive partition files. A matching row count or plausible subset does not authenticate byte identity across differently serialized sources; the local executor must separately attest equivalence if needed. Similarly, F's private source-hash output is not proof of runner configuration or correct SQL without host log review.

## E. Privacy and publication

- Organizer's Rules 2.2 and 3.3 restrict dataset sharing and team-outside substantive work. A public GitHub repository is not a team-only destination, regardless of the branch name.
- Historic temporary authorization permits scoped non-identifying work but does not license sponsor row publication or every private result. The repository's current visibility remains a live compliance issue.
- The consolidation branch contains **source links and already-public aggregate interpretations**, not private F03/G01 tables, C local reports, E/D protected outcomes, bank/account identifiers, daily rate maps or source rows.
- Do not force-add ignored `dataset/` files, publish private reports, export sensitive BIC identities, or leak small cells indirectly through totals/ratios/cross-tabs.
- Before any future public PR or merge, conduct full disclosure review and arrange team-only repository access where possible. This document is not a substitute for organiser authorization.

## F. Auditor's own time-ordered exposure log

1. Read official rules, Swift case study and project research protocol from user-provided sources.
2. Read 16 Nov project status snapshot and uploaded dataset manifest (no actual payment-row query).
3. Inspected remote A/B/C/F/G branch inventories, progress ledgers and selected original hypothesis records; checked open PR metadata.
4. Inspected earlier A/B/C methodological-review text from private Library.
5. Opened private F03 and G01 existing aggregate reports for documentary reconciliation, not independent testing.
6. Created separate coordination-only consolidation branch with derived documents. Did not modify existing investigator freezes, rerun validations, access D protected research or merge PRs.

The coordinator is **now exposed** to F03/G01 results and prior A/B/C findings. This chat must not represent itself as an independent/blind scientific evaluator of those claims.

## G. Remaining release gates

| Gate | Current state | Honest disposition |
|---|---|---|
| Accessible remote A/B/C source index | done | 63 indexed; qualifications preserved |
| Single statistical mechanism synthesis | done | public-known associations only, no causal order |
| Conflicts/failures retained | done | 7 frozen failures plus exploratory negatives |
| Private C06–C48 original evidence reconciliation | blocked | source not provided/verified |
| E original isolated checkout/freeze/result audit | blocked | local only; prior replay attested |
| F private full provenance signoff | partial | coordinator checks do not replace original executor logs |
| G01 private result source/protocol audit | partial | internal test only; population/support caveat |
| G02 frozen inference/validation | not completed | stop; no new research authorized |
| D first independent discovery | excluded | intentional isolation |
| Full raw-file byte-level verification | not done | no working local execution here |
| Final team scientific signoff | **NOT ATTAINED** | honest source-limited close-out only |
