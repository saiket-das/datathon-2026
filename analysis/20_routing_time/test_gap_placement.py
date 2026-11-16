"""Invented-data checks of conditional placeholder-placement probability laws."""
import importlib.util
from pathlib import Path

import numpy as np

SPEC = importlib.util.spec_from_file_location(
    "gap_placement", Path(__file__).with_name("H-B07_gap_placement.py")
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_single_gap_slot_laws_coincide() -> None:
    for visible in (3, 4, 5):
        cells, uniform, iid = MODULE.shape_probabilities(visible, 1)
        assert len(cells) == visible - 1
        np.testing.assert_array_equal(uniform, iid)


def test_two_gap_composition_and_iid_adjacency_differ() -> None:
    for visible in (3, 4, 5):
        cells, uniform, iid = MODULE.shape_probabilities(visible, 2)
        assert len(cells) == visible * (visible - 1) // 2
        diagonal = [a == z for a, z in cells]
        assert np.isclose(uniform[diagonal].sum(), 2 / visible)
        assert np.isclose(iid[diagonal].sum(), 1 / (visible - 1))
        assert uniform[diagonal].sum() > iid[diagonal].sum()
