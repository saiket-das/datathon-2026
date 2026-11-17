"""Explore the effective UTC date boundary of amount-implied scales.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A19_utc_scale_boundary.py
Frozen internal comparison: add --freeze SHA. Date and rate values stay in memory.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import subprocess
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("fx", HERE/"H-A03_fx_country_classes.py")
fx = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fx)


def main() -> int:
    """Compare rates from the preceding, current and following UTC dates."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze")
    args = parser.parse_args()
    phase = "validate" if args.freeze else "explore"
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        return 1
    try:
        if args.freeze:
            subprocess.run(["git","merge-base","--is-ancestor",args.freeze,"HEAD"],
                           cwd=fx.ROOT,check=True,capture_output=True)
            files = (Path(__file__).resolve(),Path(fx.__file__),Path(fx.foundation.__file__),
                     fx.ROOT/"findings/hypotheses/H-A19_utc_scale_boundary.md")
            marker = b"\n## Confirmation and robustness results"
            for path in files:
                frozen = subprocess.check_output(
                    ["git","show",f"{args.freeze}:{path.relative_to(fx.ROOT).as_posix()}"],
                    cwd=fx.ROOT,stderr=subprocess.DEVNULL,
                ).replace(b"\r\n",b"\n")
                if frozen.split(marker)[0]!=path.read_bytes().replace(b"\r\n",b"\n").split(marker)[0]:
                    raise ValueError("Freeze mismatch")
        split = "confirm" if args.freeze else "explore"
        with fx.connect() as con:
            con.execute("""CREATE VIEW amounts AS SELECT currency,USD_AMOUNT a,
                CAST(ts_utc AS DATE) d,hour(ts_utc) utc_hour,oa,ba,split
                FROM source WHERE ANOMALY_TYPE IS NULL
                  AND currency IN ('CHF','EUR','GBP')""")
            con.execute("""CREATE TEMP TABLE rates AS WITH masses AS (
                SELECT currency,d,a,pow(10,floor(log10(a))) base,count(*) n
                FROM amounts WHERE split='explore' AND a>=10000 AND a<2000000
                GROUP BY 1,2,3,4 HAVING count(*)>=20
              ) SELECT currency,d,base,a/base rate FROM masses
                QUALIFY row_number() OVER(PARTITION BY currency,d
                    ORDER BY base DESC,n DESC,a)=1""")
            con.execute(f"""CREATE VIEW scored AS
                SELECT x.currency,x.d,x.utc_hour,x.oa,x.ba,x.a,
                   c.rate current_rate,c.base current_base,
                   p.rate previous_rate,p.base previous_base,
                   f.rate next_rate,f.base next_base
                FROM amounts x LEFT JOIN rates c ON x.currency=c.currency AND x.d=c.d
                LEFT JOIN rates p ON x.currency=p.currency AND x.d-1=p.d
                LEFT JOIN rates f ON x.currency=f.currency AND x.d+1=f.d
                WHERE x.split='{split}' AND x.a>=10 AND x.a<900""")
            tables = {}
            tables["Coverage"] = fx.query(con,"""SELECT currency,count(*) scoped,
                count(*) FILTER(WHERE previous_rate IS NOT NULL AND next_rate IS NOT NULL
                     AND current_rate IS NOT NULL) eligible
                FROM scored GROUP BY 1 ORDER BY 1""")
            con.execute("""CREATE VIEW fit AS
                SELECT currency,d,oa,ba,CASE WHEN utc_hour<2 THEN '00–01'
                    WHEN utc_hour>=22 THEN '22–23' ELSE '02–21' END utc_window,
                    (abs(a-current_rate*round(a/current_rate))<=
                      .005+.005*a/current_rate/current_base+1e-8)::INT current_hit,
                    (abs(a-previous_rate*round(a/previous_rate))<=
                      .005+.005*a/previous_rate/previous_base+1e-8)::INT previous_hit,
                    (abs(a-next_rate*round(a/next_rate))<=
                      .005+.005*a/next_rate/next_base+1e-8)::INT next_hit
                FROM scored WHERE current_rate IS NOT NULL AND previous_rate IS NOT NULL
                    AND next_rate IS NOT NULL""")
            tables["UTC hour-window comparison"] = fx.query(con,"""WITH grouped AS (
                SELECT currency,utc_window,count(*) n,count(DISTINCT d) n_dates,
                  count(DISTINCT oa) senders,count(DISTINCT ba) receivers,
                  avg(current_hit) current_share,avg(previous_hit) previous_share,
                  avg(next_hit) next_share
                FROM fit GROUP BY 1,2 HAVING count(*)>=1000
                  AND count(DISTINCT oa)>=100 AND count(DISTINCT ba)>=100
             ) SELECT * FROM grouped ORDER BY currency,utc_window""")
            rng = np.random.default_rng(20261117)
            eur_scope,eur_eligible = next(row[1:] for row in tables["Coverage"][1] if row[0]=="EUR")
            decisions = []
            for window in ("00–01","22–23"):
                daily = np.asarray(con.execute("""SELECT count(*),sum(current_hit),
                    sum(current_hit-greatest(previous_hit,next_hit))
                    FROM fit WHERE currency='EUR' AND utc_window=? GROUP BY d ORDER BY d""",
                    [window]).fetchall())
                n, hits, lift = daily.sum(axis=0)
                assert n>=hits>=0 and abs(lift)<=n
                estimates = []
                for _ in range(1000):
                    starts = rng.integers(len(daily),size=int(np.ceil(len(daily)/7)))
                    indices = ((starts[:,None]+np.arange(7))%len(daily)).ravel()[:len(daily)]
                    b_n,_,b_lift = daily[indices].sum(axis=0)
                    estimates.append(b_lift/b_n)
                low,high = np.quantile(estimates,[.005,.995])
                passed = (eur_eligible/eur_scope>=.95 and n>=1000 and len(daily)>=50
                          and hits/n>=.30 and low>=.25)
                decisions.append((window,n,len(daily),hits/n,lift/n,float(low),float(high),passed))
            tables["EUR boundary tests versus union of adjacent-date hits"] = (
                ["window","n","dates","own_share","lift","lift_low99","lift_high99","pass"],decisions)
        report = fx.render("H-A19 — Effective UTC date of implied scales",tables,args.freeze or "exploration")
        if not args.freeze:
            report = report.replace(
                "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
                "Both-account bit-0 only. Phase 0 and A01–A18 prior exposure applies.")
        report += ("\nThe same rows are scored with the previous, current and next calendar "
                   "date's rate. All three anchors must be supported. "
                   "EUR is primary. CHF and GBP hour windows are descriptive.\n")
        (HERE/f"out/H-A19_utc_scale_boundary_{phase}.md").write_text(report,encoding="utf-8")
        print("OK: aggregate UTC boundary screen saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())
