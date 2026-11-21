"""Screen a structural-zero origin mechanism for Covered states.

Run: uv run python analysis/20_routing_time/H-B24_origin_structural_zero.py
Exploration only. Reuses B20's May/June plans and unseen-pair population.
"""
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys

import duckdb
import numpy as np

from routing_common import OUT, cluster_draws, interval, report, table

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("b20",HERE/"H-B20_unseen_corridor_propensities.py")
b20 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(b20)
STEM = Path(__file__).stem


def main() -> None:
    """Compare a two-rate zero witness gate with the graded origin propensity."""
    if datetime.now(timezone.utc) >= datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError("Research cutoff reached")
    with duckdb.connect(config={"memory_limit":"512MB","threads":1,"temp_directory":""}) as con:
        con.execute("SET TimeZone='UTC'; SET enable_progress_bar=false")
        b20.load(con,"explore")
        b20.score(con)
        con.execute("""
          CREATE TEMP TABLE origin_activity AS
          WITH origins AS (
            SELECT a,count(*) n,sum(class) k FROM pairs WHERE train AND pure GROUP BY a HAVING n>=25
          )
          SELECT *,k>0 active FROM origins
        """)
        con.execute("""
          CREATE TEMP TABLE evaluated AS
          WITH pooled AS (
            SELECT active,sum(k)/sum(n) two_rate FROM origin_activity GROUP BY active
          )
          SELECT e.*,o.active,p.two_rate,pow(e.class-p.two_rate,2) two_rate_error
          FROM scored e JOIN origin_activity o USING(a) JOIN pooled p USING(active)
        """)
        summaries=table(con,"""
          SELECT CASE WHEN active THEN 'Any May Covered direction'
                      ELSE 'No May Covered direction' END cohort,count(*) n,
            count(DISTINCT a) banks,count(DISTINCT b) receivers,
            count_if(class=1) covered_directions,avg(class) observed,
            avg(two_rate) two_rate_predicted,avg(origin_p) graded_predicted,
            avg(two_rate_error) two_rate_brier,avg(origin_error) graded_brier
          FROM evaluated GROUP BY active ORDER BY active
        """)
        summary=table(con,"""
          SELECT count(*) n,count(DISTINCT a) banks,count(DISTINCT b) receivers,
            avg(two_rate_error) two_rate_brier,avg(origin_error) graded_brier,
            avg(global_error) global_brier
          FROM evaluated
        """)
        summaries=(
            summaries[0],[
                tuple("<100" if idx==4 and 0<item<100 else item
                      for idx,item in enumerate(row)) for row in summaries[1]
            ]
        )
        sensitivities=[]
        for role, key in (("Origin","a"),("Receiver","b")):
            stats = np.asarray(con.execute(f"""
              SELECT count(*),sum(two_rate_error),sum(origin_error)
              FROM evaluated GROUP BY {key} ORDER BY {key}
            """).fetchall(),dtype=float)
            if len(stats)>=100:
                draws=cluster_draws(stats)
                sensitivities.append((role,len(stats),*interval(1-draws[:,2]/draws[:,1])))
    report(STEM,"explore",None,{"Two-state versus graded transfer":summary,
       "Previously inactive versus active origins":summaries,"Bank-role sensitivity":[
           ["cluster_role","clusters","graded_lift_low99","graded_lift_high99"],sensitivities]})
    result=OUT/f"{STEM}_explore.md"
    result.write_text(result.read_text(encoding="utf-8").replace("2GB; two threads","512MB; one thread")
        .replace("99% ordering-bank","99% separate bank-role"),encoding="utf-8")
    print("OK: B24 exploratory aggregate report.")


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        sys.exit(1)
