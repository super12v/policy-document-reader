"""Base parser interface."""
from abc import ABC, abstractmethod
from typing import Dict, Any
from pathlib import Path


class BaseParser(ABC):
    """Base document parser interface."""
    
    @abstractmethod
    async def parse(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse document and extract content.
        
        Args:
            file_path: Path to document file
            
        Returns:
            Dictionary containing:
                - content: Extracted text content
                - metadata: Document metadata (author, date, etc.)
        """
        pass
    
    @abstractmethod
    def supports_format(self, file_extension: str) -> bool:
        """Check if parser supports this format."""
        pass
