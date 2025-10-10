import boto3
from botocore.exceptions import ClientError
import pandas as pd
import json
from datetime import datetime
from typing import Any, Dict, Optional
import io
import os
from dotenv import load_dotenv

class S3Loader:
    """Loader for writing data to S3 (or MinIO for local dev)"""
    
    def __init__(
        self,
        bucket_name: str,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        endpoint_url: Optional[str] = None,  # For MinIO
        region_name: str = "us-east-1"
    ):
        """
        Initialize S3 client.
        
        Args:
            bucket_name: S3 bucket name
            aws_access_key_id: AWS access key (or use IAM role)
            aws_secret_access_key: AWS secret key
            endpoint_url: Custom endpoint (e.g., for MinIO)
            region_name: AWS region
        """
        self.bucket_name = bucket_name
        
        session_kwargs = {"region_name": region_name}
        if aws_access_key_id and aws_secret_access_key:
            session_kwargs["aws_access_key_id"] = aws_access_key_id
            session_kwargs["aws_secret_access_key"] = aws_secret_access_key
        
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            **session_kwargs
        )
        
        # Ensure bucket exists
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket '{self.bucket_name}' exists")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                try:
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                    print(f"Created bucket: {self.bucket_name}")
                except ClientError as create_error:
                    print(f"Error creating bucket: {create_error}")
            else:
                print(f"Error checking bucket: {e}")
        except Exception as e:
            print(f"Connection error: {e}")
            print("Make sure AWS credentials are configured or MinIO is running")
    
    def write_raw(
        self,
        data: Any,
        path: str,
        format: str = "json"
    ) -> bool:
        """
        Write raw data to S3.
        
        Args:
            data: Data to write (dict, list, or string)
            path: S3 key path (e.g., 'raw/coins/2024-01-01/bitcoin.json')
            format: Format ('json' or 'text')
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if format == "json":
                body = json.dumps(data, indent=2)
                content_type = "application/json"
            else:
                body = str(data)
                content_type = "text/plain"
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=path,
                Body=body.encode('utf-8'),
                ContentType=content_type
            )
            print(f"Wrote {format} to s3://{self.bucket_name}/{path}")
            return True
            
        except ClientError as e:
            print(f"Error writing to S3: {e}")
            return False
    
    def write_parquet(
        self,
        df: pd.DataFrame,
        path: str,
        partition_cols: Optional[list] = None
    ) -> bool:
        """
        Write DataFrame as Parquet to S3.
        
        Args:
            df: DataFrame to write
            path: S3 key path (e.g., 'processed/prices/2024-01-01/')
            partition_cols: Columns to partition by
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Write to buffer
            buffer = io.BytesIO()
            df.to_parquet(buffer, engine='pyarrow', compression='snappy', index=False)
            buffer.seek(0)
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=path,
                Body=buffer.getvalue(),
                ContentType="application/octet-stream"
            )
            print(f"Wrote Parquet to s3://{self.bucket_name}/{path}")
            return True
            
        except Exception as e:
            print(f"Error writing Parquet: {e}")
            return False
    
    def write_csv(
        self,
        df: pd.DataFrame,
        path: str
    ) -> bool:
        """
        Write DataFrame as CSV to S3.
        
        Args:
            df: DataFrame to write
            path: S3 key path
        
        Returns:
            True if successful, False otherwise
        """
        try:
            buffer = io.StringIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=path,
                Body=buffer.getvalue().encode('utf-8'),
                ContentType="text/csv"
            )
            print(f"Wrote CSV to s3://{self.bucket_name}/{path}")
            return True
            
        except ClientError as e:
            print(f"Error writing CSV: {e}")
            return False
    
    def generate_partition_path(
        self,
        base_path: str,
        dt: Optional[datetime] = None,
        coin_id: Optional[str] = None
    ) -> str:
        """
        Generate partitioned S3 path.
        
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
    
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get credentials from .env file
    aws_access_key_id = os.getenv('aws_access_key_id')
    aws_secret_access_key = os.getenv('aws_secret_access_key')
    bucket_name = os.getenv('s3_bucket_name', 'coin-project-bucket-1')
    
    # Create S3Loader with credentials from .env
    loader = S3Loader(
        bucket_name=bucket_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    
    # Test with sample data
    sample_data = {
        "coin_id": "bitcoin",
        "price": 67234.50,
        "timestamp": "2024-01-15T10:00:00Z"
    }
    
    # Write test data
    raw_path = loader.generate_partition_path("raw/prices", coin_id="bitcoin")
    loader.write_raw(sample_data, f"{raw_path}/data.json")
    
    print("S3Loader test complete!")
