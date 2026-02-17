import logging
import requests
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class GeneralScraper(BaseScraper):
    """Scraper for general information from Wikipedia"""
    
    def __init__(self):
        super().__init__(name="GeneralScraper")
        
        # Wikipedia API endpoint
        self.base_url = "https://en.wikipedia.org/api/rest_v1/page/summary"
        
        # Local database for faster queries
        self.general_data = {
            "ai": {
                "title": "Artificial Intelligence (AI)",
                "description": "Artificial Intelligence is the simulation of human intelligence processes by computer systems. AI involves developing algorithms and models that enable machines to learn from data, recognize patterns, understand language, and make decisions without explicit human instruction.",
                "applications": ["Machine Learning", "Computer Vision", "Natural Language Processing", "Robotics"],
                "examples": ["ChatGPT", "Tesla Autopilot", "Netflix Recommendations"]
            },
            "machine learning": {
                "title": "Machine Learning (ML)",
                "description": "Machine Learning is a subset of AI that enables computer systems to learn from experience without being explicitly programmed. ML algorithms process data to identify patterns and make predictions.",
                "types": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning"],
                "applications": ["Image Recognition", "Fraud Detection", "Recommendation Systems"]
            },
            "python": {
                "title": "Python Programming Language",
                "description": "Python is a high-level programming language known for its simplicity and versatility. It has become the standard language for AI and data science.",
                "libraries": ["NumPy", "Pandas", "TensorFlow", "PyTorch"],
                "use_cases": ["Data Analysis", "Machine Learning", "Web Development"]
            }
        }
        
        logger.info("GeneralScraper Initialized")
    
    # ==================== ABSTRACT METHOD 1: FETCH ====================
    
    def fetch(self, query: str) -> dict:

        if not self.validate_query(query):
            return {"error": "Invalid query", "success": False}
        
        try:
            # First try local database
            query_lower = query.lower()
            query_clean = query_lower.replace(".", "").replace("?", "").strip()
            
            # Search in local data
            for topic, info in self.general_data.items():
                if topic in query_clean or query_clean in topic:
                    logger.info(f"Found information in local database for {query}")
                    return {
                        "query": query,
                        "info": info,
                        "source": "Local Database",
                        "success": True
                    }
            
            # If not found locally, try Wikipedia
            formatted_query = query.replace(" ", "_")
            url = f"{self.base_url}/{formatted_query}"
            
            logger.info(f"Fetching Wikipedia info for '{query}'...")
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            # Parse the response
            return self.parse_data(response)
        
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"error": str(e), "success": False}
    
    # ==================== ABSTRACT METHOD 2: PARSE_DATA ====================
    
    def parse_data(self, response: requests.Response) -> dict:

        try:
            data = response.json()
            
            if "error" in data:
                return {
                    "error": "Topic not found on Wikipedia",
                    "success": False
                }
            
            formatted_response = {
                "title": data.get("title", "N/A"),
                "description": data.get("extract", "No description available"),
                "source": "Wikipedia API",
                "url": data.get("content_urls", {}).get("desktop", {}).get("page", "#"),
                "image_url": data.get("thumbnail", {}).get("source", ""),
                "success": True
            }
            
            logger.info(f"Parsed Wikipedia info")
            return formatted_response
        
        except Exception as e:
            logger.error(f"Error parsing data: {e}")
            return {"error": str(e), "success": False}
    
    # ==================== CONVENIENCE METHODS ====================
    
    def fetch_general(self, query: str) -> dict:
        #Alias for fetch
        return self.fetch(query)
    
    def validate_data(self, data: dict) -> bool:
        #Validate general information data
        if not data:
            return False
        
        return data.get("success", False)