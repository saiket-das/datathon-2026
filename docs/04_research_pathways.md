# Optional Research Pathways — UMDAC Datathon 2026

> **Status:** Non-binding research notes, **not** an agent policy, implementation plan, or prediction of the hidden rules.
>
> **Suggested use:** Read the [official competition documents](official/README.md) and [the competition brief](02_competition_brief.md) first. Inspect the actual data and draft an independent plan **before** consulting this file. Adopt, change, or reject any suggestion here based on evidence, time, and resources. Official rules always take precedence.

## Purpose

Two external research reports surveyed past data competitions, synthetic payment datasets, and possible methods for recovering data-generating rules. This document condenses their **transferable ideas**, not their conclusions about Swift's generator. The actual generator and reference rules were **not** identified or verified by those reports.

The central distinction: **describing a correlation is not the same as reconstructing a rule**. A useful candidate rule states *when* a pattern holds, *what* changes, *by how much*, *for which records*, and *where it fails*. Its supporting calculation should be reproducible. An economic explanation is an interpretation unless the dataset provides evidence to support it.

## Possible investigation sequence (adapt as needed)

| Stage | Possible activity | Evidence to preserve |
| --- | --- | --- |
| **Orient** | Inspect schema, data types, missingness, distributions, ranges, record counts, repeated identifiers, and field definitions. | Reproducible data-quality summary; assumptions and caveats. |
| **Explore** | Compare conditional distributions and interactions; consider temporal, transaction, and network structure where relevant. | Queries/code, segment sizes, numerical comparisons, charts. |
| **Hypothesise** | Convert interesting patterns into specific, falsifiable candidate rules. Consider plausible competing explanations. | Hypothesis, anticipated test, comparison group, provisional confidence. |
| **Challenge** | Test alternative explanations, derived-field relationships, subgroup stability, and out-of-sample replication. | Positive and negative results, uncertainty, failures and exceptions. |
| **Communicate** | Select only defensible findings for the dashboard and slides; distinguish observations, model-based inference, and economic interpretation. | Exact figure/query provenance and a clear trace from claim to evidence. |

These are possible activities, **not prescribed phases or mandatory gates**. An agent may find a simpler or more appropriate approach after inspecting the data.

## Method and tool menu

**Choose the smallest method that can answer the current question.** None of these tools is required merely because it appears in a research report.

| Need / question | Reasonable first option | Consider later, if justified | Caution |
| --- | --- | --- | --- |
| Querying large local files | [DuckDB](https://duckdb.org/), [Polars](https://pola.rs/) | Alternate storage or query engines | Avoid unnecessary full-memory loads. |
| Describing conditional patterns | SQL groupings, quantiles, plots, [SciPy](https://scipy.org/), [statsmodels](https://www.statsmodels.org/) | Nonlinear dependence / subgroup discovery ([pysubgroup](https://github.com/flemmerich/pysubgroup)) | Tiny p-values alone do not establish useful or causal rules. |
| Finding interpretable thresholds or interactions | Pruned [scikit-learn](https://scikit-learn.org/) trees, basic regressions | Rule learners, piecewise model trees | Trees propose candidate rules; validate splits independently. |
| Examining bank paths and repeated entities | SQL path parsing, edge aggregations, [NetworkX](https://networkx.org/) on manageable graphs | [DuckPGQ](https://github.com/cwida/duckpgq-extension), [Raphtory](https://github.com/Pometry/Raphtory) | Establish what path gaps, route types, and repeated edges mean first. |
| Finding compact numeric equations | Plots, stratified regression and residual checks | [PySR](https://github.com/MilesCranmer/PySR) symbolic regression | Use only if a stable low-dimensional functional relationship warrants it. |
| Examining probabilistic dependencies | Conditional checks, simple models | [pgmpy](https://github.com/pgmpy/pgmpy), causal-discovery packages | Observational structure seldom identifies a unique causal explanation. |
| Checking changes over time | Time-binned comparisons, temporal holdouts | [ruptures](https://github.com/deepcharles/ruptures) | Composition changes may mimic regime changes. |
| Keeping results reproducible | Git-tracked scripts and a small experiment register | [MLflow](https://mlflow.org/) | Additional infrastructure is useful only if its overhead pays off. |
| Producing evidence visuals | [Plotly](https://plotly.com/python/), Matplotlib, exported PDFs | Quarto or dashboard tools | Visual polish is not a substitute for quantified proof. |

**Useful techniques to consider, not automatically apply:** stratification; effect sizes and uncertainty intervals; appropriate multiple-testing correction when screening many candidates; permutation/placebo checks; simple benchmarks; temporal or entity-aware validation splits; residual diagnostics; comparisons of observed versus simulated *conditional* behaviour when a proposed generator is explicit.

## Validation questions for a candidate finding

A short evidence record could answer:

- **Claim and condition:** What exactly is being proposed, and when should it apply?
- **Effect and comparator:** What changes, by how much, relative to what baseline?
- **Scope:** How many eligible observations does it cover? Where does it not apply?
- **Method:** Which query, script, test, or chart produced the result?
- **Alternatives:** Could composition, confounding, leakage, derived columns, or chance explain it?
- **Robustness:** Does the *unchanged* rule hold on a suitable untouched portion of the data?
- **Confidence:** Confirmed structural relationship, replicated association, provisional hypothesis, or rejected/unstable?
- **Interpretation:** What is directly observed versus merely a plausible business/economic story?

Not every finding needs every sophisticated test. Choose checks appropriate to the claim and available sample.

### Optional hypothesis record

```yaml
id: H-001
question: ""
candidate_rule: ""            # leave empty until supported
source_fields: []
discovery_method: ""
comparison_or_null: ""
effect_size: null
coverage_n: null
coverage_fraction: null
alternative_explanations: []
validation_split_or_test: ""
result: ""
status: provisional          # provisional | replicated | rejected | uncertain
limitations: []
script_or_query: ""
figure_or_table: ""
```

This is a suggested record format, not a requirement to install an experiment-tracking system.

## Things worth checking before making strong claims

- **Derived-field circularity:** Some fields are engineered from others. For instance, the official case describes `ORDERING_TOKENS` / `BENEFICIARY_TOKENS` as derived from their corresponding detail fields. Check whether other apparent dependencies are definitions or transformations rather than independent business behaviour.
- **Unit of analysis:** Rows, accounts, banks, routes, and temporal sequences may have different dependency structures. Repeated entities can invalidate naive independent-row assumptions.
- **Causal language:** No generic correlation, tree split, Bayesian network, or causal-discovery package proves causation on its own. State assumptions and unresolved alternatives.
- **Search bias:** Automatically testing many candidates and reporting only winners can create false discoveries. Record attempted and rejected ideas; apply appropriate corrections or independent confirmation.
- **Synthetic-data interpretation:** Realistic behavioural mechanisms need not imply realistic country/population/economic marginals. Treat external domain knowledge as inspiration for tests, not proof.
- **Unwarranted complexity:** A simple, stable, quantified rule may be stronger than an elaborate model that cannot be explained or checked.

## Optional teamwork and agent workflow

With three people, one possible arrangement is independent investigation of **tabular/statistical**, **temporal/network**, and **anomaly/text** relationships, followed by cross-review. Another arrangement may fit the team better. Avoid handing out hypotheses as facts or letting every agent inherit one speculative theory.

A lightweight loop: **propose → formalise → run reproducible code → challenge → review → record**. Have a different person or agent reproduce important numbers before publication. AI can suggest analyses and generate code, but code execution and verified outputs should determine what is claimed. Use short pull requests, clear ownership, and a shared evidence register if useful.

## External resources: for background or practice only

- [SWIFT Hackathon 2021](https://www.swift.com/swift-hackathon-2021-results-are): process-level lessons from earlier synthetic-data and anomaly challenges, **not** access to UMDAC's rules.
- [U.S.–U.K. PETs Prize Challenge (NIST)](https://www.nist.gov/itl/applied-cybersecurity/privacy-engineering/collaboration-space/challenges/us-uk-pets-prize) and [DrivenData financial-crime track](https://www.drivendata.org/competitions/98/nist-federated-learning-1/page/524/): related Swift synthetic-payments work, but **a different objective and dataset**. Verify each winning method against the correct track; one research summary conflated financial-crime and pandemic-track techniques.
- [IBM AML-Data](https://github.com/IBM/AML-Data) and [IBM AMLSim](https://github.com/IBM/AMLSim): possible sources for *separate* controlled generator-recovery practice, subject to their terms. They are **not** evidence of Swift's generating logic.

**Competition boundary:** Do not commit, publish, or share the organiser's dataset, raw transaction records, credentials, or unauthorised extracts. Do not use an external dataset as primary competition data. Check licences and cite external material when used. Keep local analyses and any practice data clearly separated.

---

### Provenance and confidence

Prepared from two independent external research reports supplied by the team (one broad source/method review and one more speculative technical survey), cross-checked against the official competition framing. **These reports are leads, not authority; some specific competition-method claims conflict.** Links here are starting points for verification, not proof that a tool or method is appropriate for this dataset. The original PDFs in `docs/official/pdfs/` remain authoritative.

**Use this document as a menu, not a recipe. It is acceptable, and often preferable, to ignore most of it.**
