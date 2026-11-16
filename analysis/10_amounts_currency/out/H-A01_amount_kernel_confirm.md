# H-A01: frozen confirmation and sensitivity

Run: `uv run python analysis/10_amounts_currency/H-A01_amount_kernel.py --phase confirm --freeze 25d4703a6388baaec3d0808499dd7bebe05819da`

DuckDB 2.0.0; 2GB; two threads; no spill.
Both-account confirmation only. Unlabelled does not imply legitimate.

## Exploration support

| labelled | n | senders | receivers | nonpositive |
| --- | --- | --- | --- | --- |
| False | 2415020 | 151189 | 724650 | 0 |
| True | 1710 | 1051 | 934 | 0 |

## Primary equal-account contrasts

| contrast | accounts | matched_payments | mean_log_difference | account_SE | 97.5%_low | 97.5%_high | geometric_ratio | median_log_difference | negative_account_share | abs_difference_from_2_gt_1_share | passes_equivalence | matched_transaction_weighted_log_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| beneficiary business | 63801 | 2167328 | 1.999499834888641 | 0.007682005339142346 | 1.9822813650754714 | 2.016718304701811 | 7.385361274952141 | 2.0018273030382234 | 0.12819548282942272 | 0.529317722292754 | True | 1.9985806010951064 |
| ordering business | 43795 | 1127759 | 1.976398134975251 | 0.010805567380578055 | 1.9521785038317212 | 2.000617766118781 | 7.216702527778687 | 1.9749477983582975 | 0.16650302545952733 | 0.5901358602580203 | True | 1.9570249746814863 |

## Sensitivity: also hold endpoint-bank country corridor fixed

| contrast | accounts | matched_payments | mean_log_difference | account_SE | 97.5%_low | 97.5%_high | geometric_ratio | median_log_difference | negative_account_share | abs_difference_from_2_gt_1_share | passes_equivalence | matched_transaction_weighted_log_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| beneficiary business | 37171 | 1509465 | 1.9916796637059728 | 0.010135945766880755 | 1.968960924456249 | 2.0143984029556967 | 7.327831724188727 | 1.994884299094532 | 0.12668478114659276 | 0.5061741680342202 | True | 2.0045766762960486 |
| ordering business | 33192 | 855230 | 2.002464388728163 | 0.012199347992383208 | 1.9751207335399912 | 2.0298080439163346 | 7.407288061587035 | 1.9931560254201854 | 0.15853217642805495 | 0.5770968908170644 | True | 1.996894440885257 |

## Sensitivity: omit busiest 1% of sending accounts

| contrast | accounts | matched_payments | mean_log_difference | account_SE | 97.5%_low | 97.5%_high | geometric_ratio | median_log_difference | negative_account_share | abs_difference_from_2_gt_1_share | passes_equivalence | matched_transaction_weighted_log_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| beneficiary business | 62289 | 1191940 | 1.9999322590265278 | 0.007851428352022868 | 1.9823340439640187 | 2.0175304740890367 | 7.388555574030682 | 2.0034002775771196 | 0.13106648043795854 | 0.5370290099375492 | True | 1.9938343869342086 |
| ordering business | 30495 | 608484 | 1.938404061151116 | 0.013083429531491433 | 1.9090788229489424 | 1.9677292993532896 | 6.947654086952742 | 1.9456664668109633 | 0.16976553533366126 | 0.5916379734382685 | True | 1.9140911703721548 |

## Sensitivity: month 5 within the same account partition

| contrast | accounts | matched_payments | mean_log_difference | account_SE | 97.5%_low | 97.5%_high | geometric_ratio | median_log_difference | negative_account_share | abs_difference_from_2_gt_1_share | passes_equivalence | matched_transaction_weighted_log_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| beneficiary business | 30964 | 607460 | 2.0049916315866905 | 0.011466073032355579 | 1.9792915410937495 | 2.0306917220796312 | 7.426031752394847 | 1.990691929459996 | 0.13557679886319596 | 0.549283038367136 | True | 1.9994306331835445 |
| ordering business | 16108 | 266459 | 1.9766654744634202 | 0.018253853870246504 | 1.9357512316370882 | 2.0175797172897525 | 7.218632095252031 | 1.9725703066173157 | 0.17177799851005712 | 0.608393344921778 | True | 1.953062438558948 |

## Sensitivity: month 6 within the same account partition

| contrast | accounts | matched_payments | mean_log_difference | account_SE | 97.5%_low | 97.5%_high | geometric_ratio | median_log_difference | negative_account_share | abs_difference_from_2_gt_1_share | passes_equivalence | matched_transaction_weighted_log_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| beneficiary business | 37256 | 827037 | 1.9918682948611057 | 0.010386224608436955 | 1.9685885798650813 | 2.01514800985713 | 7.32921411192808 | 1.9921965243928066 | 0.13748121108009448 | 0.5456839166845608 | True | 1.9961325176502525 |
| ordering business | 20645 | 379685 | 1.9490378461882603 | 0.015998873962977788 | 1.91317792209102 | 1.9848977702855006 | 7.0219281543674095 | 1.9582432561462113 | 0.17079195931218213 | 0.6011140712036813 | True | 1.9482800610355184 |

## Sensitivity: month 7 within the same account partition

| contrast | accounts | matched_payments | mean_log_difference | account_SE | 97.5%_low | 97.5%_high | geometric_ratio | median_log_difference | negative_account_share | abs_difference_from_2_gt_1_share | passes_equivalence | matched_transaction_weighted_log_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| beneficiary business | 29838 | 573775 | 2.0138304318127367 | 0.011677189736311622 | 1.9876571437061985 | 2.040003719919275 | 7.491959897161193 | 2.0134655993523425 | 0.13543132917755882 | 0.5486292646960252 | True | 2.0045547081770327 |
| ordering business | 15726 | 250860 | 1.9895403734761812 | 0.018519345339267062 | 1.948031057274712 | 2.0310496896776504 | 7.312172121565323 | 1.9950867370845322 | 0.17067277120691848 | 0.6059392089533256 | True | 1.9542550150726972 |

## Sensitivity: Direct within the same account partition

| contrast | accounts | matched_payments | mean_log_difference | account_SE | 97.5%_low | 97.5%_high | geometric_ratio | median_log_difference | negative_account_share | abs_difference_from_2_gt_1_share | passes_equivalence | matched_transaction_weighted_log_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| beneficiary business | 49255 | 1337923 | 1.9934277145160557 | 0.008861186536944787 | 1.973566224428588 | 2.0132892046035233 | 7.340652348657195 | 1.9997669439867147 | 0.1305654248299665 | 0.5344229012283017 | True | 1.9971480712311198 |
| ordering business | 29864 | 651135 | 1.9620952729944747 | 0.013236138556372888 | 1.9324277523258049 | 1.9917627936631446 | 7.114217687947406 | 1.9584880019579916 | 0.17057326547013127 | 0.594495044200375 | True | 1.9492594342344447 |

## Sensitivity: Indirect within the same account partition

| contrast | accounts | matched_payments | mean_log_difference | account_SE | 97.5%_low | 97.5%_high | geometric_ratio | median_log_difference | negative_account_share | abs_difference_from_2_gt_1_share | passes_equivalence | matched_transaction_weighted_log_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| beneficiary business | 32073 | 652941 | 2.0004110640878134 | 0.011348441154982862 | 1.9749746340377115 | 2.0258474941379156 | 7.392094098899324 | 2.0105504617234757 | 0.13980606740872384 | 0.5542044710504163 | True | 2.002901891518715 |
| ordering business | 17047 | 289521 | 1.9630999191840797 | 0.017641113059291436 | 1.9235590754496448 | 2.0026407629185146 | 7.121368551081867 | 1.9882639830145843 | 0.17041121604974482 | 0.6020414149117147 | True | 1.961519294979226 |

## Sensitivity: Covered within the same account partition

| contrast | accounts | matched_payments | mean_log_difference | account_SE | 97.5%_low | 97.5%_high | geometric_ratio | median_log_difference | negative_account_share | abs_difference_from_2_gt_1_share | passes_equivalence | matched_transaction_weighted_log_difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| beneficiary business | 4643 | 66969 | 2.0336374375200363 | 0.030958256440697222 | 1.9642475086590883 | 2.103027366380984 | 7.6418325541158 | 1.9716816776500714 | 0.14602627611458108 | 0.5767822528537584 | True | 1.9955957463847251 |
| ordering business | 2883 | 27074 | 1.9809771125377753 | 0.044023803592316474 | 1.8823020270945463 | 2.0796521979810043 | 7.249823418766585 | 1.9442690069444968 | 0.18383628165105792 | 0.6340617412417621 | True | 1.9728391652228676 |

Intervals describe account-to-account variation under account independence; shared counterparties and banks can induce remaining dependence. 97.5% intervals apply a Bonferroni correction to two primary contrasts.
