import os
from dotenv import load_dotenv
import openai

#load env file from .env
load_dotenv()

#get API KEY
api_key = os.getenv("OPENAI_API_KEY")

#check if api key is in the env file
if not api_key:
    print("ERROR: OPENAI_API_KEY not Found in .env file")
    print("Make sure you created .env file with your key!")


else:
    print(f"API Key loaded: {api_key[:20]}....") #[:20] this shows the 1st 20 chars of the api key

    #testing the key by making a simple call
    try:
        client = openai.OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages=[
                {
                    "role": "user", "content" : "Say 'Hello from OpenAI!'"
                }
            ],
            max_tokens=10
        )
        print(f"\n API KEY WORKS")
        print(f"Response: {response.choices[0].message.content}")

    except Exception as e:
        print(f"❌ Error with API key: {e}")
