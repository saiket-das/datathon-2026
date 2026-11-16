"""Check frozen mismatch-law behavior on invented aggregates.

Run: uv run pytest analysis/20_routing_time/test_endpoint_mismatch.py
"""
import importlib.util
from pathlib import Path

import numpy as np

script = Path(__file__).with_name("H-B05_endpoint_mismatch.py")
spec = importlib.util.spec_from_file_location("endpoint_mismatch", script)
module = importlib.util.module_from_spec(spec)


def test_independent_and_correlated_flags_separate() -> None:
    spec.loader.exec_module(module)
    # Equal marginal rates can conceal dependence when both flags co-occur.
    stats = np.array([[40000, 2000, 2000, 100], [40000, 2000, 2000, 2000]])
    metrics = module.metrics(stats)
    assert np.allclose(metrics[0], [.05, .05, .0025, 0., 0.])
    assert np.allclose(metrics[1], [.05, .05, .05, .0475, .095])
