"""Excel document parser."""
from pathlib import Path
from typing import Dict, Any
import pandas as pd
from src.services.parsers.base import BaseParser
from src.utils.logger import logger
from src.utils.errors import DocumentParseError


class ExcelParser(BaseParser):
    """Parse Excel spreadsheets."""
    
    async def parse(self, file_path: Path) -> Dict[str, Any]:
        """Parse Excel document."""
        try:
            logger.info(f"Parsing Excel: {file_path.name}")
            
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            sheets_content = []
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                
                # Convert to readable format
                sheet_content = f"[Sheet: {sheet_name}]\n"
                sheet_content += df.to_string(index=False)
                sheets_content.append(sheet_content)
            
            metadata = {
                'sheets': excel_file.sheet_names,
                'sheet_count': len(excel_file.sheet_names),
            }
            
            return {
                'content': '\n\n'.join(sheets_content),
                'metadata': metadata,
                'format': 'xlsx'
            }
            
        except Exception as e:
            logger.error(f"Failed to parse Excel {file_path}: {e}")
            raise DocumentParseError(f"Excel parse error: {e}")
    
    def supports_format(self, file_extension: str) -> bool:
        """Check if format is supported."""
        return file_extension.lower() in ['.xlsx', '.xls']
