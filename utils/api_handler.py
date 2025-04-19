import aiohttp
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential
from cachetools import TTLCache
from dotenv import load_dotenv
import os
import logging
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache API responses for 1 hour
cache = TTLCache(maxsize=100, ttl=3600)

# Local fallback quotes
LOCAL_QUOTES = [
    {"content": "The advance of technology is based on making it fit in so that you don't really even notice it.", "author": "Bill Gates"},
    {"content": "Any sufficiently advanced technology is indistinguishable from magic.", "author": "Arthur C. Clarke"},
    {"content": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs"},
    {"content": "Technology is best when it brings people together.", "author": "Matt Mullenweg"},
    {"content": "The science of today is the technology of tomorrow.", "author": "Edward Teller"}
]

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
        # Use specific terms relevant to AI and Python
        terms = ["python", "artificial intelligence"]
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
                        # Filter for synonyms or nouns, exclude irrelevant terms
                        term_keywords = [
                            item["word"] for item in data
                            if "word" in item and "syn" in item.get("tags", []) and item["word"].lower() not in [
                                "three-toed sloth", "bradypus tridactylus", "artificial insemination", "petri",
                                "anon", "mei", "chiu", "yee", "lian", "cbs", "nsis", "nih", "nsi"
                            ]
                        ]
                        keywords.extend(term_keywords[:5])  # Limit to 5 per term
                    except Exception as e:
                        logger.error(f"Datamuse error for {term}: {str(e)}")
        # Remove duplicates and limit to 10 keywords
        keywords = list(dict.fromkeys(keywords))[:10]
        if not keywords:
            keywords = ["machine learning", "data science", "neural network", "deep learning", "programming"]
        cache[(query, "datamuse")] = keywords
        logger.info(f"Datamuse keywords retrieved: {keywords}")
        return keywords

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def fetch_quotes(self):
        logger.info("Preparing to fetch quotes from ZenQuotes.io")
        url = "https://zenquotes.io/api/random/5"  # Request 5 quotes
        async with aiohttp.ClientSession() as session:
            logger.info(f"Fetching ZenQuotes.io: {url}")
            try:
                async with session.get(url) as response:
                    logger.info(f"ZenQuotes.io status code: {response.status}")
                    response.raise_for_status()
                    data = await response.json()
                    logger.info(f"ZenQuotes.io response: {data}")
                    quotes = [
                        {"content": item["q"], "author": item["a"], "source": "zenquotes.io"}
                        for item in data[:5]  # Limit to 5 quotes
                    ]
                    if quotes:
                        cache[(url, "quotes")] = quotes
                        logger.info(f"ZenQuotes.io quotes retrieved: {len(quotes)}")
                        return quotes
            except Exception as e:
                logger.error(f"ZenQuotes.io error: {str(e)}")

            # Fallback to local quotes
            logger.warning("ZenQuotes.io failed, using local quotes")
            quotes = [random.choice(LOCAL_QUOTES)]  # Return one random local quote
            logger.info(f"Local quotes retrieved: {len(quotes)}")
            return quotes

    async def fetch_all(self, query):
        if (query, "all") in cache:
            logger.info(f"Returning cached data for query: {query}")
            return cache[(query, "all")]
        
        logger.info(f"Starting fetch_all for query: {query}")
        news_task = self.fetch_newsdata(query)
        keywords_task = self.fetch_datamuse(query)
        quotes_task = self.fetch_quotes()
        
        try:
            news, keywords, quotes = await asyncio.gather(news_task, keywords_task, quotes_task, return_exceptions=True)
            logger.info(f"fetch_all completed: news={len(news)}, keywords={len(keywords)}, quotes={len(quotes)}")
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