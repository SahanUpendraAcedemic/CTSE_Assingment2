from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Literal


def _sanitize_filename(filename: str) -> str:
    safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_."
    stem = Path(filename).stem
    sanitized = "".join(char for char in stem if char in safe_chars)
    return sanitized or "report"


def _format_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


def save_report_file(
    content: str,
    filename: str,
    file_type: Literal["md", "html"] = "md",
    output_dir: str = "outputs",
) -> str:
    """
    Save a formatted research report to a local file.

    Args:
        content: The report body to save. Must not be empty.
        filename: Base filename used to generate the saved file.
        file_type: Either "md" or "html".
        output_dir: Directory where the file is saved.

    Returns:
        The absolute path to the saved report.

    Raises:
        ValueError: If content or filename is empty or file_type is unsupported.
        OSError: If writing the file fails.
    """
    if not content or not content.strip():
        raise ValueError("Report content must not be empty.")

    if not filename or not filename.strip():
        raise ValueError("Filename must not be empty.")

    if file_type not in ("md", "html"):
        raise ValueError("file_type must be either 'md' or 'html'.")

    safe_name = _sanitize_filename(filename)
    timestamp = _format_timestamp()
    final_filename = f"{safe_name}-{timestamp}.{file_type}"
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    file_path = output_path / final_filename
    file_path.write_text(content, encoding="utf-8")
    return str(file_path.resolve())
