from __future__ import annotations

import os
from typing import Any
import requests

from tools._shared import TIMEOUT, err


import datetime


def github_search(query: str = "", sort_by: str = "stars", limit: int = 5, timeframe: str = "all") -> dict[str, Any]:
    """Search for open-source repositories on GitHub."""
    try:
        url = "https://api.github.com/search/repositories"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "Research-Agent-App"
        }
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"
            
        clean_query = query.strip() if query else ""
        if not clean_query:
            clean_query = "stars:>1"

        if timeframe and timeframe != "all":
            now = datetime.datetime.now()
            if timeframe == "day":
                delta = datetime.timedelta(days=1)
            elif timeframe == "week":
                delta = datetime.timedelta(weeks=1)
            elif timeframe == "month":
                delta = datetime.timedelta(days=30)
            elif timeframe == "year":
                delta = datetime.timedelta(days=365)
            else:
                delta = None

            if delta:
                date_str = (now - delta).strftime("%Y-%m-%d")
                clean_query = f"{clean_query} created:>{date_str}"

        params = {
            "q": clean_query,
            "sort": sort_by,
            "order": "desc",
            "per_page": int(limit or 5)
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        items = []
        for item in data.get("items", []):
            full_name = item.get("full_name", "")
            description = item.get("description") or "No description"
            html_url = item.get("html_url", "")
            stars = item.get("stargazers_count", 0)
            forks = item.get("forks_count", 0)
            updated_at = item.get("updated_at", "")
            
            items.append({
                "title": full_name,
                "url": html_url,
                "source": "GitHub",
                "summary": f"{description} (Stars: {stars}, Forks: {forks}, Updated: {updated_at})"
            })
            
        return {"tool": "github_search", "query": query, "sort_by": sort_by, "items": items}
    except Exception as exc:
        return err("github_search", exc)
