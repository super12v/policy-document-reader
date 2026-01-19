"""Parser registry and factory."""
from pathlib import Path
from typing import Dict, Any, Optional
from src.services.parsers.base import BaseParser
from src.services.parsers.pdf_parser import PDFParser
from src.services.parsers.docx_parser import DOCXParser
from src.services.parsers.excel_parser import ExcelParser
from src.services.parsers.csv_parser import CSVParser
from src.services.parsers.text_parser import TextParser
from src.utils.errors import UnsupportedFormatError
from src.utils.logger import logger


class ParserRegistry:
    """Registry of document parsers."""
    
    def __init__(self):
        self.parsers: list[BaseParser] = [
            PDFParser(),
            DOCXParser(),
            ExcelParser(),
            CSVParser(),
            TextParser(),
        ]
    
    def get_parser(self, file_extension: str) -> BaseParser:
        """Get parser for file format."""
        for parser in self.parsers:
            if parser.supports_format(file_extension):
                return parser
        raise UnsupportedFormatError(f"No parser for format: {file_extension}")
    
    async def parse_document(self, file_path: Path) -> Dict[str, Any]:
        """Parse document using appropriate parser."""
        extension = file_path.suffix
        logger.info(f"Parsing document: {file_path.name} (format: {extension})")
        
        parser = self.get_parser(extension)
        result = await parser.parse(file_path)
        
        # Add file info
        result['file_name'] = file_path.name
        result['file_path'] = str(file_path)
        result['file_size'] = file_path.stat().st_size
        
        return result


# Global parser registry
parser_registry = ParserRegistry()
