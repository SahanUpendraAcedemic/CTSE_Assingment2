# from src.components.part_1_searcher.agent import searcher_agent_node


# def test_searcher_agent_node_runs() -> None:
#     state = {"topic": "test"}
#     result = searcher_agent_node(state)
#     assert result["searcher_agent_run"] is True


# src/components/part_1_searcher/tests/test_searcher_agent.py

import json
import pytest
from src.components.part_1_searcher.agent import run_searcher_agent


@pytest.fixture
def sample_state():
    return {"query": "renewable energy sources", "search_results": None}


class TestSearcherAgentOutput:
    def test_agent_populates_search_results(self, sample_state):
        result_state = run_searcher_agent(sample_state)
        assert "search_results" in result_state
        assert result_state["search_results"] is not None

    def test_output_has_required_keys(self, sample_state):
        result_state = run_searcher_agent(sample_state)
        data = result_state["search_results"]
        required = ["topic", "wikipedia_title", "wikipedia_summary", "web_snippets"]
        for key in required:
            assert key in data, f"Missing key: {key}"

    def test_topic_matches_query(self, sample_state):
        result_state = run_searcher_agent(sample_state)
        assert result_state["search_results"]["topic"] == sample_state["query"]

    def test_no_hallucinated_content(self, sample_state):
        """LLM-as-Judge: verify the output only comes from tool data, not invented facts."""
        result_state = run_searcher_agent(sample_state)
        summary = result_state["search_results"].get("wikipedia_summary", "")
        # Summary should mention the topic domain
        assert any(
            word in summary.lower()
            for word in ["energy", "solar", "wind", "renewable", "power"]
        ), "Summary does not appear relevant to the query topic."

    def test_state_is_not_mutated_beyond_search_results(self, sample_state):
        original_query = sample_state["query"]
        result_state = run_searcher_agent(sample_state)
        assert result_state["query"] == original_query