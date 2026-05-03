from src.components.part_2_fact_checker.tools import verify_fact_wikipedia

def test_verify_fact_wikipedia_valid():
    result = verify_fact_wikipedia.invoke({"query": "Apollo 11"})
    assert isinstance(result, str)
    assert "Wikipedia findings" in result
    assert "moon" in result.lower() or "apollo" in result.lower()

def test_verify_fact_wikipedia_invalid():
    result = verify_fact_wikipedia.invoke({"query": "asdfghjkl123456789xyz"})
    assert "No verifying information found" in result