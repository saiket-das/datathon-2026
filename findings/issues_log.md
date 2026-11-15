# Data Issues Log

Every data problem we find and the decision taken. This feeds the "Data preparation" criterion (5% of the score) and becomes one slide plus one dashboard panel. Owner: A. Add a row when you find something; say which findings it could affect.

| # | Issue | Evidence | Decision | Could affect |
|---|---|---|---|---|
| 1 | Party-detail fields contain embedded line breaks (83.8M physical lines for 10M records) | `wc -l` vs record count in `00_prep/profile.py` | Read quote-aware with DuckDB; never split on newlines | Anything using row counts |
| 2 | `DISCLAIMER` column filled on the first record only | Non-null count = 1 | Dropped in `payments.parquet` | Nothing |
| 3 | `ANOMALY_TYPE` contains `CUSTOMER_RECALL` (317 rows), not in the data dictionary | `profile.py`, ANOMALY_TYPE table | Kept; investigated as an undocumented rule | Anomaly dashboard |
| 4 | No missing values in any column except `ANOMALY_TYPE` (empty = normal payment) | `profile.py`, nulls table | No imputation needed; empty label treated as "normal" | Anomaly rates |
| 5 | Extreme amount tail: median 3,662 USD, max about 15.7 billion USD | `profile.py`, overall table | Use medians and log scales; check whether extremes are `FAT_FINGER_MISTAKE` | Any amount average |
| 6 | Heavy account reuse: one ordering account has 75,803 payments | `profile.py`, account reuse | Check rules per account as well as per row; split validation by account | Any per-row statistic |
| 7 | Timestamps are UTC; first and last days are partial (30 Apr, 31 Jul) | `profile.py`, monthly table | Use UTC explicitly; derive local time from bank country; exclude partial days from daily-volume claims | Time-of-day and weekday rules |
| 8 | One pair of rows shares timestamp, amount, both accounts and path | `profile.py`, duplicates table | Check against `DUPLICATE_PAYMENT` label before deciding | Duplicate-payment rule |
