"""Test currency-specific amount quantisation, not real-world exchange rates.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A02_usd_rounding.py
Only both-account exploration data are inspected before freezing confirmation.
"""

import importlib.util
import argparse
from pathlib import Path
import sys

import duckdb

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("amount_kernel", HERE / "H-A01_amount_kernel.py")
kernel = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kernel)


def lattice_tables(con: duckdb.DuckDBPyConnection, phase: str) -> dict:
    """Evaluate fixed, exploration-learned rates outside the training amount windows."""
    con.execute(f"""CREATE TEMP TABLE lattice AS
      WITH rates AS (SELECT *,lead(rate,7) OVER(ORDER BY obs_date) wrong_rate,
        median(rate) OVER() constant_rate FROM eur_modes), s AS (
        SELECT USD_AMOUNT a,r.*,ORDERING_ACCOUNT sender,BENEFICIARY_ACCOUNT receiver,
          ORDERING_TYPE||BENEFICIARY_TYPE pair,TRANSACTION_TYPE_CODE route
        FROM t JOIN rates r ON cast(ts_utc AS DATE)=obs_date
        WHERE {kernel.partition_sql('accounts')}='{phase}' AND ANOMALY_TYPE IS NULL
          AND CURRENCY_CODE='EUR' AND USD_AMOUNT BETWEEN 10 AND 90000
          AND NOT (USD_AMOUNT BETWEEN 900 AND 1500 OR USD_AMOUNT BETWEEN 9000 AND 15000)
          AND wrong_rate IS NOT NULL)
      SELECT *, (abs(a-rate*round(a/rate))<=0.005+0.005*a/rate/base+1e-8)::INT grid,
        (abs(a-wrong_rate*round(a/wrong_rate))<=0.005+0.005*a/wrong_rate/base+1e-8)::INT wrong_grid,
        (abs(a-constant_rate*round(a/constant_rate))<=0.005+0.005*a/constant_rate/base+1e-8)::INT constant_grid
      FROM s""")
    tables = {}
    tables["Primary off-anchor EUR coverage and row-weighted fit"] = kernel.query(con, """
      SELECT count(*) n,count(DISTINCT sender) senders,count(DISTINCT receiver) receivers,
        count(DISTINCT obs_date) dates,sum(grid) grid_payments,sum(1-grid) off_grid_payments,
        avg(grid) daily_grid,avg(wrong_grid) wrong_day_grid,avg(constant_grid) constant_grid,
        avg(grid-wrong_grid) excess_grid,
        avg(grid)>=0.30 AND avg(grid-wrong_grid)>=0.20 passes_row_threshold
      FROM lattice""")
    rows = []
    for account in ("sender", "receiver"):
        values = con.execute(f"""WITH a AS (SELECT {account},avg(grid) g,
          avg(wrong_grid) w,avg(constant_grid) c,avg(grid-wrong_grid) d
          FROM lattice GROUP BY 1) SELECT count(*),avg(g),avg(w),avg(c),avg(d),
          stddev_samp(d)/sqrt(count(*)) FROM a""").fetchone()
        n,g,w,c,d,se = values
        assert n>=100 and 0<=g<=1 and se>0
        low,high = d-2.241403*se,d+2.241403*se
        rows.append((account,n,g,w,c,d,se,low,high,low>=0.20))
    tables["Primary equal-account fit and excess"] = (["weighting","accounts","daily_grid",
        "wrong_day_grid","constant_grid","excess","account_SE","97.5%_low",
        "97.5%_high","passes_excess"],rows)
    for dimension in ("pair", "route", "month(obs_date)"):
        tables[f"Sensitivity by {dimension}"] = kernel.query(con, f"""
          SELECT {dimension} category,count(*) n,count(DISTINCT sender) senders,
            count(DISTINCT receiver) receivers,avg(grid) daily_grid,
            avg(wrong_grid) wrong_day_grid,avg(grid-wrong_grid) excess_grid
          FROM lattice GROUP BY 1 HAVING count(*)>=100 AND count(DISTINCT sender)>=100
            AND count(DISTINCT receiver)>=100 ORDER BY 1""")
    tables["USD whole-unit benchmark in identical amount windows"] = kernel.query(con, f"""
      SELECT count(*) n,count(DISTINCT ORDERING_ACCOUNT) senders,
        count(DISTINCT BENEFICIARY_ACCOUNT) receivers,
        avg((abs(USD_AMOUNT-round(USD_AMOUNT))<1e-7)::INT) integer_share
      FROM t WHERE {kernel.partition_sql('accounts')}='{phase}' AND ANOMALY_TYPE IS NULL
        AND CURRENCY_CODE='USD' AND USD_AMOUNT BETWEEN 10 AND 90000
        AND NOT (USD_AMOUNT BETWEEN 900 AND 1500 OR USD_AMOUNT BETWEEN 9000 AND 15000)
        AND cast(ts_utc AS DATE) IN (SELECT DISTINCT obs_date FROM lattice)""")
    return tables


def plot_lattice(table: tuple, destination: Path, phase: str) -> None:
    """Display only the three aggregate test proportions, including negative controls."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    row = table[1][0]
    fig,ax = plt.subplots(figsize=(7.6,4.8),layout="constrained")
    values = [100*row[6],100*row[7],100*row[8]]
    bars = ax.bar(["Same-day rate", "Rate seven dates later", "Constant median rate"],
                  values,color=["#195f78","#b5bfc2","#b5bfc2"],width=.6)
    ax.bar_label(bars,labels=[f"{v:.2f}%" for v in values],padding=5)
    ax.set(ylim=(0,45),ylabel="EUR payments consistent with a converted whole-unit amount (%)",
        title=f"Daily EUR scaling recovers hidden amount rounding\n{phase}: {row[0]:,} off-anchor payments; rates learned on exploration accounts")
    ax.spines[["top","right"]].set_visible(False)
    fig.savefig(destination,dpi=180)
    plt.close(fig)


def main() -> int:
    """Measure rounding grids with broad support and no identifier output."""
    con = duckdb.connect()
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--phase", choices=["explore", "confirm"], default="explore")
        parser.add_argument("--freeze")
        args = parser.parse_args()
        freeze = kernel.freeze_guard(args.freeze) if args.phase == "confirm" else "not frozen"
        con.execute("SET memory_limit='2GB'; SET threads=2; SET temp_directory=''")
        con.execute("CREATE VIEW t AS SELECT * FROM 'dataset/payments.parquet'")
        con.execute(f"""CREATE TEMP TABLE e AS SELECT USD_AMOUNT a,CURRENCY_CODE currency,
          ORDERING_TYPE||BENEFICIARY_TYPE pair,ORDERING_ACCOUNT sender,
          BENEFICIARY_ACCOUNT receiver,ANOMALY_TYPE IS NOT NULL labelled,
          floor(log10(USD_AMOUNT)) magnitude FROM t
          WHERE {kernel.partition_sql('accounts')}='{args.phase}' AND USD_AMOUNT>0""")
        tables = {}
        tables["Rounding by currency and magnitude (unlabelled)"] = kernel.query(con, """
          SELECT CASE WHEN currency='USD' THEN 'USD' ELSE 'non-USD' END currency_group,
            magnitude,count(*) n,count(DISTINCT sender) senders,
            count(DISTINCT receiver) receivers,
            avg((abs(a-round(a))<1e-7)::INT) integer_share,
            avg((abs(a/pow(10,magnitude)-round(a/pow(10,magnitude)))<1e-9)::INT) one_sig,
            avg((abs(a/pow(10,magnitude-1)-round(a/pow(10,magnitude-1)))<1e-8)::INT) two_sig,
            avg((abs(a/pow(10,magnitude-2)-round(a/pow(10,magnitude-2)))<1e-7)::INT) three_sig
          FROM e WHERE NOT labelled GROUP BY 1,2 HAVING count(*)>=1000
            AND count(DISTINCT sender)>=100 AND count(DISTINCT receiver)>=100
          ORDER BY 1,2""")
        tables["Whole amounts by party pair and label flag"] = kernel.query(con, """
          SELECT CASE WHEN currency='USD' THEN 'USD' ELSE 'non-USD' END currency_group,
            pair,labelled,count(*) n,count(DISTINCT sender) senders,
            count(DISTINCT receiver) receivers,
            avg((abs(a-round(a))<1e-7)::INT) integer_share
          FROM e GROUP BY 1,2,3 HAVING count(*)>=100 AND count(DISTINCT sender)>=100
            AND count(DISTINCT receiver)>=100 ORDER BY 1,2,3""")
        tables["Repeated currency amount masses (>=100 of each entity)"] = kernel.query(con, """
          SELECT currency,a amount,count(*) n,count(DISTINCT sender) senders,
            count(DISTINCT receiver) receivers FROM e WHERE NOT labelled
          GROUP BY 1,2 HAVING count(*)>=300 AND count(DISTINCT sender)>=100
            AND count(DISTINCT receiver)>=100 ORDER BY n DESC""")
        con.execute(f"""CREATE TEMP TABLE eur_modes AS
          WITH masses AS (SELECT cast(ts_utc AS DATE) obs_date,USD_AMOUNT a,
              pow(10,floor(log10(USD_AMOUNT))) base,count(*) n
            FROM t WHERE {kernel.partition_sql('accounts')}='explore'
              AND ANOMALY_TYPE IS NULL AND CURRENCY_CODE='EUR'
              AND USD_AMOUNT>=1000 AND USD_AMOUNT<2000000
              AND USD_AMOUNT/pow(10,floor(log10(USD_AMOUNT))) BETWEEN 1.08 AND 1.25
            GROUP BY 1,2,3), ranked AS (
            SELECT *,row_number() OVER(PARTITION BY obs_date,base ORDER BY n DESC,a) rank
            FROM masses), selected AS (
            SELECT *,row_number() OVER(PARTITION BY obs_date ORDER BY base DESC) choice
            FROM ranked WHERE rank=1 AND n>=20)
          SELECT obs_date,a/base rate,base,n FROM selected WHERE choice=1""")
        tables["EUR daily modal anchor: aggregate support only"] = kernel.query(con, """
          SELECT count(*) dates,sum(n) anchor_payments,min(rate) min_rate,max(rate) max_rate,
            stddev_pop(rate) rate_sd FROM eur_modes""")
        tables["EUR full-range grid diagnostic (exploration only)"] = kernel.query(con, f"""
          WITH s AS (SELECT USD_AMOUNT a,r.rate,ORDERING_ACCOUNT sender,
            BENEFICIARY_ACCOUNT receiver,r.base FROM t JOIN eur_modes r ON cast(ts_utc AS DATE)=obs_date
            WHERE {kernel.partition_sql('accounts')}='explore'
              AND ANOMALY_TYPE IS NULL AND CURRENCY_CODE='EUR')
          SELECT count(*) n,count(DISTINCT sender) senders,count(DISTINCT receiver) receivers,
            avg((abs(a-rate*round(a/rate))<=0.005+0.005*a/rate/base+1e-8)::INT) unit_grid,
            avg((abs(a/rate/100-round(a/rate/100))<=0.006/rate/100)::INT) hundred_grid,
            avg((abs(a/rate/1000-round(a/rate/1000))<=0.006/rate/1000)::INT) thousand_grid
          FROM s""")
        tables["EUR off-anchor daily grid versus mismatched day and constant rate"] = kernel.query(con, f"""
          WITH rates AS (SELECT *,lead(rate,7) OVER(ORDER BY obs_date) wrong_rate,
              median(rate) OVER() constant_rate FROM eur_modes), s AS (
            SELECT USD_AMOUNT a,r.*,ORDERING_ACCOUNT sender,BENEFICIARY_ACCOUNT receiver
            FROM t JOIN rates r ON cast(ts_utc AS DATE)=obs_date
            WHERE {kernel.partition_sql('accounts')}='explore' AND ANOMALY_TYPE IS NULL
              AND CURRENCY_CODE='EUR' AND USD_AMOUNT BETWEEN 10 AND 90000
              AND NOT (USD_AMOUNT BETWEEN 900 AND 1500 OR USD_AMOUNT BETWEEN 9000 AND 15000)
              AND wrong_rate IS NOT NULL)
          SELECT count(*) n,count(DISTINCT sender) senders,count(DISTINCT receiver) receivers,
            avg((abs(a-rate*round(a/rate))<=0.005+0.005*a/rate/base+1e-8)::INT) daily_grid,
            avg((abs(a-wrong_rate*round(a/wrong_rate))<=0.005+0.005*a/wrong_rate/base+1e-8)::INT) wrong_day_grid,
            avg((abs(a-constant_rate*round(a/constant_rate))<=0.005+0.005*a/constant_rate/base+1e-8)::INT) constant_grid
          FROM s""")
        # Exploration diagnostics above always read bit-zero accounts; primary tables
        # below use the requested partition and never refit rates on confirmation.
        primary = lattice_tables(con,args.phase)
        if args.phase == "confirm":
            tables = {"Exploration-trained rate support": tables["EUR daily modal anchor: aggregate support only"]}
        tables.update(primary)
        out = HERE / f"out/H-A02_usd_rounding_{args.phase}.md"
        command = "uv run python analysis/10_amounts_currency/H-A02_usd_rounding.py"
        if args.phase == "confirm":
            command += f" --phase confirm --freeze {freeze}"
        report = kernel.render(tables,f"H-A02: {args.phase} rounding and EUR scaling",command)
        if args.phase == "confirm":
            report = report.replace("Both-account exploration only.",
                "Both-account confirmation; EUR rates fitted only to exploration.")
        report += ("\nAccount intervals assume independence of the account summaries; shared banks, "
                   "counterparties and dates limit that interpretation. Negative controls use "
                   "the same observation-specific rounding tolerance as the daily-rate rule.\n")
        out.write_text(report,encoding="utf-8")
        plot_lattice(primary["Primary off-anchor EUR coverage and row-weighted fit"],
                     out.with_suffix(".png"),args.phase.capitalize())
        print("OK: rounding exploration aggregate report written.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source details suppressed.", file=sys.stderr)
        return 1
    finally:
        con.close()


if __name__ == "__main__":
    sys.exit(main())
