# UMDAC Datathon 2026 · Swift Payments Case (Preliminary Round)

Private workspace for a 3-person team. Our task: **reverse-engineer the hidden rules Swift used to generate 10 million fake cross-border payments**, and present them as a dashboards PDF and a slide deck PDF.

**Deadline: Thursday 19 Nov 2026, 12:00 PM Malaysia time (UTC+8). No late submissions.** Team target: upload by 10:00 AM.

## New here? Read in this order

| # | Read | Why | Time |
|---|---|---|---|
| 1 | [docs/01_project_in_simple_words.md](docs/01_project_in_simple_words.md) | What the project is, in plain language, with key terms explained | 5 min |
| 2 | [docs/02_competition_brief.md](docs/02_competition_brief.md) | Deliverables, deadline, scoring weights, rules in one page | 3 min |
| 3 | [docs/03_execution_plan.md](docs/03_execution_plan.md) | Strategy, shared scientific foundation, validation protocol, responsibilities and submission checklist | 10 min |
| 4 | [docs/05_how_to_start.md](docs/05_how_to_start.md) | Step-by-step: setup, what to do first, the daily working loop, day-by-day schedule | 10 min |
| 5 | [dataset/README.md](dataset/README.md) | How to get the data and build the fast Parquet copy | 2 min, then ~5 min to run |
| 6 | [analysis/README.md](analysis/README.md) | Where to put your work and how to record a finding | 3 min |

Need the exact official wording? See [docs/official/README.md](docs/official/README.md), which says which PDF answers which question.

Optional tool and agent-integration ideas: [docs/06_potential_agent_tools.md](docs/06_potential_agent_tools.md). Use only if a specific need arises.

## Folder map

```text
README.md                  you are here
AGENTS.md                  instructions for AI assistants working in this repo
pyproject.toml, uv.lock    the Python libraries and their pinned versions (managed by uv)
.python-version            the Python version uv installs and uses (3.13)
.github/workflows/         automatic checks on every pull request (no dataset needed)
docs/
  handoff.md                     role A frozen investigation, results and exact review commands
  01_project_in_simple_words.md   plain-language introduction
  02_competition_brief.md         one-page factual brief of the rules
  03_execution_plan.md            team strategy and timeline
  04_research_pathways.md         optional method ideas (non-binding)
  05_how_to_start.md              step-by-step guide: setup, working loop, schedule
  06_potential_agent_tools.md     optional AI coding-agent tooling reference (non-binding)
  07_setup_audit_handover.md      repository audit, setup changes and how they were verified
  11_a_round2_progress.md       Round 2 A progress, validation and submission impact
  official/                       organiser PDFs + searchable Markdown copies (the authority)
dataset/                   the sponsor data lives here locally; NEVER committed
analysis/
  00_prep/                 shared: conversion, profile, scientific_checks.py, fixture tests
    out/scientific_checks.md  reproducible structural and validation aggregates
  10_amounts_currency/     owner A
    H-A01_amount_kernel.py     account-controlled business-party scale investigation
    H-A02_usd_rounding.py      exploration-trained EUR daily scaling investigation
    H-A03_fx_country_classes.py  Round 2 learned-country-class FX-count test
    test_fx_country_classes.py  invented aggregate graph tests
    out/H-A03_*                safe exploration/internal-validation reports
    test_value_mechanisms.py   dataset-independent calculation checks
    out/H-A01_*, H-A02_*       aggregate exploration/confirmation reports and charts
  20_routing_time/         owner B
  30_parties_anomalies/    owner C
    (each owner folder has out/ for charts)
findings/
    H-A01_amount_kernel.md, H-A02_usd_rounding.md  A's frozen plans and results
  issues_log.md            data problems found and the decision taken for each
  hypotheses/              one file per hypothesis (tested, confirmed or rejected)
    H-A03_fx_country_classes.md  Round 2 frozen internal-validation design
deliverables/              final dashboards PDF and slides PDF, plus the submission checklist
```

## Quick start (first time on a new machine)

You need Git and [uv](https://docs.astral.sh/uv/). uv installs Python 3.13 (pinned in `.python-version`) and the exact library versions pinned in `uv.lock`, so everyone runs the same environment.

| | Install uv |
|---|---|
| macOS | `brew install uv` |
| Windows (PowerShell) | `winget install --id=astral-sh.uv -e` |

Run these from the repository root. The commands are the same on macOS and Windows.

```bash
git clone https://github.com/saiket-das/datathon-2026.git
cd datathon-2026
# 1. check your environment (~1 min the first time, no dataset needed): the last line should say "passed" with no "failed"
uv run pytest
# 2. put the organiser CSV in dataset/ (see dataset/README.md)
# 3. build the Parquet copy once (~5 min, ~1.3 GB; needs ~3 GB free disk)
uv run python analysis/00_prep/build_parquet.py
# 4. check it works (~10 s): ends with "OK: all profile queries ran."
uv run python analysis/00_prep/profile.py
```

Need another library? For a one-off, `uv run --with <name> python <script>`. For the team, `uv add <name>` and commit `pyproject.toml` and `uv.lock` together in a pull request.

## Ground rules

- **Never commit or share the dataset** or raw records, including screenshots of individual rows in the PDFs. `.gitignore` blocks everything in `dataset/` and all data-shaped files; never override it with `git add -f`. Do not paste rows into an AI chat either: a cloud-hosted assistant is a third party.
- **Only the Swift dataset** is primary data. External statistics may support interpretation only, cited in APA style with URLs.
- **Every claim needs a script.** A number that goes in the PDFs must come from a script in `analysis/` that someone else can re-run.
- **Work on a branch, merge through a pull request**, and only edit files in your own analysis folder unless agreed. Name branches `<owner letter>/<topic>`, for example `b/duration-by-hops`; never push to `main` directly.
