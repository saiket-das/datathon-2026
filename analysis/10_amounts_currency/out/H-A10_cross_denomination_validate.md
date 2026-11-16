# H-A10 — High-value peaks and low-value rounding

Freeze: f31764d04d8d4280281ace5f0e8c0dbc8cb1dff5.
512MB; one thread; no disk spill. Aggregates only.
Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Coverage, negative controls and date stability

| currency | n | senders | receivers | daily_fit | shifted_fit | constant_fit | lift_shift | lift_constant | scoped | coverage | supported_dates | equal_date_lift | positive_date_share | passes_screen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHF | 33405 | 3542 | 19503 | 0.4111360574764257 | 0.008831013321359079 | 0.0065559048046699596 | 0.4023050441550666 | 0.40458015267175573 | 39893 | 0.8373649512445792 | 65 | 0.3954753207357357 | 1.0 | True |
| EUR | 181045 | 33976 | 84778 | 0.40352950923803477 | 0.00839017923720622 | 0.01105802424811511 | 0.3951393300008285 | 0.39247148498991963 | 200142 | 0.9045827462501624 | 84 | 0.38146642449315626 | 0.9880952380952381 | True |
| GBP | 41019 | 7277 | 24518 | 0.4035934566908018 | 0.009678441697749823 | 0.012603915258782515 | 0.393915014993052 | 0.3909895414320193 | 48215 | 0.8507518407134709 | 66 | 0.38109289308573563 | 0.9848484848484849 | True |
| SGD | 3531 | 655 | 2862 | 0.2656471254602096 | 0.001416029453412631 | 0.0002832058906825262 | 0.26423109600679695 | 0.26536391956952704 | 18553 | 0.19031962485851345 | 11 | 0.2603417192098924 | 1.0 | False |
| USD | 77077 | 22984 | 42698 | 0.404076443037482 | 0.404076443037482 | 0.404076443037482 | 0.0 | 0.0 | 85304 | 0.9035566913626559 | 83 | 0.0 | 0.0 | False |

USD is a constant-scale check. EUR is a benchmark with prior outcome exposure. CHF and GBP are primary. SGD tests the scope limit. Dates with under 100 eligible payments contribute to pooled results only. No daily rates are exported.
