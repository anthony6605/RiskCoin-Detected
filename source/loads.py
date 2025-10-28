"""
Local file system data loaders for writing raw and processed data.
Supports JSON, Parquet, and CSV formats with partitioning.
"""

import pandas as pd
import json
from datetime import datetime
from typing import Any, Dict, Optional
import os
from pathlib import Path


class LocalLoader:
    """Loader for writing data to local file system"""
    
    def __init__(self, base_path: str = "data"):
        """
        Initialize local file system loader.
        
        Args:
            base_path: Base directory for data storage (default: 'data')
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def write_raw(
        self,
        data: Any,
        path: str,
        format: str = "json"
    ) -> bool:
        """
        Write raw data to local file system.
        
        Args:
            data: Data to write (dict, list, or string)
            path: File path relative to base_path (e.g., 'raw/coins/2024-01-01/bitcoin.json')
            format: Format ('json' or 'text')
        
        Returns:
            True if successful, False otherwise
        """
        try:
            full_path = self.base_path / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            if format == "json":
                with open(full_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
            else:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(str(data))
            
            print(f"✓ Wrote {format} to {full_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error writing file: {e}")
            return False
    
    def write_parquet(
        self,
        df: pd.DataFrame,
        path: str,
        partition_cols: Optional[list] = None
    ) -> bool:
        """
        Write DataFrame as Parquet to local file system.
        
        Args:
            df: DataFrame to write
            path: File path relative to base_path (e.g., 'processed/prices/2024-01-01/data.parquet')
            partition_cols: Columns to partition by
        
        Returns:
            True if successful, False otherwise
        """
        try:
            full_path = self.base_path / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            df.to_parquet(full_path, engine='pyarrow', compression='snappy', index=False)
            print(f"✓ Wrote Parquet to {full_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error writing Parquet: {e}")
            return False
    
    def write_csv(
        self,
        df: pd.DataFrame,
        path: str
    ) -> bool:
        """
        Write DataFrame as CSV to local file system.
        
        Args:
            df: DataFrame to write
            path: File path relative to base_path
        
        Returns:
            True if successful, False otherwise
        """
        try:
            full_path = self.base_path / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            df.to_csv(full_path, index=False)
            print(f"✓ Wrote CSV to {full_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error writing CSV: {e}")
            return False
    
    def generate_partition_path(
        self,
        base_path: str,
        dt: Optional[datetime] = None,
        coin_id: Optional[str] = None
    ) -> str:
        """
        Generate partitioned file path.
        
        Args:
            base_path: Base path (e.g., 'raw/prices')
            dt: Datetime for date partitioning
            coin_id: Coin ID for coin partitioning
        
        Returns:
            Partitioned path string
        """
        if dt is None:
            dt = datetime.utcnow()
        
        parts = [base_path]
        parts.append(f"year={dt.year}")
        parts.append(f"month={dt.month:02d}")
        parts.append(f"day={dt.day:02d}")
        
        if coin_id:
            parts.append(f"coin={coin_id}")
        
        return "/".join(parts)


# Example usage
if __name__ == "__main__":
    # Local file system loader
    loader = LocalLoader(base_path="data")
    
    # Write raw JSON
    sample_data = {
        "coin_id": "bitcoin",
        "price": 67234.50,
        "timestamp": "2024-01-15T10:00:00Z"
    }
    
    raw_path = loader.generate_partition_path("raw/prices", coin_id="bitcoin")
    loader.write_raw(sample_data, f"{raw_path}/data.json")
    
    # Write Parquet
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=10, freq="H"),
        "price": [50000 + i * 100 for i in range(10)],
        "volume": [1e9 + i * 1e8 for i in range(10)]
    })
    
    parquet_path = loader.generate_partition_path("processed/prices", coin_id="bitcoin")
    loader.write_parquet(df, f"{parquet_path}/data.parquet")
    
    print("\n✓ Local loader test complete!")
    print(f"  Data written to {loader.base_path}/")
    print(f"  Raw JSON: {raw_path}/data.json")
    print(f"  Parquet: {parquet_path}/data.parquet")
