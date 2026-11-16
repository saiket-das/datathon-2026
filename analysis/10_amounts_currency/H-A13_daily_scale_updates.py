"""Screen a bounded daily update mechanism for amount-implied currency scales.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A13_daily_scale_updates.py
Internal re-extraction: add --phase validate --freeze SHA. No daily rates exported.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy.stats import kstest, norm

HERE = Path(__file__).resolve().parent
WIDTH = 0.015
TOLERANCE = 0.01501
SPEC = importlib.util.spec_from_file_location("fx", HERE / "H-A03_fx_country_classes.py")
fx = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fx)


def uniform_cdf(x: np.ndarray) -> np.ndarray:
    return np.clip((x+WIDTH)/(2*WIDTH),0,1)


def shape_distances(values: np.ndarray) -> tuple[float,float]:
    return (kstest(values,uniform_cdf).statistic,
            kstest(values/(WIDTH/np.sqrt(3)),norm.cdf).statistic)


def main() -> int:
    """Compare stable currency increments with competing daily-update shapes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("explore", "validate"), default="explore")
    parser.add_argument("--freeze")
    args = parser.parse_args()
    if datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        print("Research cutoff reached.")
        return 1
    try:
        if args.phase == "validate":
            if not args.freeze:
                raise ValueError("Freeze required")
            subprocess.run(["git","merge-base","--is-ancestor",args.freeze,"HEAD"],
                           cwd=fx.ROOT,check=True,capture_output=True)
            files = (Path(__file__).resolve(),Path(fx.__file__),Path(fx.foundation.__file__),
                     fx.ROOT/"findings/hypotheses/H-A13_daily_scale_updates.md")
            marker = b"\n## Confirmation and robustness results"
            for path in files:
                frozen = subprocess.check_output(
                    ["git","show",f"{args.freeze}:{path.relative_to(fx.ROOT).as_posix()}"],
                    cwd=fx.ROOT,stderr=subprocess.DEVNULL,
                ).replace(b"\r\n",b"\n")
                if frozen.split(marker)[0] != path.read_bytes().replace(b"\r\n",b"\n").split(marker)[0]:
                    raise ValueError("Freeze mismatch")
        split = "confirm" if args.phase == "validate" else "explore"
        with fx.connect() as con:
            con.execute(f"""CREATE TEMP TABLE anchors AS
              WITH masses AS (
                SELECT currency,CAST(ts_utc AS DATE) d,USD_AMOUNT a,
                  pow(10,floor(log10(USD_AMOUNT))) base,count(*) n
                FROM source WHERE split='{split}' AND ANOMALY_TYPE IS NULL
                  AND currency IN ('CHF','EUR','GBP','USD')
                  AND USD_AMOUNT>=100 AND USD_AMOUNT<2000000
                GROUP BY 1,2,3,4
              ), candidates AS (
                SELECT *,row_number() OVER(PARTITION BY currency,d,base ORDER BY n DESC,a) r
                FROM masses
              )
              SELECT currency,d,a/base scale,base,n FROM candidates WHERE r=1 AND n>=20
              QUALIFY row_number() OVER(PARTITION BY currency,d ORDER BY base DESC)=1""")
            con.execute("""CREATE TEMP TABLE increments AS
              WITH lags AS (
                SELECT *,lag(scale) OVER(PARTITION BY currency ORDER BY d) prev,
                  d-lag(d) OVER(PARTITION BY currency ORDER BY d) gap
                FROM anchors
              )
              SELECT *,scale/prev-1 change,prev/scale-1 inverse_change FROM lags WHERE gap=1""")
            tables = {}
            tables["Eligible payment and date scope"] = fx.query(con, f"""
                WITH scope AS (
                  SELECT currency,count(*) payments,count(DISTINCT CAST(ts_utc AS DATE)) scoped_dates
                  FROM source WHERE split='{split}' AND ANOMALY_TYPE IS NULL
                    AND currency IN ('CHF','EUR','GBP','USD') AND USD_AMOUNT>=100 AND USD_AMOUNT<2000000
                  GROUP BY currency
                ), supported AS (SELECT currency,count(*) anchor_dates FROM anchors GROUP BY currency)
                SELECT currency,payments,scoped_dates,coalesce(anchor_dates,0) anchor_dates,
                  scoped_dates-coalesce(anchor_dates,0) excluded_dates
                FROM scope LEFT JOIN supported USING(currency) ORDER BY currency""")
            tables["Anchor support"] = fx.query(con, """SELECT currency,count(*) dates,
              sum(n) anchor_payments,min(base) min_base,max(base) max_base
              FROM anchors GROUP BY 1 ORDER BY 1""")
            tables["Observed adjacent-day changes"] = fx.query(con, """SELECT currency,count(*) increments,
              avg(change) mean_change,stddev_samp(change) sd_change,min(change) minimum,
              max(change) maximum,quantile_cont(change,[0.1,0.25,0.5,0.75,0.9]) quantiles,
              count(*) FILTER(WHERE abs(change)>0.01501) beyond_candidate_bound
              FROM increments GROUP BY 1 ORDER BY 1""")
            # Dates are local aggregate model indices. Only summary estimates leave this process.
            rows = con.execute("""SELECT currency,d,change,inverse_change FROM increments
                WHERE currency<>'USD' ORDER BY d,currency""").fetchall()
            values = np.asarray([row[2] for row in rows],dtype=float)
            dates = sorted(set(row[1] for row in rows))
            by_date = [np.asarray([row[2:] for row in rows if row[1]==date]) for date in dates]
            rng = np.random.default_rng(20261117)
            summaries = []
            for _ in range(1000):
                indices = np.concatenate([
                    (start+np.arange(7)) % len(dates)
                    for start in rng.integers(0,len(dates),int(np.ceil(len(dates)/7)))
                ])[:len(dates)]
                sample = np.concatenate([by_date[i] for i in indices])
                direct, inverse = sample.T
                u,g = shape_distances(inverse)
                summaries.append([direct.mean(),direct.std(ddof=1),
                                  np.mean(abs(direct)>TOLERANCE),u,g-u])
            intervals = np.quantile(summaries,[.005,.995],axis=0)
            uniform_ks,gaussian_ks = shape_distances(values)
            gaussian_tail = 2*norm.sf(TOLERANCE/(WIDTH/np.sqrt(3)))
            tables["Pooled fixed-shape comparison"] = (
                ["increments","dates","uniform_KS","Gaussian_KS","Gaussian_expected_tail_share",
                 "observed_tail_share"],
                [(len(values),len(dates),uniform_ks,gaussian_ks,gaussian_tail,
                  np.mean(abs(values)>TOLERANCE))])
            tables["Seven-date circular-block sensitivity, shared across currencies"] = (
                ["statistic","low99","high99"],
                [(label,*intervals[:,i]) for i,label in enumerate(
                    ["direct mean","direct SD","direct tail share","inverse uniform KS",
                     "inverse Gaussian minus uniform KS"])])
            tables["Lag-one diagnostic within contiguous observed triples"] = fx.query(con, """
                WITH lagged AS (
                  SELECT *,lag(change) OVER(PARTITION BY currency ORDER BY d) prev_change,
                    d-lag(d) OVER(PARTITION BY currency ORDER BY d) delta_days
                  FROM increments
                )
                SELECT currency,count(*) adjacent_pairs,corr(change,prev_change) lag1
                FROM lagged WHERE delta_days=1 AND currency<>'USD'
                GROUP BY 1 ORDER BY 1""")
            tables["Inverse-scale alternative"] = fx.query(con, """
                SELECT currency,count(*) increments,avg(inverse_change) mean_inverse,
                  stddev_samp(inverse_change) sd_inverse,min(inverse_change) minimum_inverse,
                  max(inverse_change) maximum_inverse,
                  count(*) FILTER(WHERE abs(inverse_change)>0.01501) beyond_inverse_bound
                FROM increments GROUP BY 1 ORDER BY 1""")
            inverse = np.asarray([row[3] for row in rows],dtype=float)
            tables["Inverse shape descriptive comparison"] = (
                ["increments","uniform_KS","Gaussian_KS"],
                [(len(inverse),*shape_distances(inverse))])
            inverse_ks, gaussian_inverse_ks = tables["Inverse shape descriptive comparison"][1][0][1:]
            counts = tables["Inverse-scale alternative"][1]
            nonusd = [row for row in counts if row[0] != "USD"]
            usd = next(row for row in counts if row[0] == "USD")
            passed = (len(nonusd)==3 and min(row[1] for row in nonusd)>=40
                      and sum(row[-1] for row in nonusd)==0
                      and usd[1]>=40 and usd[5]==usd[4]==0
                      and inverse_ks<=0.12 and gaussian_inverse_ks-inverse_ks>=0.015)
            tables["Practical decision"] = (["all_criteria_met"],[(passed,)])
        report = fx.render("H-A13 — Bounded daily scale updates",tables,args.freeze or "exploration only")
        if args.phase == "explore":
            report = report.replace(
                "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
                "Only both-account bit-0 data queried. Phase 0 and A01–A12 exposure applies.")
        report += ("\nCandidate comparisons use fixed zero-centred shapes without fitting their parameters. "
                   "KS values are descriptive after hypothesis selection. Block intervals condition on fitted "
                   "anchors. Selection of supported dates can bias the inferred update law. "
                   "No iid or original-code claim follows.\n")
        (HERE/f"out/H-A13_daily_scale_updates_{args.phase}.md").write_text(report,encoding="utf-8")
        print("OK: aggregate daily-update screen saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())
