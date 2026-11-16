# C investigation handoff

## 1. Goal and task scope

Independent role C investigation of entities/anomalies, assigned by worktree
`datathon-2026-C`. Started at detached `94fd417`; all work is on
`codex/c-entities-anomalies`. No other developing investigator branch, PR or
provisional finding was read. Shared scientific foundation was not changed.

## 2. Actions completed and files modified

- Read AGENTS, the official PDFs, scientific foundation, hypothesis template and
  owner instructions. Official PDFs remain unchanged.
- Used sender MD5 bit 0 for exploration, retaining whole sender sequences. Shared
  Phase 0 full-data exposure and account/bank overlap are disclosed in both plans.
- Screened six labels with aggregate amount, duration, type, repetition and entity
  consistency checks. Prioritised two falsifiable copy-burst signatures over broad
  anomaly correlations. Four other labels remain mechanistically unresolved.
- H-C01 reconstructs exact-amount/context duplicate batches; H-C02 reconstructs
  consumer-origin, chronological, variable-amount batches to either receiver type.
- Rejected variants are preserved: an unlabelled original per duplicate family;
  consumer-only romance receivers; exact amount repetition as a complete romance
  signature. Context template reuse, ordinary repeat invoices and file construction
  remain alternative explanations, rather than claims about original source code.
- Reproducible scripts, invented-data tests and aggregate reports/charts live in
  `analysis/30_parties_anomalies/`; full plans/results in `findings/hypotheses/`.
  README indexes and the issues log were extended with the new records.
- Frozen commit: `bd61bc32dc61f4985c757244051404fb6622a71b`,
  2026-11-16 08:19:47 UTC / 16:19:47 Malaysia. Both plans recorded the SHA before
  confirmation was opened; confirmation enforces identical frozen scripts.

## 3. Current status and test results

Both discovery signatures match every target-labelled exploration payment and no
unlabelled exploration payment. H-C01 also overlaps a small portion of romance
payments and is explicitly not exclusive. Exact copy context and file adjacency
are stronger claims than ordinary pair/amount repetition, but source-row adjacency
would disappear under row shuffling. Romance exploration cases occur only in the
first three million-row source blocks, despite spanning all three calendar months.

`uv run pytest`: **71 passed**, including 11 invented-data C tests. Both exploration
and both unchanged primary confirmation runs completed successfully. No script or
acceptance threshold changed after freeze. All four aggregate charts were visually
inspected. Confirmation is sender transfer conditional on prior Phase 0 exposure,
with shared receivers/banks/text; it is not complete entity-independent replication.

| Frozen confirmation | Target rows matching | Sender support | Unlabelled matches | Exact one-sided 97.5% lower bound, all-success senders |
|---|---|---|---|---|
| H-C01 duplicate bursts | 367/367 | 100 | 0/4,898,616 | 96.3783% |
| H-C02 romance bursts | 1,154/1,154 | 236 | 0/4,898,616 | 98.4491% |

Primary tests pass; no target exceptions were found. H-C01 also matches about
1.04% of romance-labelled confirmation rows, so it is not label-exclusive.
Romance business receivers replicate (26.1698%), and the restriction to the first
three million-row file blocks persists. Month/party/file-block checks are explicitly
descriptive and overlapping. Full denominators and limitations are in both records.

## 4. Blockers / pending approvals

None requiring user input. The GitHub connector returns 404 for this repository;
the authenticated local `gh` CLI can access the private repository and is the PR
fallback. No dashboard or slide production was attempted.

All sponsor processing runs locally. The dataset is accessed via a local hard link
inside ignored `dataset/`; there is no uploaded dataset, row export or committed
identifier. Reports expose only aggregate cohorts and suppress small strata.

Tools: Codex AI assistance, existing shared `scientific_checks.py` partition helper,
uv-pinned DuckDB/NumPy/SciPy/Matplotlib/Pytest, and pypdf for read-only original-PDF
extraction (`uv run --with pypdf`; no project dependency change). No external primary
data or external execution service was used. Ponytail and PDF skills guided focused
implementation and document inspection; neither authorises dataset disclosure.

## 5. Exact next step for the next agent

Review the unmerged C research PR against `main`. A teammate should independently
rerun both commands below before using a headline in the final PDFs:

```text
uv run python analysis/30_parties_anomalies/H-C01_duplicate_bursts.py --phase confirm --freeze-commit bd61bc32dc61f4985c757244051404fb6622a71b
uv run python analysis/30_parties_anomalies/H-C02_romance_bursts.py --phase confirm --freeze-commit bd61bc32dc61f4985c757244051404fb6622a71b
```

Use `out/*_confirm.png` as aggregate chart assets after review. Do not strengthen
the claims into original-code identification, an independent receiver/bank holdout,
or an operational fraud classifier. Account/detail/token mechanisms outside these
bursts, and the remaining four labels, are open questions for later work.
