# Agent Instructions

1. Read `docs/02_competition_brief.md` and consult the relevant original PDFs in `docs/official/pdfs/` before relying on competition requirements. The Markdown versions in `docs/official/markdown/` are searchable references; `docs/official/README.md` maps each question to its document. `README.md` describes the folder layout.
2. **Do not assume which hidden rules exist, or prescribe methods before inspecting evidence.** Form your own plan, state hypotheses as hypotheses and revise them when tests disagree.
3. Make every material claim traceable to reproducible calculations or charts. Distinguish observations, interpretations, rejected hypotheses and remaining uncertainty.
4. Honour the competition's restrictions. Never commit or publish the sponsor dataset, raw records, private credentials, or unauthorised extracts. Do not incorporate outside primary datasets.
5. Keep changes small and reviewable. Preserve existing team work; document how to reproduce any new analytical result. Coordinate substantial changes through branches and pull requests.

This is a neutral handoff, not a prescribed solution, tool stack or list of expected findings.

## Folder structure (follow it; do not invent new top-level folders)

| What you are creating | Where it goes | Naming |
|---|---|---|
| Analysis script | The owner's folder: `analysis/10_amounts_currency/` (A), `analysis/20_routing_time/` (B), `analysis/30_parties_anomalies/` (C) | `H-<owner letter><number>_<short_name>.py`, matching its hypothesis file |
| Shared data preparation | `analysis/00_prep/` | Numbered or descriptive, e.g. `build_parquet.py` |
| Chart or aggregate table produced by a script | `out/` inside the same analysis folder | Same stem as the script |
| Hypothesis record (confirmed, rejected or uncertain) | `findings/hypotheses/` | Copy `H-000_template.md` to `H-<owner letter><number>_<short_name>.md` |
| Data problem and the decision taken | Add a row to `findings/issues_log.md` | — |
| Team notes, plans, explanations | `docs/`, numbered to continue the reading order | `NN_short_name.md` |
| Final submission PDFs | `deliverables/` | `dashboards.pdf`, `slides.pdf` |
| Sponsor data and anything derived at row level | `dataset/` only (git-ignored) | — |

Rules:

1. Before creating a file, check whether an existing file already covers it and extend that instead. Do not create duplicate plans, summaries or scratch notes in the repository; use a temporary directory outside the repo for scratch work.
2. Do not move, rename or delete existing files or folders unless the user asks.
3. Every script starts with a docstring stating what it tests and the exact command to run it from the repository root. Scripts read `dataset/payments.parquet`, not the CSV, and output aggregates only.
4. When you add a folder or a document, update the folder map in `README.md` and any index that lists it.
5. Git does not track empty folders. A folder that must exist before it has content holds an empty `.gitkeep` file; leave those in place.
6. Files in `docs/official/` are organiser documents: read-only.
