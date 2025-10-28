"""
Data cleaning and normalization transformers.
Handles timestamp conversion, missing values, and data type standardization.
"""

import pandas as pd
from datetime import datetime, timezone
from typing import Optional


def normalize_timestamps(df: pd.DataFrame, timestamp_col: str = "timestamp") -> pd.DataFrame:
    """
    Normalize timestamps to UTC datetime format.
    
    Args:
        df: DataFrame with timestamp column
        timestamp_col: Name of timestamp column
    
    Returns:
        DataFrame with normalized timestamps
    """
    df = df.copy()
    
    # Convert to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df[timestamp_col]):
        # Try multiple formats
        if df[timestamp_col].dtype in [int, float]:
            # Assume Unix timestamp (milliseconds or seconds)
            if df[timestamp_col].max() > 1e12:  # Milliseconds
                df[timestamp_col] = pd.to_datetime(df[timestamp_col], unit='ms', utc=True)
            else:  # Seconds
                df[timestamp_col] = pd.to_datetime(df[timestamp_col], unit='s', utc=True)
        else:
            # Try parsing string
            df[timestamp_col] = pd.to_datetime(df[timestamp_col], utc=True)
    
    # Ensure UTC
    if df[timestamp_col].dt.tz is None:
        df[timestamp_col] = df[timestamp_col].dt.tz_localize('UTC')
    else:
        df[timestamp_col] = df[timestamp_col].dt.tz_convert('UTC')
    
    return df


def resample_timeseries(
    df: pd.DataFrame,
    rule: str,
    timestamp_col: str = "timestamp",
    agg_config: Optional[dict] = None
) -> pd.DataFrame:
    """
    Resample time series data to a specific frequency.
    
    Args:
        df: DataFrame with timestamp column
        rule: Resampling frequency ('1min', '5min', '1h', '1d', etc.)
        timestamp_col: Name of timestamp column
        agg_config: Aggregation configuration dict (col -> agg_func)
    
    Returns:
        Resampled DataFrame
    """
    df = df.copy()
    
    # Set timestamp as index
    df = df.set_index(timestamp_col)
    
    # Default aggregation: OHLCV pattern
    if agg_config is None:
        agg_config = {
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum',
            'price': 'mean'  # For non-OHLC data
        }
    
    # Filter to only existing columns
    agg_config = {k: v for k, v in agg_config.items() if k in df.columns}
    
    # Resample
    resampled = df.resample(rule).agg(agg_config)
    
    # Forward fill missing values
    resampled = resampled.ffill()
    
    # Reset index
    resampled = resampled.reset_index()
    
    return resampled


def handle_missing_values(
    df: pd.DataFrame,
    method: str = "ffill",
    threshold: float = 0.5
) -> pd.DataFrame:
    """
    Handle missing values in DataFrame.
    
    Args:
        df: Input DataFrame
        method: Handling method ('ffill', 'bfill', 'interpolate', 'drop')
        threshold: Max fraction of missing values per column before dropping
    
    Returns:
        DataFrame with handled missing values
    """
    df = df.copy()
    
    # Drop columns with too many missing values
    missing_frac = df.isnull().sum() / len(df)
    cols_to_drop = missing_frac[missing_frac > threshold].index.tolist()
    if cols_to_drop:
        print(f"Dropping columns with >{threshold*100}% missing: {cols_to_drop}")
        df = df.drop(columns=cols_to_drop)
    
    # Handle remaining missing values
    if method == "ffill":
        df = df.ffill()
    elif method == "bfill":
        df = df.bfill()
    elif method == "interpolate":
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].interpolate(method='linear')
    elif method == "drop":
        df = df.dropna()
    
    return df


def standardize_coin_symbols(df: pd.DataFrame, symbol_col: str = "symbol") -> pd.DataFrame:
    """
    Standardize coin symbols to uppercase format.
    
    Args:
        df: DataFrame with symbol column
        symbol_col: Name of symbol column
    
    Returns:
        DataFrame with standardized symbols
    """
    df = df.copy()
    
    if symbol_col in df.columns:
        df[symbol_col] = df[symbol_col].str.upper().str.strip()
    
    return df


def remove_duplicates(
    df: pd.DataFrame,
    subset: Optional[list] = None,
    keep: str = "last"
) -> pd.DataFrame:
    """
    Remove duplicate rows.
    
    Args:
        df: Input DataFrame
        subset: Columns to consider for duplicates (None = all)
        keep: Which duplicate to keep ('first', 'last', False)
    
    Returns:
        DataFrame without duplicates
    """
    df = df.copy()
    
    before = len(df)
    df = df.drop_duplicates(subset=subset, keep=keep)
    after = len(df)
    
    if before > after:
        print(f"Removed {before - after} duplicate rows")
    
    return df


def validate_numeric_ranges(
    df: pd.DataFrame,
    col: str,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None
) -> pd.DataFrame:
    """
    Validate and clip numeric values to acceptable ranges.
    
    Args:
        df: Input DataFrame
        col: Column name
        min_val: Minimum acceptable value
        max_val: Maximum acceptable value
    
    Returns:
        DataFrame with validated values
    """
    df = df.copy()
    
    if col not in df.columns:
        return df
    
    # Remove negative prices/volumes
    if min_val is not None:
        outliers = df[df[col] < min_val]
        if len(outliers) > 0:
            print(f"Clipping {len(outliers)} values below {min_val} in {col}")
            df[col] = df[col].clip(lower=min_val)
    
    # Remove unrealistic high values
    if max_val is not None:
        outliers = df[df[col] > max_val]
        if len(outliers) > 0:
            print(f"Clipping {len(outliers)} values above {max_val} in {col}")
            df[col] = df[col].clip(upper=max_val)
    
    return df


# Example usage
if __name__ == "__main__":
    # Create sample data
    data = {
        "timestamp": [1609459200000, 1609545600000, 1609632000000],
        "symbol": ["btc", "eth", "bnb"],
        "price": [29000, 730, 38],
        "volume": [1000000, 500000, 200000]
    }
    df = pd.DataFrame(data)
    
    print("Original:")
    print(df)
    
    # Normalize timestamps
    df = normalize_timestamps(df)
    print("\nNormalized timestamps:")
    print(df)
    
    # Standardize symbols
    df = standardize_coin_symbols(df)
    print("\nStandardized symbols:")
    print(df)
