from pathlib import Path

from src.components.part_4_formatter.tools import save_report_file


def test_save_report_file_creates_markdown_file(tmp_path: Path) -> None:
    output_dir = tmp_path / "outputs"
    output_path = save_report_file("# Test Report", "test report", "md", output_dir=str(output_dir))
    saved_file = Path(output_path)

    assert saved_file.exists()
    assert saved_file.suffix == ".md"
    assert saved_file.read_text(encoding="utf-8") == "# Test Report"


def test_save_report_file_creates_html_file(tmp_path: Path) -> None:
    output_dir = tmp_path / "outputs"
    output_path = save_report_file("<h1>OK</h1>", "report html", "html", output_dir=str(output_dir))
    saved_file = Path(output_path)

    assert saved_file.exists()
    assert saved_file.suffix == ".html"
    assert saved_file.read_text(encoding="utf-8") == "<h1>OK</h1>"


def test_save_report_file_rejects_empty_content(tmp_path: Path) -> None:
    try:
        save_report_file("", "test", "md", output_dir=str(tmp_path))
    except ValueError as exc:
        assert "content" in str(exc).lower()
    else:
        raise AssertionError("Expected ValueError for empty content")


def test_save_report_file_rejects_empty_filename(tmp_path: Path) -> None:
    try:
        save_report_file("valid content", "", "md", output_dir=str(tmp_path))
    except ValueError as exc:
        assert "filename" in str(exc).lower()
    else:
        raise AssertionError("Expected ValueError for empty filename")


def test_save_report_file_rejects_unsupported_file_type(tmp_path: Path) -> None:
    try:
        save_report_file("valid content", "test", "txt", output_dir=str(tmp_path))  # type: ignore[arg-type]
    except ValueError as exc:
        assert "file_type" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unsupported file type")


def test_save_report_file_sanitizes_filename(tmp_path: Path) -> None:
    output_path = save_report_file("content", "unsafe<>filename:??", "md", output_dir=str(tmp_path))
    saved_file = Path(output_path)

    assert "unsafe" in saved_file.stem
    assert saved_file.exists()
