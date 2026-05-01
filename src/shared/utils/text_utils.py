from __future__ import annotations

from html import escape as _html_escape
from typing import Iterable


def escape_html(value: str) -> str:
    """Escape text for safe HTML rendering."""
    return _html_escape(value, quote=True)


def flatten_lines(lines: Iterable[str]) -> str:
    """Convert a sequence of text lines into a single normalized string."""
    return "\n".join(line.strip() for line in lines if line is not None)
