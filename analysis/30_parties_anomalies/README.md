# Parties and anomalies (owner C)

Columns: `ORDERING_ACCOUNT`, `BENEFICIARY_ACCOUNT`, `ORDERING_DETAILS`, `BENEFICIARY_DETAILS`, `ORDERING_TOKENS`, `BENEFICIARY_TOKENS`, `ANOMALY_TYPE`.

Starting questions:
- Does an account always keep the same type, bank, country and name?
- How are the `_TOKENS` fields derived from `_DETAILS`, and does address format depend on country?
- For each anomaly type, what exactly differs from a normal payment (amount, timing, repeats, accounts)?
- What is `CUSTOMER_RECALL`? It is not in the data dictionary.
