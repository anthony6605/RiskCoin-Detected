"""
CoinGecko API Client for extracting crypto market data.
Fetches OHLCV, metadata, and market information.
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import time


class CoinGeckoClient:
    """Client for CoinGecko API v3"""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"x-cg-pro-api-key": api_key})
    
    def fetch_ohlcv(
        self, 
        coin_id: str, 
        vs_currency: str = "usd",
        days: int = 30,
        interval: str = "daily"
    ) -> List[List]:
        """
        Fetch OHLCV (Open, High, Low, Close, Volume) data.
        
        Args:
            coin_id: CoinGecko coin ID (e.g., 'bitcoin')
            vs_currency: Target currency (default: 'usd')
            days: Number of days of data (1, 7, 14, 30, 90, 180, 365, 'max')
            interval: Data interval ('daily' or 'hourly')
        
        Returns:
            List of [timestamp, open, high, low, close] arrays
        """
        endpoint = f"{self.BASE_URL}/coins/{coin_id}/ohlc"
        params = {
            "vs_currency": vs_currency,
            "days": days
        }
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching OHLCV for {coin_id}: {e}")
            return []
    
    def fetch_metadata(self, coin_id: str) -> Dict:
        """
        Fetch detailed metadata for a coin.
        
        Args:
            coin_id: CoinGecko coin ID
        
        Returns:
            Dictionary with coin metadata including:
            - name, symbol, description
            - market_cap, total_volume, prices
            - market_cap_rank, circulating_supply
        """
        endpoint = f"{self.BASE_URL}/coins/{coin_id}"
        params = {
            "localization": "false",
            "tickers": "false",
            "community_data": "true",
            "developer_data": "false"
        }
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching metadata for {coin_id}: {e}")
            return {}
    
    def fetch_market_data(
        self, 
        vs_currency: str = "usd",
        per_page: int = 250,
        page: int = 1
    ) -> List[Dict]:
        """
        Fetch market data for multiple coins.
        
        Args:
            vs_currency: Target currency
            per_page: Number of results per page (max 250)
            page: Page number
        
        Returns:
            List of coin market data dictionaries
        """
        endpoint = f"{self.BASE_URL}/coins/markets"
        params = {
            "vs_currency": vs_currency,
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page,
            "sparkline": "false",
            "price_change_percentage": "24h,7d,30d"
        }
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching market data: {e}")
            return []
    
    def fetch_trending(self) -> Dict:
        """Fetch trending coins"""
        endpoint = f"{self.BASE_URL}/search/trending"
        
        try:
            response = self.session.get(endpoint, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching trending: {e}")
            return {}
    
    def rate_limit_safe(self, func, *args, **kwargs):
        """Execute function with rate limit handling"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:  # Rate limit
                    wait_time = (attempt + 1) * 2
                    print(f"Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise
        return None


# Example usage
if __name__ == "__main__":
    client = CoinGeckoClient()
    
    # Fetch Bitcoin OHLCV
    btc_ohlc = client.fetch_ohlcv("bitcoin", days=30)
    print(f"Fetched {len(btc_ohlc)} OHLC data points for Bitcoin")
    
    # Fetch Bitcoin metadata
    btc_meta = client.fetch_metadata("bitcoin")
    if btc_meta:
        print(f"Bitcoin: {btc_meta.get('name')}, Rank: {btc_meta.get('market_cap_rank')}")
    
    # Fetch top 20 coins
    top_coins = client.fetch_market_data(per_page=20)
    print(f"Fetched {len(top_coins)} top coins")