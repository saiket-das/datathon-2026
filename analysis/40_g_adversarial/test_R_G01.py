"""Dataset-independent synthetic fixture tests for Investigator G R-G01."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import duckdb

MODULE = Path(__file__).with_name("R-G01_visible_endpoints.py")
SPEC = spec_from_file_location("g_r01_module", MODULE)
assert SPEC and SPEC.loader
r01 = module_from_spec(SPEC)
SPEC.loader.exec_module(r01)


def test_visible_path_extraction_ignores_gaps_and_rejects_non_bic():
    db = duckdb.connect(":memory:")
    result = db.execute("""
        WITH t AS (
            SELECT list_filter(
              string_split(' AAAAAAAA ;...; XXXXXXX ; BBBBBBBB ', ';'),
              lambda x: regexp_full_match(trim(x), '^[A-Z0-9]{8}$')
            ) AS nodes
        )
        SELECT trim(list_extract(nodes, 1)),
               trim(list_extract(nodes, array_length(nodes))),
               array_length(nodes)
        FROM t
    """).fetchone()
    assert result == ("AAAAAAAA", "BBBBBBBB", 2)
    db.close()


def test_independent_pair_map_and_reverse_negative_controls():
    db = duckdb.connect(":memory:")
    db.execute("""
        CREATE TEMP TABLE selected (
          period VARCHAR, label VARCHAR, path VARCHAR, node_count BIGINT,
          first_bic VARCHAR, last_bic VARCHAR
        )
    """)
    db.executemany("INSERT INTO selected VALUES(?,?,?,?,?,?)", [
        ("2026-05", "Covered", "AAAAAAAA;BBBBBBBB", 2, "AAAAAAAA", "BBBBBBBB"),
        ("2026-05", "Covered", "AAAAAAAA;XXXXXXXX;BBBBBBBB", 3, "AAAAAAAA", "BBBBBBBB"),
        ("2026-05", "Indirect", "BBBBBBBB;AAAAAAAA", 2, "BBBBBBBB", "AAAAAAAA"),
        ("2026-05", "Covered", "AAAAAAAA;CCCCCCCC", 2, "AAAAAAAA", "CCCCCCCC"),
        ("2026-07", "Covered", "AAAAAAAA;YYYYYYYY;BBBBBBBB", 3, "AAAAAAAA", "BBBBBBBB"),
        ("2026-07", "Indirect", "AAAAAAAA;ZZZZZZZZ;BBBBBBBB", 3, "AAAAAAAA", "BBBBBBBB"),
        ("2026-07", "Indirect", "BBBBBBBB;XXXXXXXY;AAAAAAAA", 3, "BBBBBBBB", "AAAAAAAA"),
        ("2026-07", "Covered", "DDDDDDDD;EEEEEEEE", 2, "DDDDDDDD", "EEEEEEEE"),
    ])
    r01.make_cohort(db, "may", "2026-05")
    r01.build_maps(db)
    r01.make_cohort(db, "july", "2026-07")
    r01.build_eval(db)
    counts = r01.summarize_model(db, "directed", "novel_path")
    assert counts["total"] == 4
    assert counts["supported"] == 3
    assert counts["unseen"] == 1
    assert counts["errors"] == 1
    assert counts["pair_units"] == 2
    assert counts["bad_pair_units"] == 1
    assert r01.summarize_model(db, "reverse", "novel_path")["supported"] >= 2
    assert r01.paired_control(db, "unordered", "novel_path")["common_n"] < 4
    db.close()


def test_one_sided_bound_and_public_small_cell_suppression():
    assert r01.upper_one_sided(0, 0) == "undefined"
    assert r01.upper_one_sided(0, 100) != "undefined"
    assert r01.upper_one_sided(1, 1) == "100.000000%"
    assert r01.safe_count(1) == "[1–9 suppressed]"
    assert r01.safe_count(10) == "10"
