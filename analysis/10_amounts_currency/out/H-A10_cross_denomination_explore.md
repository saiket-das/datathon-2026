# H-A10 — High-value peaks and low-value rounding

Freeze: exploration.
512MB; one thread; no disk spill. Aggregates only.
Both-account bit-0 exploration only.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## Coverage, negative controls and date stability

| currency | n | senders | receivers | daily_fit | shifted_fit | constant_fit | lift_shift | lift_constant | scoped | coverage | supported_dates | equal_date_lift | positive_date_share | passes_screen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHF | 38015 | 3757 | 21130 | 0.4079968433513087 | 0.009838221754570563 | 0.00715507036696041 | 0.39815862159673815 | 0.4008417729843483 | 45646 | 0.8328221530911799 | 65 | 0.3906543869512671 | 1.0 | True |
| EUR | 182810 | 34516 | 83707 | 0.404589464471309 | 0.008391225862917783 | 0.01086373830753241 | 0.3961982386083912 | 0.3937257261637766 | 201796 | 0.905914884338639 | 84 | 0.3828786324896556 | 0.9880952380952381 | True |
| GBP | 61199 | 7685 | 32578 | 0.4046634748933806 | 0.010326966126897498 | 0.013039428748835765 | 0.39433650876648313 | 0.3916240461445448 | 72198 | 0.8476550596969445 | 66 | 0.3787426656558398 | 0.9848484848484849 | True |
| SGD | 4241 | 695 | 3266 | 0.2553643008724357 | 0.0007073803348266918 | 0.0007073803348266918 | 0.2546569205376091 | 0.2546569205376091 | 22043 | 0.1923966792178923 | 11 | 0.2533507711558976 | 1.0 | False |
| USD | 82341 | 23326 | 44069 | 0.404415783145699 | 0.404415783145699 | 0.404415783145699 | 0.0 | 0.0 | 91173 | 0.9031292158862821 | 83 | 0.0 | 0.0 | False |

USD is a constant-scale check. EUR is a benchmark with prior outcome exposure. CHF and GBP are primary. SGD tests the scope limit. Dates with under 100 eligible payments contribute to pooled results only. No daily rates are exported.
