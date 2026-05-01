# from __future__ import annotations

# from src.components.part_1_searcher.agent import searcher_agent_node
# from src.components.part_2_fact_checker.agent import fact_checker_agent_node
# from src.components.part_3_summarizer.agent import summarizer_agent_node
# from src.components.part_4_formatter.agent import formatter_agent_node
# from src.orchestration.graph import build_agent_graph
# from src.orchestration.state_router import route_state
# from src.shared.schemas.research_state import ResearchState


# def main() -> None:
#     graph = build_agent_graph()
#     state: ResearchState = {
#         "topic": "Local Smart Research Hub",
#         "verified_claims": [
#             {"claim": "The system uses local Ollama-compatible models.", "source": "local state", "confidence": "high"}
#         ],
#         "rejected_claims": [
#             {"claim": "This agent performs web search.", "reason": "Formatter Agent only formats shared state."}
#         ],
#         "logs": [],
#     }

#     state = searcher_agent_node(state)
#     state = route_state(state, graph["transitions"]["part_1_searcher"])
#     state = fact_checker_agent_node(state)
#     state = route_state(state, graph["transitions"]["part_2_fact_checker"])
#     state = summarizer_agent_node(state)
#     state["output_format"] = "md"
#     state = formatter_agent_node(state)

#     print(f"Report saved to: {state['output_file_path']}")


# if __name__ == "__main__":
#     main()


from __future__ import annotations
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

# ── safely import only what exists ──────────────────────────────────────────
from src.components.part_1_searcher.agent import run_searcher_agent

try:
    from src.components.part_2_fact_checker.agent import fact_checker_agent_node
    FACT_CHECKER_READY = True
except ImportError:
    FACT_CHECKER_READY = False
    print("[WARNING] Fact Checker not ready yet, skipping.")

try:
    from src.components.part_3_summarizer.agent import summarizer_agent_node
    SUMMARIZER_READY = True
except ImportError:
    SUMMARIZER_READY = False
    print("[WARNING] Summarizer not ready yet, skipping.")

try:
    from src.components.part_4_formatter.agent import formatter_agent_node
    FORMATTER_READY = True
except ImportError:
    FORMATTER_READY = False
    print("[WARNING] Formatter not ready yet, skipping.")


def main() -> None:
    # ── initial state ────────────────────────────────────────────────────────
    state: dict = {
        "query": "artificial intelligence",   # change topic here
        "search_results": None,
        "verified_claims": [],
        "rejected_claims": [],
        "summary": None,
        "output_format": "md",
        "output_file_path": None,
        "logs": [],
    }

    # ── Agent 1: Searcher ────────────────────────────────────────
    print("\n=== Agent 1: Searcher ===")
    state = run_searcher_agent(state)
    print(json.dumps(state["search_results"], indent=2))

    # # ── Agent 2: Fact Checker ────────────────────────────────────────────────
    # if FACT_CHECKER_READY:
    #     print("\n=== Agent 2: Fact Checker ===")
    #     state = fact_checker_agent_node(state)

    # # ── Agent 3: Summarizer ──────────────────────────────────────────────────
    # if SUMMARIZER_READY:
    #     print("\n=== Agent 3: Summarizer ===")
    #     state = summarizer_agent_node(state)

    # # ── Agent 4: Formatter ───────────────────────────────────────────────────
    # if FORMATTER_READY:
    #     print("\n=== Agent 4: Formatter ===")
    #     state["output_format"] = "md"
    #     state = formatter_agent_node(state)
    #     print(f"Report saved to: {state['output_file_path']}")

    print("\n=== Done ===")


if __name__ == "__main__":
    main()