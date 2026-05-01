"""Custom validation tool for the Part 3 Summarizer Agent.

The tool is intentionally deterministic and local-only. It validates the
summary text already produced from shared state; it does not perform research,
network calls, or model calls.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

EXPECTED_SUMMARY_BULLETS = 3
BULLET_PREFIX = "- "
MIN_CLAIM_TEXT_LENGTH = 8

_STATE_ONLY_PHRASES = (
    "no verified claims were available",
    "cannot report evidence-backed findings",
    "additional verified claims are required",
    "only one verified claim was supplied",
    "only two verified claims were supplied",
    "remaining summary slots are intentionally left",
)


def _normalise_text(value: Any) -> str:
    """Return clean text for a known string value, otherwise an empty string."""
    if not isinstance(value, str):
        return ""
    return " ".join(value.split())


def _extract_claim_text(claim: Mapping[str, Any]) -> str:
    """Extract the supported claim text field from a verified/rejected claim."""
    for key in ("claim", "text", "statement"):
        text = _normalise_text(claim.get(key))
        if text:
            return text
    return ""


def _claim_texts(claims: Sequence[Mapping[str, Any]] | None) -> list[str]:
    """Return non-empty claim texts from state-like claim dictionaries."""
    if claims is None:
        return []
    if isinstance(claims, (str, bytes)):
        return []

    texts: list[str] = []
    for claim in claims:
        if not isinstance(claim, Mapping):
            continue
        text = _extract_claim_text(claim)
        if len(text) >= MIN_CLAIM_TEXT_LENGTH:
            texts.append(text)
    return texts


def _is_state_only_bullet(text: str) -> bool:
    """Return True when a bullet only reports safe state metadata."""
    folded = text.casefold()
    return any(phrase in folded for phrase in _STATE_ONLY_PHRASES)


def validate_summary_quality(
    summary: Sequence[str],
    *,
    verified_claims: Sequence[Mapping[str, Any]] | None = None,
    rejected_claims: Sequence[Mapping[str, Any]] | None = None,
    expected_bullet_count: int = EXPECTED_SUMMARY_BULLETS,
) -> bool:
    """Validate that a summary satisfies the Part 3 assignment constraints.

    Args:
        summary: Candidate executive summary bullets.
        verified_claims: Optional shared-state verified claims used as the only
            allowed factual source for the summary.
        rejected_claims: Optional shared-state rejected claims that must never
            appear in the summary.
        expected_bullet_count: Required number of executive-summary bullets.

    Returns:
        True when the summary is exactly the expected length, formatted as
        bullets, grounded in verified claims or safe state-only messages, and
        free from rejected claim text. Invalid inputs return False instead of
        raising so the agent can handle validation failures cleanly.
    """
    try:
        if expected_bullet_count != EXPECTED_SUMMARY_BULLETS:
            return False
        if isinstance(summary, (str, bytes)):
            return False
        if len(summary) != expected_bullet_count:
            return False

        cleaned_summary: list[str] = []
        for bullet in summary:
            if not isinstance(bullet, str):
                return False
            cleaned = _normalise_text(bullet)
            if not cleaned.startswith(BULLET_PREFIX) or len(cleaned) <= len(BULLET_PREFIX):
                return False
            cleaned_summary.append(cleaned)

        combined_summary = "\n".join(cleaned_summary).casefold()
        for rejected_text in _claim_texts(rejected_claims):
            if rejected_text.casefold() in combined_summary:
                return False

        allowed_claims = _claim_texts(verified_claims)
        if allowed_claims:
            allowed_folded = [claim.casefold() for claim in allowed_claims]
            for bullet in cleaned_summary:
                folded_bullet = bullet.casefold()
                if any(claim in folded_bullet for claim in allowed_folded):
                    continue
                if _is_state_only_bullet(bullet):
                    continue
                return False

        return True
    except (AttributeError, TypeError, ValueError):
        return False
