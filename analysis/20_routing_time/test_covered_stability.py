"""Invented-data checks for B04 uncertainty, suppression and freeze gate.

Run from repository root: uv run pytest analysis/20_routing_time/test_covered_stability.py
"""
import importlib.util
from pathlib import Path
import subprocess
import sys
import numpy as np
import pytest

SCRIPT = Path(__file__).with_name('H-B04_covered_bank_stability.py')
spec = importlib.util.spec_from_file_location('covered_stability', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def test_identical_cluster_errors_keep_known_ratios() -> None:
    stats = np.tile([10., 1., 4., 2., .2], (100, 1))
    low, high = m.intervals(stats)
    assert np.allclose(low, [.25, .5, .02])
    assert np.allclose(high, low)


def test_uncertainty_refuses_few_clusters() -> None:
    with pytest.raises(ValueError, match='insufficient'):
        m.intervals(np.ones((99, 5)))


def test_small_cohort_masks_statistics_and_identifier_columns_rejected() -> None:
    result = m.safe_table(['group', 'n', 'senders', 'value'], [('toy', 20, 3, 9123.4567)])
    assert '9123.4567' not in result and 'suppressed' in result
    with pytest.raises(AssertionError):
        m.safe_table(['ORDERING_BIC8'], [('INVENTED',)])


def test_confirmation_requires_freeze_before_opening_source() -> None:
    run = subprocess.run([sys.executable, str(SCRIPT), '--phase', 'confirm'], capture_output=True, text=True)
    assert run.returncode != 0 and 'requires --freeze' in run.stderr