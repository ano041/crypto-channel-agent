from tavily import TavilyClient
from config import settings
from utils.logger import logger

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY) if settings.TAVILY_API_KEY else None

async def tavily_search(query: str, max_results: int = 4) -> list:
    if not tavily_client:
        logger.warning("Tavily API key not configured")
        return []
    try:
        resp = await tavily_client.aquery(
            query=query,
            search_depth="advanced",
            max_results=max_results,
        )
        return [
            {"title": r["title"], "url": r["url"], "content": r.get("content", "")[:600]}
            for r in resp.get("results", [])
        ]
    except Exception as e:
        logger.error("Tavily search error", error=str(e))
        return []