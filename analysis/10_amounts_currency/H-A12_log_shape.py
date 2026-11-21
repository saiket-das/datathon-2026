"""Explore log-amount shape after conditioning on currency and party types.

Run: uv run python analysis/10_amounts_currency/H-A12_log_shape.py
Frozen internal validation: add --phase validate --freeze SHA.
Only unlabelled both-account bit-0 training and the selected July split are queried.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
import math
from pathlib import Path
import subprocess
import sys

import duckdb
import numpy as np

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("foundation", HERE.parent / "00_prep/scientific_checks.py")
foundation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(foundation)
CUTOFF = datetime(2026, 11, 18, 12, tzinfo=timezone.utc)

# Normal cut points also yield matched-scale logistic and Laplace comparisons.
CUTS = (-3, -2, -1, 0, 1, 2, 3)
LOGISTIC = [1 / (1 + math.exp(-x * math.pi / math.sqrt(3))) for x in CUTS]
LAPLACE = [0.5 * math.exp(math.sqrt(2) * x) if x <= 0 else
           1 - 0.5 * math.exp(-math.sqrt(2) * x) for x in CUTS]
NORMAL = [0.5 * (1 + math.erf(x / math.sqrt(2))) for x in CUTS]
COMPARATORS = np.diff([[0, *cdf, 1] for cdf in (NORMAL, LOGISTIC, LAPLACE)], axis=1)


def distances(cumulative: np.ndarray, n: float) -> np.ndarray:
    """Compare an eight-bin histogram with equal-scale reference shapes."""
    empirical = np.diff(np.r_[0, cumulative / n, 1])
    return 0.5 * np.abs(COMPARATORS - empirical).sum(axis=1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', choices=['explore','validate'], default='explore')
    parser.add_argument('--freeze')
    args = parser.parse_args()
    if args.phase == 'explore' and datetime.now(timezone.utc) >= CUTOFF:
        return 1
    try:
        if args.phase == 'validate':
            if not args.freeze:
                raise ValueError('Freeze required')
            root = HERE.parents[1]
            subprocess.run(['git','merge-base','--is-ancestor',args.freeze,'HEAD'],cwd=root,check=True,capture_output=True)
            for path in [Path(__file__).resolve(),Path(foundation.__file__)]:
                frozen = subprocess.check_output(['git','show',f'{args.freeze}:{path.relative_to(root).as_posix()}'],cwd=root)
                if frozen.replace(b'\r\n',b'\n') != path.read_bytes().replace(b'\r\n',b'\n'):
                    raise ValueError('Frozen source mismatch')
        with duckdb.connect() as con:
            con.execute("SET memory_limit='512MB'; SET threads=1; SET temp_directory=''; SET preserve_insertion_order=false")
            split = foundation.partition_sql("accounts")
            source = f"""SELECT
                CURRENCY_CODE currency, concat(ORDERING_TYPE,BENEFICIARY_TYPE) party_pair,
                ln(USD_AMOUNT) log_amount, ORDERING_ACCOUNT sender,
                BENEFICIARY_ACCOUNT receiver, ORDERING_BIC8 bank,
                ts_utc < TIMESTAMP '2023-07-01' training
                FROM read_parquet('dataset/payments.parquet')
                WHERE ANOMALY_TYPE IS NULL AND USD_AMOUNT>0 AND {split}='explore'"""
            con.execute(f'CREATE VIEW scope AS {source}')
            evaluation = source.replace("='explore'", "='confirm'") if args.phase == 'validate' else source
            con.execute(f'CREATE VIEW evaluation AS {evaluation}')
            con.execute("""CREATE TEMP TABLE models AS
                SELECT currency,party_pair,avg(log_amount) loc,stddev_samp(log_amount) scale,
                       count(*) n
                FROM scope WHERE training GROUP BY 1,2 HAVING count(*)>=1000 AND scale>0""")
            con.execute("""CREATE VIEW scored AS
                SELECT s.*,m.loc,m.scale,
                       (log_amount-m.loc)/m.scale z
                FROM evaluation s JOIN models m USING(currency,party_pair) WHERE NOT training""")
            expressions = ", ".join(
                f"round(avg((z<={cut})::INT),6) "
                f"z_le_{'minus' if cut<0 else 'plus'}{abs(cut)}" for cut in CUTS
            )
            queries={
                "Training support": """SELECT count(*) groups,sum(n) fit_payments,
                    round(min(scale),6) minimum_fit_sd,round(median(scale),6) median_fit_sd,
                    round(max(scale),6) maximum_fit_sd FROM models""",
                "Score coverage": """SELECT
                    (SELECT count(*) FROM evaluation WHERE NOT training) scoped,
                    count(*) eligible,count(DISTINCT sender) senders,
                    count(DISTINCT receiver) receivers FROM scored""",
                "Standardised empirical cumulative probabilities": f"""SELECT
                    CASE WHEN grouping(party_pair)=1 THEN 'All' ELSE party_pair END party_pair,
                    count(*) n,count(DISTINCT sender) senders,count(DISTINCT receiver) receivers,
                    round(avg(z),6) mean_z,round(stddev_samp(z),6) sd_z,
                    {expressions}
                    FROM scored GROUP BY GROUPING SETS ((), (party_pair))
                    HAVING count(*)>=1000 AND count(DISTINCT sender)>=100
                        AND count(DISTINCT receiver)>=100 ORDER BY 1""",
            }
            lines = ["# H-A12: Conditional log-amount shape", "",
                f"Phase {args.phase}; freeze {args.freeze or 'not frozen'}. Fit pre-July bit-0, score selected July population.",
                "Locations and scales are training currency/party means and sample SDs.",
                "At least 1,000 training payments per fitted group. Prior Phase 0, Round 1 and A03-A11 exposure applies.", ""]
            for title,query in queries.items():
                result=con.execute(query)
                columns=[column[0] for column in result.description]
                rows=result.fetchall()
                lines += ["## "+title,"","| "+" | ".join(columns)+" |","| "+" | ".join(["---"]*len(columns))+" |"]
                lines += ["| "+" | ".join(map(str,row))+" |" for row in rows]
                lines.append("")
            # Bank IDs establish cluster order internally. Only aggregate results are written.
            cumulative = ','.join(f"sum((z<={cut})::INT)" for cut in CUTS)
            bank_rows = con.execute(f"SELECT bank,count(*),{cumulative} FROM scored GROUP BY bank ORDER BY bank").fetchall()
            banks = np.asarray([row[1:] for row in bank_rows], dtype=float)
            rng = np.random.default_rng(20261116)
            estimates = []
            for _ in range(1000):
                sample = banks[rng.integers(0,len(banks),len(banks))].sum(axis=0)
                fit = distances(sample[1:], sample[0])
                estimates.append([fit[0],fit[1]-fit[0],fit[2]-fit[0]])
            intervals = np.quantile(estimates,[.005,.995],axis=0)
            pooled = banks.sum(axis=0)
            normal, logistic, laplace = distances(pooled[1:],pooled[0])
            scoped, eligible, senders, receivers = con.execute(queries['Score coverage']).fetchone()
            shared_banks = con.execute("""SELECT count(DISTINCT bank) FROM scored
                WHERE bank IN (SELECT DISTINCT bank FROM scope WHERE training)""").fetchone()[0]
            passed = (eligible/scoped>=.90 and min(senders,receivers,len(banks))>=100
                      and intervals[1,0]<=.02 and intervals[0,1]>=.02 and intervals[0,2]>=.05)
            lines += ['## Eight-bin shape and declared ordering-bank sensitivity', '',
                      f'Gaussian / logistic / Laplace TV: {normal:.6f} / {logistic:.6f} / {laplace:.6f}.',
                      f'Ordering banks: {len(banks)}. Shared ordering banks with training: {shared_banks}.',
                      'Both-role literal account separation applies in validation. Related entities can overlap.',
                      f'All practical criteria met: {passed}.', '',
                      '| statistic | low99 | high99 |', '| --- | --- | --- |']
            labels = ['Gaussian TV','logistic minus Gaussian TV','Laplace minus Gaussian TV']
            lines += [f'| {label} | {low:.6f} | {high:.6f} |' for label,(low,high) in zip(labels, intervals.T)]
        (HERE/f"out/H-A12_log_shape_{args.phase}.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
        print(f"OK: aggregate log-shape {args.phase} saved. Criteria met: {passed}.")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}; source values hidden.",file=sys.stderr)
        return 1


if __name__=="__main__":
    sys.exit(main())
