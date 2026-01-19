"""PDF document parser."""
from pathlib import Path
from typing import Dict, Any
import pdfplumber
from src.services.parsers.base import BaseParser
from src.utils.logger import logger
from src.utils.errors import DocumentParseError


class PDFParser(BaseParser):
    """Parse PDF documents."""
    
    async def parse(self, file_path: Path) -> Dict[str, Any]:
        """Parse PDF document."""
        try:
            logger.info(f"Parsing PDF: {file_path.name}")
            
            content = []
            metadata = {}
            
            with pdfplumber.open(file_path) as pdf:
                # Extract metadata
                metadata = {
                    'pages': len(pdf.pages),
                    'metadata': pdf.metadata or {},
                }
                
                # Extract text from each page
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        content.append(f"[Page {page_num}]\n{text}")
            
            return {
                'content': '\n\n'.join(content),
                'metadata': metadata,
                'format': 'pdf'
            }
            
        except Exception as e:
            logger.error(f"Failed to parse PDF {file_path}: {e}")
            raise DocumentParseError(f"PDF parse error: {e}")
    
    def supports_format(self, file_extension: str) -> bool:
        """Check if format is supported."""
        return file_extension.lower() in ['.pdf']
