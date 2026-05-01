from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class ResearchState(TypedDict, total=False):
    topic: str
    raw_findings: List[Dict[str, Any]]
    extracted_claims: List[str]
    verified_claims: List[Dict[str, Any]]
    rejected_claims: List[Dict[str, Any]]
    summary: List[str]
    sources: List[str]
    output_format: str
    output_file_path: str | None
    logs: List[Dict[str, Any]]
