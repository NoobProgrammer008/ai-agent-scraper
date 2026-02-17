# #This is base agent class
# #Foundation for all a.i agents it will act as the Parent class and other classes will inherit its basic functions

# # Agents think, reason, and use tools to complete tasks
# from __future__ import annotations

# import logging
# from abc import ABC, abstractmethod
# from typing import Any, Callable
# from datetime import datetime

# logger = logging.getLogger(__name__)

# #TOOLS CLASS (what agents going to use)
# class Tool:
#     #like scrapeWebsiteTool, Analyze tool

#     def __init__(
#             #parameter of init function also the tools structure
#             self, 
#             name: str,
#             description: str,
#             function: Callable,
#             parameter: dict = None
#     ):
#         self.name = name
#         self.description = description
#         self.function = function
#         self.parameter = parameter or {}

#         logger.info(f"Created Tool: {name}")

#     def execute(self, **kwargs) -> Any:
#         # execute to execute the tool given parameter
#         #**kwargs: parameters to pass to function 

#         try:
#             logger.info(f"Executing tool: {self.name} with {kwargs}")
#             result = self.function(**kwargs)
#             logger.info(f"Tool {self.name} executed successfully") 
#             return result
        
#         except Exception as e:
#             logger.info(f"Error executing tool {self.name}: {e}")
#             return f"Error: {str(e)}"

#     def to_dict(self) -> dict:
#         #Convert tool to dictionary format (For AI)
#         #AI needs to understand tools in structured format

#         return{
#             'name': self.name,
#             'description': self.description,
#             'parameter': self.parameter
#         }
    
# #AGENT MEMORY CLASS
# class AgentMemory:
#     #it stores what the agent has done and learned
#     #WHY MEMORY?
#     # Agent needs to remember:
#     # - What tools it has called
#     # - What results it got
#     # - What the user asked
#     # - What steps it took

#     def __init__(self):
#         #initialize empty memory
#         self.history = []
#         self.task = None
#         self.tool_calls = []
    
#     def set_task(self, task: str) -> None:
#         #stores the users task
#         self.task = task
#         self.history.append({
#             'type': 'task',
#             'content': 'task',
#             'timestamp': datetime.now().isoformat()
#         })
#         logger.info(f"Agent Task: {task}")

#     def add_thoughts(self, thought: str) ->None:
#         #agent thinks some thing like when the user say get me latest news
#         #agent thinks like: user wants news i should scrape website

#         self.history.append({
#             'type': 'thought',
#             'content': 'thought',
#             'timestamp': datetime.now().isoformat()
#         })
#         logger.info(f"Agent Thought: {thought}")

#     def add_tool_call(self, tool_name: str, params:dict, result: Any) -> None:
#         #Args:
#             # tool_name: Name of tool called
#             # params: Parameters passed
#             # result: What the tool returned

#             call = {
#                 'tool': tool_name,
#                 'parameters': params,
#                 'result': result,
#                 'timestamp': datetime.now().isoformat()
#             }
#             self.tool_calls.append(call)
#             self.history.append({
#                 'type': 'tool_call',
#                 'content': call,
#                 'timestamp': datetime.now().isoformat()
#             })

#             logger.info(f"Tool called: {tool_name} -> {str(result)[:100]}")

#     def get_history(self) -> list:
#         #get all history
#         return self.history
    
#     def get_summary(self) -> dict:
#         #get summary of agent's work
#         return{
#             'task': self.task,
#             'total_steps': len(self.history),
#             'tool_calls': len(self.tool_calls),
#             'tools_used': list(set(call['tool'] for call in self.tool_calls)),
#         }
    
# #BASE AGENT CLASS
# class BaseAgent(ABC):
#     #this is Abstract base class for all AI agents
#     def __init__(self, name: str, description: str):
#         self.name = name
#         self.description = description
#         self.tools = {} #tools this agent can use
#         self.memory = AgentMemory() #Agent's memory
#         self.max_iterations = 10 #this prevent infinite loop

#         logger.info(f"Initialized agent: {name}")

#     #TOOL MANAGEMENT
#     def register_tool(self, tool: Tool ) -> None:
#         #register the tool the agent can use means telling the agent you can use this tool
#         self.tools[tool.name] = tool
#         logger.info(f"Registered Tool: {tool.name}")

#     #LIST OF TOOLS
#     def get_tools(self) -> list:
#         #this gives the list of all the tools the agent has
#         return[tool.to_dict() for tool in self.tools.values()]
    

#     #THINKING AND REASONING
#     def think(self, task: str) -> str:
#         #this is where we call the OPENAI.. The agent thinks what to do
#         thought = f"I need to complete task: {task}"
#         self.memory.add_thoughts(thought)
#         return thought
    
#     def decide_tool(self, task: str) -> str:
#         #Agent decide which tool to use
#         #THIS IS AGENT INTELLIGENCE!
#         # Given a task, which tool should I use?

#         if 'scrape' in task.lower():
#             return 'scrape_website'
#         elif 'analyze' in task.lower():
#             return 'analyze'
#         elif 'summarize' in task.lower():
#             return 'summarize'
#         else: 
#             return list(self.tools.keys())[0] if self.tools else None
        
#     #Execute the tool which the agent has decided
#     def execute_tool(self, tool_name: str, **params) -> Any:
#         if tool_name not in self.tools:
#             logger.error(f"Tool not found: {tool_name}")
#             return f"Error: Tool '{tool_name}' not found"
        
#         tool = self.tools[tool_name]
#         result = tool.execute(**params)
#         self.memory.add_tool_call(tool_name, params, result)

#         return result
    
#     #ABSTRACT RUN METHOD
#     @abstractmethod
#     def run(self, task: str) -> str:
#         pass

#     #UTILITY METHODS
#     #this gives the summary of what agent did
#     def get_memory_summary(self) -> dict:
#         return self.memory.get_summary()
    
#     def clear_memory(self) -> None:
#         #this clears agent memory to start fresh
#         self.memory = AgentMemory()
#         logger.info(f"Cleared Memory for {self.name}")

#     def get_status(self) -> dict:
#         #this gives the agents current status
#         return{
#             'name': self.name,
#             'description': self.description,
#             'tools_available': len(self.tools),
#             'tools_name': list(self.tools.keys()),
#             'memory_entries': len(self.memory.get_history())
#         }

from __future__ import annotations

import logging
from typing import Any, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# ==================== TOOL CLASS ====================

@dataclass
class Tool:
    """Represents a tool the agent can use"""
    name: str
    description: str
    function: callable
    
    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


# ==================== MEMORY CLASS ====================

class Memory:
    """Agent memory to track state and history"""
    
    def __init__(self):
        self.task = None
        self.thoughts = []
        self.tool_calls = 0
        self.findings = []
        self.history = []
    
    def set_task(self, task: str) -> None:
        """Set the current task"""
        self.task = task
        self.history.append(f"Task set: {task}")
    
    def add_thoughts(self, thought: str) -> None:
        """Add a thought to memory"""
        self.thoughts.append(thought)
        self.history.append(f"Thought: {thought}")
    
    def record_tool_call(self, tool_name: str) -> None:
        """Record that a tool was called"""
        self.tool_calls += 1
        self.history.append(f"Tool called: {tool_name}")
    
    def add_finding(self, finding: str) -> None:
        """Add a finding to memory"""
        self.findings.append(finding)
        self.history.append(f"Finding: {finding}")
    
    def get_summary(self) -> dict:
        """Get memory summary"""
        return {
            "task": self.task,
            "thoughts": self.thoughts,
            "tool_calls": self.tool_calls,
            "findings": self.findings,
            "history_length": len(self.history)
        }
    
    def clear(self) -> None:
        """Clear memory"""
        self.task = None
        self.thoughts = []
        self.tool_calls = 0
        self.findings = []
        self.history = []


# ==================== BASE AGENT CLASS ====================

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, name: str = "Agent", description: str = "Base Agent"):
        self.name = name
        self.description = description
        self.memory = Memory()
        self.tools: List[Tool] = []
        
        logger.info(f"Initialized {self.name}")
    
    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the agent"""
        self.tools.append(tool)
        logger.info(f"Added tool: {tool.name}")
    
    def get_tools(self) -> List[Tool]:
        """Get all available tools"""
        return self.tools
    
    def think(self, thought: str) -> None:
        """Agent thinks (records thought)"""
        self.memory.add_thoughts(thought)
        logger.info(f"{self.name} thought: {thought}")
    
    def act(self, action: str) -> Any:
        """Agent takes an action"""
        logger.info(f"{self.name} acting: {action}")
        return None
    
    def reset(self) -> None:
        """Reset agent state"""
        self.memory.clear()
        logger.info(f"{self.name} reset")
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"



        




