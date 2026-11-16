# The project in simple words

**The story.** Swift is the messaging network banks use to send money across borders. Real payment data is private, so Swift wrote a computer program that invents fake payments that behave like real ones. That program follows rules its authors typed in, such as "businesses send bigger amounts than individuals". Swift gave you 10 million of these fake payments and kept the rules secret.

**Your job.** Work backwards from the fake payments to the secret rules. This is called _reverse-engineering_: looking at the output of something to figure out how it was made. It is like tasting a dish and writing down the recipe.

**What you are not doing.** You are not predicting anything, and there is no score from a computer. Human judges read your two PDFs and mark them against a rubric (a marking sheet).

## What one payment looks like

Each row is one payment, described by 20 columns. In plain terms:

| Group            | Columns                                                                                                         | Meaning                                                                                                                                                            |
| ---------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| When             | `EPOCH_SECONDS`                                                                                                 | The time of the payment, stored as seconds counted from 1 Jan 1970                                                                                                 |
| How much         | `CURRENCY_CODE`, `USD_AMOUNT`                                                                                   | The currency used, and the value converted to US dollars                                                                                                           |
| Who              | `ORDERING_*`, `BENEFICIARY_*`                                                                                   | The sender ("ordering" party) and receiver ("beneficiary"), each with an account, a name and address, and a type: B for business or C for consumer (an individual) |
| Which banks      | `ORDERING_BIC8`, `BENEFICIARY_BIC8`, `BIC8_PATH`                                                                | A BIC is a bank's ID code. The path lists every bank the money passed through.                                                                                     |
| How it travelled | `TRANSACTION_TYPE_CODE`, `PARTICIPANT_COUNT`, `TOTAL_DURATION`, `CURRENCY_CONVERSION_COUNT`, `CONTINUITY_QFLAG` | Whether it went straight or via middle banks, how many banks, how many seconds it took, how many currency exchanges, and whether part of the route is hidden       |
| Is it bad        | `ANOMALY_TYPE`                                                                                                  | Almost always empty. In 7 of every 10,000 rows it names a scam or mistake, such as a romance scam or a duplicate payment.                                          |

## What a "rule" is

A rule is a precise sentence about how one column depends on others. The judges want four parts: when it applies, what changes, by how much, and which rows it covers.

- **Weak finding:** "Amount is related to customer type." This is only a _correlation_, meaning two things move together, with no detail.
- **Strong rule:** "When a business pays a business, the typical amount is about 22,900 USD, roughly 50 times the 463 USD typical between two individuals; this covers 23% of all payments." We already measured those numbers.

Two more terms you will hear:

- **Hypothesis:** a guess you can test, such as "payments with more banks in the path take longer". You check it with the data and it either holds or fails. Failed guesses still earn marks if you report them honestly.
- **Confounder:** a hidden third factor that fakes a pattern. Example: euro payments might look bigger only because more businesses use euros. You rule this out by comparing like with like (businesses in euros against businesses in dollars). That is called _stratifying_.

## What you hand in

1. **Dashboards PDF:** 5 to 15 pages, one per feature group (for example amounts, routing, anomalies). Each states the rules and shows charts that prove them.
2. **Slide deck PDF:** 10 to 20 slides covering how you worked, your main rules, and a real-world reason for each one.

Deadline: Thursday 19 Nov 2026, 12:00 PM Malaysia time.

## Where the project stands (as of 15 Nov 2026)

- **Done:** the data is in a fast format (`dataset/payments.parquet`, built by `analysis/00_prep/build_parquet.py`), and a first overview has been run (`analysis/00_prep/profile.py`).
- **Not started:** finding rules, charts, dashboards, slides.

## What to do next, in order

1. **Share the setup with your two teammates** (today). Each person needs the dataset and should run the build script once. Agree who is A, B and C:
   - **A:** amounts, currencies, party types, currency-conversion count; also owns shared data prep and the issues log.
   - **B:** routing path, route type, continuity, duration, timestamps, bank geography; also owns the dependency graph and methodology slides.
   - **C:** party details and tokens, account behaviour, anomaly types; also owns the dashboard template and deck assembly.
2. **Read the shared factual foundation first.** [Execution plan section 6](03_execution_plan.md#6-shared-scientific-foundation-and-validation) separates documented meanings, executed structural checks and unresolved semantics. It also explains how to choose validation suited to each investigation.
3. **Each person explores their own columns** (Monday). The loop is: look at a chart, write a guess, test it with a query, record the result with its numbers.
4. **Deepen and challenge** (Tuesday). For each promising rule, test one confounder, and have a teammate try to break it.
5. **Build the PDFs** (Wednesday), re-check every number, and submit Thursday morning.

You do not need to write the queries yourself. Tell the AI assistant a column group or a guess in plain words and it can run the test, show the chart and explain what it means. Step 2 is the natural place to begin.
