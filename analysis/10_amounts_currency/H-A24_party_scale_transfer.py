"""Explore transfer of amount-implied currency scales across sender party types.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A24_party_scale_transfer.py
Frozen internal re-extraction: add --freeze SHA. Date-specific scales stay local.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import subprocess
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("fx",HERE/"H-A03_fx_country_classes.py")
fx = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fx)


def main() -> int:
    """Fit separate B/C peaks and compare them on common date support."""
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze")
    args=parser.parse_args()
    phase="validate" if args.freeze else "explore"
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        return 1
    try:
        if args.freeze:
            subprocess.run(["git","merge-base","--is-ancestor",args.freeze,"HEAD"],
                           cwd=fx.ROOT,check=True,capture_output=True)
            files=(Path(__file__).resolve(),Path(fx.__file__),Path(fx.foundation.__file__),
                   fx.ROOT/"findings/hypotheses/H-A24_party_scale_transfer.md")
            marker=b"\n## Confirmation and robustness results"
            for path in files:
                old=subprocess.check_output(
                    ["git","show",f"{args.freeze}:{path.relative_to(fx.ROOT).as_posix()}"],
                    cwd=fx.ROOT,stderr=subprocess.DEVNULL,
                ).replace(b"\r\n",b"\n")
                if old.split(marker)[0]!=path.read_bytes().replace(b"\r\n",b"\n").split(marker)[0]:
                    raise ValueError("Freeze mismatch")
        with fx.connect() as con:
            split=fx.foundation.partition_sql("accounts")
            chosen="confirm" if args.freeze else "explore"
            con.execute(f"""CREATE VIEW amounts AS SELECT CURRENCY_CODE currency,
                USD_AMOUNT a,CAST(ts_utc AS DATE) d,ORDERING_TYPE sender_type,
                ORDERING_TYPE||BENEFICIARY_TYPE pair,ORDERING_ACCOUNT oa,
                BENEFICIARY_ACCOUNT ba
                FROM read_parquet('dataset/payments.parquet')
                WHERE {split}='{chosen}' AND ANOMALY_TYPE IS NULL
                  AND CURRENCY_CODE IN ('EUR','USD','GBP','CHF')
                  AND USD_AMOUNT>0""")
            con.execute("""CREATE TEMP TABLE rates AS WITH masses AS (
                SELECT currency,d,sender_type,a,pow(10,floor(log10(a))) base,count(*) n
                FROM amounts WHERE a>=1000 AND a<2000000 GROUP BY 1,2,3,4,5
                HAVING count(*)>=20
              ) SELECT currency,d,sender_type,base,a/base rate,n
                FROM masses QUALIFY row_number() OVER(PARTITION BY currency,d,sender_type
                    ORDER BY base DESC,n DESC,a)=1""")
            con.execute("""CREATE TEMP TABLE joined AS SELECT b.currency,b.d,
                b.rate business_rate,b.base business_base,c.rate consumer_rate,c.base consumer_base
                FROM rates b JOIN rates c USING(currency,d)
                WHERE b.sender_type='B' AND c.sender_type='C'""")
            tables={}
            tables["Date support and scale comparison"] = fx.query(con,"""SELECT currency,
                count(*) dates,min(consumer_base) min_consumer_base,
                max(consumer_base) max_consumer_base,
                avg((abs(ln(business_rate/consumer_rate))<0.0001)::INT) near_equal,
                avg((abs(ln(business_rate/consumer_rate))>ln(1.5))::INT) large_ratio,
                min(business_rate/consumer_rate) minimum_ratio,
                max(business_rate/consumer_rate) maximum_ratio
                FROM joined GROUP BY currency ORDER BY currency""")
            con.execute("""CREATE VIEW scored AS
                SELECT a.*,business_rate,business_base,consumer_rate,consumer_base,
                  (abs(a-business_rate*round(a/business_rate))<=
                    .005+.005*a/business_rate/business_base+1e-8)::INT business_hit,
                  (abs(a-consumer_rate*round(a/consumer_rate))<=
                    .005+.005*a/consumer_rate/consumer_base+1e-8)::INT consumer_hit
                FROM amounts a JOIN joined USING(currency,d) WHERE a>=10 AND a<900""")
            tables["Common support by scored party pair"] = fx.query(con,"""
              SELECT currency,pair,count(*) n,count(DISTINCT oa) senders,
                count(DISTINCT ba) receivers,count(DISTINCT d) dates,
                avg(business_hit) business_fit,avg(consumer_hit) consumer_fit,
                avg((business_hit<>consumer_hit)::INT) different_fit
              FROM scored GROUP BY 1,2 HAVING count(*)>=1000
                AND count(DISTINCT oa)>=100 AND count(DISTINCT ba)>=100 ORDER BY 1,2""")
            tables["Small-amount coverage"] = fx.query(con,"""SELECT currency,count(*) scoped,
                count(*) FILTER(WHERE d IN (SELECT d FROM joined j WHERE j.currency=a.currency)) covered
                FROM amounts a WHERE a>=10 AND a<900 GROUP BY currency ORDER BY currency""")
            rng=np.random.default_rng(20261117)
            decisions=[]
            for pair in ("BB","BC","CB","CC"):
                daily=np.asarray(con.execute("""SELECT count(*),sum((business_hit<>consumer_hit)::INT)
                    FROM scored WHERE currency='EUR' AND pair=? GROUP BY d ORDER BY d""",[pair]).fetchall())
                n,errors=daily.sum(axis=0)
                resampled=[]
                for _ in range(1000):
                    starts=rng.integers(len(daily),size=int(np.ceil(len(daily)/7)))
                    indices=((starts[:,None]+np.arange(7))%len(daily)).ravel()[:len(daily)]
                    b_n,b_errors=daily[indices].sum(axis=0)
                    resampled.append(b_errors/b_n)
                low,high=np.quantile(resampled,[.005,.995])
                display=any(row[0]=="EUR" and row[1]==pair for row in tables["Common support by scored party pair"][1])
                decisions.append((pair,int(n),errors/n,float(low),float(high),bool(display and high<=.002)))
            eur=next(row for row in tables["Date support and scale comparison"][1] if row[0]=="EUR")
            cov=next(row for row in tables["Small-amount coverage"][1] if row[0]=="EUR")
            passed=bool(eur[1]>=50 and eur[4]>=.99 and cov[2]/cov[1]>=.60
                        and all(row[-1] for row in decisions))
            tables["EUR paired date-block sensitivity"]=(["pair","n","disagreement","low99","high99","pass"],decisions)
            tables["EUR primary decision"]=(["all_criteria_met"],[(passed,)])
            assert all(0<=row[4]<=1 for row in tables["Date support and scale comparison"][1])
        report=fx.render("H-A24 — Party-specific scale extraction",tables,args.freeze or "exploration only")
        if not args.freeze:
            report=report.replace(
                "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
                "Unlabelled both-account bit-0 only. A01–A23 and Phase 0 outcome exposure applies.")
        report+=("\nB and C training groups have separate source records but share dates and currencies. "
                  "Unknown latent denomination can multiply a modal scale. Own-date cent tolerance "
                  "uses each trained anchor's magnitude. No hypothesis acceptance follows from compatibility alone.\n")
        (HERE/f"out/H-A24_party_scale_transfer_{phase}.md").write_text(report,encoding="utf-8")
        print("OK: aggregate party-scale exploration saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())
