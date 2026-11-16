"""Test consumer-origin, variable-amount, chronological romance copy bursts.

Run from the repository root:
    uv run python analysis/30_parties_anomalies/H-C02_romance_bursts.py --phase explore
    uv run python analysis/30_parties_anomalies/H-C02_romance_bursts.py --phase confirm --freeze-commit SHA
The exact shared implementation and safe aggregate renderer live in H-C01.
"""

from pathlib import Path
import runpy
import sys

if __name__ == "__main__":
    investigation = runpy.run_path(str(Path(__file__).with_name("H-C01_duplicate_bursts.py")))
    sys.exit(investigation["main"]("romance"))
