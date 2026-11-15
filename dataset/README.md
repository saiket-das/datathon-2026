# Dataset

The sponsor data lives in this folder **on your own machine only**. It is never committed: `.gitignore` blocks everything in this folder except this README. Do not upload it, email it, or put raw rows in the PDFs.

## Get it

1. Download `swift_umdac_datathon_2026_fictitious_payment_data.csv` (4.6 GB) from the official competition channel (the organiser's Google Drive link shared on Discord).
2. Put it in this folder, keeping the file name unchanged.

## Build the fast copy (once, about 5 minutes)

From the repository root:

```bash
uv run python analysis/00_prep/build_parquet.py
```

This writes `payments.parquet` (about 1.3 GB) here, after checking that its record count matches the CSV. If the build fails, any existing `payments.parquet` is left as it was. Always analyse the Parquet file, not the CSV: it loads in seconds and has the right types.

## What is in `payments.parquet`

All 20 original columns except `DISCLAIMER` (dropped; it holds a legal notice on the first row only), plus helper columns:

| Column | Meaning |
|---|---|
| `ROW_ID` | Original record order in the CSV, starting at 1 |
| `ts_utc` | `EPOCH_SECONDS` as a UTC timestamp |
| `ord_country`, `ben_country` | Characters 5–6 of the sender's and receiver's bank code (the country) |
| `path_len` | Number of entries in `BIC8_PATH`, including `...` placeholders |
| `gap_count` | Number of `...` placeholders in `BIC8_PATH` |

Column meanings for the original 20 fields: see the data dictionary in [../docs/official/pdfs/1_case_study_swift.pdf](../docs/official/pdfs/1_case_study_swift.pdf), pages 3–4.

## Query it

```python
import duckdb
con = duckdb.connect()
con.sql("SELECT TRANSACTION_TYPE_CODE, count(*) FROM 'dataset/payments.parquet' GROUP BY 1").show()
```
