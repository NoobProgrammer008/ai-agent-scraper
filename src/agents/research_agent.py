
from __future__ import annotations

import logging
from typing import Any, Optional

from src.scrapers.crypto_scraper import CryptoScraper
from src.scrapers.news_scraper import NewsScraper
from .base_agent import BaseAgent, Tool, Memory
from src.scrapers.general_scraper import GeneralScraper
logger = logging.getLogger(__name__)

# ==================== DUMMY SCRAPER CLASS ====================

class DummyScraper:
    """Dummy scraper for testing - returns mock data"""
    
    def __init__(self):
        self.name = "DummyScraper"
    
    def fetch_prices(self, query):
        """Fetch cryptocurrency prices"""
        return {
            "bitcoin": "$45,000",
            "ethereum": "$2,500",
            "cardano": "$0.80",
            "ripple": "$2.10",
            "query": query[0] if query else "unknown",
            "source": "Demo Data"
        }
    
    def fetch_article(self, query):
        """Fetch news article"""
        return {
            "title": f"Latest on {query}",
            "content": f"Information and analysis about {query}...",
            "source": "Demo Source",
            "date": "2024-02-09"
        }
    
    def fetch_general(self, query):
        """Fetch general information"""
        return {
            "query": query,
            "summary": f"General information about {query}",
            "details": f"Details about {query} research",
            "source": "Demo Data"
        }


# ==================== RESEARCH AGENT CLASS ====================

class ResearchAgent(BaseAgent):
    """Agent that researches topics using web scrapers and analysis"""
    
    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            description="Researches topics using web scrapers and analysis"
        )

        # Store scrapers
        self.scraper_tools = {}

        # Store analysis tools
        self.analysis_tools = {}

        # Store search results
        self.search_results = []

        # Max depth of research
        self.max_research_depth = 3

        # Register default scrapers
        self.register_scraper('crypto', CryptoScraper())
        self.register_scraper('news', NewsScraper())
        self.register_scraper('general', GeneralScraper())

        logger.info("Research Agent Initialized with default scrapers")

    # ==================== REGISTER SCRAPER METHOD ====================

    def register_scraper(self, scraper_name: str, scraper_object: Any) -> None:
        """
        Register a scraper with the agent
        
        Example:
            crypto_scraper = DummyScraper()
            agent.register_scraper('crypto', crypto_scraper)
        """
        self.scraper_tools[scraper_name] = scraper_object
        logger.info(f"Registered Scraper: {scraper_name}")

    # ==================== RESEARCH METHOD (Main logic) ====================

    def run(self, task: str) -> dict:
        # Store task in memory
        self.memory.set_task(task)
        
        logger.info(f"Starting Research on: {task}")

        # STEP 1: Parse the task
        parsed_task = self._parse_task(task)

        if not parsed_task:
            logger.error("Failed to parse task")
            return{
                "error": "Could not parse the research task",
                "task": task,
                "success": False
            }
        
        # STEP 2: Decide which scraper to use
        scraper_name = self._decide_scraper(parsed_task)

        self.memory.add_thoughts(
            f"Decided to use: '{scraper_name}' scraper for this research"
        )

        # STEP 3: Execute the scraper
        if scraper_name not in self.scraper_tools:
            logger.error(f"Scraper not found: {scraper_name}")
            return{
                "error": f"Scraper '{scraper_name}' not registered",
                "available_scraper": list(self.scraper_tools.keys()),
                "success": False
            }
        
        scraper = self.scraper_tools[scraper_name]
        self.memory.record_tool_call(scraper_name)
        scraped_data = self._execute_scraper(scraper, parsed_task)

        if not scraped_data:
            logger.error("Failed to scrape data")
            return{
                "error": "Could not scrape data",
                "task": task,
                "success": False
            }
        
        # STEP 4: Analyze data
        analysis = self._analyze_data(scraped_data, parsed_task)
        self.memory.add_finding(analysis)

        # STEP 5: Compile results
        research_result = {}
        
        research_result['query'] = parsed_task.get('query')
        research_result['scraped_data'] = scraped_data
        research_result['analysis'] = analysis
        research_result['success'] = True

        self.search_results.append(research_result)
        logger.info("Research Completed Successfully")
        
        return research_result
    
    # ==================== HELPER METHODS ====================

    def _parse_task(self, task: str) -> dict:

        # Validate input
        if not task or not isinstance(task, str):
            logger.error("Invalid task format")
            return {}
        
        task_lower = task.lower()
        parsed = {}
        parsed['topic'] = task

        # Determine task type
        if 'bitcoin' in task_lower or 'btc' in task_lower or 'crypto' in task_lower:
            parsed['query'] = 'bitcoin'
            parsed['type'] = 'crypto'
        elif 'news' in task_lower or 'article' in task_lower:
            parsed['query'] = task
            parsed['type'] = 'news'
        else:
            parsed['query'] = task
            parsed['type'] = 'general'

        logger.info(f"Parsed Task: {parsed}")
        return parsed
    
    def _decide_scraper(self, parsed_task: dict) -> str:

        task_type = parsed_task.get('type', 'general')

        if task_type == 'crypto':
            return 'crypto'
        elif task_type == 'news':
            return 'news'
        else:
            return 'general'
    
    def _execute_scraper(self, scraper: Any, parsed_task: dict) -> Any:

        try:
            query = parsed_task.get('query')

            # Try different scraper methods
            if hasattr(scraper, 'fetch_prices'):
                return scraper.fetch_prices([query])
            
            elif hasattr(scraper, 'fetch_article'):
                return scraper.fetch_article(query)
            
            elif hasattr(scraper, 'fetch_general'):
                return scraper.fetch_general(query)
            
            else:
                logger.error("Scraper has no recognized method")
                return None
            
        except Exception as e:
            logger.error(f"Scraper error: {e}")
            return None
    
    def _analyze_data(self, data: Any, parsed_task: dict) -> str:

        if not data:
            return "No data to analyze"
    
        task_type = parsed_task.get('type')
        topic = parsed_task.get('topic')
    
    # ==================== FORMAT BY TYPE ====================
    
        if task_type == 'crypto':
            # Crypto data format
            crypto_data = data
            analysis = f"Research findings for {topic}:\n\n"
        
            if 'results' in crypto_data:
                results = crypto_data['results']
                analysis += f"{results.get('symbol', '')} Information:\n"
                analysis += f"Current Price: {results.get('price', 'N/A')}\n"
                analysis += f"24h Change: {results.get('change', 'N/A')}\n"
                analysis += f"Market Cap: {results.get('market_cap', 'N/A')}\n"
            else:
                for key, value in crypto_data.items():
                    if key not in ['query', 'source', 'success']:
                     analysis += f"{key.upper()}: {value}\n"
        
            return analysis
    
        elif task_type == 'news':
        # News data format
            analysis = f"Research findings for {topic}:\n\n"
        
            if 'articles' in data:
                articles = data['articles']
                for i, article in enumerate(articles, 1):
                    analysis += f"Article {i}: {article.get('title', 'N/A')}\n"
                    analysis += f"Content: {article.get('content', 'N/A')}\n"
                    analysis += f"Source: {article.get('source', 'N/A')}\n"
                    analysis += f"Date: {article.get('date', 'N/A')}\n\n"
        
            return analysis
    
        elif task_type == 'general':
            # General information format - PARAGRAPH TEXT
            analysis = f"Research findings for {topic}:\n\n"
        
            if 'info' in data:
                info = data['info']
            
                # Main title
                analysis += f"**{info.get('title', 'Information')}**\n\n"
            
                # Description as paragraph
                analysis += f"{info.get('description', '')}\n\n"
            
                # Format other fields as readable text
                if 'applications' in info:
                    analysis += f"Key Applications: {', '.join(info['applications'])}\n"
            
                if 'examples' in info:
                    analysis += f"Examples: {', '.join(info['examples'])}\n"
            
                if 'types' in info:
                    analysis += f"Types: {', '.join(info['types'])}\n"
            
                if 'libraries' in info:
                    analysis += f"Popular Libraries/Tools: {', '.join(info['libraries'])}\n"
            
                if 'use_cases' in info:
                    analysis += f"Use Cases: {', '.join(info['use_cases'])}\n"
            
                if 'layers' in info:
                    analysis += f"Components: {', '.join(info['layers'])}\n"
            
                if 'process' in info:
                    analysis += f"Process Steps: {' → '.join(info['process'])}\n"
        
            return analysis
    
        else:
            # Default format
            return f"Research findings for {topic}:\n{str(data)}\n"
    
    # ==================== PUBLIC UTILITY METHODS ====================

    def get_research_history(self) -> list:
        # """Get all research history"""
        return self.search_results
    
    def get_research_summary(self) -> dict:
        # """Get summary of research conducted"""
        return{
            'total_research': len(self.search_results),
            'successful': sum(1 for r in self.search_results if r.get('success')),
            'queries': [r.get('query') for r in self.search_results],
            'agent_memory': self.memory.get_summary()
        }
    
    def clear_history(self) -> None:
        # """Clear research history"""
        self.search_results = []
        logger.info("Research history cleared")




