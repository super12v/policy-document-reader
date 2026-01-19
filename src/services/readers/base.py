"""Base source reader interface."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pathlib import Path


class BaseReader(ABC):
    """Base document source reader interface."""
    
    @abstractmethod
    async def read_file(self, path: str, credentials: Dict[str, Any]) -> Path:
        """
        Read file from source and return local path.
        
        Args:
            path: Source path (URL, UNC path, etc.)
            credentials: Authentication credentials
            
        Returns:
            Local file path where file was downloaded
        """
        pass
    
    @abstractmethod
    async def list_files(self, path: str, credentials: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        List files in directory/location.
        
        Args:
            path: Directory path
            credentials: Authentication credentials
            
        Returns:
            List of file metadata dictionaries
        """
        pass
    
    @abstractmethod
    def supports_protocol(self, uri: str) -> bool:
        """Check if reader supports this protocol."""
        pass
