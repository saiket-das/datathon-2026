# H-A20 — Currency mode transfer across training routes

Freeze: exploration.
512MB; one thread; no disk spill. Aggregates only.
Both-account bit-0 only. Phase 0 and A01–A19 prior exposure applies.
Phase 0 and Round 1 aggregate/outcome exposure applies. Unlabelled does not imply legitimate.

## July route coverage

| route | n | two_mapped | multi_mapped | joint_mapped |
| --- | --- | --- | --- | --- |
| Covered | 32334 | 32177 | 32057 | 32057 |
| Direct | 473855 | 472449 | 471552 | 471552 |
| Indirect | 242877 | 241873 | 241284 | 241284 |

## FX count errors on jointly mapped rows

| route | n | senders | receivers | banks | two_errors | multi_errors | disagreement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Covered | 32057 | 10044 | 19042 | 1929 | 0 | 0 | 0 |
| Direct | 471552 | 71964 | 191277 | 5324 | 0 | 0 | 0 |
| Indirect | 241284 | 50853 | 111835 | 4849 | 0 | 0 | 0 |

## Routing coverage sensitivity and decision

| route | joint_coverage | scoped_ordering_banks | coverage_low99 | coverage_high99 | pass |
| --- | --- | --- | --- | --- | --- |
| Covered | 0.9914331663264675 | 1969 | 0.985141208668986 | 0.9950869417315555 | True |
| Direct | 0.9951398634603412 | 5426 | 0.9940524710910812 | 0.9961040932647434 | True |
| Indirect | 0.9934411245198187 | 4946 | 0.9922948840504785 | 0.9943719131019659 | True |

Training uses payment currencies and first visible countries, without FX labels. Route categories in scoring are supplied labels. Training categories use visible path length. Joint support prevents coverage differences from distorting accuracy.
