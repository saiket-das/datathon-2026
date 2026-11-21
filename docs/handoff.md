# Role A independent research handoff

## 1. Goal and task scope

Investigate value mechanisms independently, using only local sponsor data and the assigned A domain. This desktop worktree began detached at `94fd417`, matching the A worktree/`research/a-amounts` starting point. Work is isolated on **`codex/a-value-mechanisms`**. No B/C branch, PR or developing hypothesis was read; the shared foundation and organiser documents were read. Shared foundation files and other investigators' analyses are unchanged.

## 2. Actions completed and files modified

- [H-A01](../findings/hypotheses/H-A01_amount_kernel.md): account/currency-controlled business-type amount scale, including geography, concentration, time and route sensitivity.
- [H-A02](../findings/hypotheses/H-A02_usd_rounding.md): EUR date-specific scaling/rounding component learned on exploration accounts and evaluated outside all training amount windows.
- Two reproducible scripts, invented-data tests and aggregate reports/PNGs in [A's folder](../analysis/10_amounts_currency/README.md). README indexes updated. No dashboards/slides created.
- Both plans and scripts frozen in **`25d4703a6388baaec3d0808499dd7bebe05819da`**, 16 Nov 2026 **16:15:05 Malaysia time**. Both confirmation scripts verified their code against this commit before accessing confirmation. Plans remain visible verbatim at that commit; results were appended afterward.
- A local ignored hard link exposes the existing Parquet at `dataset/payments.parquet`; no CSV or row-level copy was made, no sponsor data was changed, and no row-level output was printed or staged. SHA-256 is recorded in H-A01. Reports contain support-filtered aggregates only. Small daily anchor groups and their per-date rate values are not published.

## 3. Current status and test results

Both predeclared hypotheses **replicated** on the MD5 both-account confirmation partition. This separates literal accounts across roles, while banks and dates remain shared. Known Phase 0 full-data exposure is disclosed. Alternate validation schemes were not pooled or queried for new outcomes.

- H-A01: business-beneficiary contrast **1.999500 log units / 7.3854x** across 63,801 sending accounts; business-ordering contrast **1.976398 / 7.2167x** across 43,795 receiving accounts. Both 97.5% account intervals lie within the frozen [1.85,2.15] band. Country-corridor, top-sender removal, calendar-month and route sensitivities retain the approximate rule. Individual-account deterministic versions are rejected; negative/noisy contrasts are reported.
- H-A02: **36.9088%** grid fit among **516,299** eligible confirmation EUR payments versus **0.9221%** wrong-date and **1.1997%** constant-rate fit. Equal-sender and equal-receiver excess lower bounds exceed 35 points, above the frozen 20-point criterion. **325,739** off-grid payments remain unexplained. Same-day transfer to separated accounts is supported; unseen-date transfer and historical-rate accuracy were not tested.
- **`uv run pytest`: 63 passed in 26.41s**, including three new invented-data calculation/guard checks. Both confirmation commands exited 0 and produced the committed aggregate reports/charts; both PNGs were visually inspected. Git diff confirms executable scripts are unchanged from the freeze commit.
- Tools/code used: OpenAI Codex assistance; local uv-pinned Python/DuckDB/Matplotlib; existing `scientific_checks.py` partition/query helpers; pytest; temporary `pypdf` extraction for reading original official PDFs. No outside primary data or cloud computation of sponsor records.

## 4. Blockers / pending approvals

No analysis blocker or approval request. PR creation is authorised; leave it **unmerged**. Independent teammate review/rerun is pending. Confidence intervals assume independence of account summaries and do not remove all shared-counterparty, bank or date dependence. No causal or exact-code claim is made. Broader currency-conversion-count investigation was not attempted in this focused pass.

## 5. Exact next step for the next agent

On a local machine with the same ignored Parquet, review the frozen hypothesis records, then run:

```bash
uv run pytest
uv run python analysis/10_amounts_currency/H-A01_amount_kernel.py --phase confirm --freeze 25d4703a6388baaec3d0808499dd7bebe05819da
uv run python analysis/10_amounts_currency/H-A02_usd_rounding.py --phase confirm --freeze 25d4703a6388baaec3d0808499dd7bebe05819da
```

Compare aggregates with `analysis/10_amounts_currency/out/*_confirm.md` (floating-point last digits can vary with grouping order). Review the marked limitations and negative results before choosing submission headlines. The two confirmation PNGs are aggregate chart assets for later PDF production. Any new mechanism or threshold informed by these confirmation outcomes is exploratory and needs a fresh honest validation design; do not relabel these outcomes as unseen.
