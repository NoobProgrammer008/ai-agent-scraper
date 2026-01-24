from __future__ import annotations
import requests
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

#configure logging
logging.basicConfig(
    level=logging.INFO,    # "level=logging.INFO" = Show INFO and higher messages
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 
    # Example output:
    # "2024-01-22 14:30:45 - BaseScraper - INFO - Starting scrape""
) 

logger = logging.getLogger(__name__)

#BASE SCRAPER CLASS
class BaseScraper(ABC):
    #This is the FOUNDATION that all scrapers inherit from.
    #It provides common scraping functionality.

    def __init__(self, timeout: int = 10, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.scraped_data = []

        logger.info(f"Initialized {self.__class__.__name__} scraper")


    #FETCH URL METHOD
    def fetch_url(self, url: str) -> Optional[requests.Response]:
        logger.info(f"Fetching URL: {url}") #message that we are fetching a URL
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    url,
                    timeout = self.timeout,
                    headers = self.headers
                )

                #check if the response is successful
                response.raise_for_status()

                logger.info(f"Successfully fetched URL: {url}")

                return response
            
            except requests.exceptions.Timeout:
                #this catches timeout errors
                logger.warning(f"Timeout on attempt {attempt + 1}/{self.max_retries}")

            except requests.exceptions.ConnectionError:
                #this catches connection errors
                logger.warning(f"Connection error on attempt {attempt + 1}/{self.max_retries}")

            except requests.exceptions.HTTPError as e:
                #this catches HTTP errors
                logger.warning(f"HTTP error on attempt {attempt + 1}/{self.max_retries}: {e}")

            except Exception as e:
                #this catches any other exceptions
                logger.error(f"Unexpected error: {e}")

        logger.error(f"Failed to fetch URL after {self.max_retries} attempts: {url}")
        return None
    

    @abstractmethod
    def parse_data(self, response: requests.Response) -> Dict[str, Any]:


        pass

    #VALIDATE DATA METHOD
    def validate_data(self, data: Any) -> bool:
        return True
    
    #SAVE DATA METHOD
    def save_data(self, data: Dict[str, Any]) -> None:
        #add metadata
        data_with_metadata = {
            **data,
            'scraped_at': datetime.now().isoformat()
        }

        self.scraped_data.append(data_with_metadata)
        logger.info(f"Data Saved: {data}")

    #RUN SCRAPER METHOD
    def run(self, url: str) -> Optional[Dict[str, Any]]:
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
            logger.error("Data validation Failed")
            return None
        # STEP 4: Save the data
        self.save_data(parsed_data)

        logger.info(f"Successfully completed scrape of")
        return parsed_data
    
    #GET SCRAPED DATA METHOD
    def get_scraped_data(self) -> List[Dict[str, Any]]:
        #this gets all the scraped data collected so far
        return self.scraped_data
    

    #CLEAR SCRAPED DATA METHOD
    def clear_data(self) -> None:
        #clear all stored data
        #useful for starting fresh scrapes
        self.scraped_data = []
        logger.info("Cleared all scraped data")

    #SCRAPED SUMMARY METHOD
    def summary(self) -> Dict[str, Any]:
        #get the summary of scraping activity
        return{
            'total_records': len(self.scraped_data),
            'scraper_type': self.__class__.__name__,
            'timeout': self.timeout,
            'max_retries' : self.max_retries
        }
    
    #CONTEXT MANAGER SUPPORT
    def __enter__(self):
        logger.info(f"Entering{self.__class__.__name__} context")
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        logger.info(f"Exiting {self.__class__.__name__} context")
        self.session.close()

        




