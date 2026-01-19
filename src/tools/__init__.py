"""Tool registry."""
from typing import Dict, Any, Callable
from src.tools.policy import read_document, list_documents


class ToolRegistry:
    """Registry of MCP tools."""
    
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self._register_tools()
    
    def _register_tools(self):
        """Register all available tools."""
        self.register_tool(
            read_document.TOOL_METADATA['name'],
            read_document.read_document,
            read_document.TOOL_METADATA
        )
        
        self.register_tool(
            list_documents.TOOL_METADATA['name'],
            list_documents.list_documents,
            list_documents.TOOL_METADATA
        )
    
    def register_tool(self, name: str, handler: Callable, metadata: Dict[str, Any]):
        """Register a tool."""
        self.tools[name] = {
            'handler': handler,
            'metadata': metadata
        }
    
    def get_tool(self, name: str) -> Dict[str, Any]:
        """Get tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> list[Dict[str, Any]]:
        """List all available tools."""
        return [tool['metadata'] for tool in self.tools.values()]
    
    async def execute_tool(self, name: str, arguments: Dict[str, Any], agent_id: str) -> Dict[str, Any]:
        """Execute a tool."""
        tool = self.get_tool(name)
        if not tool:
            return {
                'status': 'error',
                'error': f'Tool not found: {name}'
            }
        
        handler = tool['handler']
        return await handler(arguments, agent_id)


# Global tool registry
tool_registry = ToolRegistry()
