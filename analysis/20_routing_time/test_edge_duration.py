"""Check B15 against invented directed paths and a frozen offset transfer."""
import importlib.util
from pathlib import Path
import duckdb

SPEC = importlib.util.spec_from_file_location('b15', Path(__file__).with_name('H-B15_edge_duration.py'))
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_edge_sum_transfer_uses_june_offset_and_scores_same_rows() -> None:
    with duckdb.connect() as c:
        c.execute("""
            CREATE TABLE source AS
            WITH banks AS (SELECT i, 'A'||i a, 'B'||i b, 'C'||i z FROM range(100)r(i)),
            training AS (
                SELECT 20+i::DOUBLE duration,2 visible,5 AS month,'Direct' route,a ordering_bank,
                       a||j sender,b||j receiver,[a,b] p
                FROM banks CROSS JOIN range(10)r(j)
                UNION ALL
                SELECT 50+(i*7)%100,2,5,'Direct',a,a||j,z||j,[b,z]
                FROM banks CROSS JOIN range(10)r(j)
                UNION ALL
                SELECT 500,2,5,'Direct',a,a||j,z||j,[a,z]
                FROM banks CROSS JOIN range(10)r(j)
            ), evaluation AS (
                SELECT 70+i+(i*7)%100+5+(j%5)-2 AS duration,3 visible,m AS month,
                       'Indirect' route,a ordering_bank,a||j sender,z||j receiver,[a,b,z] p
                FROM banks CROSS JOIN range(20)r(j) CROSS JOIN (VALUES (6),(7))months(m)
            ) SELECT * FROM training UNION ALL SELECT * FROM evaluation
        """)
        report=MODULE.evaluate(c,'confirm','invented-freeze')
        assert 'sum 5.0' in report
        assert '2,000/2,000' in report
        assert '| 1.200000 |' in report
        assert 'PASS (unchanged frozen internal test)' in report
        assert 'A0' not in report
