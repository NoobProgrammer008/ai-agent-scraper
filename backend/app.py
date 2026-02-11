# In backend/app.py
from src.agents.research_agent import ResearchAgent
from src.utils.memory import Memory

# Use your existing code
agent = ResearchAgent()
results = agent.run(query)
memory = agent.memory.get_summary()