"""Challenge a common Covered-origin duration increment on May-June records.

Run from repository root:
    uv run python analysis/20_routing_time/H-B26_origin_penalty.py
"""
from datetime import datetime, timezone
from pathlib import Path
import sys

import duckdb

from duration_reversals import load_reversals, estimate_reversals


def main() -> None:
    if datetime.now(timezone.utc) >= datetime(2026, 11, 18, 12, tzinfo=timezone.utc):
        raise ValueError('Research cutoff reached')
    with duckdb.connect(config={'memory_limit':'512MB','threads':1,'temp_directory':''}) as con:
        load_reversals(con,'explore',None)
        estimate_reversals(con)
        con.execute("""
            CREATE TEMP TABLE labels AS
            WITH paths AS (
                SELECT list_filter(string_split(bic8_path,';'),lambda x:x<>'...') p,
                       transaction_type_code='Covered' covered
                FROM read_parquet('dataset/payments.parquet')
                WHERE anomaly_type IS NULL AND participant_count BETWEEN 3 AND 5
                  AND ts_utc>=TIMESTAMP '2023-05-01' AND ts_utc<TIMESTAMP '2023-07-01'
                  AND (('0x'||substr(md5(ordering_bic8),1,8))::UBIGINT%2)=0
                  AND (('0x'||substr(md5(beneficiary_bic8),1,8))::UBIGINT%2)=0
            )
            SELECT p[1] a,p[-1] b,min(covered)::INT covered FROM paths
            GROUP BY a,b HAVING min(covered)=max(covered)
        """)
        con.execute("""
            CREATE TEMP TABLE excess AS
            SELECT CASE WHEN f.covered=1 THEN r.a ELSE r.b END origin,
                   CASE WHEN f.covered=1 THEN r.b ELSE r.a END receiver,
                   CASE WHEN f.covered=1 THEN gap ELSE -gap END duration_gap
            FROM reversals r JOIN labels f USING(a,b)
            JOIN labels v ON r.a=v.b AND r.b=v.a
            WHERE f.covered+v.covered=1 AND short_center<100 AND abs(gap)>20
        """)
        pairs,origins,receivers=con.execute('SELECT count(*),count(DISTINCT origin),count(DISTINCT receiver) FROM excess').fetchone()
        multi, multi_pairs, variable=con.execute("""
            SELECT count(*),sum(n),count_if(span>20) FROM (
                SELECT origin,count(*) n,max(duration_gap)-min(duration_gap) span
                FROM excess GROUP BY origin HAVING n>=2
            )
        """).fetchone()
        assert variable <= multi and multi_pairs <= pairs
        mask=lambda count: '<100' if 0<count<100 else str(count)
        lines=[
            '# H-B26 common Covered-origin increment falsification','',
            'May-June unlabelled endpoint bit0/0 only.512MB,one thread,no spill.',
            'Direct medians need10 payments per direction; shorter median<100; positive Covered-associated gap>20.',
            'Multibank pure labels come from separate payments with3-5 visible bank occurrences.',
            'Phase0/Round1/Round2 including B19/B20-B25 outcomes are already exposed. No July query here.','',
            '| Qualified pairs | Actual Covered-origin banks | Receiving banks |',
            '| ---: | ---: | ---: |',f'| {pairs} | {mask(origins)} | {mask(receivers)} |','',
            '| Origins with at least2 qualified corridors | Associated corridors | Origins whose gap range exceeds20 seconds |',
            '| ---: | ---: | ---: |',f'| {mask(multi)} | {multi_pairs} | {mask(variable)} |','',
            f'All repeated-origin cohorts exceed20-second range: {multi==variable and multi>0}.',
            'The candidate common increment is falsified in these selected observed corridors.',
            'Actual Covered-origin support is below100, so no population-level origin independence or uncertainty claim is made.',
            'Pair-specific baselines, estimation error and selection remain relevant to broader models.',
        ]
    (Path(__file__).parent/'out'/'H-B26_origin_penalty_explore.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Saved B26 supported aggregate screen with low bank support masked.')


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(f'ERROR: {type(exc).__name__}; source values hidden.',file=sys.stderr)
        sys.exit(1)
