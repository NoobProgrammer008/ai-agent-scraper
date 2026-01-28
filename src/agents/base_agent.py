#This is base agent class
#Foundation for all a.i agents it will act as the Parent class and other classes will inherit its basic functions

# Agents think, reason, and use tools to complete tasks
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Callable
from datetime import datetime

logger = logging.getLogger(__name__)

#TOOLS CLASS (what agents going to use)
class Tool:
    #like scrapeWebsiteTool, Analyze tool

    def __init__(
            #parameter of init function also the tools structure
            self, 
            name: str,
            description: str,
            function: Callable,
            parameter: dict = None
    ):
        self.name = name
        self.description = description
        self.function = function
        self.parameter = parameter or {}

        logger.info(f"Created Tool: {name}")

    def execute(self, **kwargs) -> Any:
        # execute to execute the tool given parameter
        #**kwargs: parameters to pass to function 

        try:
            logger.info(f"Executing tool: {self.name} with {kwargs}")
            result = self.function(**kwargs)
            logger.info(f"Tool {self.name} executed successfully") 
            return result
        
        except Exception as e:
            logger.info(f"Error executing tool {self.name}: {e}")
            return f"Error: {str(e)}"

