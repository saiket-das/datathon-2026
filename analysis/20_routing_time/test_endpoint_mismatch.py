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


def test_validation_reports_visible_path_bank_overlap() -> None:
    import duckdb

    spec.loader.exec_module(module)
    with duckdb.connect() as connection:
        connection.execute("""
            CREATE TABLE sample AS SELECT i::VARCHAR sender, i::VARCHAR receiver,
              i::VARCHAR ob, i::VARCHAR bb,
              [i::VARCHAR, '...'] path, i::VARCHAR po, i::VARCHAR pb,
              i%20=0 o, i%20=1 b, 'Direct' route, 'BB' party
            FROM range(120) t(i)
        """)
        connection.execute("CREATE VIEW earlier AS SELECT * FROM sample")
        assert "| visible path banks | 120 |" in module.evaluate(connection, "confirm", "fixture")