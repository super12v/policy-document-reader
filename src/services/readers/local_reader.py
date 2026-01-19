"""Local filesystem reader."""
from pathlib import Path
from typing import List, Dict, Any
import shutil
from src.services.readers.base import BaseReader
from src.utils.logger import logger
from src.utils.errors import NotFoundError


class LocalReader(BaseReader):
    """Read documents from local filesystem."""
    
    def __init__(self, temp_dir: Path = Path("/tmp/policy-reader")):
        self.temp_dir = temp_dir
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    async def read_file(self, path: str, credentials: Dict[str, Any] = None) -> Path:
        """Read file from local filesystem."""
        logger.info(f"Reading local file: {path}")
        
        file_path = Path(path)
        if not file_path.exists():
            raise NotFoundError(f"File not found: {path}")
        
        # For local files, return the path directly
        # (no need to copy unless we want isolation)
        return file_path
    
    async def list_files(self, path: str, credentials: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """List files in local directory."""
        logger.info(f"Listing local directory: {path}")
        
        dir_path = Path(path)
        if not dir_path.exists():
            raise NotFoundError(f"Directory not found: {path}")
        
        files = []
        for file_path in dir_path.iterdir():
            if file_path.is_file():
                stats = file_path.stat()
                files.append({
                    'name': file_path.name,
                    'path': str(file_path),
                    'size': stats.st_size,
                    'modified': stats.st_mtime,
                })
        
        return files
    
    def supports_protocol(self, uri: str) -> bool:
        """Check if protocol is supported."""
        return uri.startswith('file://') or not '://' in uri
