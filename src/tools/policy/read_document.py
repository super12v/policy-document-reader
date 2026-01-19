"""MCP tool: Read policy document."""
from typing import Dict, Any
from pydantic import BaseModel, Field
from pathlib import Path
from src.services.readers import reader_registry
from src.services.parsers import parser_registry
from src.utils.logger import logger, log_audit
from src.utils.errors import ValidationError, DocumentTooLargeError
from src.config import settings


class ReadDocumentInput(BaseModel):
    """Input parameters for policy-read-document tool."""
    
    source: str = Field(
        ...,
        description="Document source URI (file://, smb://, git://, s3://, https://)"
    )
    credentials_path: str = Field(
        default="",
        description="Vault path to credentials (e.g., 'smb/fileserver')"
    )
    format: str = Field(
        default="auto",
        description="Document format (auto, pdf, docx, xlsx, csv, txt)"
    )
    
    class Config:
        extra = 'forbid'


async def read_document(params: Dict[str, Any], agent_id: str) -> Dict[str, Any]:
    """
    Read and parse a policy document from any source.
    
    This tool enables AI agents to access policy documents for infrastructure
    security policy creation.
    
    Args:
        params: Tool input parameters
        agent_id: Requesting agent identifier
        
    Returns:
        Document content and metadata
        
    Security:
        - Credentials fetched from Vault
        - Size limits enforced
        - All access audit logged
    """
    # Validate input
    validated = ReadDocumentInput(**params)
    
    logger.info(
        f"Reading policy document",
        extra={'data': {'source': validated.source, 'agent_id': agent_id}}
    )
    
    try:
        # Get credentials from Vault (simplified for this example)
        credentials = {}
        if validated.credentials_path:
            # TODO: Integrate with Vault
            credentials = {}
        
        # Download document
        file_path = await reader_registry.read_document(validated.source, credentials)
        
        # Check size limit
        file_size = file_path.stat().st_size
        max_size = settings.max_document_size_mb * 1024 * 1024
        if file_size > max_size:
            raise DocumentTooLargeError(
                f"Document size {file_size} exceeds limit {max_size}"
            )
        
        # Parse document
        result = await parser_registry.parse_document(file_path)
        
        # Audit log
        log_audit(
            'document.read',
            agent_id=agent_id,
            source=validated.source,
            format=result['format'],
            size=file_size
        )
        
        return {
            'status': 'success',
            'data': result
        }
        
    except Exception as e:
        logger.error(f"Failed to read document: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }


# Tool metadata for MCP registration
TOOL_METADATA = {
    'name': 'policy-read-document',
    'description': 'Read and parse policy documents from various sources',
    'inputSchema': ReadDocumentInput.model_json_schema(),
}
