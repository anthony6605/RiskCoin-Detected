"""
Binance API Client for extracting order book, trade data, and real-time prices.
Uses Binance public API (no authentication required for public endpoints).
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime
import time


class BinanceClient:
    """Client for Binance Public API"""
    
    BASE_URL = "https://api.binance.us/api/v3"
    
    def __init__(self):
        self.session = requests.Session()
    
    def fetch_ticker_24h(self, symbol: Optional[str] = None) -> Dict:
        """
        Fetch 24-hour ticker price change statistics.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT'). If None, fetches all symbols.
        
        Returns:
            Ticker data dictionary or list of dictionaries
        """
        endpoint = f"{self.BASE_URL}/ticker/24hr"
        params = {}
        if symbol:
            params["symbol"] = symbol
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching 24h ticker: {e}")
            return {} if symbol else []
    
    def fetch_orderbook(self, symbol: str, limit: int = 100) -> Dict:
        """
        Fetch order book (market depth) for a trading pair.
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            limit: Depth limit (5, 10, 20, 50, 100, 500, 1000, 5000)
        
        Returns:
            Order book with bids and asks
        """
        endpoint = f"{self.BASE_URL}/depth"
        params = {
            "symbol": symbol,
            "limit": limit
        }
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching order book for {symbol}: {e}")
            return {"bids": [], "asks": []}
    
    def fetch_recent_trades(self, symbol: str, limit: int = 500) -> List[Dict]:
        """
        Fetch recent trades.
        
        Args:
            symbol: Trading pair
            limit: Number of trades (max 1000)
        
        Returns:
            List of recent trades
        """
        endpoint = f"{self.BASE_URL}/trades"
        params = {
            "symbol": symbol,
            "limit": limit
        }
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching trades for {symbol}: {e}")
            return []
    
    def fetch_klines(
        self,
        symbol: str,
        interval: str = "1h",
        limit: int = 500,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None
    ) -> List[List]:
        """
        Fetch kline/candlestick data.
        
        Args:
            symbol: Trading pair
            interval: Kline interval (1m, 5m, 15m, 1h, 4h, 1d, 1w, 1M)
            limit: Number of klines (max 1000)
            start_time: Start time in milliseconds
            end_time: End time in milliseconds
        
        Returns:
            List of klines [open_time, open, high, low, close, volume, ...]
        """
        endpoint = f"{self.BASE_URL}/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching klines for {symbol}: {e}")
            return []
    
    def compute_liquidity_score(self, symbol: str) -> float:
        """
        Compute a liquidity score based on order book depth.
        Higher score = better liquidity.
        
        Args:
            symbol: Trading pair
        
        Returns:
            Liquidity score (0-100)
        """
        orderbook = self.fetch_orderbook(symbol, limit=100)
        
        if not orderbook.get("bids") or not orderbook.get("asks"):
            return 0.0
        
        # Calculate total volume at top 20 levels
        bid_volume = sum(float(bid[1]) for bid in orderbook["bids"][:20])
        ask_volume = sum(float(ask[1]) for ask in orderbook["asks"][:20])
        total_volume = bid_volume + ask_volume
        
        # Calculate spread
        best_bid = float(orderbook["bids"][0][0]) if orderbook["bids"] else 0
        best_ask = float(orderbook["asks"][0][0]) if orderbook["asks"] else 0
        spread = (best_ask - best_bid) / best_ask * 100 if best_ask > 0 else 100
        
        # Score: high volume + low spread = high liquidity
        volume_score = min(total_volume / 1000, 50)  # Cap at 50
        spread_score = max(0, 50 - spread * 10)  # Lower spread is better
        
        return min(volume_score + spread_score, 100)


# Example usage
if __name__ == "__main__":
    client = BinanceClient()
    
    # Fetch Bitcoin 24h ticker
    btc_ticker = client.fetch_ticker_24h("BTCUSDT")
    print(f"BTC Price: ${btc_ticker.get('lastPrice')}, 24h Change: {btc_ticker.get('priceChangePercent')}%")
    
    # Fetch order book
    orderbook = client.fetch_orderbook("BTCUSDT", limit=20)
    print(f"Order book depth: {len(orderbook.get('bids', []))} bids, {len(orderbook.get('asks', []))} asks")
    
    # Compute liquidity
    liquidity = client.compute_liquidity_score("BTCUSDT")
    print(f"Liquidity Score: {liquidity:.2f}/100")
    
    # Fetch recent klines
    klines = client.fetch_klines("BTCUSDT", interval="1h", limit=24)
    print(f"Fetched {len(klines)} hourly klines")
