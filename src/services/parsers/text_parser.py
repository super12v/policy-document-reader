"""Text document parser."""
from pathlib import Path
from typing import Dict, Any
import aiofiles
from src.services.parsers.base import BaseParser
from src.utils.logger import logger
from src.utils.errors import DocumentParseError


class TextParser(BaseParser):
    """Parse plain text and markdown files."""
    
    async def parse(self, file_path: Path) -> Dict[str, Any]:
        """Parse text document."""
        try:
            logger.info(f"Parsing text file: {file_path.name}")
            
            # Read file content
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            # Get file stats
            stats = file_path.stat()
            
            metadata = {
                'size_bytes': stats.st_size,
                'lines': len(content.splitlines()),
                'encoding': 'utf-8',
            }
            
            return {
                'content': content,
                'metadata': metadata,
                'format': file_path.suffix.lstrip('.')
            }
            
        except Exception as e:
            logger.error(f"Failed to parse text {file_path}: {e}")
            raise DocumentParseError(f"Text parse error: {e}")
    
    def supports_format(self, file_extension: str) -> bool:
        """Check if format is supported."""
        return file_extension.lower() in ['.txt', '.md', '.markdown', '.json', '.yaml', '.yml']
