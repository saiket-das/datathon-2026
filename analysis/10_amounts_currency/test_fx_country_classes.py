"""Check latent FX country grouping on invented aggregates.

Run from repository root:
    uv run pytest analysis/10_amounts_currency/test_fx_country_classes.py
"""
import importlib.util
from pathlib import Path

SPEC=importlib.util.spec_from_file_location('fx_country_classes',Path(__file__).with_name('H-A03_fx_country_classes.py'))
MODULE=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_components_join_only_supported_all_zero_pairs():
    pairs=[('AA','BB',100,100),('BB','CC',200,200),('CC','DD',300,299),('EE','FF',99,99)]
    result=MODULE.components(pairs)
    assert result['AA']==result['BB']==result['CC']
    assert result['DD']!=result['CC']
    assert 'EE' not in result and 'FF' not in result
    assert result==MODULE.components(list(reversed(pairs)))


def test_components_keep_distinct_country_pairs_separate():
    result=MODULE.components([('AA','BB',1000,0),('AA','AA',100,100)])
    assert result['AA']!=result['BB']


def test_render_retains_failed_decision_and_disclosure():
    rendered=MODULE.render('invented',{'decision':(['passes','n'],[(False,123)])},'abc')
    assert '| False | 123 |' in rendered
    assert 'not an independent holdout' in rendered

def test_static_sql_parses():
    import ast
    import duckdb
    tree=ast.parse(Path(MODULE.__file__).read_text(encoding='utf-8'))
    con=duckdb.connect()
    for node in ast.walk(tree):
        if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value.lstrip().startswith(('SELECT','WITH')):
            con.extract_statements(node.value)
    con.close()


def test_scoring_uses_class_transitions_and_rejects_unknown_country():
    import duckdb
    con=duckdb.connect()
    con.execute("CREATE TABLE classes(country VARCHAR,group_id VARCHAR,wrong_id VARCHAR)")
    con.execute("INSERT INTO classes VALUES ('AA','ONE','ONE'),('BB','ONE','TWO'),('CC','TWO','ONE')")
    con.execute("""CREATE TABLE source AS SELECT 1 ROW_ID,'sender' oa,'receiver' ba,'BANKAA00' ob,
        1 fx,'Indirect' route,TIMESTAMP '2023-06-01' ts_utc,NULL::VARCHAR ANOMALY_TYPE,
        ['BANKAA00','BANKBB00','BANKCC00'] path,'explore' split
        UNION ALL SELECT 2,'sender','receiver','BANKAA00',1,'Indirect',TIMESTAMP '2023-06-01',NULL,
        ['BANKAA00','BANKXX00','BANKCC00'],'explore'""")
    MODULE.score(con,'explore')
    assert con.execute('SELECT eligible,predicted,country_predicted FROM scored WHERE ROW_ID=1').fetchone()==(True,1,2)
    assert con.execute('SELECT eligible FROM scored WHERE ROW_ID=2').fetchone()==(False,)
    con.close()