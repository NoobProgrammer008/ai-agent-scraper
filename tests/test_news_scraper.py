"""Test the new NewsAPI-based NewsScraper"""

import os
from dotenv import load_dotenv
from src.scrapers.news_scraper import NewsScraper

# Load environment variables
load_dotenv()

print("=" * 60)
print("TESTING NEW NEWS API-BASED NEWS SCRAPER")
print("=" * 60)

# Create scraper
scraper = NewsScraper()

# Test 1: Fetch articles for a query
print("\n1️⃣ Test: Fetching articles for 'bitcoin'...")
print("-" * 60)

result = scraper.fetch("bitcoin")

if result.get("success"):
    print("✅ SUCCESS!")
    print(f"Found {result.get('total_results')} articles\n")
    
    # Show first article
    articles = result.get("articles", [])
    if articles:
        first_article = articles[0]
        print(f"📰 First Article:")
        print(f"  Title: {first_article.get('title')}")
        print(f"  Source: {first_article.get('source')}")
        print(f"  Author: {first_article.get('author')}")
        print(f"  Published: {first_article.get('published_at')}")
        print(f"  URL: {first_article.get('url')}")
        print(f"  Description: {first_article.get('description')[:100]}...")
else:
    print("❌ FAILED!")
    print(f"Error: {result.get('error')}")

# Test 2: Fetch articles for multiple queries
print("\n" + "=" * 60)
print("2️⃣ Test: Fetching articles for multiple queries...")
print("-" * 60)

queries = ["AI", "Python", "technology"]
results = scraper.fetch_multiple_queries(queries)

for query, data in results.items():
    if data.get("success"):
        print(f"✅ {query}: Found {data.get('total_results')} articles")
    else:
        print(f"❌ {query}: Error - {data.get('error')}")

# Test 3: Get summary
print("\n" + "=" * 60)
print("3️⃣ Test: Getting summary...")
print("-" * 60)

summary = scraper.get_summary()
print(f"Total articles cached: {summary.get('total_articles')}")
print(f"Total words: {summary.get('total_words')}")
print(f"Average words per article: {summary.get('average_words_per_article')}")

# Test 4: Single search and display
print("\n" + "=" * 60)
print("4️⃣ Test: Single search for 'machine learning'...")
print("-" * 60)

result = scraper.fetch("machine learning")

if result.get("success"):
    print(f"✅ Found {result.get('total_results')} articles\n")
    
    for i, article in enumerate(result.get("articles", [])[:3], 1):
        print(f"\n📄 Article {i}:")
        print(f"   Title: {article.get('title')}")
        print(f"   Source: {article.get('source')}")
        print(f"   URL: {article.get('url')}")
else:
    print(f"❌ Error: {result.get('error')}")

print("\n" + "=" * 60)
print("✅ TESTING COMPLETE!")
print("=" * 60)