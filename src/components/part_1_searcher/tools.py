# from __future__ import annotations

# from typing import Dict, Any


# def search_tool(query: str) -> Dict[str, Any]:
#     """Placeholder tool for search operations within the local system."""
#     return {"query": query, "results": []}



# src/components/part_1_searcher/tools.py

import requests
from typing import Optional

def search_wikipedia(query: str, sentences: int = 5) -> dict[str, str]:
    """
    Search Wikipedia and return a plain-text summary for a given query.

    Uses the Wikipedia REST API (no API key required).

    Args:
        query: The search term or topic to look up on Wikipedia.
        sentences: Number of sentences to return in the summary (default 5).

    Returns:
        A dict with keys:
            - 'title': The Wikipedia article title matched.
            - 'summary': The extracted plain-text summary.
            - 'url': The full URL to the Wikipedia article.
            - 'error': Non-empty string if something went wrong, else empty string.

    Example:
        >>> result = search_wikipedia("quantum computing")
        >>> print(result['title'])
        'Quantum computing'
    """
    base_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
    try:
        response = requests.get(
            f"{base_url}{requests.utils.quote(query)}",
            headers={"User-Agent": "CTSE-MAS-Assignment/1.0"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        # Trim to requested sentence count
        summary = data.get("extract", "")
        trimmed = ". ".join(summary.split(". ")[:sentences]) + "."

        return {
            "title": data.get("title", ""),
            "summary": trimmed,
            "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
            "error": "",
        }
    except requests.exceptions.Timeout:
        return {"title": "", "summary": "", "url": "", "error": "Request timed out."}
    except requests.exceptions.HTTPError as e:
        return {"title": "", "summary": "", "url": "", "error": f"HTTP error: {e}"}
    except Exception as e:
        return {"title": "", "summary": "", "url": "", "error": str(e)}


def search_duckduckgo(query: str, max_results: int = 3) -> list[dict[str, str]]:
    """
    Search the web using the DuckDuckGo Instant Answer API (no API key required).

    Note: DuckDuckGo's free API returns a best-match abstract, not a list of links.
    This function returns structured results parsed from the response.

    Args:
        query: The search query string.
        max_results: Maximum number of related topics to include (default 3).

    Returns:
        A list of result dicts, each containing:
            - 'text': Snippet of the result text.
            - 'url': Source URL (if available).
        Returns a list with one error dict if the request fails.

    Example:
        >>> results = search_duckduckgo("climate change effects")
        >>> for r in results:
        ...     print(r['text'])
    """
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_html": "1", "skip_disambig": "1"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results: list[dict[str, str]] = []

        # Main abstract (best single answer)
        if data.get("AbstractText"):
            results.append({
                "text": data["AbstractText"],
                "url": data.get("AbstractURL", ""),
            })

        # Related topics
        for topic in data.get("RelatedTopics", [])[:max_results]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append({
                    "text": topic["Text"],
                    "url": topic.get("FirstURL", ""),
                })

        return results if results else [{"text": "No results found.", "url": ""}]

    except requests.exceptions.Timeout:
        return [{"text": "Request timed out.", "url": ""}]
    except Exception as e:
        return [{"text": f"Error: {str(e)}", "url": ""}]