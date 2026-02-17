"""Scrapers module"""

from .base_scraper import BaseScraper
from .crypto_scraper import CryptoScraper
from .news_scraper import NewsScraper
from .general_scraper import GeneralScraper

__all__ = [
    'BaseScraper',
    'CryptoScraper',
    'NewsScraper',
    'GeneralScraper'
]