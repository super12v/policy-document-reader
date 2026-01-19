"""S3 bucket reader."""
from pathlib import Path
from typing import List, Dict, Any
from urllib.parse import urlparse
import boto3
from src.services.readers.base import BaseReader
from src.utils.logger import logger
from src.utils.errors import SourceConnectionError, NotFoundError


class S3Reader(BaseReader):
    """Read documents from AWS S3 buckets."""
    
    def __init__(self, temp_dir: Path = Path("/tmp/policy-reader")):
        self.temp_dir = temp_dir
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    async def read_file(self, path: str, credentials: Dict[str, Any]) -> Path:
        """
        Read file from S3.
        
        Path format: s3://bucket-name/path/to/file.pdf
        """
        logger.info(f"Reading from S3: {path}")
        
        try:
            # Parse S3 URL
            parsed = urlparse(path)
            bucket = parsed.hostname
            key = parsed.path.lstrip('/')
            
            # Create S3 client
            s3_client = boto3.client(
                's3',
                aws_access_key_id=credentials.get('access_key_id'),
                aws_secret_access_key=credentials.get('secret_access_key'),
                region_name=credentials.get('region', 'us-east-1')
            )
            
            # Download file
            filename = Path(key).name
            temp_file = self.temp_dir / filename
            
            s3_client.download_file(bucket, key, str(temp_file))
            
            logger.info(f"Downloaded s3://{bucket}/{key} to {temp_file}")
            return temp_file
            
        except Exception as e:
            logger.error(f"S3 read failed for {path}: {e}")
            raise SourceConnectionError(f"S3 error: {e}")
    
    async def list_files(self, path: str, credentials: Dict[str, Any]) -> List[Dict[str, Any]]:
        """List files in S3 bucket/prefix."""
        logger.info(f"Listing S3 path: {path}")
        
        try:
            parsed = urlparse(path)
            bucket = parsed.hostname
            prefix = parsed.path.lstrip('/')
            
            s3_client = boto3.client(
                's3',
                aws_access_key_id=credentials.get('access_key_id'),
                aws_secret_access_key=credentials.get('secret_access_key'),
                region_name=credentials.get('region', 'us-east-1')
            )
            
            response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
            
            files = []
            for obj in response.get('Contents', []):
                files.append({
                    'name': Path(obj['Key']).name,
                    'path': f"s3://{bucket}/{obj['Key']}",
                    'size': obj['Size'],
                    'modified': obj['LastModified'].timestamp(),
                })
            
            return files
            
        except Exception as e:
            logger.error(f"S3 list failed for {path}: {e}")
            raise SourceConnectionError(f"S3 error: {e}")
    
    def supports_protocol(self, uri: str) -> bool:
        """Check if protocol is supported."""
        return uri.startswith('s3://')
