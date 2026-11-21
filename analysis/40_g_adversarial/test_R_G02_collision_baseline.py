"""Synthetic mathematical controls; no sponsor records."""
import importlib.util
from pathlib import Path
import math
import pytest

spec = importlib.util.spec_from_file_location(
    "r_g02_baseline", Path(__file__).with_name("R_G02_collision_baseline.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def test_uniform_two_draws():
    assert m.collision_probability([1, 1, 1, 1], 2) == pytest.approx(0.25)


def test_skewed_two_draws():
    assert m.collision_probability([9, 1], 2) == pytest.approx(0.82)


def test_birthday_three_draws():
    assert m.collision_probability([1, 1, 1], 3) == pytest.approx(7 / 9)


def test_structurally_ineligible_and_pigeonhole():
    assert m.collision_probability([1, 2], 0) == 0
    assert m.collision_probability([1, 2], 1) == 0
    assert m.collision_probability([1, 0, 2], 3) == 1


def test_scale_invariance():
    assert m.collision_probability([2, 3, 5], 2) == pytest.approx(
        m.collision_probability([0.2, 0.3, 0.5], 2))


@pytest.mark.parametrize("weights,k", [
    ([], 2), ([0, 0], 2), ([-1, 2], 2),
    ([float("nan"), 1], 2), ([float("inf"), 1], 2),
    ([1, 1], -1), ([1, 1], 1.5), ([1, 1], True),
])
def test_invalid_inputs_fail_closed(weights, k):
    with pytest.raises(ValueError):
        m.collision_probability(weights, k)


def test_many_categories_no_factorial_overflow():
    # Previous factorial(k) * e_k implementation overflowed for k >= 171.
    assert m.collision_probability([1] * 200, 171) == pytest.approx(1.0)
    assert m.collision_probability([1] * 200, 200) == pytest.approx(1.0)


def test_two_draw_probability_large_support():
    # Exact birthday probability for uniform categorical draws.
    assert m.collision_probability([1] * 1000, 2) == pytest.approx(0.001)
