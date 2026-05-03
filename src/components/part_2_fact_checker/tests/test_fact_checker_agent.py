from src.components.part_2_fact_checker.agent import fact_checker_node

def test_fact_checker_catches_hallucination():
    """
    LLM-as-a-Judge test: Feed the agent a known lie and ensure it corrects it.
    """
    # Fake state simulating output from Agent 1
    mock_state = {
        "research_data": "The Python programming language was invented by Elon Musk in 2015."
    }
    
    # Run the node
    result_state = fact_checker_node(mock_state)
    verified_text = result_state["verified_data"].lower()
    
    # Assertions
    # It should correct Elon Musk to Guido van Rossum, and 2015 to 1991
    assert "guido van rossum" in verified_text
    assert "elon musk" not in verified_text or "not invented by elon musk" in verified_text