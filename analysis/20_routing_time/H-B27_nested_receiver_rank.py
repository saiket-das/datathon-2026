"""Challenge a single receiver-rank threshold for Covered route state.

Run from repository root:
    uv run python analysis/20_routing_time/H-B27_nested_receiver_rank.py
"""
from datetime import datetime, timezone
from pathlib import Path
import sys
import duckdb


def evaluate(con: duckdb.DuckDBPyConnection, agreements: bool, min_witnesses: int = 1) -> tuple:
    """Count alternating labels across shared receivers without exporting identities."""
    con.execute(f"""
        CREATE OR REPLACE TEMP TABLE labels AS
        WITH paths AS (
            SELECT list_filter(string_split(bic8_path,';'),lambda x:x<>'...') p,
                   ordering_bic8 ob,beneficiary_bic8 bb,transaction_type_code='Covered' covered
            FROM read_parquet('dataset/payments.parquet')
            WHERE anomaly_type IS NULL AND participant_count BETWEEN 3 AND 5
              AND ts_utc>=TIMESTAMP '2023-05-01' AND ts_utc<TIMESTAMP '2023-07-01'
              AND (('0x'||substr(md5(ordering_bic8),1,8))::UBIGINT%2)=0
              AND (('0x'||substr(md5(beneficiary_bic8),1,8))::UBIGINT%2)=0
        )
        SELECT p[1] a,p[-1] b,min(covered)::INT covered FROM paths
        WHERE {'ob=p[1] AND bb=p[-1]' if agreements else 'TRUE'}
        GROUP BY a,b HAVING min(covered)=max(covered) AND count(*)>={min_witnesses}
    """)
    con.execute('''CREATE OR REPLACE TEMP TABLE supported AS SELECT * FROM labels
                   WHERE a IN (SELECT a FROM labels GROUP BY a HAVING count(*)>=100)''')
    population=con.execute('SELECT count(*),count(DISTINCT a),count(DISTINCT b) FROM supported').fetchone()
    return (*population,*checkerboards(con))


def checkerboards(con: duckdb.DuckDBPyConnection) -> tuple:
    """Count forbidden crossings in an existing supported(a,b,covered) table."""
    return con.execute('''
        WITH shared AS (
            SELECT f.a first_bank,v.a second_bank,count(*) n,
                   count_if(f.covered=1 AND v.covered=0) u,
                   count_if(f.covered=0 AND v.covered=1) z
            FROM supported f JOIN supported v ON f.b=v.b AND f.a<v.a
            GROUP BY f.a,v.a HAVING count(*)>=20
        )
        SELECT count(*),count(DISTINCT first_bank),count(DISTINCT second_bank),sum(n),
               count_if(u>0 AND z>0),sum(u*z),avg((u>0 AND z>0)::INT),
               sum(least(u,z))::DOUBLE/sum(n)
        FROM shared
    ''').fetchone()


def main() -> None:
    if datetime.now(timezone.utc)>=datetime(2026,11,18,12,tzinfo=timezone.utc):
        raise ValueError('Research cutoff reached')
    lines=[
        '# H-B27 shared receiver-rank threshold falsification','',
        'May-June unlabelled v3-5, endpoint bit0/0. 512MB, one thread, no spill.',
        'Pure ordered visible-endpoint labels only. Origins need 100 corridors and origin pairs 20 shared receivers.',
        'A checkerboard means both origins have a Covered receiver that the other origin marks Indirect.',
        'Shared receiver ranks with one threshold per origin imply zero such checkerboards.',
        'Bank and corridor identities stay local. Cohorts with insufficient bank support are suppressed.','',
        '| Cohort | Corridors | Origins | Receivers | Origin pairs | First-role origins | Second-role origins | Repeated shared-receiver comparisons | Checkerboard origin pairs | Motifs | Checkerboard-pair fraction | Pairwise minimum editing fraction |',
        '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |',
    ]
    with duckdb.connect(config={'memory_limit':'512MB','threads':1,'temp_directory':''}) as con:
        for agreements,witnesses,label in ((False,1,'All'),(True,1,'Declared endpoints agree'),(False,2,'At least two witnesses per corridor')):
            row=evaluate(con,agreements,witnesses)
            corridors,origins,receivers,pairs,first,second,comparisons,violations,motifs,fraction,edits=row
            if min(corridors,origins,receivers,pairs,first,second)<100:
                lines.append(f'| {label} | Suppressed | — | — | — | — | — | — | — | — | — | — |')
            else:
                lines.append(f'| {label} | {corridors:,} | {origins:,} | {receivers:,} | {pairs:,} | {first:,} | {second:,} | {comparisons:,} | {violations:,} | {motifs:,} | {fraction:.6%} | {edits:.6%} |')
    lines += ['', 'Exact shared-rank thresholding is rejected on supported observed comparisons.',
              'Motifs and origin pairs share most underlying corridors, so their count gives no independent-sample uncertainty.',
              'Pairwise editing fractions describe local nesting and do not give the minimum global matrix edits.',
              'Approximate rank effects, idiosyncratic pair states and probabilistic models remain possible.',
              'Phase0/Round1/Round2 Covered-state and direction outcomes are exposed. No new July outcome was queried.']
    (Path(__file__).parent/'out'/'H-B27_nested_receiver_rank_explore.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Saved supported B27 checkerboard aggregate screen.')


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(f'ERROR: {type(exc).__name__}; source values hidden.',file=sys.stderr)
        sys.exit(1)
