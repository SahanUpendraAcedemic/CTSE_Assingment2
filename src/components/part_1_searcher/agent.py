"""Part 1 Searcher Agent: responsible for producing raw findings into shared state."""

from __future__ import annotations

from typing import Any, Dict
from src.shared.schemas.research_state import ResearchState


def searcher_agent_node(state: ResearchState) -> ResearchState:
    """LangGraph-compatible searcher agent node."""
    return {**state, "searcher_agent_run": True}
