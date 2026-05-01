from __future__ import annotations

from src.components.part_1_searcher.agent import searcher_agent_node
from src.components.part_2_fact_checker.agent import fact_checker_agent_node
from src.components.part_3_summarizer.agent import summarizer_agent_node
from src.components.part_4_formatter.agent import formatter_agent_node
from src.orchestration.graph import build_agent_graph
from src.orchestration.state_router import route_state
from src.shared.schemas.research_state import ResearchState


def main() -> None:
    graph = build_agent_graph()
    state: ResearchState = {
        "topic": "Local Smart Research Hub",
        "verified_claims": [
            {"claim": "The system uses local Ollama-compatible models.", "source": "local state", "confidence": "high"}
        ],
        "rejected_claims": [
            {"claim": "This agent performs web search.", "reason": "Formatter Agent only formats shared state."}
        ],
        "logs": [],
    }

    state = searcher_agent_node(state)
    state = route_state(state, graph["transitions"]["part_1_searcher"])
    state = fact_checker_agent_node(state)
    state = route_state(state, graph["transitions"]["part_2_fact_checker"])
    state = summarizer_agent_node(state)
    state["output_format"] = "md"
    state = formatter_agent_node(state)

    print(f"Report saved to: {state['output_file_path']}")


if __name__ == "__main__":
    main()
