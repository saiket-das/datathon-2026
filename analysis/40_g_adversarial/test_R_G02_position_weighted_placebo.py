"""Synthetic G-040 controls, no sponsor data."""
from math import isclose, isnan
import pytest
from R_G02_position_weighted_placebo import position_weighted_placebo as run


def test_position_preference_breaks_uniform_half_null():
    early = [("A", "B")] * 9 + [("B", "A")]
    r = run(early, [("A", "B")])
    # Both orders are in dictionary, so recurrence is necessarily one.
    assert r["weighted_null_recurrence"] == 1.0


def test_single_order_dictionary_with_positional_bias():
    early = [("A", "B")] * 9 + [("A", "C"), ("C", "B")]
    r = run(early, [("B", "A")])
    assert 0.5 < r["weighted_null_recurrence"] < 1
    assert r["observed_supported_recurrence"] == 0


def test_repeated_identities_are_not_multiplied():
    early = [("A", "A", "B")]
    r = run(early, [("A", "A", "B")])
    assert isclose(r["weighted_null_recurrence"], 0.5)


def test_unseen_category_abstains_and_denominator_preserved():
    r = run([("A", "B")], [("A", "B"), ("A", "Z")])
    assert r["n"] == 2
    assert r["supported_n"] == 1
    assert r["support_share"] == 0.5


def test_empty_training_abstains():
    r = run([], [("A", "B")])
    assert r["supported_n"] == 0 and isnan(r["weighted_null_recurrence"])


def test_invalid_k_and_alpha():
    with pytest.raises(ValueError):
        run([("A", "B")], [("A", "B", "C")])
    with pytest.raises(ValueError):
        run([("A", "B")], [("A", "B")], alpha=0)


def test_cap_abstains_without_approximation():
    r = run([("A", "B", "C")], [("A", "B", "C")], max_distinct_permutations=2)
    assert r["supported_n"] == 0
