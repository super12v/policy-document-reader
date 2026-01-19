"""FastAPI application."""
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
from src.config import settings
from src.tools import tool_registry
from src.utils.logger import logger


app = FastAPI(
    title="Policy Document Reader MCP Server",
    description="Read policy documents from multiple sources for AI agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ToolCallRequest(BaseModel):
    """Tool call request."""
    name: str
    arguments: Dict[str, Any]


class ToolListResponse(BaseModel):
    """Tool list response."""
    tools: list[Dict[str, Any]]


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "policy-document-reader",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/api/v1/tools", response_model=ToolListResponse)
async def list_tools():
    """List available MCP tools."""
    tools = tool_registry.list_tools()
    return {"tools": tools}


@app.post("/api/v1/tools/call")
async def call_tool(
    request: ToolCallRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Execute an MCP tool.
    
    Security:
        - Requires JWT token in Authorization header
        - Agent ID extracted from token
    """
    try:
        # Extract agent ID from JWT (simplified)
        agent_id = "agent-123"  # TODO: Extract from JWT token
        
        logger.info(
            f"Tool call: {request.name}",
            extra={'data': {'agent_id': agent_id}}
        )
        
        # Execute tool
        result = await tool_registry.execute_tool(
            request.name,
            request.arguments,
            agent_id
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check for k8s."""
    return {"status": "healthy"}


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    # TODO: Return Prometheus metrics
    return {"status": "metrics_available"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.server_host,
        port=settings.server_port,
        log_level=settings.log_level.lower()
    )
