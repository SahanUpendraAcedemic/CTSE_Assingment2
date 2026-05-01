from src.components.part_1_searcher.agent import searcher_agent_node


def test_searcher_agent_node_runs() -> None:
    state = {"topic": "test"}
    result = searcher_agent_node(state)
    assert result["searcher_agent_run"] is True
