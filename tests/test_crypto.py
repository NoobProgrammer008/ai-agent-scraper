from src.scrapers.crypto_scraper import CryptoScraper

# Create scraper
scraper = CryptoScraper()

# Test building URL
url = scraper.build_price_url(['bitcoin', 'ethereum'], 'usd')
print(f"Built URL: {url}")

# Test getting crypto data (REAL API CALL)
print("\nFetching real cryptocurrency data...")
result = scraper.fetch_prices(['bitcoin', 'ethereum', 'cardano'])

if result:
    print(f"\n✅ Successfully scraped data!")
    print(f"Data: {result}")
else:
    print("\n❌ Failed to scrape")

# Get summary
print(f"\nSummary: {scraper.summary()}")