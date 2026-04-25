# test_api.py

import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_PLACES_API_KEY")
print(f"[debug] Key loaded: {api_key}")

url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
params = {
    "query": "plumbing in Port of Spain, Trinidad",
    "key": api_key,
}

print(f"[debug] Params being sent: {params}")

response = requests.get(url, params=params)
data = response.json()

print(f"[debug] Status: {data.get('status')}")
print(f"[debug] Error message: {data.get('error_message')}")
print(f"[debug] Full response: {data}")