import requests
from langchain_core.tools import tool

@tool
def verify_fact_wikipedia(query: str) -> str:
    """
    Searches the Wikipedia API to cross-reference and verify a specific claim.
    """
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "utf8": 1,
        "srlimit": 1
    }
    
    # ADD THIS: Identify your app to Wikipedia so they don't block you
    headers = {
        "User-Agent": "CTSE_Assignment2_Bot/1.0 (Educational Project)"
    }
    
    try:
        # UPDATE THIS: Pass the headers into the get request
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data["query"]["search"]:
            snippet = data["query"]["search"][0]["snippet"]
            clean_snippet = snippet.replace('<span class="searchmatch">', '').replace('</span>', '')
            return f"Wikipedia findings for '{query}': {clean_snippet}"
        else:
            return f"No verifying information found on Wikipedia for '{query}'."
            
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Wikipedia API: {str(e)}"