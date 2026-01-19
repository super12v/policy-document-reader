"""CSV document parser."""
from pathlib import Path
from typing import Dict, Any
import pandas as pd
from src.services.parsers.base import BaseParser
from src.utils.logger import logger
from src.utils.errors import DocumentParseError


class CSVParser(BaseParser):
    """Parse CSV files."""
    
    async def parse(self, file_path: Path) -> Dict[str, Any]:
        """Parse CSV document."""
        try:
            logger.info(f"Parsing CSV: {file_path.name}")
            
            # Read CSV
            df = pd.read_csv(file_path)
            
            # Convert to readable format
            content = df.to_string(index=False)
            
            metadata = {
                'rows': len(df),
                'columns': list(df.columns),
                'column_count': len(df.columns),
            }
            
            return {
                'content': content,
                'metadata': metadata,
                'format': 'csv'
            }
            
        except Exception as e:
            logger.error(f"Failed to parse CSV {file_path}: {e}")
            raise DocumentParseError(f"CSV parse error: {e}")
    
    def supports_format(self, file_extension: str) -> bool:
        """Check if format is supported."""
        return file_extension.lower() in ['.csv']
