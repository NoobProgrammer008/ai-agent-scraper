from __future__ import annotations # for forward compatibility with future Python versions
import requests
import logging 
from bs4 import BeautifulSoup
from datetime import datetime
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__) # module-specific logger

#NEWS ARTICLE SCRAPER CLASS
class NewsScraper(BaseScraper):
    #Class variables
    #common html selector used by many media sites
    COMMON_SELECTORS = {
        'title' : [
            'h1.title',
            'h1.article-title',
            'h1.headline',
            'h1#title',
            'article h1',
            'h1',
        ],
        'content' : [
            'article.content',
            'div.article-content',
            'div.article-body',
            'div.story-body',
            'main',
            'article',
            'div.content',
        ],
        'author' : [
            'span.author',
            'div.author-name',
            'a.author',
            'span[itemprop="author]',
            '.by-author',
        ],
        'date' : [
            'time',
            'span.publish-date',
            'span.date',
            'div.published-date',
            'time[itemprop="datePublished]',
        ],
    }
    
    #INITIALIZATION METHOD
    def __init__(self, timeout: int = 15, max_retries = 3):

        super().__init__(timeout=timeout, max_retries=max_retries)
        self.article = []
        logger.info("NEWS Article Scraper Initialized")

    #PARSE DATA (REQUIRE ABSTRACT METHOD)
    def parse_data(self, response: requests.Response) -> dict:
        try:
            html = response.text #this gives raw html content
            soup = BeautifulSoup(html, 'html.parser') #parse html content

            #Extract article data
            article_data = self.extract_article(soup, response.url)

            logger.info(f"Article data extracted from {response.url}")
            return article_data
        
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return {}
        
    #EXTRACT ARTICLE DATA METHOD
    def extract_article(self, soup: BeautifulSoup, url: str) -> dict:
        #find data using multiple selectors 
        #because different sites use different html structures
        article = {
            'url' : url,
            'title': self.extract_element(soup, 'title'),
            'author' : self.extract_element(soup, 'author'),
            'date' : self.extract_element(soup, 'date'),
            'content' : self.extract_element(soup, 'content'),
            'scraped_at' : datetime.now().isoformat(),
        }
        return article
    
    #EXTRACT ELEMENT METHOD
    #in this method we extract 
    def extract_element(self, soup: BeautifulSoup, element_type: str) -> str:
        #above method we just defined what to extract
        #now here we will implement how to Extract specific element using multiple selectors.
        selectors = self.COMMON_SELECTORS.get(element_type,[])

        for selector in selectors:
            try:

                element = soup.select_one(selector) #selector is css selector

                if element:
                #if found it! extract and clean text
                    text = element.get_text(strip = True) #strip removes leading/trailing whitespace
                
                    if text:
                        logger.debug(f"Extracted {element_type} using selector '{selector}")
                        return text
            
            except Exception as e:
                #log error but continue trying other selectors
                logger.debug(f"Error extracting {element_type} with selector '{selector}' : {e}")

        #if we reach here means no selector worked
        logger.warning(f"Failed to extract {element_type}")
        return ""
    
    #CLEAN TEXT METHOD
    def clean_text(self, text: str) -> str:
        #clean and normalize text
        if not text: 
            return ""
        
        #remove multiple spaces
        text = ' '.join(text.split()) #text.split() removes extra spaces, then .join join with single space 
        #like this "This   is   text" -> ["This", "is", "text"] -> "This is text"
        return text
    

        #remove common ad and spam phrases
        spam_phrases = [
            "Click here to subscribe",
            "Read more at",
            "Advertisement",
            "Sponsored content",
            "Follow us on social media",
            "Subscribe now",
        ]

        for phrase in spam_phrases:
            text = text.replace(phrase, "")
        return text
     
    #VALIDATE ARTICLE METHOD (OVERRIDE PARENT METHOD)
    def validate_data(self, data: dict) -> bool:

        if not data:
            logger.warning("No data of article to validate")
            return False
        
        #check required fields
        if not data.get('title'):
            logger.warning("Article is missing title")
            return False
        
        if not data.get('content'):
            logger.warning("Article is missing content")
            return False
        
        #check for url
        if not data.get('url'):
            logger.warning("Article is missing URL")
            return False
        
        #check content length
        content = data.get('content', '')
        if len(content) < 50:
            logger.warning(f"Article content too short {len(content)} characters")
            return False
        
        logger.info("Article data validated successfully")
        return True
    
    #FETCH ARTICLE METHOD (CONVENIENCE METHOD)
    #Fetch and parse a single article.
    #Convenience method combining fetch and parse.
    def fetch_article(self, url: str) ->dict: 
        logger.info("Fetching article from URL: {url}")

        #use parents run method 
        #it handles fetching, parsing, validating and saving
        result = self.run(url)

        if result:
            #if found data add to articles list
            self.article.append(result)
            logger.info(f"Successfully scraped article: {result.get('title')}")
        return result
    
    #FETCH MULTIPLE ARTICLES METHOD
    def fetch_multiple_articles(self, urls: list) -> list:

        result = []
        for url in urls:
            article = self.fetch_article(url)
            if article:
                result.append(article)
        
        logger.info(f"Fetched {len(result)} articles out of {len(urls)} URLs")
        return result
    
    #GET ARTICLES SUMMARY METHOD
    def get_summary(self) -> dict:
        #get summary of scraped articles
        total_articles = len(self.article)
        total_words = sum(len(article.get('content', '').split())
                          for article in self.articles
                          )
        return {
            'total_articles' : total_articles,
            'total_words' : total_words,
            'average_words_per_article': (
                total_words // total_articles if total_articles > 0 else 0
            ),
            'articles' : self.articles
        }
        







