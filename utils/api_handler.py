import aiohttp
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential
from cachetools import TTLCache
from dotenv import load_dotenv
import os

# Cache API responses for 1 hour
cache = TTLCache(maxsize=100, ttl=3600)

class APIHandler:
    def __init__(self):
        load_dotenv()
        self.newsdata_api_key = os.getenv("NEWSDATA_API_KEY")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def fetch_newsdata(self, query):
        url = f"https://newsdata.io/api/1/news?apikey={self.newsdata_api_key}&q={query}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                cache[(url, query)] = data
                return data.get("results", [])

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def fetch_datamuse(self, query):
        url = f"https://api.datamuse.com/words?rel_jja={query}&max=10"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                cache[(url, query)] = data
                return [item["word"] for item in data]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def fetch_quotable(self, tag="technology"):
        url = f"https://api.quotable.io/quotes?tags={tag}&limit=5"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                cache[(url, tag)] = data
                return [{"content": item["content"], "author": item["author"]} for item in data["data"]]

    async def fetch_all(self, query):
        if (query, "all") in cache:
            return cache[(query, "all")]
        
        news_task = self.fetch_newsdata(query)
        keywords_task = self.fetch_datamuse(query)
        quotes_task = self.fetch_quotable()
        
        news, keywords, quotes = await asyncio.gather(news_task, keywords_task, quotes_task, return_exceptions=True)
        
        research_data = {
            "news": news if not isinstance(news, Exception) else [],
            "keywords": keywords if not isinstance(keywords, Exception) else [],
            "quotes": quotes if not isinstance(quotes, Exception) else []
        }
        cache[(query, "all")] = research_data
        return research_data