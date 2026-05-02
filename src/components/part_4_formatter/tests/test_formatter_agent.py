import copy
from pathlib import Path

import pytest
from src.components.part_4_formatter.agent import formatter_agent_node
from src.shared.schemas.research_state import ResearchState


def _build_base_state() -> ResearchState:
    return {
        "topic": "Local Smart Research Hub",
        "summary": ["Analyzed verified findings.", "Produced a concise report."],
        "verified_claims": [
            {"claim": "Local models can format verified facts.", "source": "internal state", "confidence": "high"}
        ],
        "rejected_claims": [
            {"claim": "The system can invent new facts.", "reason": "Not supported by design."}
        ],
        "sources": ["internal state", "agent logs"],
        "output_format": "md",
        "logs": [],
    }


def test_formatter_agent_node_writes_markdown_and_updates_state(tmp_path: Path) -> None:
    state = _build_base_state()
    original_state = copy.deepcopy(state)

    result = formatter_agent_node(state)

    assert result["output_file_path"].endswith(".md")
    assert Path(result["output_file_path"]).exists()
    assert result["logs"][-1]["status"] == "success"
    assert result["logs"][-1]["input_summary_count"] == len(state["summary"])
    assert state["verified_claims"] == original_state["verified_claims"]
    assert state["rejected_claims"] == original_state["rejected_claims"]
    assert state["summary"] == original_state["summary"]
    assert state["sources"] == original_state["sources"]

    content = Path(result["output_file_path"]).read_text(encoding="utf-8")
    assert "Research Brief: Local Smart Research Hub" in content
    assert "Analyzed verified findings." in content
    assert "Local models can format verified facts." in content
    assert "The system can invent new facts." in content
    assert "internal state" in content


def test_formatter_agent_node_writes_html_when_requested() -> None:
    state = _build_base_state()
    state["output_format"] = "html"

    result = formatter_agent_node(state)

    assert result["output_file_path"].endswith(".html")
    assert Path(result["output_file_path"]).exists()
    content = Path(result["output_file_path"]).read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content
    assert "Local Smart Research Hub" in content


def test_formatter_agent_node_raises_for_missing_topic() -> None:
    state = _build_base_state()
    del state["topic"]

    with pytest.raises(ValueError, match="topic"):
        formatter_agent_node(state)


def test_formatter_agent_node_raises_for_empty_summary() -> None:
    state = _build_base_state()
    state["summary"] = []

    with pytest.raises(ValueError, match="summary"):
        formatter_agent_node(state)


def test_formatter_agent_node_escapes_unsafe_html() -> None:
    state = {
        "topic": "<Unsafe Topic>",
        "summary": ["<script>alert('x')</script>"],
        "verified_claims": [{"claim": "<b>Unsafe claim</b>", "source": "state"}],
        "rejected_claims": [],
        "sources": ["<source>"],
        "output_format": "html",
        "logs": [],
    }

    result = formatter_agent_node(state)
    content = Path(result["output_file_path"]).read_text(encoding="utf-8")

    assert "&lt;Unsafe Topic&gt;" in content
    assert "&lt;script&gt;alert(&#x27;x&#x27;)&lt;/script&gt;" in content
    assert "&lt;b&gt;Unsafe claim&lt;/b&gt;" in content
    assert "&lt;source&gt;" in content
