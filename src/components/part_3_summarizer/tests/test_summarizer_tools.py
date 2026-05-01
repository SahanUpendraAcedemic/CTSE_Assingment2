from src.components.part_3_summarizer.tools import validate_summary_quality


def test_validate_summary_quality_placeholder() -> None:
    assert validate_summary_quality(["Placeholder summary bullet."]) is True
    assert validate_summary_quality([]) is False
