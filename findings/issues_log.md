# Data Issues Log

Every data problem we find and the decision taken. This feeds the "Data preparation" criterion (5% of the score) and becomes one slide plus one dashboard panel. Owner: A. Add a row when you find something; say which findings it could affect.

| # | Issue | Evidence | Decision | Could affect |
|---|---|---|---|---|
| 1 | Party-detail fields contain embedded line breaks (83.8M physical lines for 10M records) | `wc -l` vs record count in `00_prep/profile.py` | Read quote-aware with DuckDB; never split on newlines | Anything using row counts |
| 2 | `DISCLAIMER` column filled on the first record only | Non-null count = 1 | Dropped in `payments.parquet` | Nothing |
| 3 | `ANOMALY_TYPE` contains `CUSTOMER_RECALL` (317 rows), not in the data dictionary | `profile.py`, ANOMALY_TYPE table | Kept; investigated as an undocumented rule | Anomaly dashboard |
| 4 | No missing values in any column except `ANOMALY_TYPE` | `profile.py`, nulls table | No imputation needed; call absent labels "unlabelled", without assuming absence of anomalous behaviour | Anomaly rates |
| 5 | Extreme amount tail: median 3,662 USD, max about 15.7 billion USD | `profile.py`, overall table | Use medians and log scales; check whether extremes are `FAT_FINGER_MISTAKE` | Any amount average |
| 6 | Heavy account reuse: one ordering account has 75,803 payments | `profile.py`, account reuse | Check per account as well as per row; choose entity separation using the [validation protocol](../docs/03_execution_plan.md#6-shared-scientific-foundation-and-validation) | Any per-row statistic |
| 7 | Timestamps are UTC; first and last days are partial (30 Apr, 31 Jul) | `profile.py`, monthly table | Use UTC explicitly; bank country alone does not define a unique local timezone; exclude partial days from daily-volume claims | Time-of-day and weekday rules |
| 8 | One pair of rows shares timestamp, amount, both accounts and path | `profile.py`, duplicates table | Check against `DUPLICATE_PAYMENT` label before deciding | Duplicate-payment rule |
| 9 | 767,204 paths have extra placeholder entries; participant count equals non-placeholder entries throughout | `scientific_checks.py`, Structural counts | Keep both entry and participant counts; do not count placeholders as institutions or infer how many hidden institutions they represent | Routing and FX |
| 10 | Ordering/beneficiary path endpoints disagree with bank fields in 498,399 / 499,265 records | `scientific_checks.py`, Structural counts | Preserve both sources; mechanism unresolved, no automatic repair | Bank geography, routing and bank holdouts |
| 11 | Type is stable within each role but disagrees for 127,584 shared identifiers; 61,606 beneficiary identifiers have multiple banks | `scientific_checks.py`, Account consistency and Cross-role identity consistency | Preserve role distinctions; literal-identifier separation is a safeguard, not proof of globally consistent customers | Account-level analysis and validation |
| 12 | Identical visible details have different complete token strings in 324 ordering / 41,432 beneficiary detail groups | `scientific_checks.py`, Visible details to tokens (exact-string checks after repeated-hash screening) | Keep both fields; do not rebuild tokens assuming visible details uniquely determine them | Text features and text leakage |
