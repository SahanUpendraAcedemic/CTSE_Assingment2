from src.components.part_2_fact_checker.tools import validate_claims


def test_validate_claims_splits_verified_and_rejected() -> None:
    claims = [
        {"text": "A", "verified": True},
        {"text": "B", "verified": False},
    ]
    result = validate_claims(claims)
    assert result["verified_claims"] == [{"text": "A", "verified": True}]
    assert result["rejected_claims"] == [{"text": "B", "verified": False}]
