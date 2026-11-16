# B: independent routing and duration investigation

## Scope and provenance

Investigator B was identified from worktree `datathon-2026-B`, initially detached at
`94fd417`. Work is isolated on `codex/b-routing-mechanisms`; no other investigator's
developing branch, PR or provisional findings were read. The shared scientific foundation
was not changed. Primary data: organiser Parquet only. A local ignored hard link in
`dataset/` points to the prepared Parquet on this machine; no sponsor file was uploaded.

Read AGENTS.md, the competition brief, the complete shared execution plan, hypothesis
template, B folder instructions and shared executed scientific checks. Consulted the five
original organiser PDFs (locally extracted with pypdf), especially the case-study feature
dictionary and scientific-method rubric, and the handbook/rules restrictions. Synthetic
data is not assumed representative of real-world geography or traffic. No external primary
data, web service or cloud computation was used for sponsor data. Tools: Codex-assisted
Python/SQL, pinned DuckDB/NumPy/SciPy/Matplotlib and pytest; pypdf was used only for
organiser-document reading. Code is newly written here, except reused foundation helpers.

## Discovery search ledger (before confirmation)

Selected the foundation's **bank** scheme for routing transfer, using both declared
endpoint-bank MD5 parity bits. Initial discovery queries were restricted to bit0/bit0.
Foundation baseline/partition outcomes were already exposed at full-data scope; confirmation
is conditional on that prior exposure. Shared intermediaries, accounts and endpoint/path
mismatches mean this is not a network-wide bank holdout. Schemes were not rerolled.

| Candidate/search | Exploration observation | Decision before freezing |
| --- | --- | --- |
| B01 duration by route, participants, FX, party and gaps | Strongly tailed durations; large bank heterogeneity | Reject a common hop-only explanation; test additive bank effects |
| B01 effects fitted to Direct path-bank pairs | Unrestricted additive effects predict longer exploration routes, but some coefficients are negative | Select a statistical approximation with explicit coverage/error tests; do not claim literal service times |
| B02 route length and gap counts | Visible-count tail and increasing gap risk fit a joint fixed event law; adjacent placeholders exist | Freeze the .35/.05/.60 law with an independence baseline and bank-cluster criteria |
| B03 .10 independent Covered coin | Near .10 row share conceals large bank concentration and excess zero-Covered banks | Reject during discovery; remove from B02 before freezing, retain falsification script/record |
| Initial broad UTC hour/day aggregate | Volume changes over UTC hours; no unique customer timezone follows from bank country | No local-time/business-hours claim selected or tuned |

Early unscaled latency solver trials reached their iteration limit. They were discovery
diagnostics only. Final code scales columns by exposure and requires convergence; the
exploration fit converged in 45 iterations. A trial with separate sender/receiver effects
was not selected: the same-bank additive approximation is simpler. No exact original
generator-code, causal-direction or nonnegative-processing-time claim follows.

The first B02 exploration report tested the compound count-law-plus-Covered candidate
and returned false because the Covered cluster interval was too wide. The candidate was
split **before freeze**; B03 retains that failure. Final primary B02 criteria apply only
to joint visible/gap counts. No confirmation statistic informed these changes.

## Frozen plans and reproduction

Full criteria, denominators, alternatives and uncertainty are in
[H-B01](../findings/hypotheses/H-B01_bank_additive_duration.md),
[H-B02](../findings/hypotheses/H-B02_route_gap_process.md), and rejected
[H-B03](../findings/hypotheses/H-B03_covered_coin.md).

Freeze commit: **`0607592078394baacf5454c6a1737916ea9b84c6`**, committed
**16 November 2026, 16:22:47 Malaysia time (UTC+8)**. This SHA/time was recorded before
any confirmation query. No confirmation outcome had been accessed at freeze. Plan/code verification is
enforced by `--freeze`. All excluded cross-bank-bit records remain unexamined by this
investigation, including robustness analyses. Monthly and labelled checks stay inside
the same selected partition; they are not additional independent holdouts.

```text
uv run python analysis/20_routing_time/H-B01_bank_additive_duration.py --phase explore
uv run python analysis/20_routing_time/H-B02_route_gap_process.py --phase explore
uv run python analysis/20_routing_time/H-B03_covered_coin.py
uv run pytest
```

Both selected tests were subsequently run unchanged with
`--phase confirm --freeze 0607592078394baacf5454c6a1737916ea9b84c6`.
Reports contain all predeclared subgroups, exceptions, coverage, actual eligible entity
overlap and cluster sensitivity intervals. Never label exploration Direct fit as validation.

## Results and handoff

| Investigation | Frozen confirmation outcome | Permitted conclusion |
| --- | --- | --- |
| [H-B02 joint route/gap law](../findings/hypotheses/H-B02_route_gap_process.md) | Pass on 2,730,400 unlabelled payments; TV=.000967, 99% bank interval [.000424,.001778]; distance ratio to independence=.027911 | An approximate .35 visible / .05 gap / .60 finish recipe reproduces the coarse joint counts; no exact-code or causal claim |
| [H-B01 duration approximation](../findings/hypotheses/H-B01_bank_additive_duration.md) | Fail: R2=.900205 (required >=.95); coverage 34.8982% (required >=60%) | Bank effects are useful partial evidence but the broad transfer rule is rejected |
| [H-B03 Covered coin](../findings/hypotheses/H-B03_covered_coin.md) | Rejected during discovery; no selected independent confirmation | The near-10% exploration row share does not establish independent payment-level assignment |

B02's visible-event 99% sensitivity interval [.348792,.349862] excludes exactly .35;
the predeclared practical tolerance passes, but exact probability equality is unsupported.
Actual unlabelled explore/confirm overlap is 11,558 account strings and 6,708 path banks,
with zero shared row IDs or declared endpoint banks. This limits independence claims.
Pooled labelled payments differ and are not covered by the primary rule. Cross-bit
records were never inspected; the count rule should not be asserted to hold there yet.

B01's eligible subset retains a substantial MSE improvement, but its chart must be
accompanied by the failed R2/coverage criteria when reused. All 1,827 eligible confirmation
path banks are shared with training. Negative effects preclude literal service-time claims.
No failed threshold was relaxed; no confirmation-refined model is labelled confirmed.

Confirmation reports and all four exploration/confirmation PNG charts are in
[`analysis/20_routing_time/out/`](../analysis/20_routing_time/out/), with matching stems.
Charts were visually inspected. Aggregate tables suppress low-support statistics.
The executable files are unchanged from the freeze commit; only result documents and
confirmation aggregates were added after freezing.

1. **Goal and scope:** precise, falsifiable routing/duration relationships, safe aggregates,
   a reviewable PR to main; no dashboard or slide production.
2. **Completed/files:** three hypothesis records, corresponding analysis scripts, shared
   local helpers, dataset-independent checks and exploration/confirmation reports/charts in B's folder.
   README maps updated. Other investigators' files and shared foundation untouched.
3. **Status/checks:** both unchanged frozen tests completed, including negative outcomes;
   full suite passed with 65 tests before freeze. Final pre-PR `uv run pytest`:
   **65 passed in 25.00 seconds**; `git diff --check` passed; executable diff against
   the freeze commit is empty. All four charts visually inspected with readable labels.
4. **Blockers:** none for review. Exact hidden implementation, latency interpretation
   and bank-dependent Covered assignment are unresolved.
5. **Exact next step for reviewer:** use the recorded freeze SHA and commands to rerun
   B02's confirmation; verify its primary and sensitivity tables. Review the H-B01 failure
   before selecting headline findings. Continue production planning only after independent
   review; a revised duration or Covered rule requires a new validation design and disclosure
   of the confirmation outcomes already exposed here.

Independent teammate review must rerun eventual headline figures. It has not been performed
by this investigator and must not be claimed as complete.
