from mcp.server.fastmcp import FastMCP

def register_tools(mcp: FastMCP):
    """Register calculator tools with the MCP server."""
    
    @mcp.tool()
    def add(a: float, b: float) -> float:
        """Add two numbers."""
        return a + b

    @mcp.tool()
    def subtract(a: float, b: float) -> float:
        """Subtract two numbers."""
        return a - b

    @mcp.tool()
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b

    @mcp.tool()
    def divide(a: float, b: float) -> float:
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b