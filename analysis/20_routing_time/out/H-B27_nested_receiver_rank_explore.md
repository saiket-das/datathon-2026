# H-B27 shared receiver-rank threshold falsification

May-June unlabelled v3-5, endpoint bit0/0. 512MB, one thread, no spill.
Pure ordered visible-endpoint labels only. Origins need 100 corridors and origin pairs 20 shared receivers.
A checkerboard means both origins have a Covered receiver that the other origin marks Indirect.
Shared receiver ranks with one threshold per origin imply zero such checkerboards.
Bank and corridor identities stay local. Cohorts with insufficient bank support are suppressed.

| Cohort | Corridors | Origins | Receivers | Origin pairs | First-role origins | Second-role origins | Repeated shared-receiver comparisons | Checkerboard origin pairs | Motifs | Checkerboard-pair fraction | Pairwise minimum editing fraction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| All | 95,742 | 249 | 4,332 | 30,171 | 248 | 248 | 4,157,818 | 14,829 | 1,179,238 | 49.149846% | 0.965146% |
| Declared endpoints agree | 83,668 | 225 | 3,098 | 25,005 | 224 | 224 | 3,620,063 | 12,940 | 901,187 | 51.749650% | 0.934984% |
| At least two witnesses per corridor | 39,602 | 168 | 1,834 | 13,886 | 167 | 167 | 1,501,299 | 8,250 | 403,450 | 59.412358% | 1.266570% |

Exact shared-rank thresholding is rejected on supported observed comparisons.
Motifs and origin pairs share most underlying corridors, so their count gives no independent-sample uncertainty.
Pairwise editing fractions describe local nesting and do not give the minimum global matrix edits.
Approximate rank effects, idiosyncratic pair states and probabilistic models remain possible.
Phase0/Round1/Round2 Covered-state and direction outcomes are exposed. No new July outcome was queried.
