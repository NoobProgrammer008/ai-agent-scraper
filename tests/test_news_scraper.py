from src.scrapers.news_scraper import NewsScraper

# Test with a real news article
scraper = NewsScraper()

# Using HackerNews (simple, allows scraping)
test_url = "https://news.ycombinator.com/"

print("Testing NewsArticleScraper...")
print(f"URL: {test_url}\n")

result = scraper.fetch_article(test_url)

if result:
    print("✅ Successfully scraped article!")
    print(f"Title: {result.get('title', 'N/A')}")
    print(f"Author: {result.get('author', 'N/A')}")
    print(f"Date: {result.get('date', 'N/A')}")
    print(f"Content length: {len(result.get('content', ''))} chars")
    print(f"URL: {result.get('url')}")
else:
    print("❌ Failed to scrape article")

print(f"\nSummary: {scraper.summary()}")