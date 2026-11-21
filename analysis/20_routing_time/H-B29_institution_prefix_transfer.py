"""Screen institution-prefix transfer across distinct origin banks.

Run from root: uv run python analysis/20_routing_time/H-B29_institution_prefix_transfer.py
"""
import importlib.util
from pathlib import Path
from datetime import datetime, timezone
import sys
import duckdb
from routing_common import OUT,report,table

STEM=Path(__file__).stem


def main() -> None:
    """Compare other-bank prefix rates on the existing unseen-pair exploration cohort."""
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError("Cutoff reached")
    spec=importlib.util.spec_from_file_location("b20",Path(__file__).with_name("H-B20_unseen_corridor_propensities.py"))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with duckdb.connect(config={"memory_limit":"512MB","threads":1,"temp_directory":""}) as c:
        c.execute("SET enable_progress_bar=false")
        module.load(c,"explore")
        module.score(c)
        c.execute("""
          CREATE TEMP TABLE eligible AS
          WITH bank AS (SELECT a,count(*) n,sum(class) k FROM pairs WHERE train AND pure GROUP BY 1),
          family AS (SELECT substr(a,1,4) prefix,count(*) banks,sum(n) n,sum(k) k FROM bank GROUP BY 1)
          SELECT s.*,(f.k-o.k+10*global_p)/(f.n-o.n+10) prefix_p,f.banks
          FROM scored s JOIN bank o USING(a) JOIN family f ON substr(s.a,1,4)=f.prefix
          WHERE f.n-o.n>=25 AND f.banks>=2
        """)
        tables={"Existing B20 June cohort and prefix eligibility":table(c,"""
          SELECT (SELECT count(*) FROM scored) original_corridors,count(*) n,
            count(DISTINCT a) banks,count(DISTINCT b) receivers,
            count(DISTINCT substr(a,1,4)) prefix_groups,sum(payments) payments,
            avg(class) observed,avg(prefix_p) prefix_rate,
            avg(pow(class-prefix_p,2)) prefix_brier,avg(global_error) global_brier,
            avg(origin_error) origin_brier,avg(country_error) country_brier FROM eligible
        """),
        "Within-May bank-level similarity, excluding own bank from prefix":table(c,"""
          WITH bank AS (SELECT a,count(*) n,sum(class) k FROM pairs WHERE train AND pure GROUP BY 1),
          family AS (SELECT substr(a,1,4) prefix,count(*) banks,sum(n) n,sum(k) k FROM bank GROUP BY 1),
          joined AS (SELECT o.a,(o.k+1.)/(o.n+20) own,(f.k-o.k+1.)/(f.n-o.n+20) others
            FROM bank o JOIN family f ON substr(o.a,1,4)=f.prefix WHERE o.n>=25 AND f.n-o.n>=25)
          SELECT count(*) banks,count(DISTINCT substr(a,1,4)) prefixes,corr(own,others) correlation,
            avg(abs(own-others)) mean_absolute_gap,quantile_cont(abs(own-others),[.1,.5,.9]) gap_quantiles
          FROM joined
        """)}
    report(STEM,"explore",None,tables)
    out=OUT/f"{STEM}_explore.md"
    out.write_text(out.read_text(encoding="utf-8").replace("2GB; two threads","512MB; one thread"),encoding="utf-8")
    print("B29 safe exploration report saved.")


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        sys.exit(1)
