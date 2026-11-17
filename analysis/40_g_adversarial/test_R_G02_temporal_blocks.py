"""Invented temporal shock examples; never sponsor rows."""
import pytest
from R_G02_temporal_blocks import temporal_block_diagnostics as check


def test_ten_disjoint_bank_pairs_can_share_one_temporal_shock():
    # A bank-component bootstrap could regard these as ten independent units,
    # while a shared time shock leaves only ONE independent time block.
    rows = [("week-1", 1.0) for _ in range(10)]
    r = check(rows)
    assert r["blocks"] == 1 and r["largest_share"] == 1.0
    assert not r["ci_supported"] and r["ci_lower"] is None


def test_balanced_blocks_seeded_reproducible():
    rows = [(f"week-{i}", 1.0 if i % 2 else -1.0)
            for i in range(20) for _ in range(3)]
    a = check(rows, replicates=200)
    b = check(rows, replicates=200)
    assert a == b and a["ci_supported"]
    assert a["ci_lower"] <= a["point_difference"] <= a["ci_upper"]


def test_dominant_block_abstains():
    rows = [("early", 1.0)] * 19 + [("late", -1.0)]
    r = check(rows, min_blocks=2)
    assert not r["ci_supported"]


def test_no_fake_inference_with_few_blocks():
    rows = [(f"block-{i}", float(i)) for i in range(9)]
    assert not check(rows)["ci_supported"]


def test_rejects_nonfinite_and_invalid_blocks():
    with pytest.raises(ValueError):
        check([("", 1.0)])
    with pytest.raises(ValueError):
        check([("week", float("nan"))])
    with pytest.raises(ValueError):
        check([("week", True)])


def test_empty_rejected():
    with pytest.raises(ValueError):
        check([])
