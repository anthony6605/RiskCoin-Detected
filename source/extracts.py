import requests
import os
import json
from datetime import datetime

# Stablecoins to monitor
STABLECOINS = ["usd-coin", "tether", "dai"]  # CoinGecko IDs
VS_CURRENCY = "usd"

def fetch_stablecoin_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(STABLECOINS),
        "vs_currencies": VS_CURRENCY,
        "include_24hr_change": "true"
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()

def save_raw_data(data):
    os.makedirs("data/raw", exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filepath = f"data/raw/stablecoins_{timestamp}.json"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved raw data to {filepath}")
    return filepath

if __name__ == "__main__":
    data = fetch_stablecoin_prices()
    print("Fetched data:", data)
    save_raw_data(data)