# Phase 2 — cross-mechanism synthesis (qualified)

**Scientific role:** coordinator, integrator, not a blind replicator.  
**Evidence:** existing investigator-reported internal validations and exploratory screens. No new source-data run.  
**Interpretation rule:** arrows below are conditional associations or candidate mechanisms, NOT recovered generator program order, causal discovery, or proof of implementation identity.

## 1. Working mechanism inventory

| Layer | Proposed conditional regularity | Best existing evidence | Necessary limitation / plausible alternative |
|---|---|---|---|
| Amount scale | Business/consumer counterparty type strongly changes the distribution of log USD amount | [A01](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A01_amount_kernel.md) | Account mix, conditional tails and heterogeneous sender effects; a ~2-log-unit contrast is not an exact global multiplier |
| Amount kernel | Conditional standardized log amounts resemble a Gaussian more closely than tested logistic/Laplace reference shapes | [A12](https://github.com/saiket-das/datathon-2026/blob/codex/r2-a-amount-generation/findings/hypotheses/H-A12_log_shape.md) | Approximation on selected supported strata, not full parametric law, exact tails or hidden sampler proof |
| Denomination / timing | Specific currencies show date-conditioned amount grids and a preferred-five denomination structure | A02, A10, A19, A23, A25 | Learned alignment and controls constrain behavior; scale units, dates, off-grid mixture and factor-five ambiguity remain |
| Currency choice | Observed payment currency is associated with visible-path bank-country currency modes, and frequently belongs to the set of modes across the path | A06, A08 | First-path vs other endpoints, EUR/USD prevalence, country/route selection and uncovered exceptions |
| FX steps | Learned country-mode class changes form strong FX-count constraints; supported one-transition directed pairs have fewer unexplained residuals | A03 **failure**, A05, A11, A14, A16, A20 | A03's near-exact frozen gate failed; class-bound and scoped equality do not imply universal deterministic rule |
| Path topology | Visible-bank and gap counts have a simple approximate joint distribution; participant count and continuity agree with parsed path features | Shared foundation, B02 | Count distributions are observational; path sampling and hidden nodes unknown |
| Route classification | On supported paths, directed visible endpoint labels strongly separate Covered from Indirect | B04, B12, B20, B30 | Selection requires known directed pairs; origin propensities and geography matter; no universal label function established |
| Intermediary choice | Weighted observed bank populations approximate interior-bank collision frequencies | B14 | Competing conditional/position-aware copying processes can produce similar marginals; G02 unresolved |
| Duration floor | Certain learned bank-associated classes exclude sub-100-second observed durations on supported routes | B09 | Association may stand for latent bank/network class, not physical waiting time |
| Directional duration | Direct timing centers can differ substantially by direction and correlate with Covered route status; supported adjacent-bank effects transfer to selected three-bank paths | B13 rejection of symmetry; B17, B18, B19, B23 | Pair selection and shared latent state; fitted edge effects are not service delays or causal process durations |
| Gaps / placeholders | Matched placeholder presence need not shift supported durations by more than the frozen equivalence bound | B28 | Not proof that hidden hops have no latency or that placeholders are missing at random |
| Scheduling | Matched UTC weekend timing differs from weekdays | B06 | UTC observations and bank-country are insufficient to establish local business-hours generator |
| Anomaly sequences | Duplicate and romance labels track row-adjacent short bursts with preserved payment context and distinct amount/time behaviors | C01, C02 | Depends on original `ROW_ID` order; alternative file construction and templated batches remain |
| Text / labels | Visible detail strings and token representations have observed mismatches; receiving-end concordance in some scam labels is descriptive | shared foundation, C05 frozen combined failure | Token grammar, hidden context and anomaly editing remain unidentified; do not infer a deterministic tokenizer |

## 2. Explicitly constrained dependency sketch

The following is a **candidate statistical factorisation**, not a claim that Swift implemented this order:

```text
Party-type composition ──associated with────► USD_AMOUNT scale / log shape
CURRENCY_CODE × UTC date ──associated with───► denomination-grid signatures
Visible path bank countries ──associated with► payment currency / FX constraints
Visible directed endpoint pair ──associated with► Covered vs Indirect route label
Origin bank / partner geography ──associated ► Covered propensity / coverage
Directed path edges & latent states ────────► observed duration distribution
UTC calendar ──associated with──────────────► payment scheduling distribution
Anomaly-labelled row sequence ──associated──► duplicated / varying contexts
Party details + unknown context ────────────► token patterns (not exact mapping)
```

### Important non-implications

- A13 and A19 date effects are not proof of a true real-world FX conversion series or local timezone switching.
- A05's empirical FX **upper bound** is not A03's failed exact-count equality claim.
- A20's cross-route mode agreement conditions on jointly mapped records; it does not prove universal unseen-region transport.
- B12's no-error supported subset does not establish zero errors for its unsupported endpoint pairs or future banks. A separate private G method report has a coverage limitation; exact contents stay in private review.
- B14's moment agreement is not evidence that independently sampling intermediaries is the unique generator. G explicitly found model-comparison/inference pitfalls while developing its uncompleted competing-model protocol.
- B18's approximate bounded gap shape is not a unique sampling law for unselected corridors.
- C01/C02 signatures are label/sequence constraints, not a fraud classifier to deploy on live transactions.
- Cross-mechanism FX-duration associations in F01–F03 are **exploratory and confounded**. No claim that FX steps physically shorten or lengthen settlement time is justified.

## 3. Candidate integrated explanations, ranked by evidence

### Tier 1 — strongest internally supported constraints
1. Visible-path geography constrains recorded currency and FX-count relationships on high-coverage subsets; evidence A05/A08/A14/A20.
2. Directed bank endpoints and bank-specific propensity carry substantial information for route classifications; B04/B12/B20/B30.
3. Structured amount-scale and currency/date rounding signatures recur with meaningful controls; A01/A02/A10/A12/A19/A23/A25.
4. Duration distributions contain structured directional/path-associated components and bank-dependent floors; B09/B17–B19/B23.
5. Copy-burst-style anomaly sequences are highly characteristic of the labelled target groups on original source order; C01/C02.

These are **internally supported**, not independent, and their exclusions and failures govern wording.

### Tier 2 — informative approximations and negative controls
- B02 topology count approximation; B14 interior-bank moment comparison; B28 placeholder equivalence.
- A11 sparse-pair FX residual support; A16 mode-map exclusions.
- B13 negative result for symmetric Direct timing; B24 rejects an exact origin-zero gate; B26/B27 reject simplistic duration/rank models.
- C03/C04 and C05 failures narrow, rather than solve, anomaly editing/token rules.

### Tier 3 — unconfirmed mechanisms, not usable as headline generator rules
- Exact original source code, hidden stochastic architecture and causal ordering.
- FX processing time as a physical causal delay independent of banks/path composition.
- A unique intermediary copying/sampling process (pending G02).
- A universal tokenizer/content-to-token grammar, exact anomaly-edit process or global customer identity.
- Generalization to novel banks/corridors beyond the selected support.
- Full D and local C06–C48/E scientific reconciliation without original source recovery.

## 4. Mechanistic contradictions to resolve conservatively

This synthesis favors **compatible descriptions** rather than forcing a single simulator model. A conditional law may coexist with a failed broader universal claim; a negative result on a sparse high-dimensional support set is not evidence of no relationship elsewhere; and two predictive descriptions may be observationally indistinguishable. The dedicated [conflict register](03_conflicts_and_falsification.md) records such cases without rewriting frozen decisions.

## 5. What this report does and does not certify

**Done:** integrated the public-source A/B/C findings into a coherent, testable *statistical dependency map*, preserving scope and alternatives.

**Not done:** run new data, verify private external job provenance, recover local C/E research, independently validate G/F, identify original code, or sign off all team science.

**Publishability:** This public-branch file cites only previously public investigator-source claims and qualitative limitations. Private F03/G01 reports are intentionally not copied or summarized numerically. A full team-only synthesis must remain behind the sponsor/team disclosure boundary.
