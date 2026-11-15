# UMDAC Datathon 2026 · Swift Payments Case (Preliminary Round)

Private workspace for a 3-person team. Our task: **reverse-engineer the hidden rules Swift used to generate 10 million fake cross-border payments**, and present them as a dashboards PDF and a slide deck PDF.

**Deadline: Thursday 19 Nov 2026, 12:00 PM Malaysia time (UTC+8). No late submissions.** Team target: upload by 10:00 AM.

## New here? Read in this order

| # | Read | Why | Time |
|---|---|---|---|
| 1 | [docs/01_project_in_simple_words.md](docs/01_project_in_simple_words.md) | What the project is, in plain language, with key terms explained | 5 min |
| 2 | [docs/02_competition_brief.md](docs/02_competition_brief.md) | Deliverables, deadline, scoring weights, rules in one page | 3 min |
| 3 | [docs/03_execution_plan.md](docs/03_execution_plan.md) | Our strategy: day-by-day plan, who owns what, data traps, submission checklist | 10 min |
| 4 | [docs/05_how_to_start.md](docs/05_how_to_start.md) | Step-by-step: setup, what to do first, the daily working loop, day-by-day schedule | 10 min |
| 5 | [dataset/README.md](dataset/README.md) | How to get the data and build the fast Parquet copy | 2 min, then ~5 min to run |
| 6 | [analysis/README.md](analysis/README.md) | Where to put your work and how to record a finding | 3 min |

Need the exact official wording? See [docs/official/README.md](docs/official/README.md), which says which PDF answers which question.

Optional tool and agent-integration ideas: [docs/06_potential_agent_tools.md](docs/06_potential_agent_tools.md). Use only if a specific need arises.

## Folder map

```text
README.md                  you are here
AGENTS.md                  instructions for AI assistants working in this repo
docs/
  01_project_in_simple_words.md   plain-language introduction
  02_competition_brief.md         one-page factual brief of the rules
  03_execution_plan.md            team strategy and timeline
  04_research_pathways.md         optional method ideas (non-binding)
  05_how_to_start.md              step-by-step guide: setup, working loop, schedule
  06_potential_agent_tools.md     optional AI coding-agent tooling reference (non-binding)
  official/                       organiser PDFs + searchable Markdown copies (the authority)
dataset/                   the sponsor data lives here locally; NEVER committed
analysis/
  00_prep/                 shared: CSV -> Parquet conversion, first profile
  10_amounts_currency/     owner A
  20_routing_time/         owner B
  30_parties_anomalies/    owner C
    (each owner folder has out/ for charts)
findings/
  issues_log.md            data problems found and the decision taken for each
  hypotheses/              one file per hypothesis (tested, confirmed or rejected)
deliverables/              final dashboards PDF and slides PDF, plus the submission checklist
```

## Quick start (first time on a new machine)

You need Python 3.11+ and [uv](https://docs.astral.sh/uv/) (`brew install uv` on macOS).

```bash
# 1. put the organiser CSV in dataset/ (see dataset/README.md)
# 2. build the Parquet copy once (~5 min, ~1.3 GB)
uv run --with duckdb --with pandas python analysis/00_prep/build_parquet.py
# 3. check it works (~10 s)
uv run --with duckdb --with pandas python analysis/00_prep/profile.py
```

## Ground rules

- **Never commit or share the dataset** or raw records, including screenshots of individual rows in the PDFs. `.gitignore` already blocks `*.csv` and `*.parquet`; do not override it.
- **Only the Swift dataset** is primary data. External statistics may support interpretation only, cited in APA style with URLs.
- **Every claim needs a script.** A number that goes in the PDFs must come from a script in `analysis/` that someone else can re-run.
- **Work on a branch, merge through a pull request**, and only edit files in your own analysis folder unless agreed.
