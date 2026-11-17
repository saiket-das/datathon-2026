"""Test which fractional denomination grids explain off-integer amounts.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A17_fractional_denominations.py
Exploration uses only both-account bit-0.
"""
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
STEM = Path(__file__).stem
SPEC = importlib.util.spec_from_file_location("fx", HERE/"H-A03_fx_country_classes.py")
fx = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fx)


def main() -> int:
    """Compare unit, half, quarter and tenth steps against day-shift controls."""
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        return 1
    try:
        with fx.connect() as con:
            con.execute("""CREATE VIEW amounts AS SELECT currency,USD_AMOUNT a,
                CAST(ts_utc AS DATE) d,oa,ba,ob,split
                FROM source WHERE ANOMALY_TYPE IS NULL AND currency IN ('CHF','EUR','GBP')""")
            con.execute("""CREATE TEMP TABLE rates AS WITH masses AS (
                SELECT currency,d,a,pow(10,floor(log10(a))) base,count(*) n
                FROM amounts WHERE split='explore' AND a>=10000 AND a<2000000
                GROUP BY 1,2,3,4 HAVING count(*)>=20
              ), peaks AS (
                SELECT currency,d,base,a/base rate FROM masses
                QUALIFY row_number() OVER(PARTITION BY currency,d ORDER BY base DESC,n DESC,a)=1
              ) SELECT *,lead(rate,7) OVER(PARTITION BY currency ORDER BY d) shifted FROM peaks""")
            con.execute("""CREATE VIEW scored AS SELECT x.*,base,rate,shifted
              FROM amounts x LEFT JOIN rates USING(currency,d)
              WHERE split='explore' AND a>=10 AND a<900""")
            coverage = fx.query(con,"""SELECT currency,count(*) scoped,count(shifted) eligible,
                count(DISTINCT oa) FILTER(WHERE shifted IS NOT NULL) senders,
                count(DISTINCT ba) FILTER(WHERE shifted IS NOT NULL) receivers
                FROM scored GROUP BY 1 ORDER BY 1""")
            grids = fx.query(con,"""WITH phases AS (
                SELECT currency,d,grid,
                    a/rate own, a/shifted wrong,
                    (0.005+0.005*a/rate/base+1e-8)/rate own_tol,
                    (0.005+0.005*a/shifted/base+1e-8)/shifted wrong_tol
                FROM scored CROSS JOIN (VALUES (1),(2),(4),(10)) g(grid)
                WHERE shifted IS NOT NULL
              ), scores AS (
                SELECT *,
                    abs(own-round(own*grid)/grid)<=own_tol own_hit,
                    abs(wrong-round(wrong*grid)/grid)<=wrong_tol shifted_hit,
                    abs(own-round(own))<=own_tol own_unit,
                    abs(wrong-round(wrong))<=wrong_tol shifted_unit
                FROM phases
              ), daily AS (
                SELECT currency,grid,d,count(*) n,
                  count(*) FILTER(WHERE NOT own_unit) off_unit,
                  sum(own_hit::INT) own_hits,sum(shifted_hit::INT) shifted_hits,
                  sum((own_hit AND NOT own_unit)::INT) own_extra,
                  sum((shifted_hit AND NOT shifted_unit)::INT) shifted_extra,
                  sum((shifted_hit AND NOT shifted_unit AND NOT own_unit)::INT) paired_shifted_extra
                FROM scores GROUP BY 1,2,3
              ) SELECT currency,grid,sum(n) n,sum(own_hits)/sum(n) own_rate,
                sum(shifted_hits)/sum(n) shifted_rate,
                sum(own_extra)/sum(n) extra_own,sum(shifted_extra)/sum(n) extra_shifted,
                sum(off_unit) off_unit,
                sum(own_extra)/sum(off_unit) own_among_off_unit,
                sum(paired_shifted_extra)/sum(off_unit) shifted_among_off_unit,
                count(*) FILTER(WHERE n>=100) supported_dates,
                avg((own_extra-paired_shifted_extra)/off_unit) FILTER(WHERE off_unit>=100) equal_date_paired_gain
              FROM daily GROUP BY 1,2 ORDER BY 1,2""")
            rows = con.execute("""WITH amounts AS (
                SELECT currency,d,a/rate own,a/shifted wrong,
                    (0.005+0.005*a/rate/base+1e-8)/rate tolerance,
                    (0.005+0.005*a/shifted/base+1e-8)/shifted wrong_tol
                FROM scored WHERE shifted IS NOT NULL
            ), phases AS (
                SELECT *,round((own-0.05)*10)::BIGINT phase_index,
                   abs(own-0.05-round((own-0.05)*10)/10)<=tolerance phase_hit
                FROM amounts
            ) SELECT currency,d,count(*) n,
                sum((abs(own-round(own*10)/10)<=tolerance)::INT) aligned,
                sum((abs(wrong-round(wrong*10)/10)<=wrong_tol
                     AND abs(wrong-round(wrong))>wrong_tol)::INT) shifted,
                sum(phase_hit::INT) half_phase,
                sum((phase_hit AND phase_index%10<>0)::INT) phase_remove_low,
                sum((phase_hit AND phase_index%10<>9)::INT) phase_remove_high
            FROM phases WHERE abs(own-round(own))>tolerance
            GROUP BY 1,2 ORDER BY 1,2""").fetchall()
            by_currency = {currency:np.asarray([row[2:] for row in rows if row[0]==currency])
                           for currency in ("CHF","EUR","GBP")}
            rng = np.random.default_rng(20261117)
            decisions = []
            coverages = {row[0]:row[2]/row[1] for row in coverage[1]}
            for currency, daily in by_currency.items():
                n, aligned, shifted, half_phase, phase_low, phase_high = daily.sum(axis=0)
                assert max(aligned,shifted,half_phase)<=n and max(phase_low,phase_high)<=half_phase
                draws = []
                for _ in range(1000):
                    starts = rng.integers(len(daily),size=int(np.ceil(len(daily)/7)))
                    indices = ((starts[:,None]+np.arange(7))%len(daily)).ravel()[:len(daily)]
                    b_n,b_a,b_s,_,b_low,b_high = daily[indices].sum(axis=0)
                    draws.append(((b_a-b_s)/b_n,(b_a-b_low)/b_n,(b_a-b_high)/b_n))
                low,high = np.quantile(draws,[.005,.995],axis=0)
                passed = (coverages[currency]>=.75 and n>=10000 and len(daily)>=40
                          and min(low)>=.005)
                decisions.append((currency,n,len(daily),aligned/n,shifted/n,half_phase/n,
                    phase_low/n,phase_high/n,float(low[0]),float(high[0]),
                    float(low[1]),float(high[1]),float(low[2]),float(high[2]),passed))
            decision = (["currency","off_unit","dates","aligned","shifted","half_phase",
                         "phase_drop_05","phase_drop_95","shift_low99","shift_high99",
                         "drop_05_low99","drop_05_high99","drop_95_low99","drop_95_high99","pass"],
                        decisions)
        report = fx.render("H-A17 — Fractional denomination grids",
                           {"Scoped small payments":coverage,"Nested grid comparisons":grids,
                            "Tenth-unit tests with seven-date block sensitivity":decision},
                           "exploration")
        report = report.replace(
            "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
            "Both-account bit-0 only. Phase 0 and A01–A16 prior exposure applies.")
        report += ("\nGrid 2 is half-unit, 4 is quarter-unit and 10 is tenth-unit. "
                   "Extra shares exclude hits on the corresponding scale's integer grid, and use "
                   "the same eligible denominator. The shifted date controls accidental fit. "
                   "Paired differences condition both comparisons on the same-day off-unit subset. "
                   "Equal-date paired differences use dates with at least 100 off-unit payments. "
                   "Phase controls shift by .05 and then remove either the .05 or the .95 slot, "
                   "so each has nine candidate points per unit, as does the off-integer tenth grid.\n")
        (HERE/f"out/{STEM}_explore.md").write_text(report,encoding="utf-8")
        print("OK: aggregate denomination exploration saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())
