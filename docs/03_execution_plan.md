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
| Only 7,006 rows (0.07%) carry an anomaly label; smallest class 317 | A classifier is the wrong tool. Characterise how each label is constructed relative to normal traffic. |
| Sixth label `CUSTOMER_RECALL` (317 rows) is not in the data dictionary | Logged in the issues log; investigate as an undocumented rule. |
| No missing values except `ANOMALY_TYPE` | Data-preparation marks come from structural issues, not imputation. |
| `Direct` always has `PARTICIPANT_COUNT` = 2; `CONTINUITY_QFLAG` = N always has `...` in the path | Some columns are definitions of others. Do not present these as discovered behaviour. |
| Median amount 3,662 USD, mean 97,204, max 15.7 billion | Use logs and medians; means are meaningless here. |
| 400K ordering accounts vs 2.69M beneficiary accounts; one sender has 75,803 payments | Rows are not independent. A single hub account can drive a segment's statistics. |
| Median amount by party pair: B→B 22,888; B→C 3,119; C→B 3,229; C→C 463 | Any currency or country effect on amount may just be party mix. Always stratify. |
| 7.4% of amounts are whole numbers; 10,000 and 1,000 are the most common values | Suggests a round-number component; test by currency. |
| Timestamps are UTC; Sunday has 683,541 payments vs about 1.4–1.9M on weekdays | Local-time rules need a country from the BIC (characters 5–6). Three months cannot support seasonal claims. |

### The 5 questions EDA must answer first

1. **Dependency order:** which columns are exact functions of others (tokens from details, participant count from path, IBAN from BIC), and which are randomly drawn?
2. **Entities:** do accounts keep a fixed type, bank, country and name, and what decides who pays whom?
3. **Amounts:** what distribution does each party pair, currency and corridor follow; are round amounts round in USD or in the local currency?
4. **Time and duration:** does volume follow the sender's local business hours; is duration driven by hops, FX steps, route type or cut-off times?
5. **Anomalies:** what exactly differs between each labelled row and its normal counterpart?

## 3. Method and roadmap

**Method:** conditional-distribution analysis and determinism tests in DuckDB SQL. Every rule is found on one half of the accounts and confirmed, unchanged, on the other half. This fits because the generator is "hard-coded rules plus NumPy random calls", so rules should appear as exact functions and recognisable distributions.

| Phase | When | Output |
|---|---|---|
| Baseline | Sun 15 Nov evening – Mon 16 Nov midday | Parquet copy (done), issues log, first dependency map, one headline observation per feature group |
| Iteration | Mon 16 Nov midday – Wed 18 Nov morning | Each observation turned into a quantified rule, one confounder tested per rule, failures recorded. **No new lines of inquiry after Tue 17 Nov night.** |
| Polish | Wed 18 Nov – Thu 19 Nov 09:00 | For the top rules, simulate the rule and overlay it on the data. Build dashboards and deck; a second person re-runs every headline number. |

## 4. Who owns what

| Owner | Feature groups | Folder | Also owns |
|---|---|---|---|
| A | Amounts, currencies, party types, FX conversion count | `analysis/10_amounts_currency/` | Shared prep and [issues log](../findings/issues_log.md) |
| B | Routing path, route type, continuity, duration, timestamps, bank geography | `analysis/20_routing_time/` | Dependency map and methodology slides |
| C | Party details and tokens, account behaviour, anomaly types | `analysis/30_parties_anomalies/` | Dashboard template and deck assembly |

- One folder per owner and one file per hypothesis, so nobody edits the same file.
- Daily 15-minute cross-review: each person tries to break one of another person's rules.

## 5. Submission checklist

See [deliverables/README.md](../deliverables/README.md) for the tick-box version.
