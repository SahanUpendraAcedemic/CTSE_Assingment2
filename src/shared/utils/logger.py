from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional


def setup_logger(name: str = "formatter_agent", log_dir: str | Path | None = None) -> logging.Logger:
    """Create or return a logger configured for local observability."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    if log_dir is None:
        log_dir = Path(__file__).resolve().parents[2] / "logs" / "agent_runs"
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(log_path / f"{name}.log", encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
