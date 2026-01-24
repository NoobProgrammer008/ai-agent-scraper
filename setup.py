from setuptools import setup, find_packages

setup(
    name="ai-agent-scraper",
    version="0.1.0",
    description="AI-powered web scraping and analysis system",
    author="Annas Khan",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.2",
        "python-dotenv>=1.0.0",
        "langchain>=0.1.0",
        "openai>=1.3.0",
        "pydantic>=2.5.0",
        "pytest>=7.4.3",
    ],
)