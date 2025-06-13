from mcp.server.fastmcp import FastMCP

def register_tools(mcp: FastMCP):
    """Register tools with the MCP server."""
    @mcp.tool()
    def echo_tool(message: str) -> str:
        """Echo a message"""
        return f"Echo: {message}"
