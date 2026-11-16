# Execution Plan

Team strategy for the preliminary round. Written 15 Nov 2026; update it when decisions change.

## 1. What we are being judged on

This is **not** a prediction competition. There is no target column, no leaderboard and no automatic metric. Judges read our two PDFs and score them against the rubric in [official/pdfs/3_judging_criteria.pdf](official/pdfs/3_judging_criteria.pdf).

**Our framing:** recover the generator as a map of which features depend on which, then state each dependency as a rule: *when it applies, what changes, by how much, which records it covers, and where it fails*.

| Rubric block | Weight | What it means for us |
|---|---|---|
| Insight quality | 45% | Explanatory depth (14%) and rule precision (12%) carry the most. Correctness against Swift's hidden rules is only 9%, and a wrong rule stated as certain loses more than an uncertain one flagged honestly. |
| Evidence, method, data integrity | 23% | Every headline claim traces to a chart or calculation. "Sophistication earns no marks, and unjustified complexity can lose them." |
| Communication | 20% | The dashboard must stand alone; every chart shows the finding against a baseline, with a title that states the takeaway. |
| Economic reasoning | 12% | A plausible real-world mechanism per rule, labelled as interpretation, with at least one alternative considered. |

- **Rejected hypotheses score points.** Record every failed idea in [`findings/hypotheses/`](../findings/hypotheses/).
- **Use simple methods.** Grouped comparisons and SQL first; shallow decision trees only to *suggest* thresholds, which we then confirm with plain comparisons.

### Decisions taken

| Question | Decision | Reason |
|---|---|---|
| Team size | 3 | Confirmed by team |
| Dashboard tool | Build locally, export PDF, upload the PDF to Google Drive and share the link | Avoids uploading the dataset to Looker Studio, which would risk the no-redistribution rule |
| Two scoring schemes conflict | The detailed rubric (45/23/20/12) governs. We still cover the Submission Format weights (slides: methodology 65%) by giving methodology 2–3 slides. | The rubric is what judges score against line by line |
| Rubric mentions a "page limit" for the issues log, but none is defined | Treat as the 5–15 dashboard / 10–20 slide limits; issues log gets one slide and one dashboard panel | No document defines it |
| Submission link | Organisers will open it later | Check Discord daily |

## 2. Data facts and traps (from `analysis/00_prep/profile.py`)

10,000,000 records, 20 features, 30 Apr–31 Jul 2023 (UTC).

| Observation | Why it is a trap or a lead |
|---|---|
| 83.8M physical lines for 10M records; `DISCLAIMER` column filled only on row 1 | Party-detail fields contain line breaks. Only a quote-aware parser works. `DISCLAIMER` is dropped. |
| 4.6 GB CSV; laptops have about 8 GB RAM | pandas cannot load it. Use the Parquet copy with DuckDB. |
| Only 7,006 rows (0.07%) carry an anomaly label; smallest class 317 | Assess independent entity/event support for each method; label prediction alone would not reconstruct a generating mechanism. |
| Sixth label `CUSTOMER_RECALL` (317 rows) is not in the data dictionary | Logged in the issues log; investigate as an undocumented rule. |
| No missing values except `ANOMALY_TYPE` | Data-preparation marks come from structural issues, not imputation. |
| `Direct` always has `PARTICIPANT_COUNT` = 2; `CONTINUITY_QFLAG` = N always has `...` in the path | Distinguish documented meanings from dataset-exact observations; see section 6. |
| Median amount 3,662 USD, mean 97,204, max 15.7 billion | Use logs and medians for typical size; means describe value concentration and require tail sensitivity checks. |
| 391,132 ordering identifiers vs 2,590,877 beneficiary identifiers (exact Phase 0 counts); one sender has 75,803 payments | Rows are not independent. A single hub account can drive a segment's statistics. |
| Median amount by party pair: B→B 22,888; B→C 3,119; C→B 3,229; C→C 463 | Any currency or country effect on amount may just be party mix. Always stratify. |
| 7.4% of amounts are whole numbers; 10,000 and 1,000 are the most common values | Suggests a round-number component; test by currency. |
| Timestamps are UTC; Sunday has 683,541 payments vs about 1.4–1.9M on weekdays | Local-time rules need a country from the BIC (characters 5–6). Three months cannot support seasonal claims. |

### Investigator independence

Each investigator chooses their own falsifiable questions. Shared structural checks below
are factual safeguards, not a prescribed generator model or a causal DAG. Optional research
pathways are suggestions only; no account format, token determinism or stochastic architecture
is assumed. Bank country does not uniquely determine customer residence or local timezone.

## 3. Method and roadmap

**Method:** use the simplest comparisons appropriate to each question. Freeze each proposed
rule, comparator, rejection criterion and validation scheme before confirmation; follow section 6.
The generator's implementation and random-number library are unknown. A functional relationship
does not establish causal direction, and reconstructing the exact original code is not required
(Rules and Regulations 5.4).

| Phase | When | Output |
|---|---|---|
| Baseline | Sun 15 Nov evening – Mon 16 Nov midday | Parquet copy (done), issues log, first dependency map, one headline observation per feature group |
| Iteration | Mon 16 Nov midday – Wed 18 Nov morning | Each observation turned into a quantified rule, hypothesis-appropriate confounder and alternative-explanation checks completed, failures recorded. **No new lines of inquiry after Tue 17 Nov night.** |
| Polish | Wed 18 Nov – Thu 19 Nov 09:00 | For the top rules, simulate the rule and overlay it on the data. Build dashboards and deck; a second person re-runs every headline number. |

## 4. Who owns what

| Owner | Feature groups | Folder | Also owns |
|---|---|---|---|
| A | Amounts, currencies, party types, FX conversion count | `analysis/10_amounts_currency/` | Shared prep and [issues log](../findings/issues_log.md) |
| B | Routing path, route type, continuity, duration, timestamps, bank geography | `analysis/20_routing_time/` | Dependency map and methodology slides |
| C | Party details and tokens, account behaviour, anomaly types | `analysis/30_parties_anomalies/` | Dashboard template and deck assembly |

- Ownership assigns investigation and file responsibility, not column access. A, B and C may query any of the 20 source columns and combine domains as needed, including for C's anomaly work.
- One folder per owner and one file per hypothesis, so nobody edits the same file.
- Daily 15-minute cross-review: each person tries to break one of another person's rules.

## 5. Submission checklist

See [deliverables/README.md](../deliverables/README.md) for the tick-box version.

## 6. Shared scientific foundation and validation

Run from the repository root:

```bash
uv run python analysis/00_prep/scientific_checks.py
uv run pytest
```

Exact SQL and partition predicates live in
[`scientific_checks.py`](../analysis/00_prep/scientific_checks.py); executed safe aggregates
are in [`out/scientific_checks.md`](../analysis/00_prep/out/scientific_checks.md).
The script reads Parquet only, uses a 2GB DuckDB limit and two threads, and disables disk
spilling. Views and small candidate tables exist in memory; no additional payment copy is
materialised. Errors hide source values. Small subgroup statistics are suppressed.

### Definitions, observed relationships and open semantics

The [official case study, appendix A.1](official/pdfs/1_case_study_swift.pdf) defines the
epoch as UTC, amounts as USD-normalised, party types as B/C, paths as semicolon-separated
bank sequences and tokens as engineered text-pattern features. It describes continuity as
Y for a continuous path and N for a gap. Those are **documented meanings (A)**; the exact
generator implementation and causal ordering are unknown.

The executed report distinguishes these **dataset-exact observations (B)** from definitions:

- Participant count equals the number of non-placeholder entries, not every path entry.
- Direct holds if and only if participant count is two; N holds if and only if a placeholder exists.
- FX count never exceeds either visible links or visible bank-country changes. Equality with
  country changes is a separate, exception-bearing claim, not a definition of FX.
- Identifier-to-type consistency is role-specific. An ordering identifier retains its bank;
  beneficiary identifiers need not. Combining sender and receiver identities requires care.

**Exception-bearing observations (C):** bank fields usually agree with path endpoints but
have substantial exceptions; FX counts often equal country changes but sometimes are lower.
Identical visible detail strings sometimes have different complete token strings. These are
measured comparisons, not a reconstructed noise mechanism. Exact detail checks first shortlist
repeated detail hashes, then group by complete strings: collisions add candidates but cannot
create or hide exact-string counterexamples. Counts and denominators are preserved in the report.

**Unresolved questions (D):** what placeholders conceal; why endpoints differ; what distinguishes
Covered from Indirect beyond their labels; why beneficiaries change banks; whether shared account
strings denote the same customer across roles; which hidden context/processing produced token
differences; and what currency-country mapping underlies FX. Preserve all fields and exceptions.
No cleaning, invented causal DAG or investigator-specific hidden-rule hypothesis follows from these checks.

### What the previous validation missed

Phase 0 already examined full-data aggregates, including several structural relationships.
This foundation rechecks those observations; it does **not** independently confirm them.
Future frozen-rule confirmation remains conditional on that prior exposure. Never call these
records wholly unseen or infer that a replicated association identifies the original code.

`hash(ORDERING_ACCOUNT)%2` separates sending identifiers only. Receivers, cross-role identifiers,
banks, periods and repeated text can remain shared. DuckDB's generic hash is also not promised
stable across versions. The replacement predicates use MD5 of UTF-8 literal identifiers:
`(('0x'||substr(md5(identifier),1,8))::UBIGINT % 2)`. Python/DuckDB agreement and repeatability
are tested on invented strings. Two-fold entity membership is a candidate design, not a mandated
50/25/25 allocation. Actual retained and excluded coverage must be read before choosing.

| Executable scheme | Explore / confirm assignment | Appropriate use and remaining leakage |
|---|---|---|
| `sender` | Ordering identifier bit 0 / bit 1 | Sender-specific claims; receivers and banks can overlap. High row coverage does not imply many independent anomalous senders. |
| `accounts` | Both account bits 0 / both bits 1; crossing records excluded | Separates literal account strings in either role. Banks, text and neighbours beyond endpoints can remain shared; excludes cross-bit corridors and may lose rare classes. |
| `banks` | Both endpoint-bank bits 0 / both bits 1; crossing records excluded | Endpoint-bank transfer check. Accounts and intermediary/path banks can overlap; the report measures that overlap explicitly. Not a network-wide bank holdout. |
| `time` | Complete May/June dates / complete July dates before 31 July; boundary dates excluded | Temporal transfer check. Entities remain shared. For sequence outcomes, add a hypothesis-specific purge interval and ensure discovery outcomes finish before confirmation starts. |

Measured coverage on the prepared 10-million-record dataset (counts from the script's
`coverage and baseline stability` queries; these are not target percentages):

| Scheme | Explore | Confirm | Excluded | Key measured limitation |
|---|---:|---:|---:|---|
| sender | 5,097,938 | 4,902,062 | 0 | 388,309 account strings shared across roles; 7,838 endpoint banks shared |
| accounts | 2,579,943 | 2,416,730 | 5,003,327 | No shared accounts; 6,873 endpoint banks shared |
| banks | 2,246,981 | 2,732,147 | 5,020,872 | No shared endpoint banks; 11,565 account strings and 6,709 visible path banks shared |
| time | 7,094,560 | 2,896,968 | 8,472 | 461,216 account strings and 7,958 endpoint banks shared |

All four have zero shared record IDs. The sender scheme retains 162/155 customer-recall
records in explore/confirm; the both-account and bank schemes each have fewer than 100 in
each active partition. Duplicate-payment entity support is limited even when record counts
exceed 100. These observations motivate conditional choices, not a universal preferred split.
Currency total-variation distance is 0.050678 for sender separation and 0.143729 for endpoint-bank
separation; account/bank holdouts are not composition-identical populations. See the report for
other balance measures, entity support and calendar/file-block stability.

Use `partition_sql(scheme)` to create a local view with one `split` value per record, as the
check script does. Never publish that row-level view. Keep excluded records out of primary
confirmation and out of any discovery that informed the frozen rule. They may be examined later
as explicitly exploratory robustness evidence. Schemes are alternatives: a record can have
different roles under different schemes, so these are not independent confirmation sets to pool.

### Choosing, freezing and evaluating a test

1. Define the estimand, unit (row/account/bank/sequence), population, comparator, practical effect
   tolerance and a rejection criterion in the compact hypothesis template. Check composition and
   sample support before selecting a scheme; do not select based on which rule result looks best.
2. Inspect the executable audit: nonempty explore/confirm populations, complete coverage including excluded rows, zero shared ROW_IDs,
   the relevant entity-overlap counts, label counts and distinct senders/receivers, medians, currency/
   route/party-pair total-variation distances, and calendar/file-block summaries. High total variation
   means composition differs; it is not automatically an invalid split or a generator change.
3. For account-dependent claims, prefer both-role account separation if its eligible coverage fits
   the target population. Sender-only confirmation is defensible for sender-specific claims with
   receiver dependence explicitly controlled/caveated. It cannot substantiate global account independence.
4. For rare anomalies, preserve entity/sequence groups instead of stratifying individual rows.
   The report's 100-record/entity display threshold is a privacy/support flag, **not a power calculation**.
   Specify precision or detectable effect for the actual statistic and count relevant independent
   accounts or event families. If support is inadequate, retain an exploratory result or uncertain
   conclusion; do not reroll the seed, duplicate observations, or silently relax independence.
5. Commit the frozen test before evaluating its primary confirmation statistic. Report coverage,
   effect and uncertainty, and all exceptions. Weight/cluster at the relevant entity level; compare
   transaction- and entity-weighted results where concentration can dominate. Repeated customers
   are not independent observations merely because their transactions differ.
6. Predeclare bank/time checks as robustness tests, or explicitly designate one as primary instead.
   Describe later subgroup searches as exploratory. Revisions after seeing confirmation outcomes
   need a new test or an honest exploratory label; multiple tried rules need a search ledger and
   suitable multiplicity/uncertainty treatment. A teammate should rerun each eventual headline.

No single partition proves independence from shared text, intermediaries, neighbours or unobserved
generator state. If that dependence matters, use a justified additional exclusion/purge and rerun
the same overlap/support audit on the **eligible population**, not merely on the full dataset.
