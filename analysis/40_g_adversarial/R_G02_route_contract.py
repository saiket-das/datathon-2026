"""R-G02 B14: dataset-independent route tokenizer and eligibility contract.

DESIGN ONLY. No sponsor input, no validation, no scientific freeze.
The tokenizer deliberately returns *counts and booleans* only. Never log tokens.
"""
from __future__ import annotations
import re

BIC8 = re.compile(r"^[A-Z0-9]{8}$")


def route_features(path: object) -> dict[str, int | bool]:
    """Strictly reject malformed visible routes rather than silently repair them.

    Ellipsis indicates censored interior: a visible repeat is a lower bound,
    never an observed full-route noncollision. Endpoint nodes are excluded
    from intermediary positions, including when an endpoint repeats inside.
    """
    if not isinstance(path, str) or not path.strip():
        return {"parseable": False, "censored": False, "intermediaries": 0,
                "collision": False, "eligible": False}
    parts = [p.strip() for p in path.split(";")]
    censored = any(p in {"...", "…"} for p in parts)
    visible = [p for p in parts if BIC8.fullmatch(p)]
    malformed = any(not BIC8.fullmatch(p) and p not in {"...", "…"}
                    for p in parts)
    parseable = not malformed and len(visible) >= 2
    middle = visible[1:-1] if parseable else []
    eligible = parseable and not censored and len(middle) >= 2
    return {"parseable": parseable, "censored": censored,
            "intermediaries": len(middle), "collision": eligible and len(set(middle)) < len(middle),
            "eligible": eligible}
