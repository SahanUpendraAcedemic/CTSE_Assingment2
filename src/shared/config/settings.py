from __future__ import annotations

from pathlib import Path


class Settings:
    """Shared configuration values for the local research hub."""

    BASE_DIR: Path = Path(__file__).resolve().parents[3]
    OUTPUT_DIR: Path = BASE_DIR / "outputs"
    REPORTS_DIR: Path = OUTPUT_DIR / "reports"
    INTERMEDIATE_DIR: Path = OUTPUT_DIR / "intermediate"
    LOG_DIR: Path = BASE_DIR / "logs" / "agent_runs"
