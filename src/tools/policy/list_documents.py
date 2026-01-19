"""MCP tool: List policy documents."""
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from src.services.readers import reader_registry
from src.utils.logger import logger, log_audit


class ListDocumentsInput(BaseModel):
    """Input parameters for policy-list-documents tool."""
    
    source: str = Field(
        ...,
        description="Directory/location URI (file://, smb://, git://, s3://)"
    )
    credentials_path: str = Field(
        default="",
        description="Vault path to credentials"
    )
    pattern: str = Field(
        default="*",
        description="File pattern filter (e.g., '*.pdf')"
    )
    
    class Config:
        extra = 'forbid'


async def list_documents(params: Dict[str, Any], agent_id: str) -> Dict[str, Any]:
    """
    List available policy documents at a location.
    
    Args:
        params: Tool input parameters
        agent_id: Requesting agent identifier
        
    Returns:
        List of available documents with metadata
    """
    # Validate input
    validated = ListDocumentsInput(**params)
    
    logger.info(
        f"Listing policy documents",
        extra={'data': {'source': validated.source, 'agent_id': agent_id}}
    )
    
    try:
        # Get credentials from Vault
        credentials = {}
        if validated.credentials_path:
            # TODO: Integrate with Vault
            credentials = {}
        
        # List documents
        files = await reader_registry.list_documents(validated.source, credentials)
        
        # Filter by pattern
        if validated.pattern != "*":
            import fnmatch
            files = [f for f in files if fnmatch.fnmatch(f['name'], validated.pattern)]
        
        # Audit log
        log_audit(
            'documents.listed',
            agent_id=agent_id,
            source=validated.source,
            count=len(files)
        )
        
        return {
            'status': 'success',
            'data': {
                'files': files,
                'count': len(files)
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to list documents: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }


# Tool metadata for MCP registration
TOOL_METADATA = {
    'name': 'policy-list-documents',
    'description': 'List available policy documents at a location',
    'inputSchema': ListDocumentsInput.model_json_schema(),
}
