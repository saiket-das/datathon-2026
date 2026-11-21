"""G-043 synthetic-only exact crossed-shock tests."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pytest
from R_G02_crossed_shocks import crossed_shock_diagnostics as check


def test_time_only_shock_survives_disjoint_banks():
    rows = [(f"B{i}", f"T{j}", float(j)) for i in range(10) for j in range(10)]
    r = check(rows)
    assert r["banks"] == r["blocks"] == 10
    assert r["ss_time"] > 0 and abs(r["ss_bank"]) < 1e-10
    assert abs(r["ss_interaction"]) < 1e-10


def test_bank_only_shock_survives_multiple_time_blocks():
    rows = [(f"B{i}", f"T{j}", float(i)) for i in range(10) for j in range(10)]
    r = check(rows)
    assert r["ss_bank"] > 0 and abs(r["ss_time"]) < 1e-10
    assert abs(r["ss_interaction"]) < 1e-10


def test_additive_crossed_shocks_have_both_components():
    rows = [(f"B{i}", f"T{j}", float(i+j)) for i in range(10) for j in range(10)]
    r = check(rows)
    assert r["ss_bank"] > 0 and r["ss_time"] > 0
    assert abs(r["ss_interaction"]) < 1e-10
    assert abs(r["ss_total"]-r["ss_bank"]-r["ss_time"]) < 1e-8


def test_interaction_not_misattributed_to_additive_shocks():
    rows = [(f"B{i}", f"T{j}", float(i*j)) for i in range(3) for j in range(3)]
    assert check(rows)["ss_interaction"] > 0


def test_unbalanced_grid_abstains():
    with pytest.raises(ValueError):
        check([("B0","T0",1),("B0","T1",2),("B1","T0",3)])


def test_duplicate_cell_rejected():
    with pytest.raises(ValueError):
        check([("B0","T0",1),("B0","T0",2)])


def test_nonfinite_rejected():
    with pytest.raises(ValueError):
        check([("B0","T0",float("nan"))])


def test_boolean_rejected():
    with pytest.raises(ValueError):
        check([("B0","T0",True)])
