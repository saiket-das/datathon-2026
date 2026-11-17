"""Test origin-matched bank-country association with the Covered corridor label.

Run: uv run python analysis/20_routing_time/H-B30_same_country_corridor.py --phase explore
Internal July test: --phase confirm --freeze <SHA>.
"""
from datetime import datetime,timezone
from pathlib import Path
import importlib.util
import sys
import duckdb
import numpy as np
from routing_common import OUT,arguments,report,table,cluster_draws,interval

STEM=Path(__file__).stem


def contrast(c: duckdb.DuckDBPyConnection,condition: str) -> np.ndarray:
    """One equally weighted difference per supported origin bank."""
    return np.asarray(c.execute(f"""
      WITH groups AS (SELECT a,{condition} exposure,count(*) n,avg(class) p,
        avg(class-receiver_p) adjusted FROM target GROUP BY 1,2),
      paired AS (SELECT a,min(n) support,
        max(p) FILTER(WHERE exposure)-max(p) FILTER(WHERE NOT exposure) effect,
        max(adjusted) FILTER(WHERE exposure)-max(adjusted) FILTER(WHERE NOT exposure) adjusted
        FROM groups GROUP BY 1 HAVING count(*)=2 AND min(n)>=5)
      SELECT effect,adjusted FROM paired ORDER BY a
    """).fetchall(),dtype=float).reshape(-1,2)


def main() -> None:
    """Compute origin-matched contrasts with May receiver rates as an adjustment."""
    opts=arguments(STEM)
    if opts.phase=="explore" and datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError("Cutoff reached")
    spec=importlib.util.spec_from_file_location("b20",Path(__file__).with_name("H-B20_unseen_corridor_propensities.py"))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with duckdb.connect(config={"memory_limit":"512MB","threads":1,"temp_directory":""}) as c:
        c.execute("SET enable_progress_bar=false")
        module.load(c,opts.phase)
        c.execute("""
          CREATE TEMP TABLE target AS
          WITH receivers AS (SELECT b,count(*) n,sum(class) k FROM pairs WHERE train AND pure GROUP BY b),
          global_rate AS (SELECT avg(class) p FROM pairs WHERE train AND pure)
          SELECT t.*,(r.k+10*p)/(r.n+10) receiver_p FROM pairs t
          JOIN receivers r ON t.b=r.b AND r.n>=25 CROSS JOIN global_rate
          WHERE NOT t.train AND t.pure
        """)
        raw=contrast(c,"substr(a,5,2)=substr(b,5,2)")
        placebo=contrast(c,"substr(md5(a),1,1)<substr(md5(b),1,1)")
        rng=np.random.default_rng(20261117)
        ci=[]
        if len(raw)>=100:
            means=rng.multinomial(len(raw),np.full(len(raw),1/len(raw)),1000)@raw/len(raw)
            ci=[interval(means[:,j]) for j in (0,1)]
        placebo_mean=float(placebo[:,0].mean()) if len(placebo)>=100 else None
        passed=(len(raw)>=100 and all(x[0]>=.02 for x in ci)
                and placebo_mean is not None and abs(placebo_mean)<=.02)
        tables={"Receiver-supported target population":table(c,"""
          SELECT count(*) n,sum(payments) payments,count(DISTINCT a) banks,count(DISTINCT b) receivers,
            count_if(substr(a,5,2)=substr(b,5,2)) same_country_corridors FROM target
        """),
        "Primary retained matched population":table(c,"""
          WITH origins AS (SELECT a FROM target GROUP BY a
            HAVING count_if(substr(a,5,2)=substr(b,5,2))>=5
              AND count_if(substr(a,5,2)<>substr(b,5,2))>=5)
          SELECT count(*) n,sum(payments) payments,count(DISTINCT a) banks,
            count(DISTINCT b) receivers,count_if(substr(a,5,2)=substr(b,5,2)) same_country,
            count_if(substr(a,5,2)<>substr(b,5,2)) different_country
          FROM target JOIN origins USING(a)
        """),
        "Equal-origin matched effects":(
            ["comparison","origins","effect","low99","high99"],
            [(name,len(raw),raw[:,j].mean(),*ci[j]) for j,name in enumerate(("Raw","May receiver adjusted"))] if ci else []),
        "Hash-order placebo":(["origins","mean_effect"],[(len(placebo),placebo_mean)]),
        "Frozen practical decision":(["pass"],[(passed,)])}
    report(STEM,opts.phase,opts.freeze,tables)
    out=OUT/f"{STEM}_{opts.phase}.md"
    out.write_text(out.read_text(encoding="utf-8").replace("2GB; two threads","512MB; one thread"),encoding="utf-8")
    print(f"B30 {opts.phase} {'PASS' if passed else 'FAIL'}.")


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        sys.exit(1)
