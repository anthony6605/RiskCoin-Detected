from datetime import datetime, timezone
import pandas as pd
from typing import Optional

def normalize_timestamp(df: pd.DataFrame, timestamp_col: str) -> pd.DataFrame:
    df = df.copy()
    
    #Converte to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df[timestamp_col]):
        # Try multiple formats
        if df[timestamp_col].dtype in [int, float]:
            # if Unix timestamp (milliseconds or seconds)
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
#Resample timeseries data to a given rule
 def resample_timeseries(
    df: pd.DataFrame,
    rule: str,
    timestamp_col: str = "timestamp"
    agg_config: Optional[dict] = None
 ) -> pd.DataFrame:   

    df = df.copy()
    df = df.set_index(timestamp_col)

    if agg_config is None:
        agg_config = {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum"
        }
    
    agg_config = {k: v for k, v in agg_config.items() if k in df.columns}
    #resample timestamp 
    resampled = df.resample(rule).agg(agg_config)
    resampled = resampled.ffill()
    resampled = resampled.reset_index()
    return resampled