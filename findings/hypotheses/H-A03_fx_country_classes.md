# H-A03: Country equivalence classes approximately reconstruct FX-step counts

- **Owner:** A
- **Status:** rejected at the frozen near-exact threshold
- **Evidence level:** Rejected for the complete frozen claim. The improvement over country-transition counting is Supported but not independently confirmed.
- **Script / command:** `uv run python analysis/10_amounts_currency/H-A03_fx_country_classes.py --phase explore`; validation uses `--phase validate --freeze 2196f80cc3ab647ce67e7eb493aeed23cc190628` instead.
- **Chart:** none yet; complete aggregate tables in the matching exploration/validation Markdown reports.

## Proposed rule and scope

Learn country equivalence classes from unlabelled, two-visible-bank payments in the
shared both-account exploration partition: a pair with at least 100 payments is joined
only if every observed FX count is zero. Take connected components of that graph;
other supported countries remain singleton groups. Country codes come only from visible
BIC positions 5-6; no external currency/country table is used. These are latent equivalence
classes, not established legal-tender mappings.

Predict a longer visible path's FX count by the number of changes between adjacent learned
country classes. Ignore `...` markers exactly as the shared visible-path construction does;
this makes no claim about how many hidden institutions exist. Eligible rows are unlabelled,
have more than two visible banks, and all visible countries are supported by training.
All visible transitions, including repeats/reversals, contribute. Payment currency is not
an input to this candidate prediction. The target is the supplied conversion count.

## Test plan (freeze before validation)

- **Exploration:** `partition_sql('accounts')='explore'`, both literal account MD5 parity bits 0. No labelled rows enter model fitting or primary evaluation. Train only on paths with two visible banks, evaluate on >2 visible banks. Minimum pair support exactly 100; union condition exactly `zero_count == count`.
- **Validation:** same model trained only on bit-0 exploration; evaluate unlabelled >2-visible-bank paths in `partition_sql('accounts')='confirm'` (both account bits 1). Cross-bit rows excluded. Countries unsupported by training cause whole-path exclusion, not default singleton assignment. No tuning after validation.
- **Comparator:** number of adjacent visible country changes, without equivalence pooling. Negative mapping: sorted supported country labels shifted seven positions, then mapped to their trained classes. It preserves the group-size multiset but deliberately mismatches countries; it is descriptive, not a causal randomisation test.
- **Frozen primary acceptance:** all of (i) >=90% eligible coverage of unlabelled >2-visible-bank validation payments; (ii) >=100 sending and >=100 receiving accounts; (iii) lower end of a 99% ordering-bank-cluster sensitivity interval on exact count agreement >=99.5%; (iv) lower end of the corresponding interval on agreement lift over country transitions >=2 percentage points. Report failure if any fails; retain raw agreement, errors and coverage.
- **Uncertainty:** 1,000 whole-declared-ordering-bank resamples with replacement, NumPy seed 20261116, percentile .005/.995. Intermediaries, country classes, counterparties and text can remain dependent; these are cluster sensitivity intervals, not proven independent-sampling confidence intervals.
- **Audits and sensitivity:** distinct record support, literal account split predicate, visible-bank overlap with two-bank training; Covered/Indirect and calendar-month aggregate comparisons inside the same selected split. Small route/month rows require >=100 payments and >=100 senders/receivers. These are overlapping internal diagnostics, not independent holdouts. No per-bank coefficients or identities are published.
- **Alternatives:** country-group collisions can stand for a hidden shared currency or other synthetic country metadata. Connected-component transitivity can create wrong merges; sparse pair support and unobserved equivalences can cause missed joins. Missing-path markers and endpoint exceptions can leave irreducible discrepancies. No exact original generator order, code, or real-world FX-currency interpretation is established.
- **Freeze identity:** the introducing commit is the freeze; its SHA/time must be recorded before the first validation query. Complete frozen code remains retrievable at that commit.

## Prior exposure and independence

Phase 0 full-data structural and distribution aggregates and Round 1 A01/A02 outcomes were
already exposed. Coordinator synthesis also exposed B/C Round 1 aggregate findings. The
Round 1 account-confirmation records and aggregates have already been used; they are not
an independent holdout for this work. New country-class prediction outcomes were not queried
in bit-1 accounts before this freeze. A frozen success can support internal transfer of a
new mechanism conditional on prior exposure, labelled **Supported but not independently
confirmed**. It must not be advertised as a new independent replication.

The main bank/account partition alternatives overlap and are not pooled. No other Round 2
investigator developing branch or outcome was read. Original Round 1 files remain unchanged.

## Discovery evidence

Only both-account bit-0 exploration outcomes were queried. Among 1,630,239 unlabelled
2-visible-bank payments, 246,141 have FX=0, 1,384,098 FX=1, none FX>1. For 1,988
country pairs with >=100 payments (1,438,644 rows), every pair has either 100% zero-FX
or 0% zero-FX: no mixed supported pair. This motivated the equivalence graph candidate.

Training covers 158 countries in 131 connected components. Of 947,930 multibank exploration
payments, 934,229 (98.5546%) are eligible, with 99,409 senders and 330,699 receivers.
Exact prediction holds for 930,635/934,229 = 99.6153%; the country-transition comparator
agrees on 81.6487%, and the shifted mapping on 80.6935%. Mean absolute error is .004165,
maximum error 2. There are 3,594 mismatched payments; the rule is approximate, not exact.

The bank-cluster sensitivity interval for agreement is [.995054,.996899]; the lift interval
is [.170987,.189023]. These are exploration outcomes, not validation. Frozen cutoffs were
chosen during exploration and are never to be moved after validation. Covered/Indirect
exploration agreement is 99.6869% / 99.6057%. All results are reproduced by the script.

An initial materialised exploration table exceeded the 512MB limit and was abandoned;
streaming views succeeded within the same memory budget, one thread, and no disk spill.
A DuckDB lambda-syntax compatibility error was fixed before any valid model run. Neither
error accessed validation or changed the scientific population.

## Validation and robustness results

Freeze commit 2196f80cc3ab647ce67e7eb493aeed23cc190628 was recorded at 17:31:22 MYT on 16 November 2026. No bit-1 country-class score was recorded before the freeze. The interrupted process finished writing the bit-0 exploration overlap and month summaries after the freeze commit. These additions come from the frozen executable and belong to exploration. The frozen script and shared partition helper matched the committed versions at execution.

The unchanged validation command was:

```text
uv run python analysis/10_amounts_currency/H-A03_fx_country_classes.py --phase validate --freeze 2196f80cc3ab647ce67e7eb493aeed23cc190628
```

| Frozen criterion | Internal validation result | Outcome |
| --- | --- | --- |
| Eligible coverage >=90% | 876,388 / 888,944 = 98.5875% | Pass |
| At least 100 eligible senders and receivers each | 97,364 senders and 323,316 receivers | Pass |
| 99% bank-cluster interval lower bound for agreement >=99.5% | [99.4690%, 99.6805%] | **Fail** |
| 99% bank-cluster interval lower bound for lift >=2 percentage points | [17.3691, 19.5347] percentage points | Pass |

Exact FX count agreement was 872,830 / 876,388 (99.5940%). The country-transition baseline
agreed on 81.2848% and the shifted-class comparison on 80.3338%. There were 3,558 errors.
Mean absolute error was 0.004363 conversions and the maximum absolute error was 3.
Eligible records had distinct row IDs and separated literal accounts by construction.
Of 7,110 visible validation banks, 6,530 also occurred in two-bank training.
Covered and Indirect exact agreement was 99.7293% and 99.5776%, respectively.
The April sensitivity had 545 payments and 98.7156% agreement. The three other displayed
months ranged from 99.5834% to 99.6048%. All are subgroups of the same validation split.
See the [validation report](../../analysis/10_amounts_currency/out/H-A03_fx_country_classes_validate.md).
The process exited successfully and reported `practical decision=False`.
The executable, comparator, thresholds and split did not change after the freeze.

## Assessment

The frozen near-exact claim failed. The learned grouping nonetheless improved observed
agreement by 18.3092 percentage points on eligible longer visible paths, consistent with a
country-equivalence mechanism. This approximate relationship is supported by internal
validation on a reused Round 1 account population. Bank overlap, eligibility exclusions,
and unresolved mismatches limit transfer. The currency identity of each latent group and
the generator's operation order remain unresolved.

## Real-world explanation (interpretation, not evidence)

Several countries can share a currency, so moving between them need not require FX. A
synthetic country-group attribute unrelated to actual currency could create the same pattern;
only the local dataset was used and the two explanations are not distinguished here.