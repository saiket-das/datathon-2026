"""Check the count law, latency fit, privacy suppression and freeze gate with invented data.

Run from the repository root: uv run pytest analysis/20_routing_time/test_routing_research.py
No sponsor dataset is needed.
"""

import importlib.util
from pathlib import Path
import sys

import duckdb
import numpy as np
import pytest

HERE = Path(__file__).parent


def load(stem: str):
    """Load a hyphen-named investigation without relying on pytest's import mode."""
    sys.path.insert(0, str(HERE))
    try:
        spec = importlib.util.spec_from_file_location(stem, HERE / f"{stem}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


def test_joint_law_matches_closed_form() -> None:
    module = load("H-B02_route_gap_process")
    cells = module.cell_probabilities().reshape(6, 3)
    assert cells.sum() == pytest.approx(1)
    assert cells[0, 0] == pytest.approx(.60)
    assert cells[0, 1] == pytest.approx(.60 * .05)
    assert cells[1, 1] == pytest.approx(.60 * 2 * .35 * .05)
    assert cells[0].sum() == pytest.approx(.60 / .95)
    assert cells[5].sum() == pytest.approx((.35 / .95) ** 5)
    assert 1 - cells[2, 0] / cells[2].sum() == pytest.approx(1 - .95 ** 3)


def test_additive_fit_and_duplicate_bank_multiplicity() -> None:
    module = load("H-B01_bank_additive_duration")
    effects = np.array([4., 12., 80.])
    pairs = np.array([[a, b, n, n * (effects[a] + effects[b])]
                      for a, b, n in [(0, 1, 100), (0, 2, 200), (1, 2, 300), (0, 0, 100)]])
    fitted, support, iterations = module.fit_effects(pairs, 3)
    assert fitted == pytest.approx(effects, abs=1e-6)
    assert support.tolist() == [500, 400, 500]
    assert iterations < 2000


def test_small_groups_suppressed(tmp_path, monkeypatch) -> None:
    common = load("routing_common")
    monkeypatch.setattr(common, "OUT", tmp_path)
    common.report("fixture", "explore", None, {
        "privacy": (["group", "n", "senders", "receivers", "banks", "mean"],
                    [("small", 3, 2, 2, 1, 123456.), ("thin", 500, 2, 400, 120, 654321.)])})
    result = (tmp_path / "fixture_explore.md").read_text()
    assert "123456" not in result and "654321" not in result
    assert "suppressed" in result


def test_confirmation_requires_freeze(monkeypatch) -> None:
    common = load("routing_common")
    monkeypatch.setattr(sys, "argv", ["fixture", "--phase", "confirm"])
    with pytest.raises(SystemExit):
        common.arguments("fixture")


def test_eligible_overlap_includes_cross_role_accounts() -> None:
    common = load("routing_common")
    with duckdb.connect() as con:
        con.execute("""CREATE TABLE sample AS SELECT 1 ROW_ID,'sender' oa,'receiver' ba,
          'bank_a' ob,'bank_b' bb,['bank_a','middle','bank_b'] path,false labelled""")
        common.remember_exploration(con)
        con.execute("""CREATE OR REPLACE TABLE sample AS SELECT 2 ROW_ID,'new' oa,'sender' ba,
          'bank_c' ob,'bank_d' bb,['bank_c','middle','bank_d'] path,false labelled""")
        columns, rows = common.overlaps(con, "sample", "NOT labelled")
        assert columns == ["row_ids", "either_role_accounts", "endpoint_banks", "visible_path_banks"]
        assert rows == [(0, 1, 0, 1)]


def test_receiver_rank_checkerboard_counterexample() -> None:
    module = load("H-B27_nested_receiver_rank")
    with duckdb.connect() as con:
        con.execute("""CREATE TABLE supported AS
            SELECT origin a,receiver b,
                   (receiver<CASE WHEN origin=0 THEN 30 ELSE 60 END)::INT covered
            FROM range(2) o(origin) CROSS JOIN range(100) r(receiver)""")
        nested = module.checkerboards(con)
        assert nested[0] == 1 and nested[3] == 100
        assert nested[4:7] == (0, 0, 0)
        con.execute("""UPDATE supported SET covered=(b>=50)::INT WHERE a=1""")
        crossed = module.checkerboards(con)
        assert crossed[4] == 1 and crossed[5] == 1500
        assert crossed[6] == 1 and crossed[7] == pytest.approx(.3)
