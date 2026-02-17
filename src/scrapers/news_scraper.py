"""Real news scraper using NewsAPI"""

from __future__ import annotations
import os
import requests
import logging
from datetime import datetime
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class NewsScraper(BaseScraper):
    
    def __init__(self):
        super().__init__(name="NewsScraper")
        from dotenv import load_dotenv
        from pathlib import Path
        # Load .env from project root
        env_path = Path(__file__).parent.parent.parent / ".env"
        load_dotenv(dotenv_path=env_path)
        
        # Get API key from environment variable
        self.api_key = os.getenv("NEWS_API_KEY")
        
        if not self.api_key:
            logger.warning("NEWS_API_KEY not found in environment variables")
        
        # NewsAPI endpoint
        self.base_url = "https://newsapi.org/v2/everything"
        
        # Store articles (FIX: was self.article, now self.articles)
        self.articles = []
        
        logger.info("News Scraper Initialized with NewsAPI")
    
    # ==================== ABSTRACT METHOD 1: FETCH ====================
    
    def fetch(self, query: str) -> dict:
        """
        Fetch real news articles from NewsAPI
        
        Args:
            query: Search term
        
        Returns:
            dict: News data
        """
        if not self.validate_query(query):
            return {"error": "Invalid query", "success": False}
        
        if not self.api_key:
            return {
                "error": "NEWS_API_KEY not configured in .env file",
                "success": False
            }
        
        try:
            logger.info(f"Fetching news for: {query}")
            
            params = {
                "q": query,
                "sortBy": "publishedAt",
                "language": "en",
                "pageSize": 5,
                "apiKey": self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse the response
            return self.parse_data(response)
        
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"error": str(e), "success": False}
    
    # ==================== ABSTRACT METHOD 2: PARSE_DATA ====================
    
    def parse_data(self, response: requests.Response) -> dict:
        """
        Parse news data from API response
        
        This implements the abstract method from BaseScraper
        
        Args:
            response: requests.Response object from API
        
        Returns:
            dict: Parsed news data
        """
        try:
            data = response.json()
            
            # Check for API errors
            if data.get("status") == "error":
                error_msg = data.get("message", "Unknown error")
                logger.error(f"NewsAPI error: {error_msg}")
                return {
                    "error": f"NewsAPI Error: {error_msg}",
                    "success": False
                }
            
            # Format articles
            articles = []
            for article in data.get("articles", []):
                formatted_article = {
                    "title": article.get("title", "N/A"),
                    "description": article.get("description", "N/A"),
                    "content": article.get("content", "")[:500],
                    "source": article.get("source", {}).get("name", "Unknown"),
                    "author": article.get("author", "Unknown"),
                    "url": article.get("url", "#"),
                    "published_at": article.get("publishedAt", "N/A"),
                    "image_url": article.get("urlToImage", ""),
                    "scraped_at": datetime.now().isoformat()
                }
                
                if self.validate_data(formatted_article):
                    articles.append(formatted_article)
                    self.articles.append(formatted_article)
            
            result = {
                "articles": articles,
                "total_results": len(articles),
                "source": "NewsAPI",
                "timestamp": datetime.now().isoformat(),
                "success": True
            }
            
            logger.info(f"Parsed {len(articles)} articles")
            return result
        
        except Exception as e:
            logger.error(f"Error parsing data: {e}")
            return {"error": str(e), "success": False}
    
    # ==================== CONVENIENCE METHODS ====================
    
    def fetch_article(self, query: str) -> dict:
        #Alias for fetch
        return self.fetch(query)
    
    def fetch_multiple_queries(self, queries: list) -> dict:
        #Fetch articles for multiple queries
        results = {}
        for query in queries:
            results[query] = self.fetch(query)
        return results
    
    def get_summary(self) -> dict:
       #Get summary of scraped articles
        total_articles = len(self.articles)
        
        if total_articles == 0:
            return {
                "total_articles": 0,
                "total_words": 0,
                "average_words_per_article": 0,
                "articles": []
            }
        
        total_words = sum(
            len(article.get("description", "").split()) + 
            len(article.get("content", "").split())
            for article in self.articles
        )
        
        return {
            "total_articles": total_articles,
            "total_words": total_words,
            "average_words_per_article": total_words // total_articles if total_articles > 0 else 0,
            "articles": self.articles
        }
    
    def validate_data(self, article: dict) -> bool:
        #Validate article data
        if not article:
            return False
        
        if not article.get("title") or not article.get("url"):
            return False
        
        if not article.get("description") and not article.get("content"):
            return False
        
        return True

# """News scraper"""

# import logging
# from .base_scraper import BaseScraper

# logger = logging.getLogger(__name__)


# class NewsScraper(BaseScraper):
#     """Scraper for news articles"""
    
#     def __init__(self):
#         super().__init__(name="NewsScraper")
        
#         # Mock news data
#         self.news_data = {
#             "ai": [
#                 {
#                     "title": "AI Breakthroughs in 2024",
#                     "content": "Recent advancements in artificial intelligence...",
#                     "source": "TechNews",
#                     "date": "2024-02-09"
#                 },
#                 {
#                     "title": "Machine Learning Applications",
#                     "content": "How ML is transforming industries...",
#                     "source": "AIDaily",
#                     "date": "2024-02-08"
#                 }
#             ],
#             "bitcoin": [
#                 {
#                     "title": "Bitcoin Price Surge",
#                     "content": "Bitcoin hits new highs in recent trading...",
#                     "source": "CryptoNews",
#                     "date": "2024-02-09"
#                 },
#                 {
#                     "title": "BTC Analysis",
#                     "content": "Technical analysis shows strong momentum...",
#                     "source": "BlockchainDaily",
#                     "date": "2024-02-08"
#                 }
#             ]
#         }
    
#     def fetch(self, query: str) -> dict:
#         """Fetch news articles"""
#         if not self.validate_query(query):
#             return {"error": "Invalid query"}
        
#         query_lower = query.lower()
        
#         # Search in news data
#         for topic, articles in self.news_data.items():
#             if query_lower in topic.lower():
#                 logger.info(f"Found articles for {query}")
#                 return {
#                     "query": query,
#                     "articles": articles,
#                     "count": len(articles),
#                     "success": True
#                 }
        
#         logger.warning(f"No articles found for {query}")
#         return {
#             "query": query,
#             "articles": [],
#             "count": 0,
#             "success": False
#         }
    
#     def fetch_article(self, query: str) -> dict:
#         """Fetch single article"""
#         return self.fetch(query)
    
#     def fetch_latest(self) -> dict:
#         """Get latest news"""
#         latest = []
#         for topic, articles in self.news_data.items():
#             if articles:
#                 latest.append(articles[0])
        
#         return {
#             "latest": latest,
#             "success": True
#         }





