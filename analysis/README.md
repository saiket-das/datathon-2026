# Analysis

All code that produces a number or chart for the submission lives here. Run every script from the repository root with `uv run python <path>`. DuckDB, pandas, Matplotlib and SciPy are pinned in `pyproject.toml` and `uv.lock`. For a one-off extra library use `uv run --with <name> python <path>` and say so in the script's docstring; to add one for everyone, `uv add <name>` and commit both files in a pull request.

| Folder | Owner | Covers |
|---|---|---|
| [00_prep/](00_prep/) | A (shared) | CSV → Parquet, profile, and `scientific_checks.py` structural/partition audits. Safe aggregate evidence: [out/scientific_checks.md](00_prep/out/scientific_checks.md). Dataset-independent tests: `uv run pytest`. |
| [10_amounts_currency/](10_amounts_currency/) | A | `USD_AMOUNT`, `CURRENCY_CODE`, `ORDERING_TYPE`, `BENEFICIARY_TYPE`, `CURRENCY_CONVERSION_COUNT` |
| [20_routing_time/](20_routing_time/) | B | `BIC8_PATH`, BIC codes, `TRANSACTION_TYPE_CODE`, `PARTICIPANT_COUNT`, `CONTINUITY_QFLAG`, `TOTAL_DURATION`, `EPOCH_SECONDS` |
| [30_parties_anomalies/](30_parties_anomalies/) | C | `*_ACCOUNT`, `*_DETAILS`, `*_TOKENS`, `ANOMALY_TYPE` |
| [40_g_adversarial/](40_g_adversarial/) | G (isolated) | R-G## adversarial replication; durable exposure ledger, independent code, aggregate-only external execution |

## How to work

Owners may query any of the 20 source columns and analyse relationships across domains;
ownership determines where the investigation's files live, not which columns it may use.
Validation schemes are alternatives with overlapping records across schemes, not independent
holdouts. Freeze a primary scheme and label additional checks as robustness evidence.

1. **Guess.** Write the hypothesis first, as a file in [`../findings/hypotheses/`](../findings/hypotheses/) copied from the template.
2. **Test.** Write one script per question in your folder, named after the hypothesis, e.g. `H-A03_round_amounts.py`. Start the script with a docstring saying what it tests and how to run it.
3. **Record.** Put the result, with numbers, back into the hypothesis file, including when the idea fails.
4. **Save charts** to an `out/` folder next to the script (`analysis/10_amounts_currency/out/`). Charts may go in Git; tables of raw rows may not. Git accepts only `.png`, `.jpg`, `.svg`, `.pdf` and `.md` files directly inside `out/`, so save an aggregate table as Markdown.

## Rules for scripts

- Read `dataset/payments.parquet`, never the CSV.
- Print or save **aggregates only** (counts, medians, shares), never individual records.
- Stratify before claiming an effect: compare like with like (for example, same party pair).
- Choose and freeze a hypothesis-appropriate partition and falsification criterion using the [shared protocol](../docs/03_execution_plan.md#6-shared-scientific-foundation-and-validation). A sender-only split does not separate receivers or banks; inspect executed coverage and overlap audits before choosing.
