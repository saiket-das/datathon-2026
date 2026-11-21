"""G-039 invented fixtures for conditional permutation placebo."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent))
from R_G02_permutation_placebo import permutation_placebo_exact


def test_two_orderings_exact_half_null():
    result = permutation_placebo_exact({("A", "B")}, [("A", "B"), ("B", "A")])
    assert result["observed_ordered_recurrence"] == pytest.approx(0.5)
    assert result["permutation_null_expected_recurrence"] == pytest.approx(0.5)
    assert result["independent_route_null_sd"] == pytest.approx((0.5 / 4) ** 0.5)


def test_repeated_bank_reduces_distinct_permutations():
    result = permutation_placebo_exact({("A", "A", "B")}, [("B", "A", "A")])
    assert result["permutation_null_expected_recurrence"] == pytest.approx(1 / 3)
    assert result["observed_minus_null"] == pytest.approx(-1 / 3)


def test_full_permutation_dictionary_is_not_order_identifiable():
    result = permutation_placebo_exact(
        {("A", "B"), ("B", "A")}, [("A", "B"), ("B", "A")]
    )
    assert result["permutation_null_expected_recurrence"] == 1.0
    assert result["observed_minus_null"] == 0.0
    assert result["independent_route_null_sd"] == 0.0


def test_unsupported_multiset_has_zero_conditional_recall():
    result = permutation_placebo_exact({("A", "B")}, [("C", "D")])
    assert result["permutation_null_expected_recurrence"] == 0.0
    assert result["multiset_supported_share"] == 0.0


def test_reject_mixed_k_and_short_k():
    with pytest.raises(ValueError):
        permutation_placebo_exact({("A", "B")}, [("A", "B", "C")])
    with pytest.raises(ValueError):
        permutation_placebo_exact(set(), [("A",)])
    assert permutation_placebo_exact(set(), []) is None


def test_early_dictionary_is_set_not_frequency_weighted():
    result = permutation_placebo_exact({("A", "B")}, [("B", "A")] * 10)
    assert result["permutation_null_expected_recurrence"] == pytest.approx(0.5)
    assert result["observed_ordered_recurrence"] == 0.0
