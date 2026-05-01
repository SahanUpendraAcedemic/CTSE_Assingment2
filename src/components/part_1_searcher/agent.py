# """Part 1 Searcher Agent: responsible for producing raw findings into shared state."""

# from __future__ import annotations

# from typing import Any, Dict
# from src.shared.schemas.research_state import ResearchState


# def searcher_agent_node(state: ResearchState) -> ResearchState:
#     """LangGraph-compatible searcher agent node."""
#     return {**state, "searcher_agent_run": True}


# src/components/part_1_searcher/agent.py

import json
import logging
from typing import Any

from langchain_ollama import OllamaLLM  # pip install langchain-ollama
from langchain_core.messages import HumanMessage, SystemMessage

from .prompts import SEARCHER_SYSTEM_PROMPT
from .tools import search_wikipedia, search_duckduckgo

logger = logging.getLogger(__name__)


def run_searcher_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    LangGraph node function for the Searcher Agent.

    Reads 'query' from the shared state, calls search tools,
    and writes structured search results back into state.

    Args:
        state: The shared LangGraph state dict. Must contain key 'query'.

    Returns:
        Updated state dict with 'search_results' populated.
    """
    query: str = state.get("query", "")
    logger.info(f"[SearcherAgent] Starting search for: {query!r}")

    # --- Call tools directly (deterministic, no hallucination risk) ---
    wiki_result = search_wikipedia(query)
    web_results = search_duckduckgo(query)

    errors = []
    if wiki_result["error"]:
        errors.append(f"Wikipedia: {wiki_result['error']}")
    if web_results and web_results[0].get("text", "").startswith("Error"):
        errors.append(f"DuckDuckGo: {web_results[0]['text']}")

    search_results = {
        "topic": query,
        "wikipedia_title": wiki_result["title"],
        "wikipedia_summary": wiki_result["summary"],
        "wikipedia_url": wiki_result["url"],
        "web_snippets": web_results,
        "search_errors": errors,
    }

    logger.info(f"[SearcherAgent] Completed. Wikipedia title: {wiki_result['title']!r}")
    logger.info(f"[SearcherAgent] Web snippets found: {len(web_results)}")

    # Use LLM only to validate/clean the output format (optional but shows LLM usage)
    llm = OllamaLLM(model="llama3:8b", temperature=0)
    messages = [
        SystemMessage(content=SEARCHER_SYSTEM_PROMPT),
        HumanMessage(content=f"Raw tool results: {json.dumps(search_results)}. Return clean JSON only."),
    ]
    try:
        llm_response = llm.invoke(messages)
        # Try to parse the LLM's cleaned output
        cleaned = json.loads(llm_response)
        state["search_results"] = cleaned
    except (json.JSONDecodeError, Exception) as e:
        logger.warning(f"[SearcherAgent] LLM cleanup failed ({e}), using raw tool output.")
        state["search_results"] = search_results

    return state