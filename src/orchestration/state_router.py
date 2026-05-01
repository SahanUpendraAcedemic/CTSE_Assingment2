from __future__ import annotations

from typing import Any, Dict


def route_state(state: Dict[str, Any], next_agent: str) -> Dict[str, Any]:
    """Return shared state prepared for the next agent in the pipeline."""
    return {**state, "current_agent": next_agent}
