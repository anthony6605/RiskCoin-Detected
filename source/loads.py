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



