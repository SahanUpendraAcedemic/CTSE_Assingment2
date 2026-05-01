from __future__ import annotations

from typing import Any, Dict


def build_agent_graph() -> Dict[str, Any]:
    """Create a simple runtime graph definition for LangGraph-style orchestration."""
    return {
        "agents": [
            "part_1_searcher",
            "part_2_fact_checker",
            "part_3_summarizer",
            "part_4_formatter",
        ],
        "transitions": {
            "part_1_searcher": "part_2_fact_checker",
            "part_2_fact_checker": "part_3_summarizer",
            "part_3_summarizer": "part_4_formatter",
        },
    }
