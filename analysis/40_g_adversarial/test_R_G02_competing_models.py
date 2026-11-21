"""Synthetic-only G-035 falsification fixtures. No dataset imports or payment rows."""
from pathlib import Path
import sys
import pytest

sys.path.insert(0, str(Path(__file__).parent))
from R_G02_competing_models import (
    brier, iid_collision, may_weights, may_week_mixture,
    motif_recurrence_probability, strict_no_replacement, template_mixture,
)


def test_global_may_weights_keep_unobserved_may_universe_categories():
    w = may_weights({"A": 3, "B": 1}, ["A", "B", "C"])
    assert w == pytest.approx({"A": 4 / 7, "B": 2 / 7, "C": 1 / 7})
    assert sum(w.values()) == pytest.approx(1.0)


def test_unseen_july_identity_never_enlarges_may_universe():
    w = may_weights({"A": 1, "B": 1}, ["A", "B"])
    assert motif_recurrence_probability({("A", "Z")}, w) == 0.0
    with pytest.raises(ValueError):
        may_weights({"Z": 1}, ["A", "B"])


def test_template_copying_mixture_is_distinct_from_iid_collision():
    weights = {"A": 0.5, "B": 0.5}
    early = [("A", "A")] * 100
    late = [("A", "A")] * 75 + [("A", "B")] * 25
    est = template_mixture(early, late, weights)
    assert est is not None
    assert est["iid_motif_mass"] == pytest.approx(0.25)
    assert est["lambda"] == pytest.approx(2 / 3)
    assert est["recurrence_probability"] == pytest.approx(0.75)
    assert est["collision_probability"] > est["iid_collision"]


def test_template_estimator_abstains_on_support_or_identifiability():
    weights = {"A": 0.5, "B": 0.5}
    assert template_mixture([("A", "A")] * 99,
                            [("A", "A")] * 100, weights) is None
    all_motifs = [("A", "A"), ("A", "B"), ("B", "A"), ("B", "B")]
    assert template_mixture(all_motifs * 25, all_motifs * 25, weights) is None
    with pytest.raises(ValueError):
        template_mixture([("A", "A")] * 100, [("A",)] * 100, weights)


def test_collision_is_not_a_template_recurrence_test():
    w = {"A": 0.5, "B": 0.5}
    assert iid_collision(w, 2) == pytest.approx(0.5)
    assert motif_recurrence_probability({("A", "B")}, w) == pytest.approx(0.25)
    assert motif_recurrence_probability({("B", "A")}, w) == pytest.approx(0.25)
    assert ("A", "B") != ("B", "A")


def test_no_replacement_structural_support():
    assert strict_no_replacement(2, 2) == 0.0
    assert strict_no_replacement(3, 2) is None
    assert strict_no_replacement(1, 2) is None
    with pytest.raises(ValueError):
        strict_no_replacement(2.0, 4)


def test_week_mixture_not_marginal_pooling():
    counts = [{"A": 90, "B": 10}, {"A": 10, "B": 90}, {}, {}, {}]
    routes = [100, 100, 0, 0, 0]
    p = may_week_mixture(counts, routes, ["A", "B"], 2)
    assert p is not None and p > 0.8
    pooled = may_weights({"A": 100, "B": 100}, ["A", "B"])
    assert iid_collision(pooled, 2) == pytest.approx(0.5)
    assert p != pytest.approx(iid_collision(pooled, 2))


def test_week_mixture_abstains_without_2_supported_blocks():
    counts = [{"A": 300}, {"A": 99}, {}, {}, {}]
    assert may_week_mixture(counts, [100, 99, 0, 0, 0], ["A"], 2) is None
    with pytest.raises(ValueError):
        may_week_mixture([{"A": 300}], [100], ["A"], 2)


def test_brier_score_requires_probability_and_binary_outcome():
    assert brier(1, 0.8) == pytest.approx(0.04)
    assert brier(0, 0.2) == pytest.approx(0.04)
    for p in (-0.01, 1.01, float("nan")):
        with pytest.raises(ValueError):
            brier(0, p)


def test_unordered_motif_mass_counts_permutations_once():
    from R_G02_competing_models import unordered_motif_recurrence_probability
    w = {"A": 0.5, "B": 0.5}
    assert unordered_motif_recurrence_probability({("A", "B")}, w) == pytest.approx(0.5)
    assert unordered_motif_recurrence_probability(
        {("A", "B"), ("B", "A")}, w
    ) == pytest.approx(0.5)
    assert unordered_motif_recurrence_probability(
        {("A", "A", "B")}, w
    ) == pytest.approx(3 / 8)
    assert unordered_motif_recurrence_probability(
        {("A", "A", "A")}, w
    ) == pytest.approx(1 / 8)


def test_ordered_recurrence_fails_to_identify_multiset_cache():
    from R_G02_competing_models import ordered_vs_unordered_recurrence
    early = {("A", "B")}
    late = [("B", "A")] * 100
    scores = ordered_vs_unordered_recurrence(early, late)
    assert scores == pytest.approx({
        "ordered_recurrence": 0.0,
        "unordered_recurrence": 1.0,
        "order_sensitive_gap": 1.0,
    })
    assert all(len(set(t)) == 2 for t in late)
    assert all(len(set(t)) == 2 for t in early)


def test_recurrence_placebo_rejects_mixed_k():
    from R_G02_competing_models import ordered_vs_unordered_recurrence
    with pytest.raises(ValueError):
        ordered_vs_unordered_recurrence({("A", "B")}, [("A", "B", "C")])
    assert ordered_vs_unordered_recurrence(set(), []) is None
