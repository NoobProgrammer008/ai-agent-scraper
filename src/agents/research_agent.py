from __future__ import annotations

import logging
from typing import Any, Optional
from .base_agent import BaseAgent, Tool

logger = logging.getLogger(__name__)

#RESEARCH AGENT CLASS
class ResearchAgent(BaseAgent):
    #Agent that researches topics using web scrapers.
    def __init__(self):
        super().__init__(
            name = "ResearchAgent",
            description="Researches topics using web scrapers and analysis"
        )

        #now to store scrapers data
        self.scraper_tools = {}

        #now to store analysis tools
        self.analysis_tools = {}

        #now to store search results
        self.search_results = [] #[] #this tracks what we have researched

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

        self.scraper_tools[scraper_name] = scraper_object

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

        research_result = {} #empty dictionary to store results
        
        research_result['query'] = parsed_task.get('query') #stores what we researched remembers what user asked

        #store the data we got
        research_result['scraped_data'] = scraped_data

        research_result['analysis'] = analysis

        research_result['success'] = True #marked the research as successful

        self.search_results.append(research_result)
        logger.info("Research Completed Successfully")
        
        return research_result
    
    #HELPER METHODS (private only used internally)
    def _parse_task(self, task: str) -> dict:

        #first check if the string is proper
        if not task or not isinstance(task, str):
            logger.error("Invalid task format")
            return{}
        
        task_lower = task.lower()

        #now to store the parsed data
        parsed = {}

        parsed['topic'] = task

        #decide which type of research should the agent do
        if 'bitcoin' in task_lower or 'btc' in task_lower:
            parsed['query'] = 'bitcoin'
            parsed['type'] = 'crypto'
        elif 'news' in task_lower:
            parsed['query'] = 'news'
            parsed['type'] = 'news'
        else:
            parsed['query'] = task
            parsed['type'] = 'general'

        logger.info(f"Parsed Task: {parsed}")
        return parsed
    
    def _decide_scraper(self, parsed_task: dict) -> str:
        #decide which scraper to use based on task
        task_type = parsed_task.get('type', 'general')

        if task_type == 'crypto':
            return 'crypto'
        
        elif task_type == 'news':
            return 'news'
        
        else: 
            return 'crypto'
        
    
    def _execute_scraper(self, scraper: Any, parsed_task: dict) -> Any:
        try:
            query = parsed_task.get('query') #gets what to research

            if hasattr(scraper, 'fetch_prices'):
                return scraper.fetch_prices([query])
            
            elif hasattr(scraper, 'fetch_article'):
                return scraper.fetch_article(query)
            
            else:
                logger.error("Scrapper has no recognized method")
                return None
            
        except Exception as e:
            logger.error(f"Scrapper error: {e}")
            return None
        
    def _analyze_data(self, data: Any, parsed_task: dict) -> str:
            if not data:
                return "No Data to analyze"
            
            analysis = f"Research findings for {parsed_task.get('topic')}:\n"

            analysis += f"Data obtained: {str(data)[:200]}...\n"

            return analysis
    
    #PUBLIC UTILITY METHODS
    def get_research_history(self) -> list:

        #get all the research history
        return self.search_results
    
    def get_research_summary(self) -> dict:
        
        #gets the summary of the research conducted
        return{
            'total_research': len(self.search_results),

            'successful': sum(1 for r in self.search_results if r.get('success')), #1 for r in means gives '1' if research is successful
            
            'queries':  [r.get('query') for r in self.search_results],

            'agent_memory': self.memory.get_summary()

        }

            


    





