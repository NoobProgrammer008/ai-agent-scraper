from __future__ import annotations
from typing import Dict, List, Any
import requests
import logging

#import the base scraper class
from .base_scraper import BaseScraper

#set up logging
#each module has its own logger
logger = logging.getLogger(__name__)

#CRYPTO SCRAPER CLASS
class CryptoScraper(BaseScraper):
    BASE_URL = "https://api.coingecko.com/api/v3"
    VALID_CRYPTOS = [
        'bitcoin',
        'ethereum',
        'cardano',
        'ripple',
        'solana',
        'polkadot',
        'litecoin',
        'dogecoin',
        'chainlink',
        'uniswap'
    ]

    #INITIALIZATION METHOD
    def __init__(self, timeout: int =10, max_retries: int = 3):

        #calls the class __init__ method from the base scraper
        super().__init__(timeout=timeout , max_retries=max_retries)

        #crypto specific initialization
        self.current_currency = 'usd' #track the current currency which is usd by default
        self.crypto_list = []

        logger.info("CryptoScraper initialized successfully")


    #BUILD CRYPTO URL METHOD
    def build_price_url(self, crypto_ids: List[str], currency: str = 'usd') -> str:

        crypto_string = ','.join(crypto_ids)

        url = (
            f"{self.BASE_URL}/simple/price"
            f"?ids={crypto_string}"
            f"&vs_currencies={currency}"
            f"&include_24hr_change=true"
            f"&include_market_cap=true"
        )
        logger.info(f"Built URL: {url}")
        return url
    
    #PARSE DATA (REQUIRED ABSTRACT METHOD)
    def parse_data(self, response: requests.Response) -> Dict[str, Any]:
        #Parse Crypto data from API response
        #This implements the abstract method from BaseScraper
        try:
            raw_data = response.json()

        except ValueError as e:
            logger.error(f"Failed to parse JSON: {e}")
            return {}
        
        #transform raw data into structured format
        parsed_data = {}

        for crypto_name, prices in raw_data.items():
            #loop through each cryptocurrency in the response
            currency = list(prices.keys())[0]  #get the currency key (e.g., 'usd')

            #extract and structure the data
            parsed_data[crypto_name] = {
                'price': prices.get(currency),
                'currency': currency,
                '24h_change': prices.get(f'{currency}_24_change'),
                'market_cap': prices.get(f'{currency}_market_cap'),
                'trending': self.is_trending(prices.get(f'{currency}_24h_change', 0))
                #is_trending() = Custom method to check if trending
            }

        logger.info(f"Parsed data for {len(parsed_data)} cryptocurrencies")
        return parsed_data
    
    #CUSTOM HELPER METHOD
    def is_trending(self, price_change: float) -> bool:
        #determine if a cryptocurrency is trending based on 24h price change
        return abs(price_change) > 5.0 #abs Absolute value greater than 5%
    
    #VALIDATE DATA METHOD (OVERRIDE PARENT METHOD)
    def validate_data(self, data: Dict[str, Any]) -> bool:
        
        #check if the data is empty
        if not data:
            logger.warning("Data is empty")
            return False
        
        #check each cryptocurrency's data
        for crypto_name, crypto_data in data.items():
            #check required fields
            required_fields = ['price', 'currency', '24h_change']

            for field in required_fields:
                if field not in crypto_data:
                    logger.warning(f"Missing field  '{field}' in {crypto_name}")
                    return False
                
            #check if price is a positive number
            price = crypto_data.get('price')

            if price is None or price <= 0:
                logger.warning(f"Invalid price for {crypto_name}: {price}")
                return False
    
        logger.info("Data validation passed")
        return True
    
    #FETCH PRICES (CONVENIENCE METHOD)
    def fetch_prices(self, crypto_ids: List[str], currency: str = 'usd') -> Dict[str, Any]:
        #method to fetch prices for a list of cryptocurrencies
        
        #build the URL
        url = self.build_price_url(crypto_ids, currency)
        # Use parent's run() method to do everything
        # run() calls: fetch_url() → parse_data() → validate_data() → save_data()
        result = self.run(url)

        return result
    
    #GET TRENDING CRYPTOS METHOD
    def get_trending(self, min_change: float = 5.0) -> List[Dict[str, Any]]:
        #get the list of trending cryptocurrencies based on 24h price change

        trending_list = []

        #loop through scraped data
        for data_entry in self.scraped_data:

            #check if this entry is for a crypto not metadata
            if 'price' in data_entry and '24h_change' in data_entry:
                change = data_entry.get('24h_change', 0)


                #check if trending
                if abs(change) >= min_change:
                    trending_list.append({
                        'name': data_entry.get('name', 'Unknown'),
                        'price' : data_entry.get('price'),
                        'change': change,
                        'currency': data_entry.get('currency')
                    })

        logger.info(f"Found{len(trending_list)} trending cryptocurrencies")
        return trending_list
    


