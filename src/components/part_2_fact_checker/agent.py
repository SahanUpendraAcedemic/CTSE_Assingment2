"""Part 2 Fact Checker Agent: responsible for verifying candidate claims in shared state."""

from __future__ import annotations

from typing import Any, Dict
from src.shared.schemas.research_state import ResearchState


def fact_checker_agent_node(state: ResearchState) -> ResearchState:
    """LangGraph-compatible fact checker agent node."""
    return {**state, "fact_checker_agent_run": True}
