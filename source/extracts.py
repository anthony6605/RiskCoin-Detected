import os
import requests
import json
from datetime import datetime

# Create data directory if it doesn’t exist
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_coins():
    """
    Fetch market data for top coins from CoinGecko.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": "false"
    }

    print(f"Fetching data from {url}...")
    resp = requests.get(url, params=params)

    if resp.status_code != 200:
        raise Exception(f"Error {resp.status_code}: {resp.text}")

    return resp.json()

def save_json(data, filename):
    """
    Save JSON data to the raw data directory with timestamp.
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(DATA_DIR, f"{filename}_{timestamp}.json")

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved data to {filepath}")
    return filepath

if __name__ == "__main__":
    try:
        data = fetch_coins()
        save_json(data, "coins")
    except Exception as e:
        print(f"❌ Extract failed: {e}")
