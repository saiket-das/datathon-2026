# Setup Audit and Handover

Written 15 Nov 2026. Records the repository audit, the setup changes in [pull request #2](https://github.com/saiket-das/datathon-2026/pull/2), how they were verified, and what is left for the owner to decide. It covers repository readiness only; no competition analysis was done.

**Status:** pull request #2 is open and not merged. Its checks pass on Ubuntu and Windows. The existing `dataset/payments.parquet` is confirmed correct, so nobody who already built it needs to rebuild.

## Two things to know first

1. **Seven raw rows were exposed to an AI session during the audit.** A search command was scoped too broadly, matched inside the sponsor CSV, and printed seven synthetic records into a conversation with a cloud-hosted model. Nothing went to Git, a file or the pull request. `AGENTS.md` now has a rule against exactly this (rule 7).
2. **One of three full builds wrote a damaged Parquet file.** It had the right size and record count, but the start of one column (`BENEFICIARY_TOKENS`, about 2.9 KB) was zeros and could not be read back. The cause was not established; the repeat run was clean and byte-identical to the existing file. The build now reads every column back and compares it with the CSV before replacing the output, so a damaged file is rejected instead of used.

## A. Audit summary

### What was inspected

- Every tracked file, both remote branches, the merged pull request #1 and the full Git history.
- All five official PDFs in `docs/official/pdfs/`, and both Markdown copies compared against them word by word.
- Both preparation scripts, run against the real dataset on the owner's machine (macOS arm64, 8 GB RAM).

### Already correct

- The repository is private. No data file has ever been committed.
- The Markdown copies match the PDFs: 98–100% of each PDF's text is present; the remainder is page headers and footers.
- The existing Parquet matches the CSV: 10,000,000 records, original order preserved, no missing values except `ANOMALY_TYPE`.
- The figures quoted in the issues log reproduce from `profile.py` (for example 7,006 labelled rows, 317 `CUSTOMER_RECALL`, 75,803 payments from the busiest ordering account).
- All relative links between documents resolved, except one (below).

### Verified defects (all fixed in pull request #2)

| Defect | Evidence |
|---|---|
| `.gitignore` only blocked a list of extensions | `git check-ignore` showed `dataset/sample.xlsx`, `dataset/extract.json`, `dataset/rows.txt` and `out/rows.json` were all committable |
| `build_parquet.py` printed three individual records | Last line of the old script selected `ROW_ID <= 3` and printed it |
| `build_parquet.py` wrote straight onto the output | A failed re-run would destroy a good `payments.parquet`; there was no check that the CSV existed |
| `profile.py` hid failures | A failing query printed `ERR` and the script still exited with status 0 |
| Dependencies were unpinned | `uv run --with duckdb --with pandas` resolved to DuckDB 2.0.0 and pandas 3.1.1 on the day; DuckDB 2.0 has removed a call that 1.x had |
| `docs/06_potential_agent_tools.md` had a broken link and a wrong dataset size | Link pointed to `RESEARCH_PATHWAYS.md`; size given as 1.56 GB (the CSV is 4.6 GB, the Parquet 1.3 GB) |
| Install instructions covered macOS only | `brew install uv` was the only command given |
| `AGENTS.md` did not say that terminal output reaches the model provider | No rule on displaying records in a terminal or chat |

### Flagged, not changed

These are analytical or team decisions, so they were left as written.

- [03_execution_plan.md](03_execution_plan.md) quotes the generator as "hard-coded rules plus NumPy random calls". That phrase is in no official document. Treat it as an assumption.
- The account-half validation split (`hash(ORDERING_ACCOUNT) % 2`) is prescribed in three documents, although `AGENTS.md` says not to prescribe methods before inspecting evidence.
- The execution plan says Sunday has 683,541 payments against "about 1.4–1.9M on weekdays". Weekdays are 1.70–1.83M, and Saturday (434,935) is not mentioned.
- The execution plan says "400K ordering accounts". That figure is an approximate count; the exact number is 391,132.
- The judging rubric (criteria 2.1 and 3.4) says explanations may not draw on data from outside the provided dataset, while the handbook (3.3) allows cited external reference statistics. The safest reading is to use none.
- The submission-format PDF allows a dashboard as a link or a PDF; the rules (4.3) require PDF. The team already chose PDF.
- The handbook says the round starts at 11:40 AM and the rules say 11:50 AM; the handbook also calls 30 November a Tuesday (it is a Monday). Neither affects the deadline.
- `profile.py` shares its name with a standard-library module. It was not renamed; pytest is configured so it cannot interfere.

### Order of authority when sources disagree

1. The official PDFs and later organiser announcements.
2. Team decisions and owner instructions, where compatible with the official rules.
3. Repository conventions and `AGENTS.md`.
4. The optional research notes (`04_research_pathways.md`, `06_potential_agent_tools.md`).

## B. Setup plan and status

| Priority | Item | Status |
|---|---|---|
| P0 | Ignore all of `dataset/`; restrict `out/` folders to charts and Markdown | Done |
| P0 | Remove raw-row printing from the build | Done |
| P1 | Temporary-file write, read-back check and input check in the build | Done |
| P1 | Non-zero exit from the profile when a query fails | Done |
| P1 | `pyproject.toml` and `uv.lock` | Done |
| P1 | Dataset-independent tests, run on every pull request | Done |
| P1 | Windows instructions, documentation fixes, three new `AGENTS.md` rules | Done |
| P2 | Branch protection on `main` | Needs owner approval |
| P2 | Block `*.ipynb` (notebook outputs can embed rows) | Needs owner decision |
| Deferred | Polars, Pandera, statsmodels, Quarto, marimo, MCP servers, agent frameworks | No present need |

## C. Changes made

| Commit | Files | Before | After |
|---|---|---|---|
| `995f349` | `.gitignore` | Blocked extensions only | `dataset/` ignored except its README; `out/` accepts only `.png .jpg .svg .pdf .md`; more data-shaped extensions blocked everywhere |
| `d259a66` | `pyproject.toml`, `uv.lock` | No pinned environment | DuckDB, pandas, Matplotlib and SciPy locked; pytest as a development dependency |
| `05e6677` | `.github/workflows/checks.yml` | No automation | Locked install and pytest on Ubuntu and Windows; needs no secrets and no data |
| `62da345` | `README.md`, `AGENTS.md`, `analysis/README.md`, `dataset/README.md`, `docs/05_how_to_start.md`, `docs/06_potential_agent_tools.md` | Unpinned commands, macOS-only install, broken link | New commands, clone and Windows steps, link and size fixes, agent rules 7–9 |
| `1d4a024` | `analysis/00_prep/build_parquet.py`, `profile.py`, `test_prep.py` | See defects above | See below |

**`build_parquet.py`** now:
- prints aggregate checks only, never records;
- stops with a clear message if the CSV is missing;
- writes to a temporary file, reads every column back, and compares the record count and one exact figure per column against the CSV;
- moves the file into place only if those checks pass, so a failed run leaves an existing `payments.parquet` untouched;
- accepts `--src` and `--out` (used by the tests) and a `DUCKDB_MEMORY_LIMIT` environment variable (default 5GB).

**`profile.py`** now exits with status 1 if the Parquet file is missing or any query fails, and ends with `OK: all profile queries ran.` on success.

**`test_prep.py`** holds 31 checks that run in about 2 seconds on an invented six-record CSV: order and content are preserved, line breaks and quotes survive, no records are printed, each failure path fails loudly, `.gitignore` blocks data-shaped paths and allows the intended ones, and no data file is tracked.

## D. Environment

- **Python:** 3.11 or newer; uv installs it. Tested on 3.13.2.
- **Locked libraries:** DuckDB 2.0.0, pandas 3.1.1, Matplotlib 3.11.2, SciPy 1.18.1; pytest for development.
- **Run a script:** `uv run python <script>` from the repository root.
- **One-off extra library:** `uv run --with <name> python <script>`, noted in the script's docstring.
- **Add a library for everyone:** `uv add <name>`, then commit `pyproject.toml` and `uv.lock` together in a pull request.
- **Deliberately excluded:** Polars, Pandera, statsmodels, Quarto, marimo, MCP servers and agent frameworks. None solves a problem the repository has today.

## E. Verification

| Check | Result | Evidence | Limitation |
|---|---|---|---|
| Security | PASS | 14 data-shaped paths ignored and 9 intended paths allowed (tested); history scan clean; nothing under `dataset/` tracked except its README | A chart or Markdown file can still contain rows; that needs human review |
| Environment setup | PASS | `uv sync --locked` succeeds on macOS, Ubuntu and Windows | Windows checked in CI only, not on a teammate's laptop |
| Tests | PASS | 31 passed locally and in CI | The fixture is invented data, not the real schema's edge cases |
| Data preparation | PASS | Full build on the real CSV: 245 s, about 2.2 GB peak memory, every column matches the CSV, output byte-identical to the existing file | One earlier build was damaged, cause unknown; tested only on an 8 GB Mac |
| Profiling | PASS | All 18 queries ran on the real Parquet in about 9 s | The account-reuse quantiles are approximate and vary slightly between runs |
| Documentation | PASS | All relative links resolve; no old commands remain | External links not checked |

## F. Owner handover

1. Review [pull request #2](https://github.com/saiket-das/datathon-2026/pull/2).
2. Merge it yourself, then ask teammates to pull and run `uv run pytest`.
3. Decide on branch protection for `main` and on blocking notebooks.
4. Discuss the flagged claims in section A with the team before any of them reaches a slide.

The owner's local checkout is on the `setup/repo-hardening` branch.

## G. Teammate onboarding

1. Install uv: `brew install uv` on macOS, or `winget install --id=astral-sh.uv -e` in PowerShell on Windows.
2. Get the code:
   ```bash
   git clone https://github.com/saiket-das/datathon-2026.git
   cd datathon-2026
   ```
3. Check the environment (no dataset needed); expect `31 passed`:
   ```bash
   uv run pytest
   ```
4. Put the organiser CSV in `dataset/` (see [../dataset/README.md](../dataset/README.md)).
5. Build the Parquet copy, about 5 minutes; needs roughly 3 GB of free disk:
   ```bash
   uv run python analysis/00_prep/build_parquet.py
   ```
6. Run the profile; it ends with `OK: all profile queries ran.`:
   ```bash
   uv run python analysis/00_prep/profile.py
   ```

The commands are the same on macOS and Windows after step 1.

## H. Next phase

Once pull request #2 is merged, hypothesis work can start directly: the data is verified, the environment is locked, and the hypothesis template, owner folders and issues log are unchanged. No analysis has been started.
