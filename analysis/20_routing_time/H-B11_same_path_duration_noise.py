"""Compare fixed noise laws after differencing durations on the same visible path.

Run from the repository root:
    uv run python analysis/20_routing_time/H-B11_same_path_duration_noise.py --phase explore
For the frozen July internal test, use --phase confirm --freeze <SHA>.
"""

from datetime import datetime, timezone
import sys

import duckdb
import numpy as np
from scipy.stats import gamma, norm

from routing_common import OUT, arguments, cluster_draws, interval, report

STEM = "H-B11_same_path_duration_noise"
TAIL = 41  # Last bin pools all absolute differences of at least 41 seconds.
MODELS = ("fixed Gamma(2,5)", "matched exponential", "matched normal", "shape = visible count")
BIN_STARTS = [0, 1, 6, 11, 21, 41]


def difference_law(shape: int, scale: float) -> np.ndarray:
    """Mass of abs(X-Y) for two independent, integer-discretised draws.

    Shape zero selects a rounded normal with standard deviation scale.
    A 512-second truncation leaves negligible model mass at the studied scales.
    """
    edges = np.arange(-256, 257)
    cdf = gamma.cdf(edges, a=shape, scale=scale) if shape else norm.cdf(edges - .5, scale=scale)
    pmf = np.diff(cdf)
    autocorrelation = np.correlate(pmf, pmf, mode="full")[len(pmf) - 1:]
    bins = np.r_[autocorrelation[0], 2 * autocorrelation[1:TAIL], 2 * autocorrelation[TAIL:].sum()]
    assert abs(bins.sum() - 1) < 1e-10
    return bins


def build_pairs(con: duckdb.DuckDBPyConnection, start: str, end: str, visible: int) -> None:
    """Use each source row at most once, grouping by exact ordered visible path."""
    con.execute(f"""
      CREATE OR REPLACE TEMP TABLE paths AS
      SELECT row_id,total_duration d,ordering_account oa,
        beneficiary_account ba,transaction_type_code route,gap_count>0 gap,month(ts_utc) mon,
        list_filter(string_split(bic8_path,';'),lambda x:x<>'...') p
      FROM read_parquet('dataset/payments.parquet')
      WHERE ANOMALY_TYPE IS NULL AND ts_utc>=TIMESTAMP '{start}' AND ts_utc<TIMESTAMP '{end}'
        AND participant_count={visible}
        AND (('0x'||substr(md5(ordering_bic8),1,8))::UBIGINT%2)=0
        AND (('0x'||substr(md5(beneficiary_bic8),1,8))::UBIGINT%2)=0
    """)
    # Stable digest ordering makes pairs without using duration, time or account.
    con.execute("""
      CREATE OR REPLACE TEMP TABLE paired AS
      WITH numbered AS (
        SELECT *, row_number() OVER(PARTITION BY p ORDER BY md5(row_id::VARCHAR),row_id) i
        FROM paths
      )
      SELECT p[1] cluster, max(d)-min(d) delta, avg(d) center,
        count(DISTINCT oa)>1 AND count(DISTINCT ba)>1 different_parties,
        count(DISTINCT gap)>1 different_gap, count(DISTINCT mon)>1 different_month,
        min(route) route, count(DISTINCT route)>1 different_route,
        len(list_distinct(p)) < len(p) repeated_bank
      FROM numbered GROUP BY p,(i-1)//2 HAVING count(*)=2
    """)


def compare(con: duckdb.DuckDBPyConnection, visible: int) -> tuple[list[tuple], list[tuple], list[tuple], bool]:
    """Calculate histogram distances and bank-cluster sensitivity intervals."""
    count_columns = ",".join(f"count_if(least(delta,{TAIL})={i})" for i in range(TAIL + 1))
    stats = np.asarray(con.execute(f"""SELECT sum(delta::DOUBLE^2),{count_columns}
        FROM paired GROUP BY cluster ORDER BY cluster""").fetchall(), dtype=float)
    if len(stats) < 100 or stats[:, 1:].sum() < 100:
        return [], [], [], False
    totals = stats.sum(axis=0)
    draws = cluster_draws(stats)
    observed = totals[1:] / totals[1:].sum()
    probabilities = draws[:, 1:] / draws[:, 1:].sum(axis=1)[:, None]
    predictions = [difference_law(2, 5), difference_law(1, np.sqrt(50)),
                   difference_law(0, np.sqrt(50)), difference_law(visible, 5)]
    coarse_observed = np.add.reduceat(observed, BIN_STARTS)
    coarse_draws = np.add.reduceat(probabilities, BIN_STARTS, axis=1)
    coarse_predictions = [np.add.reduceat(model, BIN_STARTS) for model in predictions]
    errors = [np.abs(coarse_draws - model).sum(axis=1) / 2 for model in coarse_predictions]
    distances = [(visible, label, np.abs(coarse_observed - model).sum() / 2, *interval(error))
                 for label, model, error in zip(MODELS, coarse_predictions, errors)]
    fine_distances = [(visible, label, np.abs(observed - model).sum() / 2)
                      for label, model in zip(MODELS, predictions)]
    mse_interval = interval(draws[:, 0] / draws[:, 1:].sum(axis=1))
    improvement = interval(errors[3] - errors[0])
    unsupported = visible == 3 and improvement[0] < .02
    passed = (totals[1:].sum() >= 5000 and distances[0][-1] <= .020
              and mse_interval[0] >= 90 and mse_interval[1] <= 110 and not unsupported)
    summary = (visible, int(totals[1:].sum()), len(stats), totals[0] / totals[1:].sum(),
               *mse_interval, *improvement, passed)
    return [summary], distances, fine_distances, passed


def run(phase: str, freeze: str | None) -> None:
    """Analyse exploration or frozen July without exporting paths or per-path estimates."""
    start, end = ("2023-05-01", "2023-07-01") if phase == "explore" else ("2023-07-01", "2023-08-01")
    summaries, distances, fine_distances, control_rows, histograms, coverage = [], [], [], [], [], []
    decisions = []
    with duckdb.connect(config={"memory_limit": "1536MB", "threads": 1, "temp_directory": ""}) as con:
        con.execute("SET TimeZone='UTC'; SET enable_progress_bar=false")
        for visible in (2, 3, 4, 5):
            build_pairs(con, start, end, visible)
            source_rows, source_paths = con.execute("SELECT count(*),count(DISTINCT p) FROM paths").fetchone()
            pairs, clusters = con.execute("SELECT count(*),count(DISTINCT cluster) FROM paired").fetchone()
            supported = min(pairs, clusters) >= 100
            coverage.append((visible, source_rows, source_paths,
                             pairs if supported or not pairs else "<100 or thin bank support",
                             clusters if supported or not clusters else "suppressed",
                             2 * pairs / source_rows if supported or not pairs else "suppressed"))
            summary, distance, fine_distance, passed = compare(con, visible)
            summaries.extend(summary)
            distances.extend(distance)
            fine_distances.extend(fine_distance)
            if visible <= 3:
                decisions.append(passed)
            if clusters >= 100 and pairs >= 100:
                for lo, hi in ((0, 0), (1, 5), (6, 10), (11, 20), (21, 40), (41, None)):
                    where = f"delta BETWEEN {lo} AND {hi}" if hi is not None else f"delta>={lo}"
                    n = con.execute(f"SELECT count_if({where}) FROM paired").fetchone()[0]
                    probs = difference_law(2, 5)
                    expected = probs[lo:hi + 1].sum() if hi is not None else probs[lo:].sum()
                    histograms.append((visible, f"{lo}–{hi}" if hi not in (None, lo) else
                                       (f"{lo}+" if hi is None else str(lo)),
                                       "<100" if 0 < n < 100 else n,
                                       n / pairs if n >= 100 or n == 0 else "suppressed", expected))
            controls = {
                "All paired rows": "true",
                "Different senders and receivers": "different_parties",
                "Different UTC month": "different_month",
                "Only one payment has a placeholder": "different_gap",
                "Both Direct": "NOT different_route AND route='Direct'",
                "Both Indirect": "NOT different_route AND route='Indirect'",
                "Both Covered": "NOT different_route AND route='Covered'",
                "Different route labels": "different_route",
                "Repeated visible bank": "repeated_bank",
                "Pair mean below 100 s": "center<100",
                "Pair mean from 100 to below 1,000 s": "center>=100 AND center<1000",
                "Pair mean at least 1,000 s": "center>=1000",
            }
            for label, where in controls.items():
                n, banks, mse, q, tail = con.execute(f"""
                  SELECT count(*),count(DISTINCT cluster),avg(delta::DOUBLE^2),
                    quantile_disc(delta,[.5,.9,.99]),count_if(delta>100)
                  FROM paired WHERE {where}
                """).fetchone()
                if min(n, banks) >= 100:
                    control_rows.append((visible, label, n, banks, mse, q, "<100" if 0 < tail < 100 else tail))
    tables = {
        "Population and pairing coverage": (
            ["visible", "source_payments", "visible_paths", "pairs", "first_path_banks", "paired_row_share"], coverage),
        "Primary tests for two and three visible banks; longer counts descriptive": (
            ["visible", "n", "banks", "mean_square", "MS_lo99", "MS_hi99",
             "TV_gain_over_visible_shape_lo99", "TV_gain_over_visible_shape_hi99", "meets_numeric_gates"], summaries),
        "Six-bin total variation and 99% first-path-bank resampling intervals": (
            ["visible", "model", "TV", "low", "high"], distances),
        "One-second bins through 40 seconds, then 41+; descriptive": (
            ["visible", "model", "TV"], fine_distances),
        "Absolute difference distribution; small tail cells masked": (
            ["visible", "seconds", "event_count", "observed_share", "model_share"], histograms),
        "Controls with at least 100 pairs and 100 first visible banks": (
            ["visible", "group", "n", "banks", "mean_square", "p50/p90/p99 seconds", "differences_over_100s"], control_rows),
        "Overall two and three visible-bank decision": (["pass"], [(all(decisions),)]),
    }
    report(STEM, phase, freeze, tables)
    out = OUT / f"{STEM}_{phase}.md"
    metadata = out.read_text(encoding="utf-8").replace("2GB; two threads", "1536MB; one thread")
    metadata = metadata.replace("ordering-bank cluster", "first-visible-bank cluster")
    out.write_text(metadata, encoding="utf-8")
    print(f"{phase} B11 primary {'PASS' if all(decisions) else 'FAIL'}; safe aggregate report saved.")


if __name__ == "__main__":
    try:
        options = arguments(STEM)
        if options.phase == "explore" and datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
            raise ValueError("Research cutoff reached")
        run(options.phase, options.freeze)
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source details hidden.", file=sys.stderr)
        sys.exit(1)
