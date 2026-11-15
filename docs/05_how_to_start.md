# How to Start and What to Do Next

A step-by-step guide from "I just opened this project" to "we submitted". Read [01_project_in_simple_words.md](01_project_in_simple_words.md) first if the task itself is unclear.

**Deadline: Thu 19 Nov 2026, 12:00 PM Malaysia time. Team target: uploaded by 10:00 AM.**

## Where we are (15 Nov 2026)

| Done | Not started |
|---|---|
| Official documents read and summarised | Finding rules |
| Dataset converted to a fast Parquet file | Charts |
| First overview of the data ([profile script](../analysis/00_prep/profile.py)) | Dashboards PDF |
| 8 data issues logged ([issues log](../findings/issues_log.md)) | Slides PDF |
| Folder structure, plan and templates | |

## Step 0: One-time setup (each teammate, about 20 minutes)

1. **Get the code.** Clone the team's private GitHub repository.
2. **Install uv**, the tool that runs our Python scripts without manual package installs: `brew install uv` on macOS, or see <https://docs.astral.sh/uv/> for Windows and Linux.
3. **Get the data.** Download the CSV from the organisers' channel and put it in `dataset/`. Details: [dataset/README.md](../dataset/README.md).
4. **Build the fast copy** (about 5 minutes), from the project's root folder:
   ```bash
   uv run --with duckdb --with pandas python analysis/00_prep/build_parquet.py
   ```
5. **Check it works** (about 10 seconds). You should see tables of counts:
   ```bash
   uv run --with duckdb --with pandas python analysis/00_prep/profile.py
   ```
6. **Pick your role.** Agree who is A, B and C (see the table in [03_execution_plan.md](03_execution_plan.md), section 4) and write the names into that table.

## Step 1: Understand your columns (Sunday night, 1–2 hours)

1. Read the output of the profile script from top to bottom. It shows what values each column takes and how common they are.
2. Read your folder's README for your starting questions:
   - A: [analysis/10_amounts_currency/](../analysis/10_amounts_currency/README.md)
   - B: [analysis/20_routing_time/](../analysis/20_routing_time/README.md)
   - C: [analysis/30_parties_anomalies/](../analysis/30_parties_anomalies/README.md)
3. Read the official meaning of your columns in [official/pdfs/1_case_study_swift.pdf](official/pdfs/1_case_study_swift.pdf), pages 3–4.

## Step 2: Find the "free" rules (Sunday night to Monday morning)

Some columns are simply calculated from other columns. These rules are exact (true for 100% of rows), quick to prove, and tell us which columns are *not* worth deeper study. Each owner checks their own list.

| Owner | Check whether... |
|---|---|
| A | `CURRENCY_CONVERSION_COUNT` can be worked out from the path or the currencies involved |
| B | `PARTICIPANT_COUNT` always equals the number of banks in `BIC8_PATH`; `Direct` always means exactly 2 banks; `CONTINUITY_QFLAG` = N always means the path contains `...`; the first and last bank in the path equal `ORDERING_BIC8` and `BENEFICIARY_BIC8` |
| C | `_TOKENS` can be rebuilt from `_DETAILS`; the account number embeds the bank code; an account always keeps the same type (B or C), bank and name |

For each check: write a hypothesis file, write a script, record the result. The first one takes the longest; after that it is a routine.

## Step 3: The working loop (Monday and Tuesday)

Repeat this for every idea. One idea should take 20–60 minutes.

1. **Guess.** Copy [`findings/hypotheses/H-000_template.md`](../findings/hypotheses/H-000_template.md) to a new file such as `H-A01_amount_by_party_pair.md`. Fill in "Guess" and "Test" *before* looking at the answer.
2. **Test.** Write a script with the same name in your analysis folder (`H-A01_amount_by_party_pair.py`). It reads the Parquet file, computes counts or medians per group, and saves a chart to your `out/` folder.
3. **Compare like with like.** If you claim "X changes the amount", hold the sender/receiver types fixed, because business payments are far larger than personal ones and can fake almost any pattern.
4. **Confirm.** Run the same test on the other half of the accounts. A real rule gives the same numbers on both halves.
5. **Record.** Fill in "Result" and set the status: confirmed, rejected or uncertain. **Rejected ideas stay in the folder**; the judges award marks for them.
6. **Write the rule** in the required shape: *when* it applies, *what* changes, *by how much*, *which rows*, and *where it fails*.
7. **Add a real-world reason**, clearly marked as interpretation.

**Working with an AI assistant:** you do not need to write the code yourself. Describe the guess in plain words ("check whether payments with more banks take longer, for Direct and Indirect separately") and ask it to follow `AGENTS.md`. Always read the numbers yourself and make sure you can explain them; the rules require that we can justify everything we submit.

## Step 4: Daily team routine

- **15-minute call each evening.** Each person shows their best rule; the other two try to break it ("could this just be because...?").
- **One branch per person per day**, merged through a pull request, touching only your own folder. This avoids conflicts.
- **New data problem?** Add a row to the [issues log](../findings/issues_log.md).

## Day-by-day schedule

| Day | Goal | By the end of the day we have |
|---|---|---|
| **Sun 15 Nov** (evening) | Setup, Steps 0–2 | Everyone can run the scripts; first "free" rules recorded |
| **Mon 16 Nov** | Breadth: one headline finding per feature group | 10–15 hypothesis files across the team; a first sketch of which column depends on which |
| **Tue 17 Nov** | Depth: turn findings into precise rules; rule out alternative explanations. Attend the organisers' online workshop. | 2–4 confirmed rules per owner; list of 8–12 dashboard topics agreed. **No new ideas after tonight.** |
| **Wed 18 Nov** | Build: final charts, dashboards, slides. A second person re-runs every headline number. | Complete draft of both PDFs by evening; checked against [the checklist](../deliverables/README.md) |
| **Thu 19 Nov** | Final read-through by 09:00, upload by 10:00 | Submitted, two hours before the 12:00 deadline |

## What a finished feature group looks like

Each of our 5–15 feature groups (for example "payment amounts", "routing", "anomalies") ends with:

- 1–4 confirmed rules, each one sentence with numbers.
- At least one chart per rule that shows it against a comparison group, with a title stating the takeaway.
- One real-world explanation per rule, plus one alternative we considered.
- An honest note of what we tested and rejected, and what we could not explain.

That becomes **one dashboard page** and **at most one slide**.

## If you are stuck

| Problem | Do this |
|---|---|
| "I do not know what to test" | Take the first starting question in your folder's README and make one chart of it |
| "My computer runs out of memory" | Query the Parquet file with DuckDB and select only the columns you need; never load the CSV with pandas |
| "My pattern might be a coincidence" | Check it on the other half of the accounts, and inside each sender/receiver type pair |
| "I found something odd in the data" | Log it in the issues log, then carry on |
| "A rule is unclear in the official documents" | Check [official/README.md](official/README.md); if still unclear, ask the mentor on Discord |
