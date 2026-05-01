"""Part 3 Summarizer Agent.

This node reads only verified claims from the shared LangGraph-style state and
returns exactly three executive-summary bullets. It is deterministic and
local-only, so it never performs research or calls external APIs.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import Any

from src.components.part_3_summarizer.tools import (
    BULLET_PREFIX,
    EXPECTED_SUMMARY_BULLETS,
    validate_summary_quality,
)
from src.shared.schemas.research_state import ResearchState


def _normalize_text(value: Any) -> str:
    """Return whitespace-normalized text only for string inputs."""
    if not isinstance(value, str):
        return ""
    return " ".join(value.split())


def _extract_claim_text(claim: Mapping[str, Any]) -> str:
    """Extract a claim string from the supported upstream fact-checker shapes."""
    for key in ("claim", "text", "statement"):
        claim_text = _normalize_text(claim.get(key))
        if claim_text:
            return claim_text
    return ""


def _safe_claim_sequence(value: Any) -> Sequence[Mapping[str, Any]]:
    """Return claim dictionaries from shared state or an empty sequence."""
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    return [claim for claim in value if isinstance(claim, Mapping)]


def _verified_claim_texts(
    verified_claims: Sequence[Mapping[str, Any]],
    rejected_claims: Sequence[Mapping[str, Any]],
) -> list[str]:
    """Return de-duplicated verified claim text, excluding rejected/unverified items."""
    rejected_texts = {
        _extract_claim_text(claim).casefold()
        for claim in rejected_claims
        if _extract_claim_text(claim)
    }

    seen: set[str] = set()
    verified_texts: list[str] = []
    for claim in verified_claims:
        if claim.get("verified") is False:
            continue

        claim_text = _extract_claim_text(claim)
        folded_text = claim_text.casefold()
        if not claim_text or folded_text in rejected_texts or folded_text in seen:
            continue

        seen.add(folded_text)
        verified_texts.append(claim_text)

    return verified_texts


def _state_only_fillers(verified_claim_count: int) -> list[str]:
    """Return safe filler bullets based only on shared-state counts."""
    if verified_claim_count == 0:
        return [
            "No verified claims were available in shared state.",
            "The executive summary cannot report evidence-backed findings from this state.",
            "Additional verified claims are required before final formatting.",
        ]
    if verified_claim_count == 1:
        return [
            "Only one verified claim was supplied in shared state.",
            "Remaining summary slots are intentionally left without new factual claims.",
        ]
    return ["Only two verified claims were supplied in shared state."]


def _build_summary(
    verified_claims: Sequence[Mapping[str, Any]],
    rejected_claims: Sequence[Mapping[str, Any]],
) -> list[str]:
    """Build exactly three executive-summary bullets from verified state only."""
    verified_texts = _verified_claim_texts(verified_claims, rejected_claims)
    summary = [f"{BULLET_PREFIX}{claim_text}" for claim_text in verified_texts[:EXPECTED_SUMMARY_BULLETS]]

    for filler in _state_only_fillers(len(verified_texts)):
        if len(summary) == EXPECTED_SUMMARY_BULLETS:
            break
        summary.append(f"{BULLET_PREFIX}{filler}")

    return summary[:EXPECTED_SUMMARY_BULLETS]


def summarizer_agent_node(state: ResearchState) -> ResearchState:
    """LangGraph-compatible summarizer node for Part 3."""
    topic = _normalize_text(state.get("topic"))
    if not topic:
        raise ValueError("Missing or empty topic in research state.")

    verified_claims = _safe_claim_sequence(state.get("verified_claims", []))
    rejected_claims = _safe_claim_sequence(state.get("rejected_claims", []))
    summary = _build_summary(verified_claims, rejected_claims)

    if not validate_summary_quality(
        summary,
        verified_claims=verified_claims,
        rejected_claims=rejected_claims,
    ):
        raise ValueError("Generated summary failed quality validation.")

    log_entry = {
        "agent": "SummarizerAgent",
        "action": "generate_summary",
        "status": "success",
        "verified_claim_count": len(verified_claims),
        "rejected_claim_count": len(rejected_claims),
        "summary_count": len(summary),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    new_state = dict(state)
    new_state["summary"] = summary
    new_state["logs"] = list(state.get("logs", [])) + [log_entry]
    return new_state
