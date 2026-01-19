"""HTTP/REST API reader."""
from pathlib import Path
from typing import List, Dict, Any
from urllib.parse import urlparse
import httpx
from src.services.readers.base import BaseReader
from src.utils.logger import logger
from src.utils.errors import SourceConnectionError


class HTTPReader(BaseReader):
    """Read documents from HTTP/HTTPS endpoints."""
    
    def __init__(self, temp_dir: Path = Path("/tmp/policy-reader")):
        self.temp_dir = temp_dir
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    async def read_file(self, path: str, credentials: Dict[str, Any]) -> Path:
        """Download file from HTTP endpoint."""
        logger.info(f"Downloading from HTTP: {path}")
        
        try:
            # Prepare headers
            headers = {}
            if credentials:
                if 'api_key' in credentials:
                    headers['Authorization'] = f"Bearer {credentials['api_key']}"
                elif 'token' in credentials:
                    headers['Authorization'] = f"Bearer {credentials['token']}"
            
            # Download file
            async with httpx.AsyncClient() as client:
                response = await client.get(path, headers=headers, follow_redirects=True)
                response.raise_for_status()
                
                # Determine filename
                content_disposition = response.headers.get('content-disposition', '')
                if 'filename=' in content_disposition:
                    filename = content_disposition.split('filename=')[1].strip('"')
                else:
                    filename = Path(urlparse(path).path).name or 'downloaded_file'
                
                # Save to temp file
                temp_file = self.temp_dir / filename
                temp_file.write_bytes(response.content)
                
                logger.info(f"Downloaded {path} to {temp_file}")
                return temp_file
                
        except Exception as e:
            logger.error(f"HTTP download failed for {path}: {e}")
            raise SourceConnectionError(f"HTTP error: {e}")
    
    async def list_files(self, path: str, credentials: Dict[str, Any]) -> List[Dict[str, Any]]:
        """List files via REST API."""
        logger.info(f"Listing HTTP endpoint: {path}")
        
        # This would depend on the specific API
        # Many REST APIs have list/directory endpoints
        return []
    
    def supports_protocol(self, uri: str) -> bool:
        """Check if protocol is supported."""
        return uri.startswith('http://') or uri.startswith('https://')
