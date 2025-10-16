import pandas as pd
import numpy as np
from typing import List, Optional

#Compute rolling window features for price data.
def compute_rolling_features(
    df: pd.DataFrame,
    windows: List[int] = [7, 14, 30],
    price_col: str = "price"
) -> pd.DataFrame:
    df = df.copy()
    
    if price_col not in df.columns:
        print(f"Warning: {price_col} not found in DataFrame")
        return df
    
    for window in windows:
        # Rolling mean (moving average)
        df[f"ma_{window}"] = df[price_col].rolling(window=window, min_periods=1).mean()
        
        # Rolling standard deviation (volatility)
        df[f"std_{window}"] = df[price_col].rolling(window=window, min_periods=1).std()
        
        # Rolling returns
        df[f"return_{window}"] = df[price_col].pct_change(periods=window)
        
        # Rolling min/max
        df[f"min_{window}"] = df[price_col].rolling(window=window, min_periods=1).min()
        df[f"max_{window}"] = df[price_col].rolling(window=window, min_periods=1).max()
        
        # Distance from moving average
        df[f"ma_distance_{window}"] = (df[price_col] - df[f"ma_{window}"]) / df[f"ma_{window}"]
    
    return df

#Compute volatility metrics.
def compute_volatility_metrics(
    df: pd.DataFrame,
    price_col: str = "price",
    windows: List[int] = [7, 14, 30]
) -> pd.DataFrame:
    
    df = df.copy()
    
    # Log returns
    df["log_return"] = np.log(df[price_col] / df[price_col].shift(1))
    
    for window in windows:
        # Realized volatility (std of log returns)
        df[f"realized_vol_{window}"] = df["log_return"].rolling(window=window).std() * np.sqrt(365)
        
        # Parkinson volatility (high-low range)
        if "high" in df.columns and "low" in df.columns:
            df[f"parkinson_vol_{window}"] = np.sqrt(
                (np.log(df["high"] / df["low"]) ** 2).rolling(window=window).mean() / (4 * np.log(2))
            ) * np.sqrt(365)
    
    # Volatility score (0-100 scale)
    if f"realized_vol_{windows[0]}" in df.columns:
        vol = df[f"realized_vol_{windows[0]}"]
        # Normalize to 0-100 (higher vol = higher score)
        df["volatility_score"] = np.clip((vol / vol.quantile(0.95)) * 100, 0, 100)
    
    return df

#Compute momentum indicators.
def compute_momentum_indicators(
    df: pd.DataFrame,
    price_col: str = "price"
) -> pd.DataFrame:
    
    df = df.copy()
    
    # RSI (Relative Strength Index)
    delta = df[price_col].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))
    
    # MACD (Moving Average Convergence Divergence)
    exp12 = df[price_col].ewm(span=12, adjust=False).mean()
    exp26 = df[price_col].ewm(span=26, adjust=False).mean()
    df["macd"] = exp12 - exp26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_histogram"] = df["macd"] - df["macd_signal"]
    
    return df

#Compute drawdown metrics.
def compute_drawdown(df: pd.DataFrame, price_col: str = "price") -> pd.DataFrame:
    
    df = df.copy()
    
    # Running maximum
    df["running_max"] = df[price_col].cummax()
    
    # Drawdown (percentage from peak)
    df["drawdown"] = (df[price_col] - df["running_max"]) / df["running_max"] * 100
    
    # Maximum drawdown (rolling)
    df["max_drawdown_30d"] = df["drawdown"].rolling(window=30, min_periods=1).min()
    
    return df

#Compute volume-based features.
def compute_volume_features(
    df: pd.DataFrame,
    volume_col: str = "volume",
    price_col: str = "price"
) -> pd.DataFrame:
    
    
    df = df.copy()
    
    if volume_col not in df.columns:
        return df
    
    # Rolling volume mean
    df["volume_ma_7"] = df[volume_col].rolling(window=7, min_periods=1).mean()
    df["volume_ma_30"] = df[volume_col].rolling(window=30, min_periods=1).mean()
    
    # Volume ratio (current vs average)
    df["volume_ratio"] = df[volume_col] / df["volume_ma_30"]
    
    # Price-volume correlation
    df["price_volume_corr"] = df[price_col].rolling(window=30).corr(df[volume_col])
    
    # On-Balance Volume (OBV)
    df["obv"] = (np.sign(df[price_col].diff()) * df[volume_col]).cumsum()
    
    return df

#Compute liquidity proxy score.
def compute_liquidity_proxy(
    df: pd.DataFrame,
    volume_col: str = "volume",
    price_col: str = "price"
) -> pd.DataFrame:
    
    df = df.copy()
    
    if volume_col not in df.columns:
        df["liquidity_score"] = 50  # Default medium
        return df
    
    # Volume-to-market-cap ratio (proxy)
    # Normalize 24h volume
    avg_volume = df[volume_col].rolling(window=30, min_periods=1).mean()
    volume_stability = 1 - (df[volume_col].rolling(window=30).std() / avg_volume).fillna(0)
    
    # Higher volume + more stable = higher liquidity
    volume_score = np.clip((df[volume_col] / df[volume_col].quantile(0.95)) * 50, 0, 50)
    stability_score = np.clip(volume_stability * 50, 0, 50)
    
    df["liquidity_score"] = volume_score + stability_score
    
    return df


