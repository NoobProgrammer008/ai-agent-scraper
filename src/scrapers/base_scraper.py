from __future__ import annotations

import requests
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """
    Base class for all scrapers.
    Provides common scraping functionality that all scrapers inherit.
    """
    
    def __init__(self, name: str = "BaseScraper", timeout: int = 10, max_retries: int = 3):
        """
        Initialize the scraper
        
        Args:
            name: Name of the scraper
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.name = name
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.scraped_data = []
        
        logger.info(f"Initialized {self.name} scraper")
    
    # ==================== ABSTRACT METHODS ====================
    
    @abstractmethod
    def fetch(self, query: str) -> dict:
        """
        Fetch data based on a query
        
        This is an abstract method that must be implemented by child classes.
        
        Args:
            query: Search query or identifier
        
        Returns:
            dict: Fetched data
        """
        pass
    
    @abstractmethod
    def parse_data(self, response: requests.Response) -> Dict[str, Any]:
        
        # Parse data from API/web response
        
        # This is an abstract method that must be implemented by child classes.
        
        # Args:
        #     response: requests.Response object
        
        # Returns:
        #     dict: Parsed data
        
        pass
    
    # ==================== VALIDATION METHODS ====================
    
    def validate_query(self, query: str) -> bool:
        
        # Validate the query string
        
        # Args:
        #     query: Query to validate
        
        # Returns:
        #     bool: True if valid, False otherwise
        
        if not query or not isinstance(query, str):
            logger.warning("Invalid query: query must be a non-empty string")
            return False
        
        if len(query.strip()) == 0:
            logger.warning("Invalid query: query cannot be empty or whitespace only")
            return False
        
        return True
    
    def validate_data(self, data: Any) -> bool:
        
        # Validate the parsed data
        
        # Override this method in child classes for specific validation logic
        
        # Args:
        #     data: Data to validate
        
        # Returns:
        #     bool: True if valid, False otherwise
        
        return data is not None
    
    # ==================== FETCH URL METHOD ====================
    
    def fetch_url(self, url: str) -> Optional[requests.Response]:
        
        # Fetch a URL with retry logic
        
        # Args:
        #     url: URL to fetch
        
        # Returns:
        #     requests.Response or None if all retries failed
        
        logger.info(f"Fetching URL: {url}")
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    url,
                    timeout=self.timeout,
                    headers=self.headers
                )
                
                # Check if response is successful
                response.raise_for_status()
                
                logger.info(f"Successfully fetched URL: {url}")
                return response
            
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}/{self.max_retries}")
            
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error on attempt {attempt + 1}/{self.max_retries}")
            
            except requests.exceptions.HTTPError as e:
                logger.warning(f"HTTP error on attempt {attempt + 1}/{self.max_retries}: {e}")
            
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
        
        logger.error(f"Failed to fetch URL after {self.max_retries} attempts: {url}")
        return None
    
    # ==================== DATA MANAGEMENT METHODS ====================
    
    def save_data(self, data: Dict[str, Any]) -> None:
        
        # Save data with metadata
        
        # Args:
        #     data: Data to save
        
        # Add metadata
        data_with_metadata = {
            **data,
            'scraped_at': datetime.now().isoformat()
        }
        
        self.scraped_data.append(data_with_metadata)
        logger.info(f"Data saved")
    
    def get_scraped_data(self) -> List[Dict[str, Any]]:
        
        # Get all scraped data collected so far
        
        # Returns:
        #     list: All scraped data
        
        return self.scraped_data
    
    def clear_data(self) -> None:
        """Clear all stored data"""
        self.scraped_data = []
        logger.info("Cleared all scraped data")
    
    # ==================== UTILITY METHODS ====================
    
    def summary(self) -> Dict[str, Any]:

        return {
            'scraper_name': self.name,
            'total_records': len(self.scraped_data),
            'scraper_type': self.__class__.__name__,
            'timeout': self.timeout,
            'max_retries': self.max_retries
        }
    
    def run(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Run complete scraping pipeline for a URL
        
        Args:
            url: URL to scrape
        
        Returns:
            dict: Parsed and validated data
        """
        logger.info(f"Starting scrape of {url}")
        
        # STEP 1: Fetch the URL
        response = self.fetch_url(url)
        if response is None:
            logger.error("Failed to fetch URL")
            return None
        
        # STEP 2: Parse the data
        try:
            parsed_data = self.parse_data(response)
        except Exception as e:
            logger.error(f"Error parsing data: {e}")
            return None
        
        # STEP 3: Validate the data
        if not self.validate_data(parsed_data):
            logger.error("Data validation failed")
            return None
        
        # STEP 4: Save the data
        self.save_data(parsed_data)
        
        logger.info("Successfully completed scrape")
        return parsed_data
    
    # ==================== CONTEXT MANAGER SUPPORT ====================
    
    def __enter__(self):
        """Enter context manager"""
        logger.info(f"Entering {self.name} context")
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Exit context manager"""
        logger.info(f"Exiting {self.name} context")
        self.session.close()
    
    # ==================== STRING REPRESENTATION ====================
    
    def __str__(self) -> str:
        """String representation"""
        return f"{self.name} (Scraper)"
    
    def __repr__(self) -> str:
        """Developer representation"""
        return f"<{self.__class__.__name__} name='{self.name}' timeout={self.timeout}>"

# """Base scraper class"""

# from abc import ABC, abstractmethod
# import logging

# logger = logging.getLogger(__name__)


# class BaseScraper(ABC):
#     """Base class for all scrapers"""
    
#     def __init__(self, name: str = "BaseScraper"):
#         self.name = name
#         logger.info(f"Initialized {self.name}")
    
#     @abstractmethod
#     def fetch(self, query: str):
#         """
#         Fetch data based on query
        
#         Args:
#             query: Search query
        
#         Returns:
#             Data from scraper
#         """
#         pass
    
#     def validate_query(self, query: str) -> bool:
#         """Validate query before scraping"""
#         if not query or not isinstance(query, str):
#             logger.error("Invalid query")
#             return False
#         return True
    
#     def __str__(self) -> str:
#         return f"{self.name} Scraper"


