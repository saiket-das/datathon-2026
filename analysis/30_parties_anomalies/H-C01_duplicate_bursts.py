"""Test label-blind copy-burst signatures, using sender-separated partitions.

Run from the repository root:
    uv run python analysis/30_parties_anomalies/H-C01_duplicate_bursts.py --phase explore
    uv run python analysis/30_parties_anomalies/H-C01_duplicate_bursts.py --phase confirm --freeze-commit SHA
Only aggregates leave DuckDB; candidate payment tables exist in memory only.
H-C02 reuses this implementation with a different, explicit family key and rule.
"""

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys

import duckdb
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("scientific_checks", ROOT / "analysis/00_prep/scientific_checks.py")
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)
LABELS = checks.LABELS
STEMS = {"duplicate": "H-C01_duplicate_bursts", "romance": "H-C02_romance_bursts"}
TARGET = {"duplicate": "DUPLICATE_PAYMENT", "romance": "ROMANCE_SCAM"}
FIELDS = (
    "CURRENCY_CODE ORDERING_BIC8 BENEFICIARY_BIC8 BIC8_PATH TOTAL_DURATION "
    "CONTINUITY_QFLAG CURRENCY_CONVERSION_COUNT PARTICIPANT_COUNT TRANSACTION_TYPE_CODE "
    "ORDERING_DETAILS ORDERING_TOKENS BENEFICIARY_DETAILS BENEFICIARY_TOKENS "
    "ORDERING_TYPE BENEFICIARY_TYPE"
).split()


def scalar(con: duckdb.DuckDBPyConnection, sql: str) -> int:
    """Read a single count, never a source identifier."""
    return int(con.execute(sql).fetchone()[0])


def build_features(con: duckdb.DuckDBPyConnection, kind: str) -> None:
    """Screen adjacent hashes, then verify exact keys and every invariant field.

    Hash collisions only add candidate keys. Exact grouping and equality determine
    the signature. No label is used to construct the candidate population.
    """
    keys = ["ORDERING_ACCOUNT", "BENEFICIARY_ACCOUNT"]
    if kind == "duplicate":
        keys += ["CURRENCY_CODE", "USD_AMOUNT"]
    key_sql = ",".join(keys)
    con.execute(f"""CREATE TEMP TABLE candidate_hashes AS
      WITH h AS (SELECT ROW_ID,hash({key_sql}) h FROM e),
      w AS (SELECT *,lag(ROW_ID) OVER(ORDER BY ROW_ID) prev_row,
        lag(h) OVER(ORDER BY ROW_ID) prev_hash FROM h)
      SELECT DISTINCT h FROM w WHERE ROW_ID=prev_row+1 AND h=prev_hash""")
    constants = " AND ".join(f"min({x}) IS NOT DISTINCT FROM max({x})" for x in FIELDS)
    con.execute(f"""CREATE TEMP TABLE families AS
      SELECT {key_sql},count(*) family_n,min(ROW_ID) first_row,max(ROW_ID) last_row,
        max(EPOCH_SECONDS)-min(EPOCH_SECONDS) span,
        ({constants}) fixed_context,
        min(USD_AMOUNT)=max(USD_AMOUNT) fixed_amount,
        min(ORDERING_TYPE) sender_type,min(BENEFICIARY_TYPE) receiver_type,
        count(*) FILTER(WHERE ANOMALY_TYPE='{TARGET[kind]}') target_n
      FROM e WHERE hash({key_sql}) IN (SELECT h FROM candidate_hashes)
      GROUP BY {key_sql}""")
    # For romance all pair rows participate, including other currencies and labels.
    # For duplicates the exact amount/currency key deliberately separates unrelated invoices.
    con.execute(f"""CREATE TEMP TABLE members AS SELECT e.*,f.family_n,f.first_row,
      f.last_row,f.span,f.fixed_context,f.fixed_amount,f.target_n,
      EPOCH_SECONDS-lag(EPOCH_SECONDS) OVER(PARTITION BY {key_sql} ORDER BY ROW_ID) dt,
      ln(USD_AMOUNT/nullif(lag(USD_AMOUNT) OVER(PARTITION BY {key_sql} ORDER BY ROW_ID),0)) log_ratio
      FROM e JOIN families f USING({key_sql})""")
    con.execute(f"""CREATE TEMP TABLE sequence_features AS SELECT {key_sql},
      bool_and(dt>=0) monotone_time,median(log_ratio) median_log_ratio,
      avg((dt<0)::INT) backwards_share
      FROM members GROUP BY {key_sql}""")
    size_max = 5 if kind == "duplicate" else 8
    condition = (f"family_n BETWEEN 2 AND {size_max} AND last_row-first_row=family_n-1 "
                 "AND span<=7200 AND fixed_context")
    if kind == "romance":
        condition += " AND sender_type='C' AND NOT fixed_amount AND monotone_time"
    con.execute(f"""CREATE TEMP TABLE scored AS SELECT f.*,s.monotone_time,
      s.median_log_ratio,s.backwards_share,({condition}) signature
      FROM families f JOIN sequence_features s USING({key_sql})""")
    con.execute(f"""CREATE TEMP VIEW assessed AS SELECT e.ROW_ID,e.ORDERING_ACCOUNT,
      e.BENEFICIARY_ACCOUNT,e.ANOMALY_TYPE,e.ORDERING_TYPE,e.BENEFICIARY_TYPE,
      e.CURRENCY_CODE,e.ts_utc,coalesce(s.signature,false) signature
      FROM e LEFT JOIN scored s USING({key_sql})""")


def table(con: duckdb.DuckDBPyConnection, sql: str) -> tuple[list[str], list[tuple]]:
    """Fetch explicitly aggregated, non-identifying result tables only."""
    result = con.execute(sql)
    return [x[0] for x in result.description], result.fetchall()


def markdown_table(columns: list[str], rows: list[tuple]) -> str:
    """Suppress small label/stratum cohorts and mask limited entity counts."""
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        n = row[columns.index("n")] if "n" in columns else None
        cells = []
        for name, value in zip(columns, row):
            if n is not None and 0 < n < 100 and name not in ("label", "stratum", "period"):
                value = "<100" if name == "n" else "suppressed"
            elif name in ("senders", "receivers", "families", "entities") and isinstance(value, (int, float)) and 0 < value < 100:
                value = "<100"
            elif isinstance(value, float):
                value = f"{value:.6g}"
            cells.append(str(value).replace("|", "\\|").replace("\n", " "))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def entity_summary(con: duckdb.DuckDBPyConnection, kind: str) -> dict[str, float | int]:
    """Estimate sender-weighted coverage; bootstrap whole senders, never rows.

    The exact lower bound concerns the probability that a sender has no exceptions.
    It is conditional on independent sender clusters; shared receivers remain a limit.
    """
    rows = con.execute(f"""SELECT count(*) n,sum(signature::INT) hits FROM assessed
      WHERE ANOMALY_TYPE='{TARGET[kind]}' GROUP BY ORDERING_ACCOUNT""").fetchall()
    if not rows:
        raise ValueError("target absent")
    rates = np.array([hits / n for n, hits in rows])
    rng = np.random.default_rng(20261116)
    draws = np.array([rng.choice(rates, size=len(rates), replace=True).mean() for _ in range(4000)])
    successes = int(np.sum(rates == 1))
    lower = float(beta.ppf(.025, successes, len(rates)-successes+1)) if successes else 0.0
    row_rate = sum(hits for n, hits in rows) / sum(n for n, hits in rows)
    recipients = con.execute(f"""SELECT count(*) n,sum(signature::INT) hits FROM assessed
      WHERE ANOMALY_TYPE='{TARGET[kind]}' GROUP BY BENEFICIARY_ACCOUNT""").fetchall()
    return {"rows": sum(n for n, hits in rows), "senders": len(rows),
            "row_coverage": row_rate, "sender_mean_coverage": float(rates.mean()),
            "sender_bootstrap_low": float(np.quantile(draws, .025)),
            "sender_bootstrap_high": float(np.quantile(draws, .975)),
            "all_success_sender_lower_97_5": lower,
            "largest_sender_share": max(n for n, hits in rows) / sum(n for n, hits in rows),
            "receivers": len(recipients),
            "receiver_mean_coverage": float(np.mean([hits/n for n, hits in recipients])),
            "largest_receiver_share": max(n for n, hits in recipients) / sum(n for n, hits in recipients)}


def verify_freeze(sha: str) -> None:
    """Require committed scripts identical to the freeze before opening confirmation."""
    subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT, check=True,
                   capture_output=True)
    for stem in STEMS.values():
        path = f"analysis/30_parties_anomalies/{stem}.py"
        frozen = subprocess.run(["git", "show", f"{sha}:{path}"], cwd=ROOT, check=True,
                                capture_output=True).stdout.decode("utf-8")
        if frozen.splitlines() != (ROOT / path).read_text(encoding="utf-8").splitlines():
            raise ValueError("analysis differs from frozen script")


def main(kind: str = "duplicate") -> int:
    """Run one unchanged analysis for explore or confirm and save safe evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("explore", "confirm"), default="explore")
    parser.add_argument("--freeze-commit")
    args = parser.parse_args()
    con = None
    try:
        if args.phase == "confirm":
            if not args.freeze_commit:
                raise ValueError("confirmation requires a freeze commit")
            verify_freeze(args.freeze_commit)
        con = duckdb.connect()
        con.execute("SET memory_limit='2GB'; SET threads=1; SET TimeZone='UTC'; SET temp_directory=''; SET preserve_insertion_order=false")
        source = (ROOT / "dataset/payments.parquet").as_posix().replace("'", "''")
        # Only the chosen partition can supply candidate rows, labels or outcomes.
        con.execute(f"""CREATE VIEW e AS SELECT * FROM read_parquet('{source}')
          WHERE ({checks.partition_sql('sender')})='{args.phase}'""")
        print(f"Computing {kind}, {args.phase}; aggregates only.", flush=True)
        tables = {"Partition and six-label baseline": table(con, """SELECT
          coalesce(ANOMALY_TYPE,'UNLABELLED') label,count(*) n,
          count(DISTINCT ORDERING_ACCOUNT) senders,count(DISTINCT BENEFICIARY_ACCOUNT) receivers,
          median(USD_AMOUNT) amount_median,median(TOTAL_DURATION) duration_median,
          avg((ORDERING_TYPE='B')::INT) business_sender_share,
          avg((BENEFICIARY_TYPE='B')::INT) business_receiver_share
          FROM e GROUP BY 1 ORDER BY 1""")}
        repeat_keys = "ORDERING_ACCOUNT,BENEFICIARY_ACCOUNT"
        if kind == "duplicate":
            repeat_keys += ",CURRENCY_CODE,USD_AMOUNT"
        tables["Broad repeat comparator without source-order or context conditions"] = table(con, f"""
          WITH r AS (SELECT ANOMALY_TYPE,ORDERING_TYPE,BENEFICIARY_TYPE,
            count(*) OVER(PARTITION BY {repeat_keys}) repeat_n FROM e)
          SELECT coalesce(ANOMALY_TYPE,'UNLABELLED') label,count(*) n,
            sum((repeat_n>1)::INT) repeated_rows,avg((repeat_n>1)::INT) repeat_share,
            median(repeat_n) median_family_size
          FROM r GROUP BY 1 ORDER BY 1""")
        build_features(con, kind)
        target = TARGET[kind]
        tables["Signature against every label (not a legitimacy classifier)"] = table(con, """SELECT
          coalesce(ANOMALY_TYPE,'UNLABELLED') label,count(*) n,sum(signature::INT) hits,
          avg(signature::INT) coverage,count(DISTINCT ORDERING_ACCOUNT) senders,
          count(DISTINCT BENEFICIARY_ACCOUNT) receivers FROM assessed GROUP BY 1 ORDER BY 1""")
        tables["Candidate-family structure; target label used only for assessment"] = table(con, """SELECT
          CASE WHEN target_n>0 THEN 'target-containing' ELSE 'other' END label,
          sum(family_n) n,count(*) families,sum(target_n) target_rows,
          coalesce(sum(family_n) FILTER(WHERE signature),0) signature_rows,
          avg((target_n=family_n)::INT) fully_labelled_family_share,
          min(family_n) smallest_family,max(family_n) largest_family,
          median(span) median_span,max(span) max_span,
          avg(fixed_context::INT) fixed_context_share,avg(monotone_time::INT) monotone_share,
          exp(median(median_log_ratio)) median_family_growth,
          avg(backwards_share) mean_family_backwards_share
          FROM scored GROUP BY 1 ORDER BY 1""")
        # Descriptive controls only: no threshold changes or extra success tests.
        for title, dimension in (("Party-pair control", "ORDERING_TYPE||BENEFICIARY_TYPE"),
                                 ("Calendar sensitivity within the same sender split", "strftime(ts_utc,'%Y-%m')"),
                                 ("Source-file block sensitivity (zero-based million-row blocks)", "((ROW_ID-1)//1000000)::VARCHAR")):
            tables[title] = table(con, f"""SELECT {dimension} stratum,
              CASE WHEN ANOMALY_TYPE='{target}' THEN 'target' WHEN ANOMALY_TYPE IS NULL
                THEN 'UNLABELLED' ELSE 'other-label' END label,count(*) n,
              avg(signature::INT) coverage,count(DISTINCT ORDERING_ACCOUNT) senders
              FROM assessed GROUP BY 1,2 ORDER BY 1,2""")
        summary = entity_summary(con, kind)
        unlabelled_n = scalar(con, "SELECT count(*) FROM assessed WHERE ANOMALY_TYPE IS NULL")
        unlabelled_hits = scalar(con, "SELECT count(*) FROM assessed WHERE ANOMALY_TYPE IS NULL AND signature")
        false_share = unlabelled_hits / unlabelled_n
        passed = (summary["row_coverage"] >= .95 and summary["sender_mean_coverage"] >= .95
                  and summary["all_success_sender_lower_97_5"] >= .90 and false_share <= .001)
        parts = [f"# {STEMS[kind]}: {args.phase}", "",
                 f"DuckDB {duckdb.__version__}; 2GB; one thread; UTC; no disk spill.",
                 f"Freeze: `{args.freeze_commit or 'not yet frozen; discovery only'}`.",
                 "Sender MD5 parity split; whole sender clusters retained. Phase 0 full-data exposure applies.",
                 "No bank/time repartition is an independent holdout. Unlabelled does not mean legitimate.",
                 "Cohorts below 100 rows are suppressed; entity counts below 100 are masked."]
        for title, data in tables.items():
            parts += ["", "## " + title, "", markdown_table(*data)]
        parts += ["", "## Predeclared coverage decision and uncertainty", "",
                  markdown_table(list(summary), [tuple(summary.values())]), "",
                  f"Unlabelled signature share: {false_share:.8f}. Decision: {'PASS' if passed else 'FAIL'}.",
                  "Joint acceptance: row and equal-sender coverage >=95%; exact one-sided 97.5% lower bound",
                  "for an all-success sender >=90%; unlabelled signature share <=0.1%.",
                  "Two co-primary signatures use Bonferroni allocation (0.025 each) for the sender bound.",
                  "Bootstrap intervals are descriptive; all-success samples yield degenerate intervals.",
                  "Shared receivers/banks/text prevent a claim of globally independent entity replication."]
        out = HERE / "out" / f"{STEMS[kind]}_{args.phase}.md"
        out.write_text("\n".join(parts)+"\n", encoding="utf-8")
        plot(tables["Signature against every label (not a legitimacy classifier)"], kind, args.phase)
        print(f"OK: {out.relative_to(ROOT)}; decision {'PASS' if passed else 'FAIL'}.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; details hidden to protect sponsor values.", file=sys.stderr)
        return 1
    finally:
        if con is not None:
            con.close()


def plot(data: tuple[list[str], list[tuple]], kind: str, phase: str) -> None:
    """Draw cohort-level signature coverage with denominators and a full 0-100% axis."""
    columns, rows = data
    safe = [dict(zip(columns, row)) for row in rows if row[columns.index("n")] >= 100]
    labels = [str(x["label"]).replace("_", " ")+f" (n={x['n']:,})" for x in safe]
    values = [100*float(x["coverage"]) for x in safe]
    fig, ax = plt.subplots(figsize=(10, 5.2), layout="constrained")
    colors = ["#116466" if x["label"] == TARGET[kind] else "#a8b4c0" for x in safe]
    ax.barh(labels, values, color=colors)
    ax.set_xlim(0, 108)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("Payments matching the frozen signature (%)")
    for i, value in enumerate(values):
        ax.text(value+1, i, f"{value:.2f}%", va="center", fontsize=9)
    ax.set_title(f"{TARGET[kind].replace('_', ' ').title()}: copy-burst coverage\n{phase}; sender-separated, source-order signature", loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(HERE / "out" / f"{STEMS[kind]}_{phase}.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    sys.exit(main())
