"""Invented tests only; never sponsor rows."""
import pytest
from R_G02_bank_components import bank_component_diagnostics as check


def test_transitive_shared_bank_is_one_component():
    rows = [("A", "X", 1.), ("B", "X", -1.), ("B", "Y", 1.),
            ("C", "Z", 0.)]
    r = check(rows, min_components=2, max_component_share=1)
    assert r["components"] == 2
    assert r["largest_share"] == 0.75
    assert not r["ci_supported"]


def test_sender_receiver_roles_not_accidentally_collapsed():
    rows = [("A", "X", 1.), ("X", "B", 0.)]
    r = check(rows, min_components=2, max_component_share=1)
    assert r["components"] == 2


def test_deterministic_paired_cluster_bootstrap():
    rows = [(f"S{i}", f"R{i}", (-1.)**i) for i in range(20)]
    a = check(rows, replicates=200, min_components=10)
    b = check(rows, replicates=200, min_components=10)
    assert a == b and a["ci_supported"]
    assert a["ci_lower"] <= a["point_difference"] <= a["ci_upper"]


def test_giant_component_abstains():
    rows = [("A", f"R{i}", 1.) for i in range(19)] + [("B", "Q", 0.)]
    r = check(rows)
    assert not r["ci_supported"] and r["ci_lower"] is None


def test_invalid_difference_rejected():
    with pytest.raises(ValueError):
        check([("A", "B", float("nan"))])


def test_empty_rejected():
    with pytest.raises(ValueError):
        check([])
