"""Test conditional amount distributions using safe aggregates and account separation.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A01_amount_kernel.py
Discovery queries use only the both-account exploration partition.
"""

from pathlib import Path
import argparse
import math
import subprocess
import sys

import duckdb

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis/00_prep"))
from scientific_checks import partition_sql, query  # noqa: E402


def render(tables: dict, title: str, command: str) -> str:
    """Render preaggregated, support-filtered tables without treating flags as counts."""
    lines = [f"# {title}", "", f"Run: `{command}`", "",
             f"DuckDB {duckdb.__version__}; 2GB; two threads; no spill.",
             "Both-account exploration only. Unlabelled does not imply legitimate."]
    for heading, (columns, rows) in tables.items():
        lines += ["", f"## {heading}", "", "| " + " | ".join(columns) + " |",
                  "| " + " | ".join("---" for _ in columns) + " |"]
        for row in rows:
            lines.append("| " + " | ".join(str(v).replace("|", "\\|") for v in row) + " |")
    return "\n".join(lines) + "\n"


def freeze_guard(sha: str | None) -> str:
    """Require a real committed plan and identical scripts before confirmation."""
    if not sha:
        raise ValueError("confirmation requires --freeze")
    commit = subprocess.check_output(["git", "rev-parse", "--verify", sha + "^{commit}"],
                                     cwd=ROOT, text=True).strip()
    paths = [str(p.relative_to(ROOT)).replace("\\", "/")
             for p in Path(__file__).parent.glob("H-A*.py")]
    subprocess.run(["git", "diff", "--exit-code", commit, "--", *paths],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    for stem in ("H-A01_amount_kernel", "H-A02_usd_rounding"):
        subprocess.run(["git", "cat-file", "-e", f"{commit}:findings/hypotheses/{stem}.md"],
                       cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    return commit


def contrasts(con: duckdb.DuckDBPyConnection, where: str = "TRUE", corridor: bool = False) -> tuple:
    """Equal-account log contrasts, holding the account and currency fixed."""
    rows = []
    strata = "currency||':'||ord_country||':'||ben_country" if corridor else "currency"
    for account, position, name in (("sender", 2, "beneficiary business"),
                                    ("receiver", 1, "ordering business")):
        con.execute(f"""CREATE OR REPLACE TEMP TABLE contrasts AS
          WITH s AS (SELECT {account} entity,{strata} stratum,
            avg(ln(a)) FILTER(WHERE pair[{position}]='B') yb,
            avg(ln(a)) FILTER(WHERE pair[{position}]='C') yc,
            count(*) n FROM e WHERE NOT labelled AND a>0 AND ({where}) GROUP BY 1,2),
          matched AS (SELECT * FROM s WHERE yb IS NOT NULL AND yc IS NOT NULL)
          SELECT entity,avg(yb-yc) d,sum(n) matched_payments,count(*) matched_currencies,
            sum(n*(yb-yc)) transaction_logsum
          FROM matched GROUP BY 1""")
        result = con.execute("""SELECT count(*),sum(matched_payments),avg(d),
          stddev_samp(d)/sqrt(count(*)),median(d),avg((d<0)::INT),
          avg((abs(d-2)>1)::INT),sum(transaction_logsum)/sum(matched_payments)
          FROM contrasts""").fetchone()
        n, covered, mean, se, median, reversed_share, heterogeneous, transaction_mean = result
        assert n >= 100 and mean is not None and se > 0
        low, high = mean - 2.241403 * se, mean + 2.241403 * se
        rows.append((name,n,int(covered),mean,se,low,high,math.exp(mean),median,
                     reversed_share,heterogeneous,low>=1.85 and high<=2.15,transaction_mean))
    return (["contrast","accounts","matched_payments","mean_log_difference","account_SE",
             "97.5%_low","97.5%_high","geometric_ratio","median_log_difference",
             "negative_account_share","abs_difference_from_2_gt_1_share","passes_equivalence",
             "matched_transaction_weighted_log_difference"],rows)


def confirm_tables(con: duckdb.DuckDBPyConnection) -> dict:
    """Run the frozen primary contrasts and separately declared sensitivity checks."""
    tables = {"Primary equal-account contrasts": contrasts(con)}
    tables["Sensitivity: also hold endpoint-bank country corridor fixed"] = contrasts(con, corridor=True)
    con.execute("""CREATE TEMP TABLE hubs AS SELECT sender FROM e WHERE NOT labelled
      GROUP BY 1 QUALIFY row_number() OVER(ORDER BY count(*) DESC,sender)
        <=ceil(count(*) OVER()*0.01)""")
    tables["Sensitivity: omit busiest 1% of sending accounts"] = contrasts(
        con, "sender NOT IN (SELECT sender FROM hubs)")
    for month in (5,6,7):
        tables[f"Sensitivity: month {month} within the same account partition"] = contrasts(
            con, f"month(ts_utc)={month}")
    for route in ("Direct", "Indirect", "Covered"):
        tables[f"Sensitivity: {route} within the same account partition"] = contrasts(
            con, f"route='{route}'")
    return tables


def plot_contrasts(table: tuple, destination: Path, phase: str) -> None:
    """Plot aggregate effects and the frozen equivalence band."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8,4.6), layout="constrained")
    rows = table[1]
    ax.axvspan(1.85,2.15,color="#e2efea",label="Frozen practical band: 1.85 to 2.15")
    ax.axvline(2,color="#40685a",linestyle="--",linewidth=1)
    for i, row in enumerate(rows):
        ax.errorbar(row[3],i,xerr=2.241403*row[4],fmt="o",color="#195f78",capsize=5)
        ax.annotate(f" {row[3]:.3f}; {row[7]:.2f}x; {row[1]:,} accounts",(row[3],i),
                    xytext=(8,12),textcoords="offset points",fontsize=10)
    ax.set(yticks=[0,1],yticklabels=["Business beneficiary\nsame sender + currency",
        "Business ordering party\nsame receiver + currency"],xlim=(1.7,2.35),ylim=(-.6,1.6),
        xlabel="Equal-account mean difference in ln(USD amount)",
        title=f"Each business party corresponds to roughly a sevenfold amount scale\n{phase}: unlabelled, both-account partition")
    ax.spines[["top","right"]].set_visible(False)
    ax.legend(loc="upper right",fontsize=8)
    fig.savefig(destination,dpi=180)
    plt.close(fig)


def main() -> int:
    """Measure exploration amounts, publishing no identifiers or small cells."""
    con = duckdb.connect()
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--phase", choices=["explore", "confirm"], default="explore")
        parser.add_argument("--freeze")
        args = parser.parse_args()
        freeze = freeze_guard(args.freeze) if args.phase == "confirm" else "not frozen"
        con.execute("SET memory_limit='2GB'; SET threads=2; SET temp_directory=''")
        con.execute("CREATE VIEW t AS SELECT * FROM 'dataset/payments.parquet'")
        con.execute(f"""CREATE TEMP TABLE e AS SELECT USD_AMOUNT a, CURRENCY_CODE currency,
          ORDERING_TYPE||BENEFICIARY_TYPE pair, ORDERING_ACCOUNT sender,
          BENEFICIARY_ACCOUNT receiver, ANOMALY_TYPE IS NOT NULL labelled,
          ord_country, ben_country, TRANSACTION_TYPE_CODE route,
          CURRENCY_CONVERSION_COUNT fx, ts_utc
          FROM t WHERE {partition_sql('accounts')}='{args.phase}'""")
        tables = {}
        tables["Exploration support"] = query(con, """SELECT labelled,count(*) n,
          count(DISTINCT sender) senders,count(DISTINCT receiver) receivers,
          count(*) FILTER(WHERE a<=0) nonpositive FROM e GROUP BY 1""")
        if args.phase == "confirm":
            tables.update(confirm_tables(con))
            out = Path(__file__).parent / "out/H-A01_amount_kernel_confirm.md"
            report = render(tables, "H-A01: frozen confirmation and sensitivity",
                f"uv run python analysis/10_amounts_currency/H-A01_amount_kernel.py --phase confirm --freeze {freeze}")
            report = report.replace("Both-account exploration only.", "Both-account confirmation only.")
            report += ("\nIntervals describe account-to-account variation under account independence; "
                       "shared counterparties and banks can induce remaining dependence. "
                       "97.5% intervals apply a Bonferroni correction to two primary contrasts.\n")
            out.write_text(report, encoding="utf-8")
            plot_contrasts(tables["Primary equal-account contrasts"],
                          out.with_suffix(".png"), "Confirmation")
            print("OK: frozen confirmation and chart written.")
            return 0
        tables["Party-pair distribution (unlabelled)"] = query(con, """
          SELECT pair,count(*) n,count(DISTINCT sender) senders,
            count(DISTINCT receiver) receivers,
            quantile_cont(a,[0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99]) quantiles,
            avg(ln(a)) logmean,stddev_pop(ln(a)) logsd,
            avg((abs(a-round(a))<0.000001)::INT) integer_share,
            avg((abs(a/100-round(a/100))<0.00000001)::INT) hundred_share
          FROM e WHERE NOT labelled AND a>0 GROUP BY 1 ORDER BY 1""")
        tables["Currency and pair (unlabelled; at least 100 of each entity)"] = query(con, """
          SELECT currency,pair,count(*) n,count(DISTINCT sender) senders,
            count(DISTINCT receiver) receivers,median(a) med,
            avg(ln(a)) logmean,stddev_pop(ln(a)) logsd,
            avg((abs(a-round(a))<0.000001)::INT) integer_share
          FROM e WHERE NOT labelled AND a>0 GROUP BY 1,2
          HAVING count(*)>=1000 AND count(DISTINCT sender)>=100
            AND count(DISTINCT receiver)>=100 ORDER BY n DESC""")
        tables["Repeated amount masses (not individual values; >=100 entities)"] = query(con, """
          SELECT a amount,count(*) n,count(DISTINCT sender) senders,
            count(DISTINCT receiver) receivers
          FROM e WHERE NOT labelled GROUP BY 1 HAVING count(*)>=1000
            AND count(DISTINCT sender)>=100 AND count(DISTINCT receiver)>=100
          ORDER BY n DESC""")
        tables["Within sender/currency: beneficiary business contrast"] = query(con, """
          WITH s AS (SELECT sender,currency,
            avg(ln(a)) FILTER(WHERE pair[2]='B') yb,
            avg(ln(a)) FILTER(WHERE pair[2]='C') yc
            FROM e WHERE NOT labelled GROUP BY 1,2), d AS (
            SELECT sender,avg(yb-yc) d FROM s WHERE yb IS NOT NULL AND yc IS NOT NULL GROUP BY 1)
          SELECT count(*) senders,avg(d) log_difference,stddev_samp(d)/sqrt(count(*)) se,
            median(d) median_difference FROM d""")
        tables["Within receiver/currency: ordering business contrast"] = query(con, """
          WITH s AS (SELECT receiver,currency,
            avg(ln(a)) FILTER(WHERE pair[1]='B') yb,
            avg(ln(a)) FILTER(WHERE pair[1]='C') yc
            FROM e WHERE NOT labelled GROUP BY 1,2), d AS (
            SELECT receiver,avg(yb-yc) d FROM s WHERE yb IS NOT NULL AND yc IS NOT NULL GROUP BY 1)
          SELECT count(*) receivers,avg(d) log_difference,stddev_samp(d)/sqrt(count(*)) se,
            median(d) median_difference FROM d""")
        tables.update(confirm_tables(con))
        out = Path(__file__).parent / "out/H-A01_amount_kernel_explore.md"
        report = render(tables, "H-A01: exploration amount distributions",
                        "uv run python analysis/10_amounts_currency/H-A01_amount_kernel.py")
        out.write_text(report, encoding="utf-8")
        print("OK: exploration aggregate report written.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source details suppressed.", file=sys.stderr)
        return 1
    finally:
        con.close()


if __name__ == "__main__":
    sys.exit(main())
