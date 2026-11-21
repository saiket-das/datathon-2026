"""Test month-to-month persistence of sender log-amount residuals.

Run from repository root:
    uv run python analysis/10_amounts_currency/H-A26_sender_scale_persistence.py
Bit-zero May-to-June exploration only.
"""
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys

import numpy as np

HERE=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("fx",HERE/"H-A03_fx_country_classes.py")
fx=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fx)


def main() -> int:
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        return 1
    phase="explore"
    try:
        split="explore"
        target=6
        with fx.connect() as con:
            partition=fx.foundation.partition_sql("accounts")
            con.execute(f"""CREATE VIEW amounts AS
                SELECT ORDERING_ACCOUNT sender,ORDERING_BIC8 bank,
                  CURRENCY_CODE currency,ORDERING_TYPE||BENEFICIARY_TYPE pair,
                  month(ts_utc) m,ln(USD_AMOUNT) y
                FROM read_parquet('dataset/payments.parquet')
                WHERE ANOMALY_TYPE IS NULL AND USD_AMOUNT>0 AND {partition}='{split}'""")
            con.execute("""CREATE TEMP TABLE groups AS SELECT currency,pair,avg(y) loc
                FROM amounts WHERE m=5 GROUP BY 1,2 HAVING count(*)>=1000""")
            con.execute(f"""CREATE VIEW residuals AS SELECT a.*,y-loc residual FROM amounts a
                JOIN groups USING(currency,pair) WHERE m IN (5,{target})""")
            con.execute(f"""CREATE TEMP TABLE cells AS
                SELECT sender,bank,currency,pair,
                  avg(residual) FILTER(WHERE m=5) before_mean,
                  avg(residual) FILTER(WHERE m={target}) after_mean,
                  count(*) FILTER(WHERE m=5) before_n,count(*) FILTER(WHERE m={target}) after_n
                FROM residuals GROUP BY 1,2,3,4
                HAVING before_n>=10 AND after_n>=10""")
            con.execute("""CREATE TEMP TABLE history AS SELECT *,
                list(before_mean ORDER BY sender) OVER(PARTITION BY currency,pair,bank) history_means,
                row_number() OVER(PARTITION BY currency,pair,bank ORDER BY sender) rank_in_group,
                count(*) OVER(PARTITION BY currency,pair,bank) peers
                FROM cells""")
            con.execute("""CREATE TEMP TABLE matched AS SELECT sender,bank,currency,pair,
                before_mean,after_mean,after_n,
                history_means[1+(rank_in_group%peers)] rotated_mean
                FROM history WHERE peers>=2""")
            support=fx.query(con,f"""SELECT
                (SELECT count(*) FROM amounts WHERE m={target}) scoped_target,
                (SELECT count(*) FROM residuals WHERE m={target}) baseline_covered,
                (SELECT count(*) FROM cells) supported_cells,
                count(*) matched_cells,count(DISTINCT sender) senders,
                count(DISTINCT bank) banks,sum(after_n) matched_target_rows
                FROM matched""")
            summary=fx.query(con,"""WITH entities AS (
                SELECT sender,avg(before_mean) before_mean,avg(after_mean) after_mean,
                  avg(pow(after_mean,2)) baseline,
                  avg(pow(after_mean-before_mean,2)) own_error,
                  avg(pow(after_mean-rotated_mean,2)) rotated_error
                FROM matched GROUP BY sender
              )
              SELECT count(*) senders,corr(before_mean,after_mean) month_correlation,
                avg(baseline) baseline_mean_square,avg(own_error) own_history_mean_square,
                avg(rotated_error) peer_history_mean_square,
                avg(own_error)/avg(baseline) own_vs_baseline,
                avg(own_error)/avg(rotated_error) own_vs_peer
              FROM entities""")
            centered=fx.query(con,"""WITH centred_cells AS (
                SELECT sender,
                  before_mean-avg(before_mean) OVER(PARTITION BY bank,currency,pair) b,
                  after_mean-avg(after_mean) OVER(PARTITION BY bank,currency,pair) a,
                  rotated_mean-avg(before_mean) OVER(PARTITION BY bank,currency,pair) r
                FROM matched
              ), entities AS (
                SELECT sender,avg(b) b,avg(a) a,
                  avg(pow(a,2)) base,avg(pow(a-b,2)) own,avg(pow(a-r,2)) peer
                FROM centred_cells GROUP BY sender
              )
              SELECT count(*) senders,corr(b,a) centred_month_correlation,
                avg(base) baseline,avg(own) own_history_error,avg(peer) peer_history_error,
                avg(own)/avg(base) own_vs_centred_baseline,
                avg(own)/avg(peer) own_vs_centred_peer FROM entities""")
            banks=np.asarray(con.execute("""WITH entities AS (
                SELECT bank,sender,avg(pow(after_mean,2)) base,
                  avg(pow(after_mean-before_mean,2)) own,
                  avg(pow(after_mean-rotated_mean,2)) wrong
                FROM matched GROUP BY bank,sender
              ) SELECT count(*),sum(base),sum(own),sum(wrong)
                FROM entities GROUP BY bank ORDER BY bank""").fetchall(),dtype=float)
            rng=np.random.default_rng(20261117)
            samples=[]
            for _ in range(1000):
                n,base,own,wrong=banks[rng.integers(len(banks),size=len(banks))].sum(axis=0)
                samples.append([own/base,own/wrong])
            bounds=np.quantile(samples,[.005,.995],axis=0)
            intervals=(["comparison","low99","high99"],
                       [(label,*bounds[:,i]) for i,label in enumerate(("own/base","own/peer"))])
            metrics=summary[1][0]
            passed=bool(metrics[0]>=1000 and len(banks)>=100
                        and metrics[1]>=.5 and max(bounds[1])<=.80)
            decision=(["all_criteria_met"],[(passed,)])
            assert support[1][0][0]>=support[1][0][-1]
        report=fx.render("H-A26 — Persistent sender residual scale",
            {"Coverage":support,"Equal-sender paired-month aggregates":summary,
             "Exploratory centering by bank, currency and party in each month":centered,
             "Ordering-bank sensitivity":intervals,"Prespecified decision":decision},
             "exploration")
        report=report.replace(
            "Round 2 internal validation reuses Round 1 account confirmation records; it is not an independent holdout.",
            "Bit-zero May-to-June development only. Phase 0 and A01–A25 exposure applies.")
        report+=("\nEach supported sender/currency/party cell needs at least ten payments "
                   "in both months. The peer is a deterministic different sender from the "
                   "same bank/currency/party group. Repeated histories and grouped target "
                   "means condition on the selected repeated customers.\n")
        (HERE/f"out/H-A26_sender_scale_persistence_{phase}.md").write_text(report,encoding="utf-8")
        print(f"OK: aggregate sender-scale {phase} saved.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())
