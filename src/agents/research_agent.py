from __future__ import annotations

import logging
from typing import Any, Optional
from .base_agent import BaseAgent, Tool

logger = logging.getLogger(__name__)

#RESEARCH AGENT CLASS
class ResearchAgent(BaseAgent):
    #Agent that researches topics using web scrapers.
    def __init__(self):
        super.__init__(
            name = "ResearchAgent",
            description="Researches topics using web scrapers and analysis"
        )

        #now to store scrapers data
        self.scraper_tools = {}

        #now to store analysis tools
        self.analysis_tools = {}

        #now to store search results
        self.search_results = [] #this tracks what we have researched

        self.max_research_depth = 3 #don't scrape more than 3 layers
        #max depth of research, this prevents infinite loop and to much scraping
        logger.info("Research Agent Initialized")

    #REGISTER SCRAPER METHOD
    #we register the scraper bcz agent don't know about the scraper until we register
    def register_scraper(self, scraper_name: str, scraper_object: Any) -> None:
        # EXAMPLE:
        # crypto_scraper = CryptoScraper()
        # agent.register_scraper('crypto', crypto_scraper)
        # # Now agent can use CryptoScraper! 

        self.scraper_tool[scraper_name] = scraper_object

        logger.info(f"Registered Scraper: {scraper_name}")

    
    #RESEARCH METHOD (Main logic)
    def run(self, task: str) -> dict:
        
        #this stores task in agents memory so that it remembers what the user asked
        self.memory.set_task(task)
        
        logger.info(f"Starting Research on: {task}")

        #STEP: 01 (Parse the task)
        #converts users question into structured data
        parsed_task = self._parse_task(task) # _parse = Private method (only used inside class)

        if not parsed_task:
            logger.error("Failed to parse task")
            return{
                "error": "Could not parse the research task",
                "task": task,
                "success": False
            }
        
        #STEP: 02 (DECIDE WHICH SCRAPER TO USE)
        #bcz different task require different scrapers

        scraper_name = self._decide_scraper(parsed_task)

        self.memory.add_thoughts(
            f"Decided to use: '{scraper_name}' for this research "
        )

        #STEP: 03 (EXECUTE THE SCRAPER)
        if scraper_name not in self.scraper_tools:
            #checks if the scraper exists
            logger.error(f"Scraper not found: {scraper_name}")
            return{
                "error": f"Scraper '{scraper_name}' not registered",
                "available_scraper": list(self.scraper_tools.keys()),
                "success": False
            }
        
        scraper = self.scraper_tools[scraper_name] #GET the scraper from dict
        scraped_data = self._execute_scraper(scraper, parsed_task)

        if not scraped_data:
            logger.error("Failed to scrape data")
            return{
                "error": "Could not scrape data",
                "task": task,
                "success": False
            }
        

        #STEP: 04 (ANALYZE DATA)
        analysis = self._analyze_data(scraped_data, parsed_task)

        #STEP: 05 (COMPILE RESULTS)

