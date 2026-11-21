# H-A22 — USD quantization level screen

Exploration only: positive unlabelled July USD both-account bit-0.
Phase0/Round1 and A02/A10/A18 rounding exposure applies. A19 exposed UTC daily alignment; A09/A13 exposed rate movement. No new holdout is claimed.
512 MB, one thread, no spill. No data, account or bank identifiers exported.

## Population

| n | senders | receivers | selected_decades_2_to_6 | excluded_decades |
| --- | --- | --- | --- | --- |
| 129847 | 22229 | 64869 | 123641 | 6206 |

## Nested significant-digit grid increments

| magnitude | n | senders | receivers | one_sig | second_only | third_only | fourth_only | whole | fractional |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 22696 | 10112 | 15239 | 0.145841 | 0.053446 | 0.19651 | 0.056133 | 0.395797 | 0.604203 |
| 3 | 44829 | 12353 | 27060 | 0.129269 | 0.035557 | 0.028598 | 0.189632 | 0.383056 | 0.616944 |
| 4 | 38749 | 9156 | 24154 | 0.124881 | 0.032311 | 0.011587 | 0.01871 | 0.380371 | 0.619629 |
| 5 | 14943 | 4648 | 10382 | 0.125209 | 0.028776 | 0.008164 | 0.001673 | 0.376564 | 0.623436 |
| 6 | 2424 | 1405 | 1994 | 0.129538 | 0.02764 | 0.013201 | 0.000825 | 0.375 | 0.625 |

## Leading-digit grid point masses, pooled selected decades

| lead_digit | n | senders | receivers | one_sig_n | one_sig_senders | one_sig_receivers | one_sig_share | whole_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 40575 | 11434 | 25251 | 7682 | 4029 | 6113 | 0.189328 | 0.420727 |
| 2 | 21042 | 7661 | 14494 | 1155 | 935 | 1056 | 0.05489 | 0.351012 |
| 3 | 14109 | 5980 | 10300 | 884 | 728 | 828 | 0.062655 | 0.330073 |
| 4 | 10819 | 5008 | 8236 | 685 | 601 | 650 | 0.063315 | 0.323505 |
| 5 | 12404 | 5410 | 9103 | 4116 | 2536 | 3423 | 0.331828 | 0.522976 |
| 6 | 7489 | 3924 | 5901 | 569 | 495 | 540 | 0.075978 | 0.343571 |
| 7 | 6744 | 3627 | 5374 | 403 | 373 | 386 | 0.059757 | 0.354537 |
| 8 | 5558 | 3143 | 4507 | 366 | 339 | 359 | 0.065851 | 0.329975 |
| 9 | 4901 | 2917 | 4014 | 269 | 252 | 260 | 0.054887 | 0.312385 |

Grid predicates describe exact compatibility within absolute USD tolerance1e-6, not latent rounding operations. The first four columns of shares form nested-grid increments; whole/fractional overlap those increments. Leading bins are [d,d+1) in decimal mantissa, so point masses sit at bin boundaries. Their shares are not a fitted continuous-density control. Rounding can move values across observed decades. No mixture weights or causal generation stages are identified.
