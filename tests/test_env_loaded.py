import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Check if it's loaded
api_key = os.getenv("NEWS_API_KEY")

if api_key:
    print(f"✅ SUCCESS! API Key found: {api_key[:10]}...")
else:
    print("❌ FAILED! API Key not found")
    print("Make sure:")
    print("1. .env file exists in project root")
    print("2. Contains: NEWS_API_KEY=your_key")
    print("3. Restart Python after creating .env")