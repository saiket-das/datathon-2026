"""Test whether high-value amount peaks predict a low-value currency grid.

Run: uv run python analysis/10_amounts_currency/H-A10_cross_denomination.py
After freezing, add --phase validate --freeze SHA for the internal test.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STEM = Path(__file__).stem
SPEC = importlib.util.spec_from_file_location(
    "fx_model", HERE / "H-A03_fx_country_classes.py"
)
fx = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fx)


def main() -> int:
    """Fit bit-zero anchors and report supported broad aggregates."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=["explore", "validate"], default="explore")
    parser.add_argument("--freeze")
    args = parser.parse_args()
    if datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        print("Research cutoff reached.")
        return 1
    try:
        if args.phase == "validate":
            if not args.freeze:
                raise ValueError("Freeze required.")
            subprocess.run(["git", "merge-base", "--is-ancestor", args.freeze, "HEAD"],
                           cwd=ROOT, check=True, capture_output=True)
            for path in (Path(__file__).resolve(), Path(fx.__file__),
                         Path(fx.foundation.__file__), ROOT / f"findings/hypotheses/{STEM}.md"):
                old = subprocess.check_output(
                    ["git", "show", f"{args.freeze}:{path.relative_to(ROOT).as_posix()}"],
                    cwd=ROOT, stderr=subprocess.DEVNULL,
                ).replace(b"\r\n", b"\n")
                new = path.read_bytes().replace(b"\r\n", b"\n")
                marker = b"\n## Confirmation and robustness results"
                if old.split(marker)[0] != new.split(marker)[0]:
                    raise ValueError("Freeze mismatch.")
        with fx.connect() as con:
            con.execute("""CREATE VIEW amounts AS SELECT currency,USD_AMOUNT a,
                CAST(ts_utc AS DATE) d,oa,ba,split,route
                FROM source WHERE ANOMALY_TYPE IS NULL
                  AND currency IN ('CHF','GBP','SGD','EUR','USD')""")
            con.execute("""CREATE TEMP TABLE rates AS
                WITH masses AS (
                    SELECT currency,d,a,pow(10,floor(log10(a))) base,count(*) n
                    FROM amounts WHERE split='explore' AND a>=10000 AND a<2000000
                    GROUP BY 1,2,3,4 HAVING count(*)>=20
                ), peaks AS (
                    SELECT currency,d,base,a/base scale FROM masses
                    QUALIFY row_number() OVER(PARTITION BY currency,d
                        ORDER BY base DESC,n DESC,a)=1
                )
                SELECT *,lead(scale,7) OVER(PARTITION BY currency ORDER BY d) wrong,
                  median(scale) OVER(PARTITION BY currency) fixed FROM peaks""")
            split = "confirm" if args.phase == "validate" else "explore"
            con.execute(f"""CREATE VIEW eligible AS
                SELECT x.*,base,scale,wrong,fixed FROM amounts x
                JOIN rates USING(currency,d) WHERE x.split='{split}'
                  AND wrong IS NOT NULL AND a>=10 AND a<900""")
            con.execute("""CREATE VIEW scored AS SELECT *,
                (abs(a-scale*round(a/scale))<=0.005+0.005*a/scale/base+1e-8)::INT daily,
                (abs(a-wrong*round(a/wrong))<=0.005+0.005*a/wrong/base+1e-8)::INT shifted,
                (abs(a-fixed*round(a/fixed))<=0.005+0.005*a/fixed/base+1e-8)::INT constant
                FROM eligible""")
            summaries = fx.query(con, f"""WITH scope AS (
                    SELECT currency,count(*) scoped FROM amounts
                    WHERE split='{split}' AND a>=10 AND a<900 GROUP BY 1
                ), by_date AS (
                    SELECT currency,d,count(*) n,avg(daily-greatest(shifted,constant)) lift
                    FROM scored GROUP BY 1,2 HAVING count(*)>=100
                ), stability AS (
                    SELECT currency,count(*) supported_dates,avg(lift) equal_date_lift,
                        avg((lift>=0.1)::INT) positive_date_share
                    FROM by_date GROUP BY 1
                ), pooled AS (
                    SELECT currency,count(*) n,count(DISTINCT oa) senders,
                        count(DISTINCT ba) receivers,avg(daily) daily_fit,
                        avg(shifted) shifted_fit,avg(constant) constant_fit,
                        avg(daily-shifted) lift_shift,avg(daily-constant) lift_constant
                    FROM scored GROUP BY 1 HAVING count(*)>=1000
                    AND count(DISTINCT oa)>=100 AND count(DISTINCT ba)>=100
                )
                SELECT p.*,scoped,n/scoped coverage,supported_dates,equal_date_lift,positive_date_share,
                    coalesce(n/scoped>=0.50 AND supported_dates>=30 AND daily_fit>=0.25
                    AND least(lift_shift,lift_constant)>=0.20 AND positive_date_share>=0.80,false)
                    passes_screen
                FROM pooled p JOIN scope USING(currency) LEFT JOIN stability USING(currency)
                ORDER BY currency""")
        assert len(summaries[1]) == 5
        report = fx.render("H-A10 — High-value peaks and low-value rounding",
            {"Coverage, negative controls and date stability": summaries}, args.freeze or "exploration")
        if args.phase == "explore":
            report = report.replace("Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
                                    "Both-account bit-0 exploration only.")
        report += ("\nUSD is a constant-scale check. EUR is a benchmark with prior outcome exposure. "
                   "CHF and GBP are primary. SGD tests the scope limit. Dates with under 100 "
                   "eligible payments contribute to pooled results only. No daily rates are exported.\n")
        (HERE / f"out/{STEM}_{args.phase}.md").write_text(report, encoding="utf-8")
        print(f"OK: aggregate cross-denomination {args.phase} saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
