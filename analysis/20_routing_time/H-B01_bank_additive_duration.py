"""Test whether Direct-route bank effects predict longer-route durations.

Run from the repository root:
  uv run python analysis/20_routing_time/H-B01_bank_additive_duration.py --phase explore
  uv run python analysis/20_routing_time/H-B01_bank_additive_duration.py --phase confirm --freeze <SHA>
Reads dataset/payments.parquet only; exports aggregate Markdown and a PNG.
Bank effects and all row-level predictions remain in memory, never printed or saved.
"""

import sys

import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import lsqr

from routing_common import (OUT, arguments, cluster_draws, connect, interval, overlaps,
                            remember_exploration, report, selected, table)

STEM = "H-B01_bank_additive_duration"


def fit_effects(pairs: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray, int]:
    """Weighted least squares on pair sufficient statistics, scaled for convergence.

    Columns: first bank index, last bank index, count, sum(duration).
    These are statistical effects; negative coefficients forbid a literal service-time reading.
    """
    n = len(pairs)
    idx = pairs[:, :2].astype(int).ravel()
    weights = np.repeat(np.sqrt(pairs[:, 2]), 2)
    x = coo_matrix((weights, (np.repeat(np.arange(n), 2), idx)), shape=(n, k)).tocsr()
    exposure = np.bincount(idx, weights=np.repeat(pairs[:, 2], 2), minlength=k)
    scale = np.sqrt(np.maximum(exposure, 1))
    fit = lsqr(x @ diags(1 / scale), pairs[:, 3] / np.sqrt(pairs[:, 2]),
               atol=1e-10, btol=1e-10, iter_lim=2000)
    if fit[1] not in (1, 2, 4, 5) or not np.all(np.isfinite(fit[0])):
        raise ValueError("bank-effect solver did not converge")
    return fit[0] / scale, exposure, int(fit[2])


def train(con: duckdb.DuckDBPyConnection) -> tuple[list[str], list[tuple]]:
    """Fit only unlabelled Direct exploration payments; learn a route/count baseline separately."""
    selected(con, "explore")
    remember_exploration(con)
    con.execute("""CREATE TEMP TABLE banks AS SELECT b, dense_rank() OVER(ORDER BY b)-1 i
      FROM (SELECT unnest(list_filter(path,lambda x:x<>'...')) b
            FROM sample WHERE NOT labelled AND v=2) GROUP BY b""")
    pairs = np.asarray(con.execute("""SELECT a.i,b.i,count(*) n,sum(d) sy
      FROM sample JOIN banks a ON path[1]=a.b JOIN banks b ON path[-1]=b.b
      WHERE NOT labelled AND v=2 GROUP BY 1,2 ORDER BY 1,2""").fetchall(), dtype=float)
    k = con.execute("SELECT count(*) FROM banks").fetchone()[0]
    coef, exposure, iterations = fit_effects(pairs, k)
    con.execute("CREATE TEMP TABLE fitted(i BIGINT, effect DOUBLE, support DOUBLE)")
    con.executemany("INSERT INTO fitted VALUES (?,?,?)",
                    [(i, float(a), float(b)) for i, (a, b) in enumerate(zip(coef, exposure))])
    con.execute("CREATE TEMP TABLE model AS SELECT b,effect,support FROM banks JOIN fitted USING(i)")
    con.execute("""CREATE TEMP TABLE baseline AS SELECT route,v,avg(d) base
      FROM sample WHERE NOT labelled GROUP BY 1,2""")
    return ["training_rows", "model_banks", "banks_support_ge100", "negative_effects_support_ge100", "iterations"], [
        (int(pairs[:, 2].sum()), k, int((exposure >= 100).sum()),
         int(((coef < 0) & (exposure >= 100)).sum()), iterations)]


def predict(con: duckdb.DuckDBPyConnection) -> None:
    """Require every visible bank to have >=100 Direct training appearances."""
    con.execute("""CREATE OR REPLACE TEMP TABLE predicted AS
      WITH p AS (SELECT ROW_ID,sum(effect) pred,
        count(*) FILTER(WHERE support>=100)=count(*) eligible
        FROM sample,unnest(list_filter(path,lambda x:x<>'...')) t(bank)
        LEFT JOIN model ON bank=b GROUP BY ROW_ID)
      SELECT s.*,pred,eligible,coalesce(base,(SELECT avg(base) FROM baseline)) base
      FROM sample s JOIN p USING(ROW_ID) LEFT JOIN baseline USING(route,v)""")


def metrics(con: duckdb.DuckDBPyConnection, where: str, dimension: str = "'all'") -> tuple[list[str], list[tuple]]:
    """Compute only grouped errors and entity support, never individual predictions."""
    return table(con, f"""SELECT {dimension} AS \"group\",count(*) n,
      count(DISTINCT oa) senders,count(DISTINCT ba) receivers,count(DISTINCT ob) banks,
      1-sum((d-pred)^2)/nullif(sum(d*d)-sum(d)^2/count(*),0) r2,
      sqrt(avg((d-pred)^2)) rmse,avg(abs(d-pred)) mae,avg(pred-d) bias,
      sum((d-pred)^2)/nullif(sum((d-base)^2),0) mse_ratio_to_route_count
      FROM predicted WHERE {where} GROUP BY 1 ORDER BY 1""")


def analyse(con: duckdb.DuckDBPyConnection, phase: str, freeze: str | None, training: tuple) -> None:
    """Identical primary test in explore/confirm; discovery Direct fit is labelled in-sample."""
    predict(con)
    primary = "eligible AND NOT labelled AND v>2"
    tables = {"Exploration-only training": training}
    tables["Coverage and support (no identifiers)"] = table(con, """SELECT route AS \"group\",
      count(*) n,count(*) FILTER(WHERE eligible) eligible_n,
      avg(eligible::INT) eligible_share,count(DISTINCT oa) senders,
      count(DISTINCT ba) receivers,count(DISTINCT ob) banks,
      max(bank_n)::DOUBLE/count(*) largest_bank_share
      FROM (SELECT *,count(*) OVER(PARTITION BY route,ob) bank_n FROM predicted WHERE NOT labelled)
      GROUP BY 1 ORDER BY 1""")
    tables["Primary: unlabelled eligible non-Direct"] = metrics(con, primary)
    tables["Route comparison (Direct exploration is in-sample)"] = metrics(con, "eligible AND NOT labelled", "route")
    stats = np.asarray(con.execute(f"""SELECT count(*) n,sum((d-pred)^2),sum((d-base)^2),
      sum(pred-d),sum(d),sum(d*d) FROM predicted WHERE {primary} GROUP BY ob ORDER BY ob""").fetchall())
    draws = cluster_draws(stats)
    r2 = 1 - draws[:, 1] / (draws[:, 5] - draws[:, 4] ** 2 / draws[:, 0])
    ratio = draws[:, 1] / draws[:, 2]
    bias = draws[:, 3] / draws[:, 0]
    ci_rows = [(name, *interval(value)) for name, value in [("R2", r2), ("MSE ratio", ratio), ("bias seconds", bias)]]
    tables["Primary 99% bank-cluster sensitivity intervals"] = (["statistic", "low", "high"], ci_rows)
    tables["Equal ordering-bank weighting"] = (["clusters", "mse_ratio", "mean_bank_bias"], [
        (len(stats), float(np.mean(stats[:, 1] / stats[:, 0]) / np.mean(stats[:, 2] / stats[:, 0])),
         float(np.mean(stats[:, 3] / stats[:, 0])))])
    total, eligible = con.execute("SELECT count(*),sum(eligible::INT) FROM predicted WHERE NOT labelled AND v>2").fetchone()
    point = tables["Primary: unlabelled eligible non-Direct"][1][0]
    passed = (eligible / total >= .60 and min(point[2:5]) >= 100
              and interval(r2)[0] >= .95 and interval(ratio)[1] <= .10
              and interval(bias)[0] >= -60 and interval(bias)[1] <= 60)
    tables["Frozen primary decision"] = (["pass", "eligible_share", "r2_floor", "mse_ratio_ceiling", "absolute_bias_ceiling"],
                                           [(passed, eligible / total, .95, .10, 60)])
    for name, expr in {
        "Party pair": "pair", "Gap presence": "(g>0)::VARCHAR", "FX count": "least(fx,3)::VARCHAR",
        "Visible banks": "least(v,6)::VARCHAR",
        "Endpoint agreement": "(ob=path[1] AND bb=path[-1])::VARCHAR",
        "Calendar month": "strftime(ts_utc,'%Y-%m')",
    }.items():
        tables[f"Predeclared sensitivity: {name}"] = metrics(con, primary, expr)
    tables["Labelled payments pooled (descriptive sensitivity only)"] = metrics(con, "eligible AND labelled AND v>2")
    tables["Drop largest sending account (sensitivity)"] = metrics(con, primary + f""" AND oa NOT IN
      (SELECT oa FROM predicted WHERE {primary} GROUP BY 1 ORDER BY count(*) DESC,oa LIMIT 1)""")
    tables["Eligible population identity and path-bank support"] = table(con, f"""SELECT count(*) n,
      count(DISTINCT ROW_ID) distinct_rows,count(DISTINCT oa) senders,count(DISTINCT ba) receivers,
      count(DISTINCT ob) banks FROM predicted WHERE {primary}""")
    tables["Eligible visible path banks shared with training"] = table(con, f"""SELECT count(DISTINCT bank) shared_path_banks
      FROM predicted,unnest(list_filter(path,lambda x:x<>'...')) t(bank) WHERE {primary}""")
    tables["Eligible population overlap with unlabelled exploration (explore phase overlaps itself)"] = overlaps(con, "predicted", primary)
    report(STEM, phase, freeze, tables)
    plot(tables, phase)
    print(f"{phase}: primary pass={passed}; aggregate report and chart written.", flush=True)


def plot(tables: dict, phase: str) -> None:
    """Show the frozen bank model against the simpler route/count baseline."""
    columns, rows = tables["Route comparison (Direct exploration is in-sample)"]
    fig, ax = plt.subplots(figsize=(9, 5.4))
    fig.subplots_adjust(bottom=.17, top=.88, left=.10, right=.98)
    rows = [row for row in rows if min(row[1:5]) >= 100]
    labels = [str(row[0]) for row in rows]
    rmse = np.array([row[columns.index("rmse")] for row in rows])
    ratio = np.array([row[columns.index("mse_ratio_to_route_count")] for row in rows])
    x = np.arange(len(rows))
    ax.bar(x - .18, rmse / np.sqrt(ratio), .36, label="Route + visible-count baseline", color="#a8b1bd")
    ax.bar(x + .18, rmse, .36, label="Sum of bank effects", color="#236b80")
    ax.set(xticks=x, xticklabels=labels, ylabel="Duration RMSE (seconds)", ylim=(0, None),
           title=f"Bank effects predict eligible-route duration | {phase}")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(.02, .025, "Eligible banks: >=100 Direct exploration appearances. Statistical effects; shared path banks.", fontsize=8.5)
    fig.savefig(OUT / f"{STEM}_{phase}.png", dpi=180)
    plt.close(fig)


def main() -> int:
    """Do not load confirmation until the committed executable and plan are verified."""
    con = None
    try:
        args = arguments(STEM)
        con = connect()
        print("Fitting bank effects on exploration Direct payments only...", flush=True)
        training = train(con)
        if args.phase == "confirm":
            selected(con, "confirm")
        analyse(con, args.phase, args.freeze, training)
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source details hidden.", file=sys.stderr)
        return 1
    finally:
        if con is not None:
            con.close()


if __name__ == "__main__":
    sys.exit(main())
