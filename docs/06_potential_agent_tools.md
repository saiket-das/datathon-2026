# Potential Tools for AI Coding Agents — UMDAC Datathon 2026

> **Status: OPTIONAL / NON-BINDING.** This is a research-derived menu of possible tools, **not** an installation list, development mandate, architectural decision, or claim about Swift's hidden rules.
>
> **For incoming agents:** Read the official case study, competition rules, and judging rubric first. Inspect the local dataset and existing repository workflow, then propose an independent plan. Use this file **only as a reference** when a specific capability or bottleneck arises. Document why any addition is worth its setup, security, and maintenance cost. It is legitimate to use none of the optional integrations.
>
> **Research provenance:** Condensed from the team's uploaded *Tools research .md* (research dated 15 November 2026). Links and reported capabilities are leads for inspection, **not independently revalidated in this document**. Check current upstream docs, version, licences, and security advisories before installation.

## 1. What this file is for

The project involves a 4.6 GB **synthetic Swift cross-border payment dataset** (about 1.3 GB as Parquet) and a short preliminary-round deadline (**19 November 2026, noon MYT**). AI assistants may help write and execute analyses, but the **numbers and conclusions must come from reproducible local calculations**, not the assistants' descriptions.

The aim of a tool is to make an agent better at **running, checking, reproducing, or presenting** evidence. More autonomy, more MCP servers, or a larger agent roster are not goals in themselves. For scientific investigation approaches rather than tools, see [`04_research_pathways.md`](04_research_pathways.md).

## 2. Small shortlist: the default starting point

These are **candidate capabilities**, not mandatory dependencies. If equivalent, working tools already exist, retain them.

| Capability | Candidate / source | What it adds for agents | When to consider | Main caveat |
| --- | --- | --- | --- | --- |
| Large local SQL analysis | [DuckDB](https://github.com/duckdb/duckdb) | Queries large local files without copying raw rows into model context; saved `.sql` can be reviewed | Local data inspection or repeated aggregations | Prefer direct SQL before an MCP wrapper |
| Statistical verification | [SciPy](https://github.com/scipy/scipy), [statsmodels](https://github.com/statsmodels/statsmodels) | Executable tests, estimates, uncertainty, diagnostics, multiple-comparison procedures | A candidate claim needs quantification or uncertainty | A correct library call can still test the wrong hypothesis |
| Executable data checks | [Pandera](https://github.com/unionai-oss/pandera) + [pytest](https://github.com/pytest-dev/pytest) | Schema/semantic contracts and regression tests that fail visibly | Ingestion, transformations, joins, changing feature definitions | Do not confuse passing tests with a validated business rule |
| Large Python transformations | [Polars](https://github.com/pola-rs/polars) | Lazy/columnar processing, complex feature transformations | SQL becomes cumbersome or performance profiling justifies it | Avoid duplicate DuckDB and Polars pipelines without a reason |
| Reproducible PDF production | [Quarto](https://github.com/quarto-dev/quarto-cli) + chosen charting library | Connects executable analysis, charts, narrative, and exported reports | Preparing dashboard and slides from approved findings | Verify PDF rendering and slide layout; pin a stable release |
| Collaboration and history | Local `git` + [GitHub CLI (`gh`)](https://github.com/cli/cli) | Branches, reviews, issues, reproducible changes | Three-person work on shared source and artefacts | Do not put dataset/extracts/secrets into commits, PRs, or logs |

**Baseline idea (optional):** existing Claude Code, Codex or Gemini coding agents + terminal + Python + SQL + private Git. There is no need to introduce a new orchestration framework to get started.

## 3. Agent-facing additions: evaluate only if a need appears

The following are **integrations or workflows for agents**, distinct from the underlying analytical libraries.

| Candidate | Extra capability beyond terminal/code | Reasonable adoption trigger | Reasons to defer |
| --- | --- | --- | --- |
| [Anthropic Skills](https://github.com/anthropics/skills) | Reusable instructions/scripts for PDF, PPTX and document handling | A reporting agent repeatedly struggles with document formatting or validation | No improvement to statistical correctness; review scripts and licences |
| [Community data-science Claude skills](https://github.com/juanlurg/data-science-claude-skills) | Repeatable EDA/diagnosis command patterns | Commands genuinely save repetitive prompting | Claude-specific; short repo-owned instructions may suffice |
| [GitHub MCP Server](https://github.com/github/github-mcp-server) | Structured issue/PR/repository operations | `git` and `gh` operations become a measurable coordination bottleneck | Extra credentials, external access and tool attack surface |
| [MotherDuck DuckDB MCP](https://github.com/motherduckdb/mcp-server-motherduck) | Agent can explore a local DuckDB database through MCP | An interactive, **read-only, aggregate-only** SQL interface proves useful | Direct saved `.sql` is easier to audit; read-only mode is not a security boundary |
| [marimo](https://github.com/marimo-team/marimo) | Git-friendly reactive notebooks in Python | Exploratory notebooks are required and hidden notebook state causes errors | Switching from working scripts/Jupyter may waste time |
| Repository-owned evidence skill / instructions | Consistent claim/evidence format across multiple agents | Agents repeatedly omit sample size, provenance or verification | Keep it brief, portable and advisory; avoid prescribing findings |

**Portable skills:** A tool's instructions may be useful across Claude, Codex and Gemini, but **installation and execution compatibility are not interchangeable**. Keep any shared scientific protocol as plain Markdown. Add tool-specific wrappers only when tested on that tool.

### Optional MCP trial, with explicit checks

Before enabling any MCP server, establish all of the following:

1. Identify an actual task it performs materially better than `python`, `duckdb`, `git`, or `gh`.
2. Review source, install method, dependencies, version/commit, licences, hooks, network behaviour, and requested permissions.
3. Test first against an **empty or throwaway database/repository**, not the competition dataset.
4. Prefer a separate **aggregate-only** database; grant minimal OS-level filesystem and network access. An application flag labelled `read-only` is **not sufficient**.
5. Ensure tool outputs, including query logs and errors, cannot expose raw transaction records, credentials, or sensitive dataset extracts to external services.
6. Confirm queries and results can be preserved as reviewable scripts and reproducible artefacts; if not, prefer direct commands.

The source research reported that the MotherDuck server supports local DuckDB with a read-only default and documented client integrations. **Verify those details against the version you install.** This document deliberately avoids copy-paste installation commands, which can become stale or imply permissions that were never reviewed.

## 4. Other specialist tools: use only for a specific analytical question

| Need that actually emerges | Possible tool(s) | Why not default |
| --- | --- | --- |
| Transparent bank-path or account-graph exploration | [NetworkX](https://github.com/networkx/networkx) | Python-object graphs can be memory-heavy; start with aggregated SQL edges |
| Interpretable threshold / regime candidates | [scikit-learn](https://github.com/scikit-learn/scikit-learn) | Tree splits are hypotheses, not proven generating rules |
| Compact numeric formula recovery | [PySR](https://github.com/MilesCranmer/PySR) | Extra runtime and model-search complexity; justify after simple baselines |
| Subgroup search | [pysubgroup](https://github.com/flemmerich/pysubgroup) | Large search spaces can manufacture spurious discoveries |
| Probabilistic structure exploration | [pgmpy](https://github.com/pgmpy/pgmpy) | Observational graphs seldom establish a uniquely causal mechanism |
| Temporal change-point checks | [ruptures](https://github.com/deepcharles/ruptures) | Apparent changes can be population/composition effects |
| Experiment tracking at scale | [MLflow](https://github.com/mlflow/mlflow) | A Git-tracked experiment register is often enough for three people |
| Complex local data integrations | [localdata-mcp](https://github.com/ChrisGVE/localdata-mcp) | Broad tools/permissions are unlikely to help this single-dataset task |

None of these tools should be activated merely because the dataset contains columns they could process.

## 5. Interesting research frameworks, poor default deadline fit

| Research project | Useful idea to borrow | Adoption judgement |
| --- | --- | --- |
| [POPPER](https://github.com/snap-stanford/POPPER) | Actively design attempts to falsify candidate explanations | **Read for methodology**; do not assume its full framework works on this dataset |
| [AI-Scientist-v3](https://github.com/SakanaAI/AI-Scientist-v3) | Separate investigator and sealed evaluator; log ablations and failures | **Defer**; considerable execution/orchestration and permission overhead |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Stateful task coordination and hand-offs | **Defer unless already integrated and demonstrably useful** |
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | Programmatic agent coordination and tracing | **Defer unless already in use**; a framework cannot validate statistics |

A second independent coding agent running a saved calculation and attempting a counterexample is often more valuable than a newly installed multi-agent runtime.

## 6. One possible low-overhead collaboration pattern

This is an **example**, not a role assignment or a prescribed workflow.

- **Investigator:** proposes a falsifiable claim and commits the query/script that generates its numbers.
- **Independent verifier:** reruns or independently implements the test and examines at least one plausible alternative or failure case.
- **Reporter/integrator:** links verified outputs to charts, slides, and concise explanations, without manually inventing or modifying figures.

Humans can rotate roles and use multiple coding agents. Review important changes through Git. Avoid passing an investigator's persuasive narrative to the verifier as if it were established evidence.

### Optional evidence record (illustrative)

```yaml
id: H-001
claim: ""                     # hypothetical until tested
source_columns: []
code_or_sql: ""               # committed, rerunnable path
input_version_or_hash: ""      # local source fingerprint; no data upload
method_and_comparator: ""
sample_size: null
effect_size: null
uncertainty: ""
coverage: ""
alternatives_checked: []
holdout_result: ""
figure_path: ""
status: exploratory          # exploratory | supported | rejected | uncertain
reviewer: ""
```

Use a simpler record if that is sufficient. Do not confuse evidence *logging* with evidence *validation*.

## 7. Before adopting any tool: a quick decision test

An agent evaluating a new dependency should be able to answer:

1. **Purpose:** What concrete obstacle or repeated failure does it solve?
2. **Incremental value:** Why can't existing scripts/SQL/CLI solve it as well?
3. **Verification:** How will we test that its output is correct and reproducible?
4. **Data boundary:** What raw data, aggregates, credentials or repository files can it read or send?
5. **Cost:** What installation, debugging, runtime and token overhead does it introduce?
6. **Rollback:** Can it be removed without losing the team's analysis or results?

Possible outcomes: **use existing tools**, **trial in isolation**, **adopt for one narrow function**, or **defer**. Do not treat a recommendation from this file as proof that a dependency is needed.

## 8. Non-negotiable boundaries come from official rules, not this note

- Keep the organiser's dataset and unauthorised transaction extracts **out of Git, PR comments, public repositories and external analytics services**. Private GitHub access is not, by itself, permission to upload restricted data.
- Keep local raw-data directories and credentials outside version control and make the `.gitignore` explicit; validate with `git status` / `git check-ignore` before commits.
- Treat aggregate outputs as potentially disclosive when they are fine-grained or include identifiers; review before sharing.
- External datasets and generators may support separate practice or methodological research but **must not become primary evidence** about the competition dataset.
- Generated conclusions must link to executed, checkable calculations. An LLM's plausible explanation is not evidence.
- Use the official case study and judging rubric as the source of truth if this note conflicts with them.

## 9. Suggested repository placement

> **Not adopted.** The team keeps both optional notes directly in `docs/` as `04_research_pathways.md` and `06_potential_agent_tools.md`; `AGENTS.md` and the root `README.md` already point to them. The layout below is the original suggestion, kept for the record.

```text
docs/
  research/
    RESEARCH_PATHWAYS.md          # optional methods reference
    POTENTIAL_AGENT_TOOLS.md      # this file: optional tools reference
```

A root `AGENTS.md` may simply say: *“Optional research notes are in `docs/research/`; use them only after reviewing official documents and creating an independent plan.”* **Do not copy this entire tools menu into mandatory agent instructions.**

---

**Bottom line:** The smallest reliable stack can be enough. Choose additions for a demonstrated problem, preserve code-to-claim provenance, and keep analytical decisions open until the actual dataset is inspected.
