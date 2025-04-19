import aiohttp
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential
from cachetools import TTLCache
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
                logger.info(f"Fetching NewsData.io: {url}")
                response.raise_for_status()
                data = await response.json()
                logger.info(f"NewsData.io response: {len(data.get('results', []))} articles found")
                cache[(url, query)] = data
                return data.get("results", [])

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def fetch_datamuse(self, query):
        # Split query and use key terms (e.g., "python", "ai")
        terms = query.split("+")[-2:] if "+" in query else [query]  # e.g., ["python", "ai"]
        keywords = []
        async with aiohttp.ClientSession() as session:
            for term in terms:
                url = f"https://api.datamuse.com/words?ml={term}&max=10"
                async with session.get(url) as response:
                    logger.info(f"Fetching Datamuse: {url}")
                    try:
                        response.raise_for_status()
                        data = await response.json()
                        logger.info(f"Datamuse response for {term}: {data}")
                        # Filter for relevant keywords (e.g., synonyms or nouns)
                        term_keywords = [
                            item["word"] for item in data
                            if "word" in item and ("syn" in item.get("tags", []) or "n" in item.get("tags", []))
                        ]
                        keywords.extend(term_keywords[:5])  # Limit to 5 per term
                    except Exception as e:
                        logger.error(f"Datamuse error for {term}: {str(e)}")
        # Remove duplicates and limit to 10 keywords
        keywords = list(dict.fromkeys(keywords))[:10]
        cache[(query, "datamuse")] = keywords
        return keywords

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def fetch_quotable(self, tag="technology,innovation"):
        url = f"https://api.quotable.io/quotes?tags={tag}&limit=5"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                logger.info(f"Fetching Quotable.io: {url}")
                try:
                    response.raise_for_status()
                    data = await response.json()
                    logger.info(f"Quotable.io response: {data}")
                    quotes = [
                        {"content": item["content"], "author": item["author"]}
                        for item in data.get("results", [])
                    ]
                    if not quotes:
                        logger.warning(f"No quotes found for tags: {tag}")
                    cache[(url, tag)] = quotes
                    return quotes
                except Exception as e:
                    logger.error(f"Quotable.io error: {str(e)}")
                    return []

    async def fetch_all(self, query):
        if (query, "all") in cache:
            logger.info(f"Returning cached data for query: {query}")
            return cache[(query, "all")]
        
        news_task = self.fetch_newsdata(query)
        keywords_task = self.fetch_datamuse(query)
        quotes_task = self.fetch_quotable()
        
        try:
            news, keywords, quotes = await asyncio.gather(news_task, keywords_task, quotes_task, return_exceptions=True)
        except Exception as e:
            logger.error(f"Error in fetch_all: {str(e)}")
            news, keywords, quotes = [], [], []
        
        research_data = {
            "news": news if not isinstance(news, Exception) else [],
            "keywords": keywords if not isinstance(keywords, Exception) else [],
            "quotes": quotes if not isinstance(quotes, Exception) else []
        }
        cache[(query, "all")] = research_data
        return research_data