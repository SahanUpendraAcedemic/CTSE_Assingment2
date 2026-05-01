from src.components.part_3_summarizer.agent import summarizer_agent_node


def test_summarizer_agent_node_runs() -> None:
    result = summarizer_agent_node({"verified_claims": []})
    assert result["summarizer_agent_run"] is True
