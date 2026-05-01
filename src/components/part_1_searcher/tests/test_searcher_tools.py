# from src.components.part_1_searcher.tools import search_tool


# def test_search_tool_returns_query() -> None:
#     result = search_tool("example")
#     assert result["query"] == "example"
#     assert isinstance(result["results"], list)


# src/components/part_1_searcher/tests/test_searcher_tools.py

import pytest
from unittest.mock import patch, MagicMock
from src.components.part_1_searcher.tools import search_wikipedia, search_duckduckgo


class TestSearchWikipedia:
    def test_returns_dict_with_required_keys(self):
        result = search_wikipedia("Python programming language")
        assert isinstance(result, dict)
        assert all(k in result for k in ("title", "summary", "url", "error"))

    def test_valid_query_returns_non_empty_summary(self):
        result = search_wikipedia("Artificial intelligence")
        assert result["error"] == ""
        assert len(result["summary"]) > 50

    def test_returns_error_key_on_bad_query(self):
        result = search_wikipedia("xzqfjklmwpqrxyz123notarealthing")
        # Either an HTTP error or empty summary — should NOT raise an exception
        assert isinstance(result["error"], str)

    def test_timeout_is_handled_gracefully(self):
        with patch("requests.get", side_effect=__import__("requests").exceptions.Timeout):
            result = search_wikipedia("quantum computing")
        assert "timed out" in result["error"].lower()
        assert result["summary"] == ""

    def test_sentence_count_is_respected(self):
        result = search_wikipedia("Python programming language", sentences=2)
        sentences = [s for s in result["summary"].split(".") if s.strip()]
        assert len(sentences) <= 3  # 2 sentences + possible trailing empty


class TestSearchDuckDuckGo:
    def test_returns_list_of_dicts(self):
        result = search_duckduckgo("machine learning")
        assert isinstance(result, list)
        assert all(isinstance(r, dict) for r in result)

    def test_each_result_has_text_and_url(self):
        result = search_duckduckgo("climate change")
        for item in result:
            assert "text" in item
            assert "url" in item

    def test_handles_network_error_gracefully(self):
        with patch("requests.get", side_effect=Exception("network failure")):
            result = search_duckduckgo("test query")
        assert len(result) == 1
        assert "Error" in result[0]["text"]

    def test_max_results_respected(self):
        result = search_duckduckgo("space exploration", max_results=2)
        # DuckDuckGo abstract + up to 2 related = max 3 items
        assert len(result) <= 3