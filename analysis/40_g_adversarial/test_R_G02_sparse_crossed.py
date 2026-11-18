"""Invented G-044 fixtures; never sponsor records."""
import pytest
from R_G02_sparse_crossed import crossed_support


def test_complete_grid_one_incidence_component_despite_two_way_support():
    rows = [(f"B{b}", f"T{t}", float(b+t)) for b in range(10) for t in range(10)]
    x = crossed_support(rows)
    assert x["one_way_support_gates_pass"]
    assert x["incidence_components"] == 1
    assert x["largest_incidence_component_share"] == 1
    assert x["cell_coverage"] == 1
    assert x["joint_ci"] is None


def test_disjoint_diagonal_has_ten_components():
    rows = [(f"B{i}", f"T{i}", float(i)) for i in range(10)]
    x = crossed_support(rows)
    assert x["incidence_components"] == 10
    assert x["cell_coverage"] == pytest.approx(0.1)
    assert x["one_way_support_gates_pass"]


def test_bridge_merges_components_transitively():
    rows = [("A", "X", 1), ("B", "Y", 2), ("A", "Y", 3)]
    x = crossed_support(rows, min_banks=2, min_times=2, max_share=1)
    assert x["incidence_components"] == 1
    assert x["observed_cells"] == 3


def test_repeated_cell_is_not_falsely_new_support():
    x = crossed_support([("A", "X", 1), ("A", "X", 2), ("B", "Y", 3)], 2, 2, 1)
    assert x["observed_cells"] == 2
    assert x["observations"] == 3


@pytest.mark.parametrize("rows", [[], [("A", "X", float("nan"))], [("A", "X", True)], [("", "X", 1)]])
def test_invalid_rows_rejected(rows):
    with pytest.raises(ValueError):
        crossed_support(rows)


def test_one_way_gates_fail_on_concentration():
    rows = [("A", "X", 0)] * 20 + [("B", "Y", 1)]
    assert not crossed_support(rows, 2, 2)["one_way_support_gates_pass"]
