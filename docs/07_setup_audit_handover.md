# Setup Audit and Handover

Written 15 Nov 2026 and corrected the same day after an independent review of the pull request (see [Correction pass](#correction-pass-after-review)). Records the repository audit, the setup changes in [pull request #2](https://github.com/saiket-das/datathon-2026/pull/2), how they were verified, and what is left for the owner to decide. It covers repository readiness only; no competition analysis was done.

**Status:** pull request #2 is open and not merged. Its checks pass on Ubuntu and Windows. On the owner's machine the existing `dataset/payments.parquet` passes the row-level comparison with the CSV described in section D2, so there is no known reason to rebuild it. That is a digest comparison with stated limits, not a proof of exact equality.

## Two things to know first

1. **Seven raw rows were exposed to an AI session during the audit. This is recorded, not resolved.** A search command was scoped too broadly, matched inside the sponsor CSV, and printed seven synthetic records into a conversation with a cloud-hosted model. The disclosure cannot be undone; the rules added since only reduce the chance of a repeat. See [section I](#i-confidentiality-assessment) for the assessment and the owner's recorded decision to document internally without contacting organisers for now.
2. **One full build wrote a damaged Parquet file, and the cause is unknown.** Of the four full builds of this dataset (the owner's original and three run during this work), one produced a file with the right size and record count in which the start of one column (`BENEFICIARY_TOKENS`, about 2.9 KB) was zeros and could not be read back. The other three are byte-identical to each other. The build now compares the written file with the CSV before replacing the output, which rejects such a file; it does not remove whatever caused it. See [section J](#j-the-damaged-build).

## A. Audit summary

### What was inspected

- Every tracked file, both remote branches, the merged pull request #1 and the full Git history.
- All five official PDFs in `docs/official/pdfs/`, and both Markdown copies compared against them word by word.
- Both preparation scripts, run against the real dataset on the owner's machine (macOS arm64, 8 GB RAM).

### Already correct

- The repository is private. No data file has ever been committed.
- The Markdown copies match the PDFs: 98–100% of each PDF's text is present; the remainder is page headers and footers.
- The existing Parquet has 10,000,000 records, the same as the CSV, with no missing values except `ANOMALY_TYPE`. Its content and record order agree with the CSV under the row-level digest comparison in section D2.
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
| P2 | Branch protection on `main` | Owner decision recorded: require PR and passing CI, block force pushes and deletion; configure after merge where supported |
| P2 | Block `*.ipynb` (notebook outputs can embed rows) | Implemented in PR #2: ignore rule, agent instructions, regression tests |
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
- writes to a temporary file and compares it with the CSV using one MD5 digest per record over the record's position and all 20 original columns (section D2). The first version of this pull request compared only per-column totals (sums and total text lengths), which could not see same-length or sum-preserving changes; the review was right about that;
- moves the file into place only if those checks pass, so a failed run leaves an existing `payments.parquet` untouched;
- accepts `--src` and `--out` (used by the tests) and a `DUCKDB_MEMORY_LIMIT` environment variable (default 5GB).

**`profile.py`** now exits with status 1 if the Parquet file is missing or any query fails, and ends with `OK: all profile queries ran.` on success.

**`test_prep.py`** previously held 44 checks; four notebook exclusion cases were added (48 total, subject to final CI) that run in about 5 seconds on an invented six-record CSV: order and content are preserved, line breaks and quotes survive, no records or error details are printed, each failure path fails loudly, ten kinds of damage are detected (section D2), a failed verification never replaces the output, `.gitignore` blocks data-shaped paths and allows the intended ones, and no data file is tracked.

## D. Environment

- **Python:** 3.13, pinned in `.python-version`; uv downloads it if the machine does not have it. `pyproject.toml` still allows 3.11 or newer, so the lock file resolves for those versions, but only 3.13 has been run (3.13.2 on the owner's Mac; CI installs 3.13 on Ubuntu and Windows).
- **Locked libraries:** DuckDB 2.0.0, pandas 3.1.1, Matplotlib 3.11.2, SciPy 1.18.1; pytest for development.
- **Run a script:** `uv run python <script>` from the repository root.
- **One-off extra library:** `uv run --with <name> python <script>`, noted in the script's docstring.
- **Add a library for everyone:** `uv add <name>`, then commit `pyproject.toml` and `uv.lock` together in a pull request.
- **Deliberately excluded:** Polars, Pandera, statsmodels, Quarto, marimo, MCP servers and agent frameworks. None solves a problem the repository has today.

## D2. What the CSV-to-Parquet verification establishes

Run automatically at the end of every build, and on demand with `uv run python analysis/00_prep/build_parquet.py --verify-only`.

**What it checks**
- **Record count:** the same from a parallel read of the CSV, a sequential read of the CSV, and the Parquet.
- **Content and order:** for every record, an MD5 digest over its position in the file and all 20 original columns. The digests are combined by XOR and by sum into a fingerprint, computed once from a fresh sequential read of the CSV and once from the Parquet as read back from disk. The two must be equal.
- **Typed conversion:** numbers are compared after conversion, and the number of numeric fields whose CSV text is not reproduced exactly by its typed value is reported. On the real data it is 0, so every integer and amount converts back to its original text.
- **Structure:** `ROW_ID` runs 1 to n, the 26 columns are present in order, and each helper column equals its definition.

**Exact or probabilistic?** Probabilistic. A digest comparison cannot prove equality. For accidental damage (a zeroed block, a truncated file, a swapped or altered value) an undetected difference would need an MD5 collision, which is not a realistic outcome. It is not a defence against deliberate tampering.

**What can still escape**
- A fault in DuckDB's CSV reader that repeats identically in both reads, including a wrong record order. `--independent` narrows this by recomputing the CSV fingerprint with Python's `csv` module and `hashlib`, which share no code with DuckDB. It passed on the real data.
- A fault shared by both parsers, or in the CSV file itself as downloaded.
- Damage to the file after it was verified (disk fault, later overwrite). Re-run `--verify-only` if in doubt.

**When it fails:** the temporary file is deleted, the existing `payments.parquet` is not touched, the script exits with status 1, and the message names the failed check without quoting data.

**Damage patterns covered by tests** (invented fixture, through the script's own verification): one text field changed at the same length; two amounts changed with the same sum; two integers changed with the same sum; a value swapped between two rows; a label moved to another row; two records exchanging positions; a wrong helper column; a missing record; a truncated file; a block of zeros inside a file of unchanged size.

**Cost on the owner's Mac (8 GB RAM):** about 40 s added to each build, peak memory about 2.5 GB. `--independent` adds about 75 s.

## E. Verification

| Check | Result | Evidence | Limitation |
|---|---|---|---|
| Security | PASS | 18 data-shaped paths ignored and 9 intended paths allowed (the four new notebook cases require final CI); history scan clean; nothing under `dataset/` tracked except its README | A chart or Markdown file can still contain rows; that needs human review |
| Environment setup | PASS | `uv sync --locked` succeeds on macOS, Ubuntu and Windows | Windows checked in CI only, not on a teammate's laptop |
| Tests | PASS | 44 passed locally (macOS) and in CI (Ubuntu, Windows) before the notebook changes; 48 expected in updated CI | Invented six-record fixture; it shows the checks work, not that the real data is correct |
| Data preparation | PASS, with limits | Owner's machine, real CSV, final script: full build 226 s, about 2.2 GB peak memory, passed the row-level comparison; output byte-identical (`cmp`) to the existing file. `--verify-only` on the existing file: 41 s, 2.5 GB peak. `--verify-only --independent`: 116 s, passed | Digest comparison, not value-by-value proof (section D2). One of four builds was damaged, cause unknown. Run only on one 8 GB Mac; not run on Windows with real data |
| Profiling | PASS | All 18 queries ran on the real Parquet in about 9 s | The account-reuse quantiles are approximate and vary slightly between runs |
| Documentation | PASS | All relative links resolve; no old commands remain | External links not checked |

## F. Owner handover

1. Review [pull request #2](https://github.com/saiket-das/datathon-2026/pull/2).
2. Merge it yourself, then ask teammates to pull and run `uv run pytest`.
3. After merging, configure `main` to require pull requests and successful Ubuntu/Windows CI checks, without mandatory review approval; disable force pushes and deletion. Confirm whether the private repository's GitHub plan supports enforcing these rules. Notebook exclusion is implemented in this PR.
4. Discuss the flagged claims in section A with the team before any of them reaches a slide.

The owner's local checkout is on the `setup/repo-hardening` branch.

## G. Teammate onboarding

1. Install uv: `brew install uv` on macOS, or `winget install --id=astral-sh.uv -e` in PowerShell on Windows.
2. Get the code:
   ```bash
   git clone https://github.com/saiket-das/datathon-2026.git
   cd datathon-2026
   ```
3. Check the environment (no dataset needed); the last line should say `passed`, with no `failed`:
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

## I. Confidentiality assessment

**What happened.** During the audit, one search command run by the AI assistant matched inside the sponsor CSV and seven synthetic records were printed into the assistant's session. The records are not reproduced here or anywhere in the repository.

**Where the records went, and where they did not**

| Kind of exposure | Status | Basis |
|---|---|---|
| To the AI model provider | Yes, seven records | They were part of the session's input |
| In the GitHub repository | None found | Scan of all tracked files and every commit diff for account-identifier and bank-path patterns: 0 matches |
| In the pull request text, comments or reviews | None found | Same scan: 0 matches; there are no review comments |
| In CI logs or artefacts | None found | Both CI runs scanned: 0 matches, 0 artefacts |
| Public disclosure | None known | The repository is private; nothing was published |

**Relevant official rules.** Rules and Regulations 2.2: "Redistribution, publication or unauthorised disclosure of competition datasets, in whole or in part, to any third party is strictly prohibited." Against that, rule 3.6 permits AI tools including LLMs, and the case study says using AI is "explicitly allowed". The documents do not say whether data seen by an AI tool counts as disclosure, and they contain no duty to report an incident.

**Assessment.** Small in scale and in a grey area of the rules, but it did happen and cannot be reversed. Whether it breaches rule 2.2 is the organisers' call, not ours.

**Owner decision (16 Nov 2026).** Keep the incident documented internally and do not contact the organisers for now. This is not a determination that the incident complies with rule 2.2. The owner may revisit the decision if new facts or guidance arise. Nobody has contacted the organisers.

**What reduces the chance of a repeat (prevention, not resolution)**
- `AGENTS.md` rule 7 forbids displaying records and running `grep`, `cat` or `head` over `dataset/`.
- The preparation scripts print aggregates only, and hide DuckDB error text by default because it can quote a record. Tests assert both.
- These are instructions and tests, not technical barriers: an assistant with terminal access can still read the file. Human review of what an assistant runs remains necessary.

## J. The damaged build

**Facts.** Four full builds of the real CSV exist: the owner's original and three run during this work on the owner's Mac with DuckDB 2.0.0. Three produced byte-identical files. One produced a file of the same size in which about 2.9 KB at the start of one column chunk were zeros. The original per-column checks of that build passed; the damage was found only when the column was read in full.

**Cause: not established.** What can be said:
- The damaged build was the only one during which other DuckDB jobs (the test suite and the profile) were run on the same 8 GB machine. That is a correlation from one case, not a finding.
- Disk space was not exhausted (about 42 GB free).
- The CSV read is sequential by design; the Parquet writer compresses in parallel. A fault in the writer, the operating system or the storage cannot be told apart from here.
- Nothing in the script's own file handling explains it: the output is written once and renamed once, after verification.

**What protects the team.** Every build now ends with the row-level comparison, so a damaged file is rejected and the previous one kept. A test reproduces the pattern (a block of zeros in a file of unchanged size) and confirms it is rejected. Advice: do not run other heavy jobs during a build, and run `--verify-only` if a later query reports a read error.

## Correction pass after review

An independent review of pull request #2 raised three points. All were checked before changing anything.

| Finding | Verdict | Resolution |
|---|---|---|
| Integrity checks were aggregate fingerprints and were described more strongly than justified | Valid | Replaced by the row-level digest comparison in section D2; ten damage patterns tested; wording corrected here, in the script, in `dataset/README.md` and in the pull request description |
| The disclosure of seven records was reported but not assessed | Valid | Section I; error text hidden by default; the owner's decision is stated |
| Python version not pinned | Valid, minor | `.python-version` set to 3.13, the version the owner's machine already runs and all locked libraries support |

Statements in the first version of this document that were too strong, now corrected: "the existing Parquet is confirmed correct", "every column matches the CSV", and "byte-identical" used as if it showed correctness (it shows only that separate builds agree with each other).


## K. Owner's final setup decisions (16 Nov 2026)

- **Confidentiality:** Retain section I's factual record internally. No organiser or mentor contact for now; do not reproduce the exposed records or treat the decision as a finding of compliance.
- **Branch protection:** After merging PR #2, require pull requests and both Ubuntu and Windows CI checks before merging into `main`. Do not require a reviewer approval count. Disable force pushes and branch deletion; prevent bypass where available. The owner must configure these settings and verify GitHub-plan support. No protection settings were changed by this PR.
- **Notebooks:** Ignore `*.ipynb` anywhere in Git, require coding agents to keep notebooks local, add four notebook paths to the ignore-regression tests, and check the tracked-file list for notebooks. This is a Git safeguard, not a substitute for inspecting permitted charts or Markdown outputs.
