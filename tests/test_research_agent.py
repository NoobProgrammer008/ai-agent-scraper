import pytest #testing framework

from unittest.mock import Mock, patch, MagicMock
#import the agent we are testing
from src.agents.research_agent import ResearchAgent

#FIXTURES for test
@pytest.fixture
def research_agent():
    """
    CREATE A FRESH AGENT FOR EACH TEST.
    
    WHY FIXTURE?
    - Each test gets clean agent (no leftover state)
    - Reusable setup code
    - DRY (Don't Repeat Yourself)
    
    WHAT HAPPENS:
    1. pytest sees @pytest.fixture
    2. Before each test, creates new agent
    3. Passes agent to test as parameter
    4. After test, cleans up
    """
    agent = ResearchAgent()

    return agent

@pytest.fixture
def mock_crypto_scraper():
    mock_scraper = MagicMock()

    mock_scraper.fetch_prices = MagicMock(
        return_value = {
            'bitcoin':{
                'price': 45000,
                'currency': 'usd',
                '24_change': 2.5,
                'market_cap': 900000000000
            }
        }
    )

    return mock_scraper

@pytest.fixture
def agent_with_scraper(research_agent, mock_crypto_scraper):
    #Create agent with the fake mock scraper to test them combine
    research_agent.register_scraper('crypto', mock_crypto_scraper)
    return research_agent

#INITIALIZATION TESTS
def test_research_agent_initialization(research_agent):

    assert research_agent.name == "ResearchAgent"

    assert research_agent.max_research_depth == 3

    assert research_agent.memory is not None

    assert len(research_agent.scraper_tools) == 0 #Check scraper dict is empty at start

def test_register_scraper(research_agent, mock_crypto_scraper):
    
    research_agent.register_scraper('crypto', mock_crypto_scraper)

    assert 'crypto' in research_agent.scraper_tools

    assert research_agent.scraper_tools['crypto'] == mock_crypto_scraper

#TASK PARSING TEST
def test_parse_task_bitcoin(research_agent):
    #here we parse the bitcoin task works

    parsed = research_agent._parse_task("Research Bitcoin Price")

    assert parsed['query'] == 'bitcoin' 
    assert parsed['type'] == 'crypto'

def test_parse_task_news(research_agent):
    #parsing news task work

    parsed = research_agent._parse_task("Get latest A.I News")

    assert parsed['query'] == 'news'
    assert parsed['type'] == 'news'

def test_parse_task_invalid(research_agent):
    
    parsed = research_agent._parse_task(None) #we passed nothing means Invalid

    assert parsed == {} #it will return empty dict

    parsed = research_agent._parse_task("") #empty string also invalid

    assert parsed == {}


#AGENT DECISION TEST
#Agent must decide correct scraper to use
def test_decide_scraper_crypto(research_agent):

    #task parsed as crypto
    task = {'type': 'crypto', 'query': 'bitcoin'}

    scraper_name = research_agent._decide_scraper(task)
    assert scraper_name == 'crypto'

def test_decide_scraper_news(research_agent):

    task = {'type': 'news', 'query': 'ai news'}

    scraper_name = research_agent._decide_scraper(task)
    assert scraper_name == 'news'


#SCRAPER EXECUTION TEST
#test to check if the agent can execute or call the crypto scrapper
def test_execute_scraper_with_crypto(agent_with_scraper):
    task = {'type': 'crypto', 'query': 'bitcoin'}

    scraper = agent_with_scraper.scraper_tools['crypto']
    data = agent_with_scraper._execute_scraper[scraper, task]

    assert data is not None
    assert 'bitcoin' in data

def test_execute_scraper_notfound(research_agent):
    
    task = {'type': 'crypto', 'query': 'bitcoin'}
    fake_scraper = MagicMock()

    result = research_agent.execute_tool(fake_scraper, task)
    assert result is None

#DATA TEST ANALYSIS
def test_analyze_data_with_crypto(research_agent):

    data = {
        'bitcoin':{
            'price' : 45000,
            '24h_change':2.5
        }
    }
    task = {'topic': 'Bitcoin research'}

    analysis = research_agent._analyze_data(data, task)

    assert analysis is not None
    assert 'Bitcoin research' in analysis

def test_analyze_data_empty(research_agent):
    analysis = research_agent._analyze_data({}, {'topic': 'test'})

    assert 'No data' in analysis


#FULL INTEGRATION TEST
def test_full_research_flow(agent_with_scraper): #testing entire work flow 
    
    result = agent_with_scraper.run("Research Bitcoin")

    assert result['success'] == True
    assert result['query'] == 'bitcoin'
    assert 'analysis' in result
    assert 'scraped_data' in result

def test_full_research_missing_scrapper





