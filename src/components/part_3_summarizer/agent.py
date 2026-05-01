"""Part 3 Summarizer Agent placeholder."""

from __future__ import annotations

from src.shared.schemas.research_state import ResearchState


def summarizer_agent_node(state: ResearchState) -> ResearchState:
    """LangGraph-compatible summarizer placeholder."""
    return {**state, "summarizer_agent_run": True}
