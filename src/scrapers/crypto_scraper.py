"""Real cryptocurrency scraper using CoinGecko API"""

from __future__ import annotations

import requests
import logging
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class CryptoScraper(BaseScraper):
    """Scraper for real cryptocurrency data from CoinGecko API"""
    
    def __init__(self):
        super().__init__(name="CryptoScraper")
        
        # CoinGecko API endpoint
        self.base_url = "https://api.coingecko.com/api/v3"
        
        # Map common names to CoinGecko IDs
        self.crypto_map = {
            "bitcoin": "bitcoin",
            "btc": "bitcoin",
            "ethereum": "ethereum",
            "eth": "ethereum",
            "cardano": "cardano",
            "ada": "cardano",
            "ripple": "ripple",
            "xrp": "ripple",
            "solana": "solana",
            "sol": "solana",
            "litecoin": "litecoin",
            "ltc": "litecoin",
            "dogecoin": "dogecoin",
            "doge": "dogecoin",
        }
        
        logger.info("CryptoScraper Initialized")
    
    # ==================== ABSTRACT METHOD 1: FETCH ====================
    
    def fetch(self, query: str) -> dict:
        if not self.validate_query(query):
            return {"error": "Invalid query", "success": False}
        
        try:
            query_lower = query.lower()
            
            # Find matching crypto ID
            crypto_id = None
            for key, value in self.crypto_map.items():
                if key in query_lower:
                    crypto_id = value
                    break
            
            # Default to bitcoin if not found
            if not crypto_id:
                crypto_id = "bitcoin"
                logger.warning(f"Crypto not found for '{query}', defaulting to Bitcoin")
            
            # Make API request to CoinGecko
            url = f"{self.base_url}/simple/price"
            params = {
                "ids": crypto_id,
                "vs_currencies": "usd",
                "include_market_cap": "true",
                "include_24h_vol": "true",
                "include_24h_change": "true"
            }
            
            logger.info(f"Fetching data for {crypto_id}...")
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            # Parse the response
            return self.parse_data(response)
        
        except requests.exceptions.Timeout:
            error_msg = "Request timeout - CoinGecko server not responding"
            logger.error(error_msg)
            return {"error": error_msg, "success": False}
        
        except requests.exceptions.ConnectionError:
            error_msg = "Connection error - check your internet connection"
            logger.error(error_msg)
            return {"error": error_msg, "success": False}
        
        except requests.exceptions.RequestException as e:
            error_msg = f"Request error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg, "success": False}
        
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg, "success": False}
    
    # ==================== ABSTRACT METHOD 2: PARSE_DATA ====================
    
    def parse_data(self, response: requests.Response) -> dict:
        """
        Parse cryptocurrency data from API response
        
        This implements the abstract method from BaseScraper
        
        Args:
            response: requests.Response object from CoinGecko API
        
        Returns:
            dict: Parsed cryptocurrency data
        """
        try:
            data = response.json()
            
            if not data:
                return {"error": "No data in response", "success": False}
            
            # Get first crypto in response
            crypto_id = list(data.keys())[0]
            crypto_data = data[crypto_id]
            
            formatted_response = {
                "crypto_id": crypto_id.upper(),
                "price_usd": f"${crypto_data['usd']:,.2f}",
                "market_cap_usd": f"${crypto_data.get('usd_market_cap', 0):,.0f}",
                "24h_volume_usd": f"${crypto_data.get('usd_24h_vol', 0):,.0f}",
                "24h_change_percent": f"{crypto_data.get('usd_24h_change', 0):.2f}%",
                "source": "CoinGecko API",
                "success": True
            }
            
            logger.info(f"Parsed cryptocurrency data")
            return formatted_response
        
        except Exception as e:
            logger.error(f"Error parsing data: {e}")
            return {"error": str(e), "success": False}
    
    # ==================== CONVENIENCE METHODS ====================
    
    def fetch_prices(self, queries: list) -> dict:
        """Fetch prices for multiple cryptocurrencies"""
        results = {}
        for query in queries:
            results[query] = self.fetch(query)
        return results
    
    def validate_data(self, data: dict) -> bool:
        """Validate cryptocurrency data"""
        if not data:
            return False
        return data.get("success", False)


# """Cryptocurrency scraper"""

# import logging
# from .base_scraper import BaseScraper

# logger = logging.getLogger(__name__)


# class CryptoScraper(BaseScraper):
#     """Scraper for cryptocurrency data"""
    
#     def __init__(self):
#         super().__init__(name="CryptoScraper")
        
#         # Mock cryptocurrency data
#         self.crypto_data = {
#             "bitcoin": {
#                 "symbol": "BTC",
#                 "price": "$45,000",
#                 "change": "+2.5%",
#                 "market_cap": "$882B"
#             },
#             "ethereum": {
#                 "symbol": "ETH",
#                 "price": "$2,500",
#                 "change": "+1.8%",
#                 "market_cap": "$301B"
#             },
#             "cardano": {
#                 "symbol": "ADA",
#                 "price": "$0.80",
#                 "change": "+0.5%",
#                 "market_cap": "$28B"
#             },
#             "ripple": {
#                 "symbol": "XRP",
#                 "price": "$2.10",
#                 "change": "+3.2%",
#                 "market_cap": "$114B"
#             }
#         }
    
#     def fetch(self, query: str) -> dict:
#         """Fetch cryptocurrency data"""
#         if not self.validate_query(query):
#             return {"error": "Invalid query"}
        
#         query_lower = query.lower()
        
#         # Search in data
#         for crypto, data in self.crypto_data.items():
#             if query_lower in crypto.lower():
#                 logger.info(f"Found cryptocurrency data for {query}")
#                 return {
#                     "query": query,
#                     "results": data,
#                     "success": True
#                 }
        
#         logger.warning(f"No data found for {query}")
#         return {
#             "query": query,
#             "results": "Not found",
#             "success": False
#         }
    
#     def fetch_prices(self, queries: list) -> dict:
#         """Fetch prices for multiple cryptocurrencies"""
#         results = {}
#         for query in queries:
#             data = self.fetch(query)
#             results[query] = data.get('results', {})
        
#         return results
    
#     def fetch_trending(self) -> dict:
#         """Get trending cryptocurrencies"""
#         return {
#             "trending": list(self.crypto_data.keys()),
#             "success": True
#         }