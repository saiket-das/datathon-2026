"""Test stability of ordering-bank Covered propensities against non-bank baselines.

Run from repository root:
    uv run python analysis/20_routing_time/H-B04_covered_bank_stability.py --phase explore
Frozen validation: same command with --phase confirm --freeze SHA.
All sponsor reads are local; only coarse aggregates are saved. No dataset is modified.
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
CUT = datetime(2026, 11, 18, 12, tzinfo=timezone.utc)


def intervals(stats: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Whole-ordering-bank resampling, with dependence caveats stated in the plan."""
    if len(stats) < 100:
        raise ValueError("insufficient validation banks")
    rng = np.random.default_rng(20261116)
    draws = rng.multinomial(len(stats), np.full(len(stats), 1 / len(stats)), size=1000) @ stats
    ratios = np.column_stack((draws[:, 1] / draws[:, 2], draws[:, 1] / draws[:, 3], draws[:, 4] / draws[:, 0]))
    return np.quantile(ratios, .005, axis=0), np.quantile(ratios, .995, axis=0)


def safe_table(columns: list[str], rows: list[tuple]) -> str:
    """Suppress unsupported row/entity cohorts; never accept identifier columns."""
    assert not any('bic' in c.lower() or 'account' in c.lower() or c.lower() == 'bank_id' for c in columns)
    out = ['| ' + ' | '.join(columns) + ' |', '| ' + ' | '.join(['---']*len(columns)) + ' |']
    for row in rows:
        d = dict(zip(columns, row))
        small = any(k in d and 0 < d[k] < 100 for k in ('n', 'senders', 'receivers', 'banks'))
        cells = []
        for k,v in zip(columns,row):
            if small and k not in ('group','n'):
                v = 'suppressed'
            elif small and k == 'n':
                v = '<100'
            elif isinstance(v, (float, np.floating)):
                v = f'{v:.8f}'
            cells.append(str(v))
        out.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(out)


def run() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase',choices=['explore','confirm'],default='explore')
    parser.add_argument('--freeze')
    args=parser.parse_args()
    if args.phase=='explore' and datetime.now(timezone.utc)>=CUT:
        parser.error('research cutoff passed; no new exploration')
    if args.phase=='confirm':
        if not args.freeze:
            parser.error('confirmation requires --freeze')
        subprocess.run(['git','merge-base','--is-ancestor',args.freeze,'HEAD'],cwd=ROOT,check=True)
        subprocess.run(['git','diff','--exit-code','--quiet',args.freeze,'--',f'analysis/20_routing_time/{STEM}.py'],cwd=ROOT,check=True)
        plan=subprocess.check_output(['git','show',f'{args.freeze}:findings/hypotheses/{STEM}.md'],cwd=ROOT,text=True)
        if '**Status:** confirmation-ready' not in plan:
            raise ValueError('freeze needs a confirmation-ready plan')
    c=duckdb.connect(config={'memory_limit':'512MB','threads':1,'temp_directory':''})
    c.execute("SET TimeZone='UTC'")
    path=(ROOT/'dataset/payments.parquet').as_posix().replace("'","''")
    c.execute(f"""CREATE VIEW e AS SELECT ROW_ID,ORDERING_BIC8 bank,ORDERING_ACCOUNT sender,
      BENEFICIARY_ACCOUNT receiver,BENEFICIARY_BIC8 benbank,TRANSACTION_TYPE_CODE='Covered' y,
      CURRENCY_CODE currency,ORDERING_TYPE||BENEFICIARY_TYPE pair,
      least(PARTICIPANT_COUNT,5) v,strftime(ts_utc,'%Y-%m') period
      FROM read_parquet('{path}') WHERE ANOMALY_TYPE IS NULL AND PARTICIPANT_COUNT>2
      AND (('0x'||substr(md5(ORDERING_BIC8),1,8))::UBIGINT%2)=0
      AND (('0x'||substr(md5(BENEFICIARY_BIC8),1,8))::UBIGINT%2)=0""")
    train="period='2023-05'" if args.phase=='explore' else "period IN ('2023-05','2023-06')"
    valid="period='2023-06'" if args.phase=='explore' else "period='2023-07'"
    c.execute(f'CREATE VIEW training AS SELECT * FROM e WHERE {train}')
    c.execute(f'CREATE VIEW validation AS SELECT * FROM e WHERE {valid}')
    c.execute('CREATE TEMP TABLE global_fit AS SELECT avg(y::INT) p,count(*) n FROM training')
    c.execute('''CREATE TEMP TABLE bank_fit AS SELECT bank,count(*) n,(sum(y::INT)+.5)/(count(*)+1) p
      FROM training GROUP BY bank HAVING count(*)>=100''')
    c.execute('''CREATE TEMP TABLE mix_fit AS SELECT currency,pair,v,(sum(y::INT)+100*any_value(g.p))/(count(*)+100) p
      FROM training CROSS JOIN global_fit g GROUP BY currency,pair,v''')
    c.execute('''CREATE VIEW scored AS SELECT e.*,b.p bank_p,g.p global_p,coalesce(m.p,g.p) mix_p
      FROM validation e JOIN bank_fit b USING(bank) CROSS JOIN global_fit g
      LEFT JOIN mix_fit m USING(currency,pair,v)''')
    q=c.execute('''SELECT (SELECT count(*) FROM validation) all_n,count(*) n,count(DISTINCT sender) senders,
      count(DISTINCT receiver) receivers,count(DISTINCT bank) banks,avg(y::INT) covered_share,
      avg(pow(y::INT-bank_p,2)) bank_brier,avg(pow(y::INT-global_p,2)) global_brier,
      avg(pow(y::INT-mix_p,2)) composition_brier FROM scored''')
    support=q.fetchall(); cols=[x[0] for x in q.description]
    stats=np.asarray(c.execute('''SELECT count(*) n,sum(pow(y::INT-bank_p,2)) bs,
      sum(pow(y::INT-global_p,2)) gs,sum(pow(y::INT-mix_p,2)) ms,
      count(*)*abs(avg(y::INT)-any_value(bank_p)) cal FROM scored GROUP BY bank ORDER BY bank''').fetchall(),dtype=float)
    totals=stats.sum(axis=0); low,high=intervals(stats)
    metrics=[('bank/global Brier ratio',totals[1]/totals[2],low[0],high[0]),
             ('bank/composition Brier ratio',totals[1]/totals[3],low[1],high[1]),
             ('row-weighted bank calibration absolute error',totals[4]/totals[0],low[2],high[2])]
    d=dict(zip(cols,support[0])); coverage=d['n']/d['all_n']
    passed=coverage>=.60 and min(d[k] for k in ('senders','receivers','banks'))>=100 and high[0]<=.85 and high[1]<=.85 and high[2]<=.05
    parts=[f'# {STEM}: {args.phase}', '',f'Freeze: {args.freeze or "not frozen; pilot only"}.',
      '512MB; one thread; no spill. UTC. Bank-bit-0/0 unlabelled multibank payments only.',
      'Prior Phase 0 and Round 1 aggregates include these records; this is not an independent holdout.',
      'Training uses May / May-June; evaluation uses June / July for explore / confirm.',
      '', '## Support and predictive error','',safe_table(cols,support),
      '', '## Primary bank-cluster uncertainty','',safe_table(['statistic','estimate','low_99','high_99'],metrics),
      '', '## Decision','', f'Frozen internal-validation criteria pass: {passed}. Coverage: {coverage:.8f}.',
      'Brier scores are predictive errors, not fraud-classification or recovered generator code.',
      'Intervals resample ordering banks only; shared counterparties/path banks can induce residual dependence.']
    for label,expr in [('party pair','pair'),('visible count','v'),('currency','currency')]:
        q=c.execute(f'''SELECT {expr} group_name,count(*) n,count(DISTINCT sender) senders,
          count(DISTINCT receiver) receivers,count(DISTINCT bank) banks,avg(y::INT) covered_share,
          avg(pow(y::INT-bank_p,2))/avg(pow(y::INT-mix_p,2)) brier_ratio FROM scored GROUP BY 1 ORDER BY 1''')
        columns=[x[0] for x in q.description]; rows=q.fetchall()
        parts+=['',f'## Descriptive sensitivity: {label}','',safe_table(columns,rows)]
    q=c.execute('''SELECT (SELECT count(DISTINCT sender) FROM validation WHERE sender IN (SELECT sender FROM training)) shared_senders,
      (SELECT count(DISTINCT receiver) FROM validation WHERE receiver IN (SELECT receiver FROM training)) shared_receivers,
      (SELECT count(DISTINCT bank) FROM validation WHERE bank IN (SELECT bank FROM training)) shared_ordering_banks,
      (SELECT count(DISTINCT benbank) FROM validation WHERE benbank IN (SELECT benbank FROM training)) shared_beneficiary_banks''')
    parts+=['','## Aggregate entity overlap (not identifiers)','',safe_table([x[0] for x in q.description],q.fetchall())]
    destination=Path(__file__).parent/'out'/f'{STEM}_{args.phase}.md'
    destination.write_text('\n'.join(parts)+'\n',encoding='utf-8')
    c.close()
    print(f'OK: {args.phase}; aggregate report saved; criteria pass={passed}. No records exported.')
    return 0


if __name__=='__main__':
    try:
        sys.exit(run())
    except Exception as exc:
        print(f'ERROR: {type(exc).__name__}; source details hidden.',file=sys.stderr)
        sys.exit(1)