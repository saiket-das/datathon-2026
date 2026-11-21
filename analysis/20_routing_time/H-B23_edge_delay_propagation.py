"""Test whether directed delays propagate along adjacent edges or outer endpoints.

Run: uv run python analysis/20_routing_time/H-B23_edge_delay_propagation.py --phase explore
Use --phase confirm --freeze SHA only after committing the plan.
"""
from datetime import datetime, timezone
import sys

import duckdb
import numpy as np

from routing_common import OUT, arguments, cluster_draws, interval, report, table

STEM = "H-B23_edge_delay_propagation"


def prepare(con: duckdb.DuckDBPyConnection, phase: str) -> None:
    """Estimate directional penalties from May Direct payments only."""
    end = "2023-07-01" if phase=="explore" else "2023-08-01"
    con.execute("""
      CREATE TEMP TABLE payments AS
      WITH paths AS (
        SELECT list_filter(string_split(bic8_path,';'),lambda x:x<>'...') p,
          month(ts_utc) mo,total_duration d,
          transaction_type_code='Covered' covered
        FROM read_parquet('dataset/payments.parquet')
        WHERE anomaly_type IS NULL AND participant_count IN (2,3)
          AND ts_utc>='2023-05-01'::TIMESTAMP AND ts_utc<?::TIMESTAMP
          AND (('0x'||substr(md5(ordering_bic8),1,8))::UBIGINT%2)=0
          AND (('0x'||substr(md5(beneficiary_bic8),1,8))::UBIGINT%2)=0
      )
      SELECT p[1] a,p[-1] b,CASE WHEN len(p)=3 THEN p[2] END middle,mo,d,covered
      FROM paths
    """,[end])
    con.execute("""
      CREATE TEMP TABLE edges AS
      WITH estimates AS (
        SELECT a,b,median(d) center FROM payments WHERE mo=5 AND middle IS NULL
        GROUP BY 1,2 HAVING count(*)>=5
      )
      SELECT f.a,f.b,least(f.center,r.center) sym,
        f.center-least(f.center,r.center) penalty
      FROM estimates f JOIN estimates r ON f.a=r.b AND f.b=r.a
      WHERE least(f.center,r.center)<100
    """)
    con.execute("""
      CREATE TEMP TABLE predictions AS
      SELECT p.*,x.sym+y.sym edge_base,x.penalty+y.penalty edge_add,
        z.penalty outer_add
      FROM payments p JOIN edges x ON p.a=x.a AND p.middle=x.b
      JOIN edges y ON p.middle=y.a AND p.b=y.b
      JOIN edges z ON p.a=z.a AND p.b=z.b
      WHERE p.mo>=6 AND p.a<>p.b AND p.a<>p.middle AND p.b<>p.middle
    """)


def main() -> None:
    """Compare same-row attribution of a delay to adjacent or outer corridors."""
    opts=arguments(STEM)
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError("Research cutoff reached")
    with duckdb.connect(config={"memory_limit":"600MB","threads":1,"temp_directory":""}) as con:
        con.execute("SET TimeZone='UTC'; SET enable_progress_bar=false")
        prepare(con,opts.phase)
        offset=con.execute("""
          SELECT median(d-edge_base) FROM predictions WHERE mo=6 AND edge_add<=20 AND outer_add<=20
        """).fetchone()[0]
        if offset is None:
            raise ValueError("Missing June baseline")
        con.execute("""
          CREATE TEMP TABLE scored AS
          SELECT *,d-edge_base-? AS residual,
            CASE WHEN edge_add>20 THEN 'Edge marked' ELSE 'Edge unmarked' END adjacent_state,
            CASE WHEN outer_add>20 THEN 'Outer marked' ELSE 'Outer unmarked' END outer_state
          FROM predictions WHERE mo=?
        """,[float(offset),6 if opts.phase=="explore" else 7])
        report_month=6 if opts.phase=="explore" else 7
        coverage=table(con,f"""
          SELECT (SELECT count(*) FROM payments WHERE mo={report_month} AND middle IS NOT NULL) scoped,
            count(*) matched,count_if(edge_add>20 OR outer_add>20) marked,
            count(DISTINCT a) origin_banks,count(DISTINCT b) receiver_banks,
            count(DISTINCT (a,b)) outer_corridors,count(DISTINCT middle) middle_banks,
            {float(offset)} june_baseline_shift
          FROM scored
        """)
        groups=table(con,"""
          SELECT CASE WHEN grouping(adjacent_state)=1 THEN 'All' ELSE adjacent_state END adjacent_state,
            CASE WHEN grouping(outer_state)=1 THEN 'All' ELSE outer_state END outer_state,
            count(*) n,count(DISTINCT a) banks,count(DISTINCT b) receivers,
            count(DISTINCT (a,b)) outer_corridors,
            avg(covered::INT) covered_share,avg(edge_add) adjacent_delay,
            avg(outer_add) outer_delay,median(residual) median_excess_seconds,
            avg(abs(residual)) baseline_mae,avg(abs(residual-edge_add)) adjacent_mae,
            avg(abs(residual-outer_add)) outer_mae,
            avg(abs(residual-edge_add-outer_add)) both_mae
          FROM scored GROUP BY GROUPING SETS ((),(adjacent_state,outer_state))
          ORDER BY 1,2
        """)
        marked=table(con,"""
          SELECT count(*) n,count(DISTINCT a) banks,count(DISTINCT b) receivers,
            count(DISTINCT middle) interior_banks,
            count(DISTINCT (a,b)) outer_corridors,
            avg(abs(residual)) baseline_mae,avg(abs(residual-edge_add)) adjacent_mae,
            avg(abs(residual-outer_add)) outer_mae,
            avg(abs(residual-edge_add-outer_add)) both_mae,
            avg((abs(residual-edge_add)<=20)::INT) adjacent_within20
          FROM scored WHERE edge_add>20 OR outer_add>20
        """)
        sensitivities=[]
        for role, key in (("Origin","a"),("Receiver","b"),("Interior","middle")):
            stats=np.asarray(con.execute(f"""
              SELECT count(*),sum(abs(residual)),sum(abs(residual-edge_add)),
                sum(abs(residual-outer_add)),sum(abs(residual-edge_add-outer_add))
              FROM scored WHERE edge_add>20 OR outer_add>20 GROUP BY {key} ORDER BY {key}
            """).fetchall(),dtype=float).reshape(-1,5)
            if len(stats)>=100:
                draws=cluster_draws(stats)
                sensitivities.append((role,len(stats),*interval(1-draws[:,2]/draws[:,1]),
                    *interval(1-draws[:,2]/draws[:,3]),*interval(1-draws[:,2]/draws[:,4])))
        scoped, matched, marked_count, *_=coverage[1][0]
        adjacent_mae=marked[1][0][6]
        passed=(scoped>0 and matched/scoped>=.01 and matched>=1000 and marked_count>=500
                and adjacent_mae is not None and adjacent_mae<=16
                and len(sensitivities)==3
                and all(min(row[2],row[4],row[6])>=.50 for row in sensitivities))
    report(STEM,opts.phase,opts.freeze,{"Matched support":coverage,
        "Observed delay by prior edge state":groups,
        "Primary marked paths":marked,
        "Bank sensitivity on marked paths":(
            ["cluster_role","clusters","lift_vs_base_low99","lift_vs_base_high99",
             "lift_vs_outer_low99","lift_vs_outer_high99","lift_vs_both_low99","lift_vs_both_high99"],
            sensitivities),
        "Frozen decision":(["all_criteria_met"],[(passed,)])})
    result=OUT/f"{STEM}_{opts.phase}.md"
    result.write_text(result.read_text(encoding="utf-8").replace(
        "2GB; two threads","600MB; one thread").replace("99% ordering-bank","99% separate bank-role"),
        encoding="utf-8")
    print(f"OK: B23 {opts.phase} aggregate report.")


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        sys.exit(1)
