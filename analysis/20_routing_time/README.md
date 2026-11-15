# Routing and time (owner B)

Columns: `BIC8_PATH`, `ORDERING_BIC8`, `BENEFICIARY_BIC8`, `TRANSACTION_TYPE_CODE`, `PARTICIPANT_COUNT`, `CONTINUITY_QFLAG`, `TOTAL_DURATION`, `EPOCH_SECONDS`.

Starting questions:
- Which routing columns are exact functions of the path (definitions), and which are randomly drawn?
- What decides Direct vs Indirect vs Covered, and how many intermediary banks?
- Is duration explained by hops, conversions, route type or the time of day?
- Does payment volume follow the sender's local business hours?
