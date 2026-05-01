from src.components.part_3_summarizer.tools import validate_summary_quality


def test_validate_summary_quality_rejects_empty_summary() -> None:
    assert validate_summary_quality([]) is False


def test_validate_summary_quality_accepts_three_grounded_bullets() -> None:
    verified_claims = [
        {"claim": "Local Ollama-compatible models are used for generation."},
        {"text": "The shared state passes verified claims to the summarizer."},
    ]
    rejected_claims = [{"claim": "The summarizer performs live web research."}]
    summary = [
        "- Local Ollama-compatible models are used for generation.",
        "- The shared state passes verified claims to the summarizer.",
        "- Only two verified claims were supplied in shared state.",
    ]

    assert (
        validate_summary_quality(
            summary,
            verified_claims=verified_claims,
            rejected_claims=rejected_claims,
        )
        is True
    )


def test_validate_summary_quality_rejects_wrong_bullet_count() -> None:
    summary = [
        "- Local models are available locally.",
        "- Shared state contains verified claims.",
    ]

    assert validate_summary_quality(summary) is False


def test_validate_summary_quality_rejects_unformatted_bullets() -> None:
    summary = [
        "Local models are available locally.",
        "- Shared state contains verified claims.",
        "- Only two verified claims were supplied in shared state.",
    ]

    assert validate_summary_quality(summary) is False


def test_validate_summary_quality_rejects_rejected_claim_text() -> None:
    rejected_claims = [{"claim": "The summarizer performs live web research."}]
    summary = [
        "- The summarizer performs live web research.",
        "- No verified claims were available in shared state.",
        "- Additional verified claims are required before final formatting.",
    ]

    assert validate_summary_quality(summary, rejected_claims=rejected_claims) is False


def test_validate_summary_quality_rejects_invented_claim_when_verified_claims_given() -> None:
    verified_claims = [{"claim": "The system uses local model execution."}]
    summary = [
        "- The system uses local model execution.",
        "- The system calls a paid API for fallback responses.",
        "- Only one verified claim was supplied in shared state.",
    ]

    assert validate_summary_quality(summary, verified_claims=verified_claims) is False


def test_validate_summary_quality_handles_invalid_input_safely() -> None:
    assert validate_summary_quality("not a list") is False  # type: ignore[arg-type]
    assert validate_summary_quality(["- Valid bullet", None, "- Valid bullet"]) is False  # type: ignore[list-item]
