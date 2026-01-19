"""Reader registry and factory."""
from pathlib import Path
from typing import Dict, Any, List
from src.services.readers.base import BaseReader
from src.services.readers.local_reader import LocalReader
from src.services.readers.smb_reader import SMBReader
from src.services.readers.git_reader import GitReader
from src.services.readers.http_reader import HTTPReader
from src.services.readers.s3_reader import S3Reader
from src.utils.errors import UnsupportedFormatError
from src.utils.logger import logger


class ReaderRegistry:
    """Registry of document source readers."""
    
    def __init__(self):
        self.readers: list[BaseReader] = [
            S3Reader(),
            GitReader(),
            SMBReader(),
            HTTPReader(),
            LocalReader(),  # Fallback for local paths
        ]
    
    def get_reader(self, uri: str) -> BaseReader:
        """Get reader for protocol."""
        for reader in self.readers:
            if reader.supports_protocol(uri):
                return reader
        raise UnsupportedFormatError(f"No reader for protocol: {uri}")
    
    async def read_document(self, uri: str, credentials: Dict[str, Any]) -> Path:
        """Read document from any source."""
        logger.info(f"Reading document from: {uri}")
        
        reader = self.get_reader(uri)
        file_path = await reader.read_file(uri, credentials)
        
        return file_path
    
    async def list_documents(self, uri: str, credentials: Dict[str, Any]) -> List[Dict[str, Any]]:
        """List documents at location."""
        logger.info(f"Listing documents at: {uri}")
        
        reader = self.get_reader(uri)
        files = await reader.list_files(uri, credentials)
        
        return files


# Global reader registry
reader_registry = ReaderRegistry()
