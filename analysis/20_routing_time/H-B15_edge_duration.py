"""Test shifted edge-additivity on supported three-visible-bank payment paths.

Run: uv run python analysis/20_routing_time/H-B15_edge_duration.py --phase explore
After freezing: same script with --phase confirm --freeze SHA.
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys

import duckdb
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
STEM = Path(__file__).stem


def evaluate(c: duckdb.DuckDBPyConnection, phase: str, freeze: str | None) -> str:
    """Fit May directed-edge medians, calibrate in June and score fixed test cases."""
    c.execute("""
        CREATE TEMP TABLE edges AS
        SELECT p[1] AS a,p[2] AS b,median(duration) AS center,count(*) AS n
        FROM source WHERE month=5 AND visible=2
        GROUP BY a,b HAVING n>=10
    """)
    edge_count, training = c.execute("SELECT count(*),sum(n) FROM edges").fetchone()
    c.execute("""
        CREATE VIEW predictions AS
        SELECT e.*,x.center+y.center AS edge_sum,greatest(x.center,y.center) AS largest_edge,
               z.center AS direct_endpoint,least(x.center,y.center) AS smaller_edge
        FROM source e
        JOIN edges x ON p[1]=x.a AND p[2]=x.b
        JOIN edges y ON p[2]=y.a AND p[3]=y.b
        LEFT JOIN edges z ON p[1]=z.a AND p[3]=z.b
        WHERE visible=3
    """)
    sum_shift,max_shift,direct_shift = c.execute("""
        SELECT median(duration-edge_sum),median(duration-largest_edge),
               median(duration-direct_endpoint)
        FROM predictions WHERE month=6
    """).fetchone()
    month = 6 if phase=="explore" else 7
    c.execute(f"""
        CREATE VIEW scored AS
        SELECT *, abs(duration-edge_sum-({float(sum_shift)})) AS sum_error,
                  abs(duration-largest_edge-({float(max_shift)})) AS max_error,
                  abs(duration-direct_endpoint-({float(direct_shift)})) AS endpoint_error
        FROM predictions WHERE month={month}
    """)
    total = c.execute("SELECT count(*) FROM source WHERE month=? AND visible=3",[month]).fetchone()[0]
    primary = c.execute("""
        SELECT count(*), count(DISTINCT ordering_bank), count(DISTINCT sender),count(DISTINCT receiver),
               avg(sum_error),avg(max_error),quantile_cont(sum_error,.90),avg((sum_error<=20)::INT),
               median(duration-edge_sum),count_if(smaller_edge>=100)
        FROM scored
    """).fetchone()
    n,banks,senders,receivers,sum_mae,max_mae,p90,within20,residual,large = primary
    if n<100 or min(banks,senders,receivers)<100:
        raise ValueError("Insufficient entity support")
    clusters = np.asarray(c.execute("""
        SELECT count(*),sum(sum_error),sum(max_error),count_if(sum_error<=20)
        FROM scored GROUP BY ordering_bank ORDER BY ordering_bank
    """).fetchall(),dtype=float)
    rng=np.random.default_rng(20261116)
    draws=rng.multinomial(banks,np.full(banks,1/banks),1000)@clusters
    mae_upper=float(np.quantile(draws[:,1]/draws[:,0],.99))
    ratio_upper=float(np.quantile(draws[:,1]/draws[:,2],.99))
    within_lower=float(np.quantile(draws[:,3]/draws[:,0],.01))
    passed=(total>0 and n/total>=.02 and n>=1000 and mae_upper<=12
            and ratio_upper<=.75 and within_lower>=.90 and p90<=25)
    lines = [
        f"# H-B15 supported directed-edge duration: {phase}","",
        f"Freeze: {freeze or 'exploration only'}. Unlabelled endpoint bit0/0, May edge fit and June calibration.",
        "512MB, one thread, no spill. Prior Phase 0, Round 1 and Round 2 exposure applies.",
        f"May trained {edge_count:,} directed edges from {training:,} two-visible-bank witnesses.",
        f"June offsets (seconds): sum {sum_shift:.1f}, maximum {max_shift:.1f}, endpoint {direct_shift:.1f}.",
        f"Scored month {month}: {n:,}/{total:,} paths ({n/total:.4%}) across {banks:,} ordering banks, {senders:,} senders and {receivers:,} receivers.",
        f"Paths with shorter fitted edge at least100 seconds: {large:,}.",
        "",
        "| Shifted sum MAE | Shifted max MAE | MAE ratio | Sum p90 absolute error | Within20 seconds | Median unshifted sum residual |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
        f"| {sum_mae:.6f} | {max_mae:.6f} | {sum_mae/max_mae:.6f} | {p90:.6f} | {within20:.6%} | {residual:.6f} |",
        "",
        f"Ordering-bank 99% one-sided bounds: sum MAE upper {mae_upper:.6f}, ratio upper {ratio_upper:.6f}, within20 lower {within_lower:.6%}.",
        f"Practical criteria {'PASS' if passed else 'FAIL'} ({'pilot only' if phase=='explore' else 'unchanged frozen internal test'}).",
        "Bank resampling is conditional and may retain path, repeated account and shared-intermediary dependencies.",
        "",
        "## Descriptive controls",
        "",
        "Each displayed cohort requires100 payments, ordering banks, senders and receivers. No control can rescue a failed primary result.",
        "",
        "| Cohort | Payments | Banks | Sum MAE | Max MAE | Endpoint MAE |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for label, condition in [
        ("Indirect","route='Indirect'"),("Covered","route='Covered'"),
        ("Shorter edge below100s","smaller_edge<100"),("Both edges at least100s","smaller_edge>=100"),
        ("May endpoint comparator available","direct_endpoint IS NOT NULL"),
    ]:
        support = c.execute(f"""
            SELECT count(*),count(DISTINCT ordering_bank),count(DISTINCT sender),count(DISTINCT receiver),
            avg(sum_error),avg(max_error),avg(endpoint_error),
            count(DISTINCT ordering_bank) FILTER (WHERE endpoint_error IS NOT NULL),
            count(DISTINCT sender) FILTER (WHERE endpoint_error IS NOT NULL),
            count(DISTINCT receiver) FILTER (WHERE endpoint_error IS NOT NULL)
            FROM scored WHERE {condition}
        """).fetchone()
        if min(support[:4])<100:
            lines.append(f"| {label} | Suppressed | — | — | — | — |")
        else:
            endpoint = f"{support[6]:.6f}" if min(support[7:])>=100 else "Suppressed"
            lines.append(f"| {label} | {support[0]:,} | {support[1]:,} | {support[4]:.6f} | {support[5]:.6f} | {endpoint} |")
    return "\n".join(lines)+"\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase",choices=("explore","confirm"),default="explore")
    parser.add_argument("--freeze")
    args=parser.parse_args()
    upper_month = 6
    if args.phase=="explore":
        if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
            raise ValueError("Discovery cutoff reached")
    else:
        if not args.freeze or len(args.freeze)!=40 or any(x not in "0123456789abcdef" for x in args.freeze):
            raise ValueError("Full Git freeze SHA required")
        subprocess.run(["git","merge-base","--is-ancestor",args.freeze,"HEAD"],cwd=ROOT,check=True)
        original=subprocess.check_output(["git","show",f"{args.freeze}:analysis/20_routing_time/{STEM}.py"],cwd=ROOT)
        plan=subprocess.check_output(["git","show",f"{args.freeze}:findings/hypotheses/{STEM}.md"],cwd=ROOT)
        if original!=Path(__file__).read_bytes().replace(b"\r\n",b"\n") or b"**Status:** confirmation-ready" not in plan:
            raise ValueError("Unchanged code and complete frozen plan required")
        upper_month=7
    with duckdb.connect(config={"memory_limit":"512MB","threads":1,"temp_directory":""}) as c:
        c.execute("SET TimeZone='UTC'")
        c.execute(f"""
            CREATE VIEW source AS
            SELECT TOTAL_DURATION AS duration,PARTICIPANT_COUNT AS visible,month(ts_utc) AS month,
                   TRANSACTION_TYPE_CODE AS route,ORDERING_BIC8 AS ordering_bank,
                   ORDERING_ACCOUNT AS sender,BENEFICIARY_ACCOUNT AS receiver,
                   list_filter(string_split(BIC8_PATH,';'),lambda x:x<>'...') AS p
            FROM read_parquet('dataset/payments.parquet')
            WHERE ANOMALY_TYPE IS NULL AND ts_utc>=TIMESTAMP '2023-05-01'
              AND ts_utc<TIMESTAMP '2023-{upper_month+1:02d}-01'
              AND (('0x'||substr(md5(ORDERING_BIC8),1,8))::UBIGINT%2)=0
              AND (('0x'||substr(md5(BENEFICIARY_BIC8),1,8))::UBIGINT%2)=0
        """)
        report=evaluate(c,args.phase,args.freeze)
    (Path(__file__).parent/"out"/f"{STEM}_{args.phase}.md").write_text(report,encoding="utf-8")
    print("Saved supported B15 aggregate report.")


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source details hidden.", file=sys.stderr)
        sys.exit(1)
