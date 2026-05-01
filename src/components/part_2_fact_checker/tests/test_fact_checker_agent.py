from src.components.part_2_fact_checker.agent import fact_checker_agent_node


def test_fact_checker_agent_node_runs() -> None:
    state = {"verified_claims": []}
    result = fact_checker_agent_node(state)
    assert result["fact_checker_agent_run"] is True
