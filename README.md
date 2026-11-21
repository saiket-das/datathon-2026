# UMDAC Datathon 2026 Â· Swift Payments Case (Preliminary Round)

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
  01_project_in_simple_words.md   plain-language introduction
  02_competition_brief.md         one-page factual brief of the rules
  03_execution_plan.md            team strategy and timeline
  04_research_pathways.md         optional method ideas (non-binding)
  05_how_to_start.md              step-by-step guide: setup, working loop, schedule
  06_potential_agent_tools.md     optional AI coding-agent tooling reference (non-binding)
  07_setup_audit_handover.md      repository audit, setup changes and how they were verified
  08_b_routing_investigation.md   B's independent search ledger, frozen tests and review handoff
  12_b_round2_progress.md        Round2 B hypotheses, validation exposure and handoff
  official/                       organiser PDFs + searchable Markdown copies (the authority)
dataset/                   the sponsor data lives here locally; NEVER committed
analysis/
  00_prep/                 shared: conversion, profile, scientific_checks.py, fixture tests
    out/scientific_checks.md  reproducible structural and validation aggregates
  10_amounts_currency/     owner A
  20_routing_time/         owner B
    H-B01_bank_additive_duration.py  bank-effect duration approximation
    H-B02_route_gap_process.py       fixed joint route-length/placeholder count law
    H-B03_covered_coin.py            rejected independent Covered-label candidate
    H-B04_covered_bank_stability.py  frozen internal temporal test of Covered propensity
    test_covered_stability.py         invented-data guard/uncertainty tests
    H-B05_endpoint_mismatch.py        frozen test of joint endpoint disagreement
    H-B06_calendar_timing.py          matched UTC calendar timing and frozen internal test
    H-B07_gap_placement.py            conditional shape test with preserved failed gates
    H-B08_simple_paths.py             repeated-visible-bank counterexamples
    H-B09_bank_duration_exclusion.py  supported-bank short-duration exclusion test
    H-B11_same_path_duration_noise.py  within-path duration variation and fixed noise laws
    H-B12_directed_endpoint_route_class.py  directed endpoints and multibank route class
    H-B13_symmetric_direct_duration.py  duration symmetry falsification
    H-B14_intermediate_bank_sampling.py  interior bank collision and country distribution test
    H-B15_edge_duration.py              shifted directed-edge duration decomposition
    H-B16_currency_duration_location.py currency-conditioned Direct duration screen
    H-B17_directional_triangle.py     directional bank-score falsification
    H-B18_bounded_directional_gap.py  conditional shape of Direct duration gaps
    H-B19_covered_direction_duration.py  multibank labels and Direct timing
    H-B29_institution_prefix_transfer.py  transfer from other origin banks in a BIC prefix
    H-B30_same_country_corridor.py    origin-matched country relation and Covered states
    H-B31_timing_origin_state.py      transfer of timing-derived origin groups to Covered states
    H-B32_country_novelty_support.py  matching support on previously unseen pairs
    H-B20_* to H-B28_*              corridor propensities, directional delays and mechanism falsifications
    duration_reversals.py            shared directed-median query for B17–B19
    H-B10_country_bank_class.py       country-only class falsification
    routing_common.py               local validation/privacy helpers
    test_routing_research.py         dataset-independent research checks
    out/                            safe exploration/confirmation charts and Markdown tables
  30_parties_anomalies/    owner C
  40_g_adversarial/        owner G, isolated falsification scripts/ledger and local aggregate executor
    (each owner folder has out/ for charts)
findings/
  issues_log.md            data problems found and the decision taken for each
  hypotheses/              one file per hypothesis (tested, confirmed or rejected)
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
