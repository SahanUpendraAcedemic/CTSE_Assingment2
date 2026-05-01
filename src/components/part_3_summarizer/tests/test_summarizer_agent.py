import pytest

from src.components.part_3_summarizer.agent import summarizer_agent_node
from src.shared.schemas.research_state import ResearchState


def test_summarizer_agent_node_outputs_exactly_three_verified_bullets() -> None:
    state: ResearchState = {
        "topic": "Local Smart Research Hub",
        "verified_claims": [
            {"claim": "The system uses local Ollama-compatible models.", "source": "internal state"},
            {"text": "LangGraph-style orchestration passes shared state between components."},
            {"claim": "The summarizer receives verified claims after fact checking."},
            {"claim": "A fourth verified claim is available but should not create a fourth bullet."},
        ],
        "rejected_claims": [
            {"claim": "The summarizer performs live web research.", "reason": "No evidence."}
        ],
        "logs": [],
    }
    result = summarizer_agent_node(state)

    summary = result["summary"]
    assert len(summary) == 3
    assert all(bullet.startswith("- ") for bullet in summary)
    assert "local Ollama-compatible models" in summary[0]
    assert "LangGraph-style orchestration" in summary[1]
    assert "verified claims after fact checking" in summary[2]
    assert "live web research" not in "\n".join(summary)
    assert result["logs"][-1]["status"] == "success"
    assert result["logs"][-1]["summary_count"] == 3


def test_summarizer_agent_node_excludes_rejected_duplicate_claims() -> None:
    state: ResearchState = {
        "topic": "Duplicate filtering",
        "verified_claims": [
            {"claim": "This duplicated claim must be excluded.", "verified": True},
            {"claim": "This explicitly unverified claim must be excluded.", "verified": False},
            {"claim": "This clean verified claim should remain.", "verified": True},
        ],
        "rejected_claims": [{"claim": "This duplicated claim must be excluded."}],
        "logs": [],
    }
    result = summarizer_agent_node(state)
    combined_summary = "\n".join(result["summary"])

    assert "This clean verified claim should remain." in combined_summary
    assert "This duplicated claim must be excluded." not in combined_summary
    assert "This explicitly unverified claim must be excluded." not in combined_summary
    assert len(result["summary"]) == 3


def test_summarizer_agent_node_uses_safe_state_only_fillers_for_short_input() -> None:
    state: ResearchState = {
        "topic": "Short verified state",
        "verified_claims": [{"claim": "One verified claim is available in shared state."}],
        "rejected_claims": [],
        "logs": [{"agent": "FactCheckerAgent", "status": "success"}],
    }
    result = summarizer_agent_node(state)

    assert result["summary"] == [
        "- One verified claim is available in shared state.",
        "- Only one verified claim was supplied in shared state.",
        "- Remaining summary slots are intentionally left without new factual claims.",
    ]
    assert result["logs"][0]["agent"] == "FactCheckerAgent"


def test_summarizer_agent_node_handles_no_verified_claims_without_inventing_facts() -> None:
    state: ResearchState = {
        "topic": "Empty verified state",
        "verified_claims": [],
        "rejected_claims": [{"claim": "A rejected claim must stay out."}],
        "logs": [],
    }
    result = summarizer_agent_node(state)
    combined_summary = "\n".join(result["summary"])

    assert result["summary"] == [
        "- No verified claims were available in shared state.",
        "- The executive summary cannot report evidence-backed findings from this state.",
        "- Additional verified claims are required before final formatting.",
    ]
    assert "A rejected claim must stay out." not in combined_summary


def test_summarizer_agent_node_requires_topic() -> None:
    state: ResearchState = {
        "topic": "   ",
        "verified_claims": [{"claim": "A verified claim is present."}],
        "logs": [],
    }

    with pytest.raises(ValueError, match="Missing or empty topic"):
        summarizer_agent_node(state)
