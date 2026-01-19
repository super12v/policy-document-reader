"""Custom exception classes."""
from typing import Optional, Dict, Any


class MCPError(Exception):
    """Base MCP error."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ValidationError(MCPError):
    """Input validation error."""
    pass


class NotFoundError(MCPError):
    """Resource not found error."""
    pass


class UnauthorizedError(MCPError):
    """Authentication/authorization error."""
    pass


class SourceConnectionError(MCPError):
    """Error connecting to document source."""
    pass


class DocumentParseError(MCPError):
    """Error parsing document."""
    pass


class DocumentTooLargeError(MCPError):
    """Document exceeds size limit."""
    pass


class UnsupportedFormatError(MCPError):
    """Unsupported document format."""
    pass
