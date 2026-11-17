"""Screen preferred mantissa-five amounts after inferred currency scaling.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A25_scaled_five_anchor.py
After freeze add --freeze SHA. Exact daily rates and identifiers remain local.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import subprocess
import sys

import numpy as np

HERE=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("fx",HERE/"H-A03_fx_country_classes.py")
fx=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fx)


def main() -> int:
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
            paths=(Path(__file__).resolve(),Path(fx.__file__),Path(fx.foundation.__file__),
                   fx.ROOT/"findings/hypotheses/H-A25_scaled_five_anchor.md")
            marker=b"\n## Confirmation and robustness results"
            for path in paths:
                old=subprocess.check_output(
                    ["git","show",f"{args.freeze}:{path.relative_to(fx.ROOT).as_posix()}"],
                    cwd=fx.ROOT,stderr=subprocess.DEVNULL,
                ).replace(b"\r\n",b"\n")
                if old.split(marker)[0]!=path.read_bytes().replace(b"\r\n",b"\n").split(marker)[0]:
                    raise ValueError("Freeze mismatch")
        split="confirm" if args.freeze else "explore"
        with fx.connect() as con:
            con.execute("""CREATE VIEW amounts AS SELECT currency,USD_AMOUNT a,
                CAST(ts_utc AS DATE) d,oa,ba,ob,split FROM source
                WHERE ANOMALY_TYPE IS NULL AND USD_AMOUNT>0
                  AND currency IN ('EUR','CHF','GBP','USD')""")
            con.execute("""CREATE TEMP TABLE rates AS WITH masses AS (
                SELECT currency,d,a,pow(10,floor(log10(a))) base,count(*) n
                FROM amounts WHERE split='explore' AND a>=10000 AND a<2000000
                GROUP BY 1,2,3,4 HAVING count(*)>=20
              ) SELECT currency,d,base,a/base rate FROM masses
                QUALIFY row_number() OVER(PARTITION BY currency,d
                    ORDER BY base DESC,n DESC,a)=1""")
            con.execute(f"""CREATE VIEW selected AS WITH scaled AS (
                SELECT a.*,base,rate,a/rate native,
                    pow(10,floor(log10(a/rate))) place
                FROM amounts a JOIN rates USING(currency,d) WHERE a<9000 AND split='{split}'
              ), windows AS (
                SELECT *,round(native/place)::INT digit,
                    abs(a-rate*round(native/place)*place)<=
                        .005+.005*round(native/place)*place/base+1e-8 point
                FROM scaled WHERE floor(log10(native)) BETWEEN 2 AND 3
              ) SELECT * FROM windows WHERE digit BETWEEN 4 AND 8
                    AND 8.4*rate*place<9000
                    AND abs(native/place-digit)<=.4""")
            # Complete anchor families are published only when each point and background has broad support.
            families=con.execute("""SELECT currency,digit,count(*) n,
                count(*) FILTER(WHERE point) point_n,
                count(DISTINCT oa) FILTER(WHERE point) point_senders,
                count(DISTINCT ba) FILTER(WHERE point) point_receivers,
                count(*) FILTER(WHERE NOT point) background_n,
                count(DISTINCT oa) FILTER(WHERE NOT point) background_senders,
                count(DISTINCT ba) FILTER(WHERE NOT point) background_receivers
                FROM selected GROUP BY 1,2 ORDER BY 1,2""").fetchall()
            support=fx.query(con,f"""SELECT currency,
                (SELECT count(*) FROM amounts x WHERE x.currency=s.currency AND a<9000 AND split='{split}') scoped,
                count(*) selected,count(DISTINCT oa) senders,count(DISTINCT ba) receivers,
                count(DISTINCT d) dates FROM selected s GROUP BY currency ORDER BY currency""")
            safe=[]
            odds=[]
            rng=np.random.default_rng(20261117)
            for currency in ("CHF","EUR","GBP","USD"):
                family=[row for row in families if row[0]==currency]
                complete=(len(family)==5 and all(min(row[3:])>=100 for row in family))
                if not complete:
                    odds.append((currency,"insufficient point/background entity support",
                                 None,None,None,None,None,False))
                    continue
                assert all(row[2]==row[3]+row[6] for row in family)
                bank_rows=con.execute("""SELECT ob,digit,count(*) FILTER(WHERE point),
                    count(*) FILTER(WHERE NOT point) FROM selected WHERE currency=?
                    GROUP BY ob,digit ORDER BY ob,digit""",[currency]).fetchall()
                banks={}
                for bank,digit,points,background in bank_rows:
                    banks.setdefault(bank,np.zeros((5,2)))[digit-4]=points,background
                stats=np.asarray(list(banks.values()))
                def contrasts(counts: np.ndarray) -> np.ndarray:
                    primary=(counts[1,0]/counts[1,1])/(
                        (counts[0,0]+counts[2,0])/(counts[0,1]+counts[2,1]))
                    control=(counts[3,0]/counts[3,1])/(
                        (counts[2,0]+counts[4,0])/(counts[2,1]+counts[4,1]))
                    return np.asarray([primary,control])
                estimate=contrasts(stats.sum(axis=0))
                draws=[contrasts(stats[rng.integers(len(stats),size=len(stats))].sum(axis=0))
                       for _ in range(1000)]
                low,high=np.quantile(draws,[.005,.995],axis=0)
                n_dates=next(row[-1] for row in support[1] if row[0]==currency)
                passed=bool(low[0]>=3 and low[1]>=.5 and high[1]<=2 and
                            len(stats)>=100 and n_dates>=50)
                safe.extend(family)
                odds.append((currency,float(estimate[0]),float(low[0]),float(high[0]),
                             float(estimate[1]),float(low[1]),float(high[1]),passed))
            tables={"Amount-window scope":support,
                "Complete supported anchor families":(
                    ["currency","digit","n","points","point_senders","point_receivers",
                     "background","background_senders","background_receivers"],safe),
                "Mantissa-five point-background odds relative to four and six":(
                    ["currency","five_ratio_or_support","five_low99","five_high99",
                     "seven_control","seven_low99","seven_high99","pass"],odds)}
        report=fx.render("H-A25 — Scaled preferred mantissa-five screen",tables,args.freeze or "exploration")
        if not args.freeze:
            report=report.replace(
                "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
                "Both-account bit-0 only. Phase 0 and A01–A24 exposure applies.")
        report+=("\nAnchor fitting amounts are at least USD10,000 and evaluation under USD9,000. "
                   "Scale inference can alias denominations. Cent compatibility creates chance point hits. "
                   "No iid interval or exact rounding operator follows from these odds.\n")
        (HERE/f"out/H-A25_scaled_five_anchor_{phase}.md").write_text(report,encoding="utf-8")
        print("OK: aggregate scaled anchor exploration saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())
