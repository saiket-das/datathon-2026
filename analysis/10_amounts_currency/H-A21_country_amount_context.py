"""Explore endpoint-country context in log amounts beyond currency and party types.

Run: uv run python analysis/10_amounts_currency/H-A21_country_amount_context.py
Fit pre-July both-account bit-0, score July bit-0. Export grouped metrics only.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys
import subprocess

import duckdb
import numpy as np

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("foundation", HERE.parent / "00_prep/scientific_checks.py")
foundation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(foundation)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',choices=['explore','validate'],default='explore')
    parser.add_argument('--freeze')
    args=parser.parse_args()
    if args.phase=='explore' and datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        return 1
    try:
        if args.phase=='validate':
            if not args.freeze:
                raise ValueError('Freeze required')
            root=HERE.parents[1]
            subprocess.run(['git','merge-base','--is-ancestor',args.freeze,'HEAD'],cwd=root,check=True,capture_output=True)
            for path in [Path(__file__).resolve(),Path(foundation.__file__)]:
                frozen=subprocess.check_output(['git','show',f'{args.freeze}:{path.relative_to(root).as_posix()}'],cwd=root)
                if frozen.replace(b'\r\n',b'\n')!=path.read_bytes().replace(b'\r\n',b'\n'):
                    raise ValueError('Freeze mismatch')
        with duckdb.connect() as con:
            con.execute("SET memory_limit='512MB'; SET threads=1; SET temp_directory=''; SET preserve_insertion_order=false")
            split=foundation.partition_sql("accounts")
            source=f"""SELECT
                CURRENCY_CODE currency,ORDERING_TYPE||BENEFICIARY_TYPE parties,
                ln(USD_AMOUNT) y,ORDERING_ACCOUNT sender,BENEFICIARY_ACCOUNT receiver,ORDERING_BIC8 bank,
                substr(split_part(BIC8_PATH,';',1),5,2) path_send,
                substr(list_extract(string_split(BIC8_PATH,';'),-1),5,2) path_receive,
                ts_utc<TIMESTAMP '2023-07-01' training
                FROM read_parquet('dataset/payments.parquet')
                WHERE ANOMALY_TYPE IS NULL AND USD_AMOUNT>0 AND {split}='explore'"""
            con.execute(f'CREATE VIEW scope AS {source}')
            con.execute("""CREATE TEMP TABLE baseline AS SELECT currency,parties,avg(y) prediction
                FROM scope WHERE training GROUP BY currency,parties HAVING count(*)>=1000""")
            con.execute("""CREATE VIEW residuals AS SELECT s.*,b.prediction,y-b.prediction residual
                FROM scope s JOIN baseline b USING(currency,parties)""")
            for role in ("send","receive"):
                con.execute(f"""CREATE TEMP TABLE {role}_fit AS
                    SELECT path_{role} country,avg(residual) effect
                    FROM residuals WHERE training GROUP BY 1 HAVING count(*)>=100""")
            evaluation=source.replace("='explore'","='confirm'") if args.phase=='validate' else source
            con.execute(f'CREATE VIEW evaluation AS {evaluation}')
            con.execute("""CREATE VIEW evaluation_residuals AS SELECT s.*,b.prediction,y-b.prediction residual
                FROM evaluation s JOIN baseline b USING(currency,parties)""")
            con.execute("""CREATE TEMP TABLE wrong_fit AS
                SELECT country,list(effect ORDER BY country) OVER()[
                    1+((row_number() OVER(ORDER BY country)-1+7)%count(*) OVER())
                ] effect FROM send_fit""")
            con.execute("""CREATE VIEW scored AS
                SELECT r.*,s.effect send_effect,b.effect receive_effect,w.effect wrong_effect
                FROM evaluation_residuals r JOIN send_fit s ON r.path_send=s.country
                JOIN receive_fit b ON r.path_receive=b.country
                JOIN wrong_fit w ON r.path_send=w.country WHERE NOT training""")
            result=con.execute("""SELECT count(*) n,count(DISTINCT sender) senders,
                count(DISTINCT receiver) receivers,round(avg(residual*residual),6) baseline_mse,
                round(avg(pow(residual-send_effect,2))/avg(residual*residual),6) send_mse_ratio,
                round(avg(pow(residual-receive_effect,2))/avg(residual*residual),6) receive_mse_ratio,
                round(avg(pow(residual-wrong_effect,2))/avg(residual*residual),6) wrong_mse_ratio,
                round(avg(pow(residual-send_effect-receive_effect,2))/avg(residual*residual),6) additive_mse_ratio,
                round(avg(residual),6) baseline_bias,
                round(avg(residual-send_effect-receive_effect),6) additive_bias
                FROM scored""")
            coverage=([c[0] for c in result.description],result.fetchall())
            result=con.execute("""SELECT parties,count(*) n,count(DISTINCT sender) senders,
                count(DISTINCT receiver) receivers,
                round(avg(pow(residual-send_effect-receive_effect,2))/avg(residual*residual),6) additive_mse_ratio
                FROM scored GROUP BY parties HAVING count(*)>=1000
                  AND count(DISTINCT sender)>=100 AND count(DISTINCT receiver)>=100 ORDER BY parties""")
            strata=([c[0] for c in result.description],result.fetchall())
            result=con.execute("""SELECT count(*) sender_groups,
                round(avg(base_loss),6) baseline_mse,
                round(avg(send_loss)/avg(base_loss),6) send_mse_ratio,
                round(avg(receive_loss)/avg(base_loss),6) receiver_mse_ratio,
                round(avg(wrong_loss)/avg(base_loss),6) wrong_mse_ratio
                FROM (
                    SELECT sender,avg(pow(residual,2)) base_loss,
                        avg(pow(residual-send_effect,2)) send_loss,
                        avg(pow(residual-receive_effect,2)) receive_loss,
                        avg(pow(residual-wrong_effect,2)) wrong_loss
                    FROM scored GROUP BY sender
                ) accounts""")
            balanced=([c[0] for c in result.description],result.fetchall())
            support=con.execute("""SELECT (SELECT count(*) FROM evaluation WHERE NOT training),
                (SELECT count(*) FROM baseline),(SELECT count(*) FROM send_fit),(SELECT count(*) FROM receive_fit)""").fetchone()
            # A declared sender account has one declared bank in the shared foundation.
            bank_rows=con.execute("""WITH accounts AS (
                SELECT bank,sender,count(*) n,sum(residual*residual) base_ss,
                    sum(pow(residual-send_effect,2)) model_ss,
                    sum(pow(residual-receive_effect,2)) receiver_ss,
                    avg(residual*residual) account_base,
                    avg(pow(residual-send_effect,2)) account_model
                FROM scored GROUP BY bank,sender
            ) SELECT bank,sum(n),sum(base_ss),sum(model_ss),sum(receiver_ss),
                sum(account_base),sum(account_model) FROM accounts GROUP BY bank ORDER BY bank""").fetchall()
            stats=np.asarray([row[1:] for row in bank_rows],dtype=float)
            rng=np.random.default_rng(20261117)
            ratios=[]
            for _ in range(1000):
                total=stats[rng.integers(0,len(stats),len(stats))].sum(axis=0)
                ratios.append([total[2]/total[1],total[2]/total[3],total[5]/total[4]])
            intervals=np.quantile(ratios,[.005,.995],axis=0)
            primary=coverage[1][0]
            passed=(primary[0]/support[0]>=.90 and min(primary[1:3])>=100 and len(stats)>=100
                    and intervals[1,0]<=.98 and intervals[1,1]<=.99 and intervals[1,2]<=.98)
            uncertainty=(['statistic','low99','high99'],[(label,*intervals[:,i]) for i,label in enumerate(
                ['row model/baseline','row model/receiver','equal-sender model/baseline'])])
            overlap=con.execute("""SELECT count(DISTINCT bank) FROM scored
                WHERE bank IN (SELECT DISTINCT bank FROM scope WHERE training)""").fetchone()[0]
            decision=(['ordering_banks','shared_training_banks','all_criteria_met'],[(len(stats),overlap,passed)])
        lines=["# H-A21: Country context in log payment amounts","",
            f"Phase {args.phase}. Freeze {args.freeze or 'exploration only'}. Pre-July bit-0 fit, selected July score. Phase0 and A01-A20 exposure applies.",
            "Country effects are simple training residual averages after a currency/party mean. Both fitted countries required.",
            "No causal, wealth or original implementation interpretation is assigned.","",
            f"Scoped July / currency-party fits / sender-country fits / receiver-country fits: {support}.",""]
        for title,(columns,rows) in [("Same-row predictive metrics",coverage),("Party controls",strata),("Equal-sender predictive metrics",balanced),("Bank-cluster sensitivity",uncertainty),("Decision",decision)]:
            lines += ["## "+title,"","| "+" | ".join(columns)+" |","| "+" | ".join(["---"]*len(columns))+" |"]
            lines += ["| "+" | ".join(map(str,row))+" |" for row in rows]
            lines.append("")
        (HERE/f"out/H-A21_country_amount_context_{args.phase}.md").write_text("\n".join(lines),encoding="utf-8")
        print(f"OK: aggregate country-amount {args.phase} saved. Criteria met: {passed}.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())
