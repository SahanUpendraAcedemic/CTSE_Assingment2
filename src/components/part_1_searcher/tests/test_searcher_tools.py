from src.components.part_1_searcher.tools import search_tool


def test_search_tool_returns_query() -> None:
    result = search_tool("example")
    assert result["query"] == "example"
    assert isinstance(result["results"], list)
