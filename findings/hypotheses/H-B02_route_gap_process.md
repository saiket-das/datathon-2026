# H-B02: One fixed event law reconstructs route length and placeholder counts

- **Owner:** B
- **Status:** confirmation-ready
- **Script / exact command / commit:** `uv run python analysis/20_routing_time/H-B02_route_gap_process.py --phase explore`; freeze SHA to be recorded after commit. Confirmation: same command with `--phase confirm --freeze <SHA>`.
- **Chart:** `analysis/20_routing_time/out/H-B02_route_gap_process_confirm.png` (after confirmation); exploration chart uses `_explore`.

## Proposed rule and scope

For unlabelled payments, let V be non-placeholder participants and G be `...` entries.
The joint count distribution is approximately

`P(V=v,G=g) = .60 * choose(v+g-2,g) * .35^(v-2) * .05^g`, for v>=2, g>=0.

One equivalent count-generating recipe starts with the sending bank, repeatedly emits
an intermediate visible bank with probability .35 or a placeholder with probability .05,
and finishes with the receiving bank with probability .60. This is a **distributionally
compatible recipe**, not an assertion about execution order or bank identity assignment.
It predicts `V-2 ~ geometric(continuation=.35/.95)` and
`G|V ~ negative-binomial(successes=V-1, success probability=.95)`.
In particular `P(G>0|V)=1-.95^(V-1)` and repeated placeholders are permitted.
This is more precise than the documented continuity/count definitions.

Scope: all unlabelled payments in the selected partition, no cleaning or duration/amount
exclusions. Payment is the unit; unlabelled does not establish legitimate behaviour.
Covered versus Indirect assignment is deliberately outside this rule (see H-B03).

## Test plan (freeze before confirmation)

- **Comparator/statistics/tolerance:** fixed 18-cell grid V=2/3/4/5/6/7+ crossed with
  G=0/1/2+. Total variation (TV) to the fixed law must have 99% bank-cluster interval
  upper bound <=.01. Compare against an independence baseline formed from the two
  **exploration** empirical marginal distributions; require the upper 99% interval for
  TV(fixed law)/TV(independence) <=.50. No fitting to confirmation outcomes.
- **Event estimates:** pooled `visible=sum(V-2)/sum(V-1+G)`, `gap=sum(G)/sum(V-1+G)`
  and `finish=N/sum(V-1+G)`. Require their entire 99% cluster intervals inside
  [.345,.355], [.045,.055] and [.595,.605], respectively. These are practical
  tolerances, not claims of exact parameter equality. Need >=100 distinct senders,
  receivers and declared ordering banks. All criteria must pass.
- **Alternative explanations/controls:** a fixed gap probability independent of route
  length, a single Bernoulli placeholder per path, composition by party/route/FX,
  concentration in customers or banks, calendar and source-file order. Compare equal
  bank weighting both with all banks and with >=100-payment banks. Small-bank ratios
  can have finite-sample bias; do not demand equality of noisy bank-level ratios.
- **Falsification:** failure of any primary criterion rejects this practical joint count
  law. Any endpoint placeholders, visible-count mismatch or Direct/count mismatch are
  separately reported structural counterexamples; no inference about hidden bank
  counts follows. Matching the count law does not prove event independence or positions.
- **Partition/exact predicate:** foundation `banks`; `bit(x)=(('0x'||substr(md5(x),1,8))::UBIGINT % 2)`.
  Both declared endpoint-bank bits 0 explore, both 1 confirm; crossing rows excluded.
  Foundation counts: 2,246,981 / 2,732,147 / 5,020,872. Zero shared ROW_IDs/declared
  endpoint banks, but 11,565 shared account strings and 6,709 shared visible path banks
  in the full audit. Actual unlabelled counts and overlaps are recomputed by this script.
  Exploration has 2,245,252 unlabelled rows, 144,821 senders, 682,154 receivers,
  3,948 declared ordering banks. This choice supports transfer across endpoint metadata,
  not independent networks, customers or all path banks.
- **Primary confirmation/uncertainty:** same fixed law and exploration-only independence
  baseline on all unlabelled bank-confirmation payments. Whole ordering-bank cluster
  resampling, 1,000 replicates, NumPy seed 20261116, .005/.995 percentile intervals.
  Conditional sensitivity intervals do not prove independence of path banks or accounts.
  Two selected primary investigations use 99% intervals for conservatism; this is not a
  formal simultaneous confidence guarantee across dependent statistics and searches.
- **Separately labelled robustness:** monthly estimates, including July within the same
  confirmation partition; source-file million-row blocks; party pairs; route types;
  endpoint agreement; FX count 0/1/2/3+; pooled labelled payments; removal of the largest
  sender by unlabelled count. These are composition/transport checks, not independent
  confirmation partitions. Conditional route/FX selection changes the visible-event mix,
  so the marginal .35 law is not claimed within every selected subgroup.
- **Freeze/time/prior exposure:** SHA/time recorded after committing this plan, before
  opening confirmation. Read Phase 0 and shared full-data summaries, including the
  767,204 paths with placeholders, Direct/count and continuity definitions and split
  audit. That prior exposure means confirmation is not wholly unseen. Candidate
  probabilities and joint distribution were investigated only on bank exploration.
  No developing work of other investigators was read. A proposed independent 10%
  Covered coin was **removed during discovery**, before freezing, because bank-level
  concentration contradicted it; see H-B03 and the search ledger.

## Discovery evidence

Reproduce from `_explore.md`/PNG. Estimates: visible=.349848, gap=.049865,
finish=.600288. Fixed-law TV=.000571; TV ratio to the independence baseline=.016913.
99% bank-cluster intervals: visible [.349222,.350445], gap [.049597,.050137],
finish [.599640,.600996], TV [.000394,.001464], ratio [.011648,.044436].

P(gap|V=2)=70,728/1,417,991=4.9879%; for V=3 it is
50,580/522,501=9.6804%, versus fixed predictions 5% and 9.75%.
There are 8,989 paths with adjacent placeholders and 13,372 with >=2 placeholders,
contradicting the single-Bernoulli-per-path alternative. There are no endpoint gaps,
visible-count mismatches or Direct/count mismatches in this exploration population.
Largest sender contributes .4224% of rows; removing it leaves event estimates essentially
unchanged. All counts and tolerances concern distributions, not a deterministic row rule.

## Confirmation and robustness results

Pending frozen commit and unchanged test.

## Assessment

Promising reconstructed joint count law. It does not recover bank selection, Covered
assignment, hidden participants, causal direction, or the original random-number implementation.

## Real-world explanation (interpretation, not evidence)

A payment can complete or require another correspondent institution; imperfect observation
can add missing-route markers. Repeated opportunities naturally create geometric tails.
An alternative is drawing V and G directly from the equivalent geometric/negative-binomial
distributions. Their joint counts alone cannot distinguish those implementations. Placeholder
counts do not establish how many actual institutions are hidden.
