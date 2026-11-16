# Parties and anomalies (owner C)

Columns: `ORDERING_ACCOUNT`, `BENEFICIARY_ACCOUNT`, `ORDERING_DETAILS`, `BENEFICIARY_DETAILS`, `ORDERING_TOKENS`, `BENEFICIARY_TOKENS`, `ANOMALY_TYPE`.

Starting questions:
- Does an account always keep the same type, bank, country and name?
- How are the `_TOKENS` fields derived from `_DETAILS`, and does address format depend on country?
- For each anomaly type, what exactly differs from a normal payment (amount, timing, repeats, accounts)?
- What is `CUSTOMER_RECALL`? It is not in the data dictionary.

## Independent C investigation

Two hypotheses discovered using only the MD5 sender-bit-0 exploration partition:

| Record | Reproduce exploration | Evidence |
|---|---|---|
| [H-C01: duplicate copy bursts](../../findings/hypotheses/H-C01_duplicate_bursts.md) | `uv run python analysis/30_parties_anomalies/H-C01_duplicate_bursts.py --phase explore` | [Aggregate report](out/H-C01_duplicate_bursts_explore.md), [chart](out/H-C01_duplicate_bursts_explore.png) |
| [H-C02: romance copy bursts](../../findings/hypotheses/H-C02_romance_bursts.md) | `uv run python analysis/30_parties_anomalies/H-C02_romance_bursts.py --phase explore` | [Aggregate report](out/H-C02_romance_bursts_explore.md), [chart](out/H-C02_romance_bursts_explore.png) |

H-C01 contains the shared label-blind candidate and exact-field comparison code;
H-C02 invokes it with an explicit alternative key/signature. Invented-data tests
are in `test_burst_signatures.py`; run `uv run pytest`. Confirmation requires
`--phase confirm --freeze-commit SHA` and identical frozen scripts. Both plans
specify thresholds before confirmation; sender separation does not separate all
receivers/banks. Source-row adjacency is a construction signature, not a fraud
detector robust to row shuffling. Four other labels remain mechanistically unresolved.

Frozen SHA: `bd61bc32dc61f4985c757244051404fb6622a71b` (16 Nov 2026,
16:19:47 Malaysia). [C handoff](../../docs/09_c_investigation_handoff.md) records provenance and review steps.

Confirmation evidence: [H-C01 report](out/H-C01_duplicate_bursts_confirm.md) and
[chart](out/H-C01_duplicate_bursts_confirm.png);
[H-C02 report](out/H-C02_romance_bursts_confirm.md) and
[chart](out/H-C02_romance_bursts_confirm.png). Run either command above with
`--phase confirm --freeze-commit bd61bc32dc61f4985c757244051404fb6622a71b`
instead of `--phase explore`.
