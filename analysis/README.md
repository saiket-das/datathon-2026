# Analysis

All code that produces a number or chart for the submission lives here. Run every script from the repository root with `uv run python <path>`. DuckDB, pandas, Matplotlib and SciPy are pinned in `pyproject.toml` and `uv.lock`. For a one-off extra library use `uv run --with <name> python <path>` and say so in the script's docstring; to add one for everyone, `uv add <name>` and commit both files in a pull request.

| Folder | Owner | Covers |
|---|---|---|
| [00_prep/](00_prep/) | A (shared) | CSV → Parquet conversion and the first profile. Run these first. `test_prep.py` checks the setup without the dataset: `uv run pytest`. |
| [10_amounts_currency/](10_amounts_currency/) | A | `USD_AMOUNT`, `CURRENCY_CODE`, `ORDERING_TYPE`, `BENEFICIARY_TYPE`, `CURRENCY_CONVERSION_COUNT` |
| [20_routing_time/](20_routing_time/) | B | `BIC8_PATH`, BIC codes, `TRANSACTION_TYPE_CODE`, `PARTICIPANT_COUNT`, `CONTINUITY_QFLAG`, `TOTAL_DURATION`, `EPOCH_SECONDS` |
| [30_parties_anomalies/](30_parties_anomalies/) | C | `*_ACCOUNT`, `*_DETAILS`, `*_TOKENS`, `ANOMALY_TYPE` |

## How to work

1. **Guess.** Write the hypothesis first, as a file in [`../findings/hypotheses/`](../findings/hypotheses/) copied from the template.
2. **Test.** Write one script per question in your folder, named after the hypothesis, e.g. `H-A03_round_amounts.py`. Start the script with a docstring saying what it tests and how to run it.
3. **Record.** Put the result, with numbers, back into the hypothesis file, including when the idea fails.
4. **Save charts** to an `out/` folder next to the script (`analysis/10_amounts_currency/out/`). Charts may go in Git; tables of raw rows may not. Git accepts only `.png`, `.jpg`, `.svg`, `.pdf` and `.md` files directly inside `out/`, so save an aggregate table as Markdown.

## Rules for scripts

- Read `dataset/payments.parquet`, never the CSV.
- Print or save **aggregates only** (counts, medians, shares), never individual records.
- Stratify before claiming an effect: compare like with like (for example, same party pair).
- Find a rule on half of the accounts, confirm it unchanged on the other half: `WHERE hash(ORDERING_ACCOUNT) % 2 = 0` versus `= 1`.
