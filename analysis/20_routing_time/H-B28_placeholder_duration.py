"""Test an added mean-duration increment for placeholders on matched Direct paths.

Run from repository root:
    uv run python analysis/20_routing_time/H-B28_placeholder_duration.py --phase explore
Frozen internal test: add --phase confirm --freeze SHA instead of --phase explore.
"""
from datetime import datetime, timezone
from pathlib import Path
import sys

import duckdb
import numpy as np
from routing_common import arguments

STEM = "H-B28_placeholder_duration"


def contrast(con: duckdb.DuckDBPyConnection, period: str, currency: bool,
             agrees: bool) -> tuple:
    """Compare gap-bearing and gap-free means within exact visible-path cells."""
    if period not in ("month", "week"):
        raise ValueError("Invalid time period")
    con.execute(f"""CREATE OR REPLACE TEMP TABLE cells AS
      SELECT p,date_trunc('{period}',ts_utc) period,route,
        {"currency," if currency else ""}
        count_if(NOT gaps) n0,count_if(gaps) n1,
        avg(d) FILTER(WHERE gaps)-avg(d) FILTER(WHERE NOT gaps) delta,
        var_samp(d) FILTER(WHERE gaps)/count_if(gaps)
          +var_samp(d) FILTER(WHERE NOT gaps)/count_if(NOT gaps) predvar
      FROM x WHERE {"agrees" if agrees else "TRUE"}
      GROUP BY p,period,route {",currency" if currency else ""}
      HAVING count_if(NOT gaps)>=5 AND count_if(gaps)>=5
    """)
    summary=con.execute("""SELECT count(*),count(DISTINCT p),count(DISTINCT p[1]),
      count(DISTINCT p[-1]),sum(n0+n1),sum(n1),avg(delta),median(delta),
      avg(delta*delta),avg(predvar) FROM cells""").fetchone()
    intervals=[]
    for role in (1,-1):
        # Bank identities are neither fetched nor printed; only numeric sufficient statistics.
        group=np.asarray(con.execute(f"""SELECT count(*),sum(delta) FROM cells
          GROUP BY p[{role}]""").fetchall(),dtype=float)
        if len(group)<100:
            intervals.append((None,None))
            continue
        rng=np.random.default_rng(20261117)
        values=[]
        for _ in range(1000):
            draws=rng.integers(0,len(group),len(group))
            weight,effect=group[draws].sum(axis=0)
            values.append(effect/weight)
        intervals.append(tuple(np.quantile(values,[.005,.995])))
    return (*summary,*intervals)



def entity_audit(con: duckdb.DuckDBPyConnection) -> list[tuple]:
    """Count entity reuse for primary matched records; identities remain in memory."""
    con.execute("""CREATE TEMP TABLE eligible AS SELECT x.* FROM x SEMI JOIN cells c
      ON x.p=c.p AND date_trunc('month',x.ts_utc)=c.period AND x.route=c.route""")
    con.execute("""CREATE TEMP TABLE prior AS
      SELECT ordering_account oa,beneficiary_account ba,
        list_filter(string_split(bic8_path,';'),lambda x:x<>'...') p
      FROM read_parquet('dataset/payments.parquet')
      WHERE anomaly_type IS NULL AND participant_count=2 AND transaction_type_code='Direct'
        AND ts_utc>='2023-05-01'::TIMESTAMP AND ts_utc<'2023-07-01'::TIMESTAMP
        AND (('0x'||substr(md5(ordering_bic8),1,8))::UBIGINT%2)=0
        AND (('0x'||substr(md5(beneficiary_bic8),1,8))::UBIGINT%2)=0""")
    rows=[]
    for label,entities in (('Accounts, either role','SELECT oa entity FROM {source} UNION SELECT ba FROM {source}'),
                           ('Visible endpoint banks','SELECT unnest(p) entity FROM {source}')):
        total,overlap=con.execute(f"""WITH e AS ({entities.format(source='eligible')}),
          t AS ({entities.format(source='prior')})
          SELECT count(DISTINCT e.entity),count(DISTINCT e.entity) FILTER(WHERE t.entity IS NOT NULL)
          FROM e LEFT JOIN (SELECT DISTINCT entity FROM t) t USING(entity)""").fetchone()
        rows.append((label,total,overlap))
    return rows


def main() -> None:
    args=arguments(STEM)
    if args.phase=='explore' and datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError('Research cutoff reached')
    start,end=(('2023-05-01','2023-07-01') if args.phase=='explore'
               else ('2023-07-01','2023-08-01'))
    lines=[f'# {STEM}: {args.phase}', '', f'Freeze: {args.freeze or "not yet frozen"}.',
      'Unlabelled Direct, two visible banks, declared endpoint MD5 parity0/0.',
      '512MB, one thread, no spill. Exact visible path and UTC period/route matched.',
      'Each cell needs five payments with and without placeholders; equal cell weights.',
      'Intervals: separate first/last-bank resampling, 1000 draws, seed20261117; conditional, not independent banks.',
      'No identifiers or small-support cell values exported. Phase0/Round1/Round2/3 records and duration outcomes are exposed.']
    headings=['| Match/control | Cells | Paths | First banks | Last banks | Payments | Gap-bearing payments | Mean contrast seconds | Median contrast | Mean squared contrast | Expected sampling variance | First-bank99% interval | Last-bank99% interval |',
      '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |']
    with duckdb.connect(config={'memory_limit':'512MB','threads':1,'temp_directory':''}) as con:
        con.execute("SET TimeZone='UTC'")
        con.execute("""CREATE TEMP TABLE x AS
          SELECT list_filter(string_split(bic8_path,';'),lambda x:x<>'...') p,
            gap_count>0 gaps,ts_utc,transaction_type_code route,total_duration d,
            ordering_account oa,beneficiary_account ba,
            currency_code currency,
            ordering_bic8=list_filter(string_split(bic8_path,';'),lambda x:x<>'...')[1]
              AND beneficiary_bic8=list_filter(string_split(bic8_path,';'),lambda x:x<>'...')[-1] agrees
          FROM read_parquet('dataset/payments.parquet')
          WHERE anomaly_type IS NULL AND participant_count=2 AND transaction_type_code='Direct'
            AND ts_utc>=?::TIMESTAMP AND ts_utc<?::TIMESTAMP
            AND (('0x'||substr(md5(ordering_bic8),1,8))::UBIGINT%2)=0
            AND (('0x'||substr(md5(beneficiary_bic8),1,8))::UBIGINT%2)=0
        """,[start,end])
        scoped=con.execute('SELECT count(*),count(DISTINCT p),count(DISTINCT p[1]),count(DISTINCT p[-1]) FROM x').fetchone()
        source_payments,source_paths,source_first,source_last=scoped
        lines+=['', f'Scoped source: {source_payments:,} payments, {source_paths:,} visible paths, {source_first:,} first banks and {source_last:,} last banks.', '',*headings]
        decision=False
        audit=[]
        for period,currency,agrees,label in (
            ('month',False,False,'Month: primary'),('week',False,False,'Week'),
            ('month',True,False,'Month + currency'),('month',False,True,'Month + declared endpoints agree')):
            row=contrast(con,period,currency,agrees)
            cells,paths,first,last,payments,gaps,mean,median,ms,pv,fi,li=row
            supported=cells>=100 and paths>=100 and first>=100 and last>=100
            if not supported:
                lines.append(f'| {label} | Suppressed: insufficient path/bank support | — | — | — | — | — | — | — | — | — | — | — |')
                continue
            lines.append(f'| {label} | {cells:,} | {paths:,} | {first:,} | {last:,} | {payments:,} | {gaps:,} | {mean:.6f} | {median:.6f} | {ms:.6f} | {pv:.6f} | [{fi[0]:.6f},{fi[1]:.6f}] | [{li[0]:.6f},{li[1]:.6f}] |')
            if label=='Month: primary':
                if args.phase=='confirm':
                    audit=entity_audit(con)
                decision=bool(cells>=200 and paths>=200 and all(-1<=v<=1 for interval in (fi,li) for v in interval))
        if args.phase=='confirm':
            lines+=['', '## Eligible primary entity overlap with May–June scoped Direct records',
                    'Either account role and either visible endpoint role; all earlier scoped records, not just matched cells.',
                    '| Entity | Eligible distinct | Also in May–June |', '| --- | ---: | ---: |']
            for label,total,overlap in audit:
                shown='Suppressed: small overlap or complement' if (0<overlap<100 or 0<total-overlap<100) else str(overlap)
                total_text='<100' if 0<total<100 else str(total)
                lines.append(f'| {label} | {total_text} | {shown} |')
        lines+=['',f'Primary equivalence/support conjunction: {decision}.',
          'A passed internal test bounds the matched equal-cell average contrast; it does not prove zero effect on every path, independence, missing-hop absence, causality or generator stage ordering.',
          'Controls do not rescue a failed primary criterion. Paths with insufficient repeats and longer paths are outside scope.',
          'Previously exposed records and shared banks/accounts prevent an independent holdout interpretation.']
    (Path(__file__).parent/'out'/f'{STEM}_{args.phase}.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Saved aggregate-only B28 matched placeholder timing report.')


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(f'ERROR: {type(exc).__name__}; source values hidden.',file=sys.stderr)
        sys.exit(1)
