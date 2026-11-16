"""Test a fixed internal-path event law: visible bank .35, gap .05, finish .60.

Run from the repository root:
  uv run python analysis/20_routing_time/H-B02_route_gap_process.py --phase explore
  uv run python analysis/20_routing_time/H-B02_route_gap_process.py --phase confirm --freeze <SHA>
Reads dataset/payments.parquet only; exports aggregate Markdown and a PNG.
No account identifiers, bank identities or payment records leave local memory.
"""

import sys

import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from routing_common import (OUT, arguments, cluster_draws, connect, interval, overlaps,
                            remember_exploration, report, selected, table)

STEM = "H-B02_route_gap_process"
CELL = "least(v-2,5)*3+least(g,2)"


def cell_probabilities() -> np.ndarray:
    """P(V=v,G=g)=.60 * choose(v+g-2,g) * .35^(v-2) * .05^g.

    Marginal V-2 is geometric with continuation .35/.95; G|V is
    negative binomial counting failures before V-1 successes, success probability .95.
    Fixed output grid: V=2,3,4,5,6,7+ crossed with G=0,1,2+.
    """
    result = np.zeros((6, 3))
    for v in range(2, 200):
        pv = (1 - .35 / .95) * (.35 / .95) ** (v - 2)
        pg0 = .95 ** (v - 1)
        pg1 = (v - 1) * .95 ** (v - 1) * .05
        result[min(v - 2, 5)] += pv * np.array([pg0, pg1, 1 - pg0 - pg1])
    assert np.isclose(result.sum(), 1)
    return result.ravel()


def baseline(con: duckdb.DuckDBPyConnection) -> np.ndarray:
    """Learn only exploration marginals; independence is the simpler alternative."""
    rows = con.execute(f"SELECT {CELL} cell,count(*) FROM sample WHERE NOT labelled GROUP BY 1").fetchall()
    grid = np.zeros(18)
    for cell, count in rows:
        grid[cell] = count
    grid = grid.reshape(6, 3) / grid.sum()
    return np.outer(grid.sum(axis=1), grid.sum(axis=0)).ravel()


def summaries(con: duckdb.DuckDBPyConnection, where: str, dimension: str = "'all'") -> tuple[list[str], list[tuple]]:
    """Aggregate event estimates, joint-model distance, and effective support."""
    return table(con, f"""SELECT {dimension} AS \"group\",count(*) n,
      count(DISTINCT oa) senders,count(DISTINCT ba) receivers,count(DISTINCT ob) banks,
      sum(v-2)::DOUBLE/sum(v-1+g) visible_event,
      sum(g)::DOUBLE/sum(v-1+g) gap_event,
      count(*)::DOUBLE/sum(v-1+g) finish_event,
      count(*) FILTER(WHERE route='Covered')::DOUBLE/nullif(count(*) FILTER(WHERE v>2),0) covered_given_multibank,
      avg((g>0)::INT) gap_path_share,avg((g>=2)::INT) multiple_gap_share
      FROM sample WHERE {where} GROUP BY 1 ORDER BY 1""")


def cluster_statistics(con: duckdb.DuckDBPyConnection, where: str) -> np.ndarray:
    """Local bank sufficient statistics: n, extras, gaps, covered, multibank and 18 cells."""
    cells = ",".join(f"count(*) FILTER(WHERE {CELL}={i})" for i in range(18))
    return np.asarray(con.execute(f"""SELECT count(*) n,sum(v-2),sum(g),
      count(*) FILTER(WHERE route='Covered'),count(*) FILTER(WHERE v>2),{cells}
      FROM sample WHERE {where} GROUP BY ob ORDER BY ob""").fetchall(), dtype=float)


def statistics(values: np.ndarray, expected: np.ndarray, independent: np.ndarray) -> dict[str, np.ndarray]:
    """Same fixed statistics for whole sample and each bank resampling draw."""
    values = np.atleast_2d(values)
    n, extras, gaps, covered, multi = values[:, :5].T
    events = n + extras + gaps
    cells = values[:, 5:] / n[:, None]
    return {"visible_event": extras / events, "gap_event": gaps / events,
            "finish_event": n / events, "covered_given_multibank": covered / multi,
            "joint_TV": np.abs(cells - expected).sum(axis=1) / 2,
            "TV_ratio_to_independence": np.abs(cells - expected).sum(axis=1)
            / np.abs(cells - independent).sum(axis=1)}


def analyse(con: duckdb.DuckDBPyConnection, phase: str, freeze: str | None, independent: np.ndarray) -> None:
    """Evaluate the fixed law without parameter fitting or threshold adjustment."""
    expected = cell_probabilities()
    tables = {"Unlabelled population support and fixed event estimates": summaries(con, "NOT labelled")}
    stats = cluster_statistics(con, "NOT labelled")
    points = statistics(stats.sum(axis=0), expected, independent)
    draws = statistics(cluster_draws(stats), expected, independent)
    intervals = {name: interval(value) for name, value in draws.items()}
    tables["Frozen primary statistics and 99% bank-cluster sensitivity intervals"] = (
        ["statistic", "estimate", "low", "high"],
        [(name, float(value[0]), *intervals[name]) for name, value in points.items()])
    targets = {"visible_event": (.345, .355), "gap_event": (.045, .055),
               "finish_event": (.595, .605)}
    passed = (all(intervals[name][0] >= lo and intervals[name][1] <= hi
                  for name, (lo, hi) in targets.items())
              and intervals["joint_TV"][1] <= .01
              and intervals["TV_ratio_to_independence"][1] <= .5)
    support = tables["Unlabelled population support and fixed event estimates"][1][0]
    passed = passed and min(support[2:5]) >= 100
    tables["Frozen primary decision"] = (["pass", "TV_ceiling", "TV_ratio_ceiling", "clusters"],
                                           [(passed, .01, .5, len(stats))])
    totals = stats[:, 5:].sum(axis=0)
    n = totals.sum()
    cell_rows = []
    for i, count in enumerate(totals):
        vlabel = str(i // 3 + 2) if i // 3 < 5 else "7+"
        glabel = str(i % 3) if i % 3 < 2 else "2+"
        cell_rows.append((f"V={vlabel}; G={glabel}", int(count), count / n, expected[i], independent[i]))
    tables["Joint count distribution; fixed law versus independence baseline"] = (
        ["cell", "n", "observed_share", "fixed_model_share", "independent_baseline_share"], cell_rows)
    tables["Structural exceptions and concentration"] = table(con, """SELECT count(*) n,
      sum((path[1]='...' OR path[-1]='...')::INT) endpoint_gaps,
      sum((v<>len(list_filter(path,lambda x:x<>'...')))::INT) visible_count_mismatch,
      sum(((route='Direct')<>(v=2))::INT) direct_mismatch,
      sum((list_sum(list_transform(range(1,len(path)),lambda i:
        (path[i]='...' AND path[i+1]='...')::INT))>0)::INT) adjacent_placeholder_paths,
      max(bank_n)::DOUBLE/count(*) largest_ordering_bank_share,
      max(sender_n)::DOUBLE/count(*) largest_sender_share
      FROM (SELECT *,count(*) OVER(PARTITION BY ob) bank_n,
        count(*) OVER(PARTITION BY oa) sender_n FROM sample WHERE NOT labelled)""")
    tables["Equal ordering-bank weighting"] = (["clusters", "visible_event", "gap_event", "finish_event"], [
        (len(stats), *[float(np.mean(stats[:, col] / stats[:, :3].sum(axis=1))) for col in (1, 2, 0)])])
    supported = stats[stats[:, 0] >= 100]
    tables["Equal ordering-bank weighting; >=100 unlabelled payments"] = (
        ["clusters", "visible_event", "gap_event", "finish_event"], [
            (len(supported), *[float(np.mean(supported[:, col] / supported[:, :3].sum(axis=1)))
                               for col in (1, 2, 0)])])
    for name, expr in {
        "Party pair": "pair", "Route": "route", "Calendar month": "strftime(ts_utc,'%Y-%m')",
        "File block": "((ROW_ID-1)//1000000)::VARCHAR",
        "Endpoint agreement": "(ob=path[1] AND bb=path[-1])::VARCHAR",
        "FX count": "least(fx,3)::VARCHAR",
    }.items():
        tables[f"Predeclared sensitivity (composition may differ): {name}"] = summaries(con, "NOT labelled", expr)
    tables["Labelled payments pooled (descriptive sensitivity only)"] = summaries(con, "labelled")
    tables["Drop largest sending account (sensitivity)"] = summaries(con, """NOT labelled AND oa NOT IN
      (SELECT oa FROM sample WHERE NOT labelled GROUP BY 1 ORDER BY count(*) DESC,oa LIMIT 1)""")
    tables["Eligible source coverage"] = table(con, """SELECT count(*) n,
      count(*) FILTER(WHERE NOT labelled) unlabelled_n,count(*) FILTER(WHERE labelled) labelled_n,
      count(DISTINCT ROW_ID) distinct_rows FROM sample""")
    tables["Unlabelled population overlap with exploration (explore phase overlaps itself)"] = overlaps(con, "sample", "NOT labelled")
    report(STEM, phase, freeze, tables)
    plot(totals, expected, independent, phase)
    print(f"{phase}: primary pass={passed}; aggregate report and chart written.", flush=True)


def plot(totals: np.ndarray, expected: np.ndarray, independent: np.ndarray, phase: str) -> None:
    """Plot safe marginal probabilities and gap risk conditional on visible count."""
    observed = totals.reshape(6, 3)
    model = expected.reshape(6, 3)
    baseline_grid = independent.reshape(6, 3)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), layout="constrained")
    x = np.arange(6)
    axes[0].bar(x - .18, observed.sum(axis=1) / observed.sum(), .36, label="Observed", color="#236b80")
    axes[0].bar(x + .18, model.sum(axis=1), .36, label="Fixed event law", color="#d19a43")
    axes[0].set(ylabel="Payment share", title="Visible route length follows the fixed event law")
    axes[1].plot(x, 1 - observed[:, 0] / observed.sum(axis=1), "o-", label="Observed", color="#236b80")
    axes[1].plot(x, 1 - model[:, 0] / model.sum(axis=1), "s--", label="Fixed event law", color="#d19a43")
    axes[1].plot(x, 1 - baseline_grid[:, 0] / baseline_grid.sum(axis=1), ":", label="Independent gap baseline", color="#858c96")
    axes[1].set(ylabel="Share with >=1 placeholder", ylim=(0, .4), title="Gap risk rises with the visible-link count")
    for ax in axes:
        ax.set(xticks=x, xticklabels=["2", "3", "4", "5", "6", "7+"], xlabel="Visible banks (V)")
        ax.legend(frameon=False, fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle(f"Internal event probabilities: bank .35 / gap .05 / finish .60 | {phase}", fontsize=12)
    fig.savefig(OUT / f"{STEM}_{phase}.png", dpi=180)
    plt.close(fig)


def main() -> int:
    """Confirmation opens only after freeze verification; baseline always uses exploration."""
    con = None
    try:
        args = arguments(STEM)
        con = connect()
        selected(con, "explore")
        remember_exploration(con)
        independent = baseline(con)
        if args.phase == "confirm":
            selected(con, "confirm")
        analyse(con, args.phase, args.freeze, independent)
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source details hidden.", file=sys.stderr)
        return 1
    finally:
        if con is not None:
            con.close()


if __name__ == "__main__":
    sys.exit(main())
