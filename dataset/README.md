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

This writes `payments.parquet` (about 1.3 GB) here. The file is first written under a temporary name and compared with the CSV; it replaces `payments.parquet` only if the comparison passes, so a failed build leaves any existing file as it was. Do not run other heavy jobs while it builds. Always analyse the Parquet file, not the CSV: it loads in seconds and has the right types.

## Check an existing copy (about 1 minute)

```bash
uv run python analysis/00_prep/build_parquet.py --verify-only
```

This compares your `payments.parquet` with the CSV without rebuilding. Add `--independent` (about 2 minutes) to repeat the comparison with Python's own CSV reader instead of DuckDB's.

**What the comparison covers.** One MD5 digest per record, taken over the record's position in the file and all 20 original columns, combined into a fingerprint for the CSV and for the Parquet. A changed, swapped, reordered or missing value changes the fingerprint. It is a digest comparison, not a value-by-value proof; the limits are listed at the top of [build_parquet.py](../analysis/00_prep/build_parquet.py).

If a build or check fails, the error detail is hidden by default because DuckDB's messages can quote a record. `--show-error-detail` prints it; keep that output on your own machine.

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
