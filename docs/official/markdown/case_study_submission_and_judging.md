# UMDAC Datathon 2026 — Case Study, Submission Format, and Judging Criteria

Consolidated Markdown reference for the 2026 Swift preliminary-round case study, official submission format, and preliminary judging rubric. Full source-page text is retained for the case study and submission format. Scoring descriptors are transcribed from the rubric table into criterion-by-criterion Markdown so no individual performance level is lost.

**Contents**

1. Swift Case Study Preliminary Round (4 PDF pages)
2. Submission Format (1 PDF page)
3. Judging Criteria Preliminary Round (2 PDF pages)

---

## Universiti Malaya UMDAC Datathon 2026 - Swift Case Study Preliminary Round.pdf

- Original PDF: https://drive.google.com/file/d/1Pm_VGS3w96ffu8N2yZYPAm128RiEnJsL/view
- Source pages: 4
- Conversion: full source text, organized by original page; punctuation and source wording retained.

### Source page 1 of 4

Confidentiality: Public Page: 1 of 4

Date: 13 November 2026  

### UMDAC Datathon 2026 – Swift payments

### The context

Swift is a cooperative that operates the communication channels interconnecting 11,500 banks, market infrastructures, fintechs and corporates. A payment sent across borders, will in most cases reach its destination over the Swift network. The financial sector and the medical sector are the two main environments where data privacy is strongly ingrained and legally enforced around the world. As such, most development of products and services involves experiments, tests or demoes using data that is anonymised, synthesized or artificial. Accurately modelling real-world dynamics and capturing them in a meaningful way, is a key skill every data scientist benefits from.

### The data set

In this Datathon, you will be using an artificial payment data set that Swift has been using for many initiatives throughout the years. It’s been constructed by distilling business knowledge from real payments traffic, to capture how the parties of a payment interact. Note that any snapshot of a set of payments is inherently a directed temporal pseudograph, with each node/vertex and each link/edge containing their own sets of attributes/features that strongly (causally) depend on each other. In the data set you receive, we have chosen to represent these payment instructions in a timestamped tabular form, for easy consumption. A simplified conceptual example of such data is given here, while a detailed description of each feature in the full data set is provided in appendix Error! Reference source not found..

| Timestamp | Currency | Amount | From customer | To customer |
| --- | --- | --- | --- | --- |
| 2026-11-06T08:02:10.000Z | MYR | 9001.42 | Makcik Kiah; 1122 3344 5566 Avenue 10, The Vertical, Bangsar South City, No.8, Jalan Kerinchi, 59200, Kuala Lumpur, MY | Jack Smith; 000123456789; 7 Times Square; 45th floor, New York, NY 10036, US |
| 2026-11-06T19:14:55.000Z | USD | 100.00 | Jan Zonder Pet; BE40 0012 0034 5678; Avenue Adele 1, 1310 La Hulpe, BE | Maria Kumar; 98765432123; 600 Brickell Avenue, Suite 1800, Miami, FL 33131, US |

2026-11-06T19:14:55.000Z USD 100.00 Jan Zonder Pet Maria Kumar BE40 0012 0034 5678 98765432123 Avenue Adele 1, 1310 La 600 Brickell Avenue, Suite Hulpe, BE 1800, Miami, FL 33131, US

### The challenge

In a nutshell: your task is to reverse-engineer the rules used to generate the data set. Based exclusively on the raw data provided, analyse and reconstruct as much as possible of the logic, causal relationships and business knowledge used to generate it. Your findings should explain how the data was constructed and how its features relate to one another. The actual generating logic is derived from real-world economic analysis, with some rules being more complex than others. Purely for illustration, two fictitious examples of such business knowledge could be:

1) People send three times higher payment values, if their payment’s currency code starts with a consonant instead of a vowel.

2) The higher a country’s GDP, the more companies receive payments between 3 and 5pm local time.

---

### Source page 2 of 4

UMDAC Datathon 2026 – Swift Confidentiality: Public Page: 2 of 4 payments Date: 13 November 2026 As this data set is intended to be shareable for broad audiences, it is on purpose initialised using randomised distributions instead of confidential Swift network metrics. So, while market dynamics and decision-making processes remain accurately preserved, please do consider that e.g. the number of individuals living in a certain country, the relative and absolute sizes of import vs export economies, the geographic distributions of large cities, ethnic origins of names used, etc … don’t necessarily reflect reality. Using AI to support in coding, dashboard design, etc … is explicitly allowed, as teams are evaluated on how they show understanding of the data and clarity of business insights, not on visual style.

### Preliminary round

For the preliminary round, participants must submit both a dashboard and a slide deck. The judges will evaluate:

1. A set of dashboards (PDF format) presenting the identified insights, grouped by feature type (e.g. insights around currencies used, payments values, routing behaviour, anomaly types, …). For each insight, the dashboard must state the reconstructed business rule(s) clearly and include at least one chart demonstrating how the rule(s) are reflected in the data for each feature group. Note that since a dashboard can contain multiple related charts but should cover a single feature group, the expectation is that the PDF will contain between 5 and 15 dashboards.

2. A slide deck (PDF format) presenting the principal insights from the dashboard. For each selected insight, the presentation must restate the reconstructed business rule(s), copy or reference the supporting chart, and explain the real-world economic behaviour that the rule may represent. The presentation must also describe the methodology and analytical process used to identify the different rules. Each dataset feature group can have at most one slide summarizing the rules/insights related to that group (including introduction and methodology this represents 10 to 20 slides in total)

### The evaluation

Sound scientific methodologies, deep analytical insight, and clearly formulated reasoning, are the main criteria for evaluating participant submissions. A well-described and analytically grounded partial or negative result for deriving the business rule(s) making up a specific data set feature, is considered more valuable than just accidentally guessing it right. Please dig deeper than “A is correlated with B”, try to explicitly model causal relationships, as that is exactly how the original Swift data set has been constructed. Across the presentation and the dashboard, the following scoring will be applied:

| Category | Weight |
| --- | --- |
| Insight Quality | 45% |
| Interpretation and Economic Reasoning | 12% |
| Evidence, Method and Data integrity | 23% |
| Communication | 20% |

---

### Source page 3 of 4

Confidentiality: Public Page: 3 of 4

Date: 13 November 2026  

### A.1 Appendix: Features of the data set

This data set contains artificial cross-border payment records with anonymized account identifiers, BIC-based routing paths, payment amounts normalized to USD, party detail text, tokenized party-detail features, and optional anomaly labelling. Fields ending in _TOKENS are derived pattern summaries of the corresponding raw detail fields and should be treated as engineered text-pattern features rather than original payment content.

| Feature | Description |
| --- | --- |
| EPOCH_SECONDS | Transaction timestamp represented as Unix epoch seconds. Can be converted to a UTC datetime for time-based analysis. |
| CURRENCY_CODE | ISO 4217 currency code for the payment currency, e.g. GBP, EUR, USD, CNY. |
| USD_AMOUNT | Transaction amount normalized to USD. Useful for comparing payment size across currencies. |
| ORDERING_BIC8 | 8-character BIC identifying the ordering institution / sending bank at the start of the payment chain. |
| BENEFICIARY_BIC8 | 8-character BIC identifying the beneficiary institution / receiving bank at the end of the payment chain. |
| BIC8_PATH | Semicolon-separated sequence of BIC8s representing the route the payment followed through correspondent or intermediary banks. A value containing ... appears to indicate an incomplete, hidden, or discontinuous path. |
| TOTAL_DURATION | Total elapsed duration of the payment route, in seconds, from initiation to completion or observation end. |
| CONTINUITY_QFLAG | Indicates whether the full BIC path is continuous and observable. Y = continuous path; N = path contains a gap or placeholder such as ... |
| CURRENCY_CONVERSION_COUNT | Number of currency conversions / FX steps along the payment path. 0 means no conversion observed. |
| PARTICIPANT_COUNT | Number of institutions or path participants involved in the payment route. |
| TRANSACTION_TYPE_CODE | Payment routing category. Observed values include Direct, Indirect, and Covered. Direct means sender-to-recipient bank path; Indirect uses intermediaries; Covered suggests a cover-payment-style route. |
| ORDERING_ACCOUNT | Anonymized account identifier for the ordering party / sender. Values use a synthetic _FAKE_##### pattern. |
| BENEFICIARY_ACCOUNT | Anonymized account identifier for the beneficiary party / receiver. Values use a synthetic _FAKE_##### pattern. |
| ORDERING_DETAILS | Raw or semi-structured ordering party details, such as name, address, country, account hints, or free-text remittance-like information. This field may contain embedded line breaks. |
| ORDERING_TOKENS | Tokenized representation of ORDERING_DETAILS. Tokens describe recognized patterns such as names, businesses, street addresses, IBANs, country codes, finance words, stop words, line breaks, and character patterns. |
| BENEFICIARY_DETAILS | Raw or semi-structured beneficiary party details, such as name, address, country, account hints, or free-text information. This field may contain embedded line breaks. |
| BENEFICIARY_TOKENS | Tokenized representation of BENEFICIARY_DETAILS, using the same style of semantic and pattern tokens as ORDERING_TOKENS. |

---

### Source page 4 of 4

wift Confidentiality: Public Page: 4 of 4

Date: 13 November 2026  

| Feature | Description |
| --- | --- |
| ORDERING_TYPE | Type of ordering party. B = Business / corporate, C = Consumer / individual customer. |
| BENEFICIARY_TYPE | Type of beneficiary party. B = Business / corporate, C = Consumer / individual customer. |
| ANOMALY_TYPE | Label for the type of anomaly associated with the record. • ROMANCE_SCAM: Fraud where a Consumer is misled into believing they are in a long-distance relationship with another Consumer and is being convinced to repeatedly send them funds. • CEO_SCAM: Fraud where a Business is convinced to make an illegitimate payment, e.g. due to a compromised or spoofed CEO email asking the finance department to execute that payment. • ACCOUNT_REPLACEMENT_SCAM: Fraud where a real legitimate invoice is intercepted, and the account number on it is replaced by that of a fraudster or money mule. • FAT_FINGER_MISTAKE : User error where the comma separator is incorrectly placed in the USD amount • DUPLICATE_PAYMENT: Accidental repeat of a previously issued payment, e.g. due to a race condition in a Business’ back-office, or two Consumers that both pay an invoice unaware their partner already did so. |

## Structured tables from the case study

These reproduce tabular content from the PDFs; the original source-page text remains above. The sample transactions are explicitly fictitious illustrations.

### Illustrative transactions (case study page 1)

| Timestamp | Currency | Amount | From customer | To customer |
| --- | --- | --- | --- | --- |
| 2026-11-06T08:02:10.000Z | MYR | 9001.42 | Makcik Kiah; 1122 3344 5566 Avenue 10, The Vertical, Bangsar South City, No.8, Jalan Kerinchi, 59200, Kuala Lumpur, MY | Jack Smith; 000123456789; 7 Times Square; 45th floor, New York, NY 10036, US |
| 2026-11-06T19:14:55.000Z | USD | 100.00 | Jan Zonder Pet; BE40 0012 0034 5678; Avenue Adele 1, 1310 La Hulpe, BE | Maria Kumar; 98765432123; 600 Brickell Avenue, Suite 1800, Miami, FL 33131, US |

### Overall scoring (case study page 2)

| Category | Weight |
| --- | --- |
| Insight Quality | 45% |
| Interpretation and Economic Reasoning | 12% |
| Evidence, Method and Data integrity | 23% |
| Communication | 20% |

### Dataset feature dictionary (case study pages 3–4)

| Feature | Description |
| --- | --- |
| EPOCH_SECONDS | Transaction timestamp represented as Unix epoch seconds. Can be converted to a UTC datetime for time-based analysis. |
| CURRENCY_CODE | ISO 4217 currency code for the payment currency, e.g. GBP, EUR, USD, CNY. |
| USD_AMOUNT | Transaction amount normalized to USD. Useful for comparing payment size across currencies. |
| ORDERING_BIC8 | 8-character BIC identifying the ordering institution / sending bank at the start of the payment chain. |
| BENEFICIARY_BIC8 | 8-character BIC identifying the beneficiary institution / receiving bank at the end of the payment chain. |
| BIC8_PATH | Semicolon-separated sequence of BIC8s representing the route the payment followed through correspondent or intermediary banks. A value containing ... appears to indicate an incomplete, hidden, or discontinuous path. |
| TOTAL_DURATION | Total elapsed duration of the payment route, in seconds, from initiation to completion or observation end. |
| CONTINUITY_QFLAG | Indicates whether the full BIC path is continuous and observable. Y = continuous path; N = path contains a gap or placeholder such as ... |
| CURRENCY_CONVERSION_COUNT | Number of currency conversions / FX steps along the payment path. 0 means no conversion observed. |
| PARTICIPANT_COUNT | Number of institutions or path participants involved in the payment route. |
| TRANSACTION_TYPE_CODE | Payment routing category. Observed values include Direct, Indirect, and Covered. Direct means sender-to-recipient bank path; Indirect uses intermediaries; Covered suggests a cover-payment-style route. |
| ORDERING_ACCOUNT | Anonymized account identifier for the ordering party / sender. Values use a synthetic _FAKE_##### pattern. |
| BENEFICIARY_ACCOUNT | Anonymized account identifier for the beneficiary party / receiver. Values use a synthetic _FAKE_##### pattern. |
| ORDERING_DETAILS | Raw or semi-structured ordering party details, such as name, address, country, account hints, or free-text remittance-like information. This field may contain embedded line breaks. |
| ORDERING_TOKENS | Tokenized representation of ORDERING_DETAILS. Tokens describe recognized patterns such as names, businesses, street addresses, IBANs, country codes, finance words, stop words, line breaks, and character patterns. |
| BENEFICIARY_DETAILS | Raw or semi-structured beneficiary party details, such as name, address, country, account hints, or free-text information. This field may contain embedded line breaks. |
| BENEFICIARY_TOKENS | Tokenized representation of BENEFICIARY_DETAILS, using the same style of semantic and pattern tokens as ORDERING_TOKENS. |
| ORDERING_TYPE | Type of ordering party. B = Business / corporate, C = Consumer / individual customer. |
| BENEFICIARY_TYPE | Type of beneficiary party. B = Business / corporate, C = Consumer / individual customer. |
| ANOMALY_TYPE | Label for the type of anomaly associated with the record. • ROMANCE_SCAM: Fraud where a Consumer is misled into believing they are in a long-distance relationship with another Consumer and is being convinced to repeatedly send them funds. • CEO_SCAM: Fraud where a Business is convinced to make an illegitimate payment, e.g. due to a compromised or spoofed CEO email asking the finance department to execute that payment. • ACCOUNT_REPLACEMENT_SCAM: Fraud where a real legitimate invoice is intercepted, and the account number on it is replaced by that of a fraudster or money mule. • FAT_FINGER_MISTAKE : User error where the comma separator is incorrectly placed in the USD amount • DUPLICATE_PAYMENT: Accidental repeat of a previously issued payment, e.g. due to a race condition in a Business’ back-office, or two Consumers that both pay an invoice unaware their partner already did so. |

---

## Datathon 2026 Submission Format.pdf

- Original PDF: https://drive.google.com/file/d/16Gki8381UpkQAGo7Fc8IsjPuInQu98zd/view
- Source pages: 1
- Conversion: full source text, organized by original page; punctuation and source wording retained.

### Source page 1 of 1

### Datathon 2026: Submission Format

### Preliminary Round

### Submission Components:

1. A dashboard (Google Data Studio / Google Looker Studio or equivalent – link/PDF) presenting the identified insights, grouped by feature type (e.g. currencies used, payment values, routing behaviour, anomaly types, etc.).

- Clearly state the reconstructed business rules for each insight.

- Include at least one chart demonstrating how each rule is reflected in the data for every feature group.

2. A presentation slide deck (PDF format) presenting the principal insights from the dashboard.

- Restate the reconstructed business rules for each selected insight.

- Include or reference the supporting charts.

- Explain the real-world economic behaviour that each rule may represent.

- Describe the methodology and analytical process used to identify the different rules.

- Each dataset feature group can have at most one slide summarising its related rules and insights.

- Slide Requirement: 10–20 slides in total, including introduction and methodology.

### Evaluation Criteria:

- Dashboard: Visual clarity (35%), effectiveness of charts and supporting evidence (50%), and correctness and clarity of insights (15%).

- Presentation Slides: Overall presentation quality (15%), methodology (65%), and economic explanations of the identified insights (20%).

---

## Datathon 2026 Judging Criteria Preliminary Round .pdf

- Original PDF: https://drive.google.com/file/d/1Y3dsC9brXqBd_IsBlUmBS-7gCiRfldea/view
- Source pages: 2
- Conversion: full source text, organized by original page; punctuation and source wording retained.

### Datathon 2026 Judging Rubric - Preliminary Round



**Scoring bands:** Poor (0–3), Fair (4–7), Good (8–11), Very Good (12–16), Exceptional (17–20).

### Source page 1 of 2

#### INSIGHT QUALITY (45%)

##### 1.1 Task understanding & hypotheses — 5%

**What judges look for:** The team shows it understands what the problem statement asks for and turns it into specific, testable hypotheses about how the data behaves.

- **Poor (0–3):** The team does not show an understanding of the task. The submission is unrelated to the problem statement, or no hypotheses or objectives can be identified.
- **Fair (4–7):** The task is restated in broad terms. The hypotheses are vague (for example, 'some features are related') or cannot be tested with the data provided.
- **Good (8–11):** The task is understood and the team states at least one clear, testable hypothesis. The hypotheses may be few, or may not guide the later analysis consistently.
- **Very Good (12–16):** The team states specific, testable hypotheses that follow from the problem statement, and the analysis visibly follows them. The reader can see what was expected, what was tested and why.
- **Exceptional (17–20):** The hypotheses are sharply stated, prioritised and clearly drive the analysis. The team also shows how early results changed or replaced its hypotheses, so the work is purposeful rather than a search for patterns.

##### 1.2 Rule reconstruction quality — 12%

**What judges look for:** Whether each finding is stated as a rule: when it applies, what changes, by how much, and which records it covers.

- **Poor (0–3):** The submission only describes the data, such as averages, counts or charts of totals. No rule or underlying pattern is identified.
- **Fair (4–7):** A pattern is identified but not stated as a rule. The condition, the effect or the scope is missing, so it is unclear when the pattern applies or how large it is. Or the pattern is obvious and adds little.
- **Good (8–11):** At least one rule is stated with a condition and an effect, and it is supported by the data. The size or the scope of the rule may be missing or loosely defined.
- **Very Good (12–16):** The rules clearly state when they apply, what changes, by how much, and which records they cover. They are consistent with the data and go beyond simple correlations.
- **Exceptional (17–20):** The rules are precise, complete and non-obvious, including where they do not apply. They are specific enough that another team could use them to reproduce the behaviour in the data.

##### 1.3 Explanatory depth — 14%

**What judges look for:** Why the pattern happens: the comparisons or checks used, whether it is causal or only a correlation, and what remains uncertain, including hypotheses that were tested and rejected.

- **Poor (0–3):** The team reports a number or pattern with no investigation. There is no attempt to explain why it happens, and no comparison or check supports what is shown.
- **Fair (4–7):** The team offers a plausible reason for the pattern, but nothing in the submission supports it. Important uncertainties or alternative explanations go unexamined, and the reasoning is largely assumed.
- **Good (8–11):** The team supports its explanation with at least one comparison or check, for example comparing segments or periods, or controlling for another factor. The explanation is reasonable, but the investigation is limited and some gaps remain.
- **Very Good (12–16):** The team weighs several contributing factors using suitable comparisons or checks, and separates a causal rule from a correlation where it can. It reports at least one hypothesis that did not hold, and notes what the data cannot show, so the reader knows how far to trust the explanation.
- **Exceptional (17–20):** The team investigates the finding thoroughly, testing at least one alternative explanation or confounding factor and ruling it in or out with evidence. Rejected hypotheses and unexplained patterns are reported honestly, and the submission clearly separates what the data demonstrates from what remains uncertain. A well-argued partial or negative result scores higher than a correct finding with no supporting reasoning.

##### 1.4 Specificity of the finding — 5%

**What judges look for:** The headline can be said in one sentence with numbers and a segment.

- **Poor (0–3):** The finding is a topic rather than a claim, for example 'we explored the data'. A reader cannot tell what the team actually found.
- **Fair (4–7):** The direction of the finding is clear, but it is vague about who, where or how much, for example 'some records behave differently'. The reader cannot tell how large or widespread the effect is.
- **Good (8–11):** The finding names a group, area or period and gives at least one figure, though the size of the effect or the comparison behind it is not fully clear.
- **Very Good (12–16):** The headline can be stated in one sentence with a segment and numbers, for example 'Records in group X are about twice the size of records in group Y, in every region'. The reader understands the finding without further explanation.
- **Exceptional (17–20):** The headline is precise and quantified, and is set against a comparison, such as another segment or a baseline, that makes the size and importance of the effect obvious. It is easy to remember and easy for a judge to verify.

##### 1.5 Correctness of reconstructed rules — 9%

**What judges look for:** How closely each reconstructed rule matches the reference rules held by the organisers: the right feature, direction, size and scope. A well-reasoned rule honestly marked as uncertain loses fewer marks than a wrong rule presented as certain.

- **Poor (0–3):** Most of the rules reported do not match the reference rules, or the rules are too vague to be compared.
- **Fair (4–7):** A few rules match in part (for example, the right feature but the wrong direction or size), but most do not.
- **Good (8–11):** Some rules match the reference rules closely and others are partly right. Most errors are in the size or the scope of a rule.
- **Very Good (12–16):** Most rules match the reference rules in feature, direction, size and scope. Any that do not are partly right and are flagged as uncertain.
- **Exceptional (17–20):** The rules match the reference rules closely, including their limits. The team's confidence in each rule matches how accurate it turns out to be, and rules it was unsure about are marked as such.

#### INTERPRETATION & ECONOMIC REASONING (12%)

##### 2.1 Economic explanation — 5%

**What judges look for:** Why the rule may exist in the real world: a plausible economic or behavioural explanation for each key rule. Explanations may draw on general knowledge, but not on data from outside the provided dataset.

- **Poor (0–3):** No explanation of what the rule could mean in the real world is given, or the explanation is unrelated to the rule.
- **Fair (4–7):** A real-world explanation is offered, but it is generic or only restates the rule (for example, 'people just prefer this'). It is unclear how the explanation would produce the pattern.
- **Good (8–11):** A plausible real-world explanation is given for the main rule and it fits the pattern, though it may be brief or not compared with other possibilities.
- **Very Good (12–16):** Each key rule has a plausible economic or behavioural explanation that fits the pattern in the data. The reader can see how the real-world mechanism would produce the rule.
- **Exceptional (17–20):** The explanations are specific, well reasoned and draw on relevant industry or economic knowledge. The team also considers an alternative explanation for at least one rule and says why it prefers its own.

##### 2.2 Consistency with the evidence — 4%

**What judges look for:** The explanation matches what the data shows, and the team is honest about the difference between what is observed and what is only a plausible interpretation. Explanations are judged on plausibility and honesty, not on whether they match real- world facts, because the dataset may not reflect reality.

- **Poor (0–3):** The explanation contradicts the evidence shown, or speculation is presented as established fact.
- **Fair (4–7):** The explanation is broadly compatible with the data, but it goes well beyond what the evidence supports and is not labelled as interpretation.
- **Good (8–11):** The explanation is consistent with the evidence and is mostly labelled as interpretation, though some claims about the real world are stated more firmly than the data allows.
- **Very Good (12–16):** The explanation is consistent with the evidence, and the team clearly labels what is observed in the data and what is interpretation. It notes where the dataset may not reflect real-world behaviour.
- **Exceptional (17–20):** The team consistently separates observation from interpretation, and checks whether the explanation predicts something else visible in the data. Where the dataset departs from reality, the team says so and still gives a useful interpretation.

##### 2.3 Coverage & prioritisation — 3%

**What judges look for:** How much of the dataset's behaviour the rules cover, and whether the most important rules get the most attention.

- **Poor (0–3):** Only one isolated pattern is presented, or many patterns are listed with no sense of which matter.
- **Fair (4–7):** A few rules from one part of the data are presented. Coverage is narrow, and there is little sign of why these rules were chosen.
- **Good (8–11):** Rules are presented across several parts of the data, though coverage is uneven or the most important rules are not clearly identified.
- **Very Good (12–16):** The rules cover the main parts of the dataset, and the team makes clear which are the most important and why.
- **Exceptional (17–20):** The rules cover the dataset broadly and are prioritised by importance. The team also says which behaviours it could not explain, so the reader knows what coverage was achieved.

#### EVIDENCE, METHOD & DATA INTEGRITY (23%)

##### 3.1 Data preparation — 5%

**What judges look for:** Problems found in the data and the decision made for each.

- **Poor (0–3):** There is no evidence that the data was checked. Problems such as missing values, duplicates or inconsistent labels appear to have been ignored, which may have distorted the analysis.
- **Fair (4–7):** Some cleaning is described, but the reasons are not given, so the reader cannot tell why data was removed, filled or changed.
- **Good (8–11):** The team identifies the main data issues, such as missing values, duplicates, outliers or inconsistent labels, and states the decision taken for each, though the reasoning may be brief.
- **Very Good (12–16):** A concise issues log lists each problem found and the decision made, with the reasoning behind it. The log is short enough to fit in the page limit and gives the reader confidence in the data.
- **Exceptional (17–20):** The preparation is fully documented within the page limit, with reasoning for each decision. The team also explains how each decision could affect the results, so the reader knows which findings are sensitive to the cleaning.

##### 3.2 Claim-evidence linkage — 7%

**What judges look for:** Every headline claim can be traced to a chart or calculation.

- **Poor (0–3):** Key claims have no supporting chart or calculation, or the evidence shown contradicts the claim.
- **Fair (4–7):** Some claims are supported, but others are simply asserted, or correlation is described as causation, so a reader has to take parts of the story on trust.
- **Good (8–11):** Most headline claims can be traced to a chart or calculation in the submission. One or two claims may leap beyond the evidence.
- **Very Good (12–16):** Every headline claim can be traced to a chart or calculation, and the team does not present correlation as causation. A judge can verify the claims from the submission alone.
- **Exceptional (17–20):** Every headline claim is traceable and verifiable from the submission alone. Claims that rest on an estimate, assumption or interpretation are clearly labelled as such, so the reader can tell what was observed from what was inferred.

### Source page 2 of 2

##### 3.3 Method appropriateness — 8%

**What judges look for:** The method suits the question, and the team shows how it reached each rule. Sophistication earns no marks, and unjustified complexity can lose them.

- **Poor (0–3):** The method is inappropriate for the question or produces unreliable results, for example applying a technique whose assumptions the data clearly breaks.
- **Fair (4–7):** The method works but is not explained, or it is more complex than the question needs. Complexity earns no credit here, and unexplained complexity can lower the score.
- **Good (8–11):** The method is appropriate for the question and is described briefly, so the reader understands what was done.
- **Very Good (12–16):** The method is appropriate, the team gives a one- line reason why it fits the question, and the steps taken to reach each rule are described well enough for the reader to follow them.
- **Exceptional (17–20):** The method is as simple as the question allows, and the team shows the choice was deliberate. A simple method can score as high as a complex one, any added complexity is justified by what it reveals, and the work is documented so another team could repeat it.

##### 3.4 Responsible data use & compliance — 3%

**What judges look for:** Only the dataset provided by Swift is used; representativeness, bias and privacy are considered; pre- existing code and tools are disclosed.

- **Poor (0–3):** The team uses data from outside the provided dataset, breaks other dataset rules, or ignores obvious concerns, such as an unrepresentative sample or sensitive fields.
- **Fair (4–7):** The team uses only the provided dataset, but briefly mentions a concern without acting on it, or discloses its code and tools only in part.
- **Good (8–11):** The team uses only the provided dataset, discloses its code and tools, and notes at least one relevant concern, such as bias in the sample or sensitive fields.
- **Very Good (12–16):** The team uses only the provided dataset, considers representativeness, bias or privacy where relevant to the dataset and findings, and discloses every tool and piece of pre-existing code used.
- **Exceptional (17–20):** The team uses only the provided dataset, considers the concern and acts on it, for example by adjusting the analysis or caveating the findings, and follows all dataset rules.

#### COMMUNICATION (20%)

##### 4.1 Narrative structure (slides) — 6%

**What judges look for:** Leads with the headline finding, builds evidence for each rule, explains what the rules mean in the real world and ends with a clear conclusion.

- **Poor (0–3):** The slides are disorganised or read as a list of everything the team did. A reader cannot tell what the team found or why it matters.
- **Fair (4–7):** The slides cover the topics in a logical order, but the main point is buried or arrives late, so the reader must work to find the story.
- **Good (8–11):** The slides are well structured and the headline finding is clear, though it may not be stated up front and some transitions are weak.
- **Very Good (12–16):** The slides lead with the headline finding, build evidence for each rule, explain what each rule may mean in the real world, and end with a clear conclusion. The reader always knows where they are in the story.
- **Exceptional (17–20):** The slides tell a cohesive story in which each slide builds on the last. A non-technical reader can repeat the headline finding and what it means in the real world after reading it once.

##### 4.2 Dashboard — 8%

**What judges look for:** Charts and metrics that show each finding against a baseline or comparison group, with clear titles, labels and annotations.

- **Poor (0–3):** The dashboard is missing, or its content is irrelevant, misleading or unreadable.
- **Fair (4–7):** The dashboard shows basic metrics or charts, but they are generic and not clearly linked to the team's findings.
- **Good (8–11):** The dashboard shows relevant charts that support the main findings, with some comparison to a baseline or another group. Labels are adequate.
- **Very Good (12–16):** The dashboard presents charts that clearly show each key finding against a baseline or comparison group, with titles, labels and annotations that help the reader interpret each view.
- **Exceptional (17–20):** The dashboard is tightly built around the findings and tells the story on its own. A reader can understand the findings from the dashboard alone, without the slides.

##### 4.3 Visual clarity — 6%

**What judges look for:** Each visual makes one point, with a takeaway title, clean labels and no clutter.

- **Poor (0–3):** Visuals are cluttered, unreadable or purely decorative, or the charts mislead, for example through a truncated axis.
- **Fair (4–7):** Visuals are accurate and readable but generic, overloaded with information, or missing titles that state the takeaway.
- **Good (8–11):** Visuals are clear and relevant, and most have titles and labels. Some minor clutter or inconsistency remains.
- **Very Good (12–16):** Each visual makes one point, with a title that states the takeaway, clean labels and a consistent design.
- **Exceptional (17–20):** Every visual makes its point at a glance, with takeaway titles, clean labels and no clutter. Simple charts count fully; polish is not required.

**TOTAL** (overall weights sum to 100%).
