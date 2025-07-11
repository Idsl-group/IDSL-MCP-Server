from mcp.server.fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token
import jwt


def register_tools(mcp: FastMCP):
    """Register calculator tools with the MCP server."""
    
    @mcp.tool()
    def add(a: float, b: float) -> float:
        """
        Add two numbers.
        
        Args:
            a: The first number.
            b: The second number.

        Returns:
            The sum of the two numbers.
        """
        access_token = get_access_token()
        decoded = jwt.decode(access_token.token, "your_secret", algorithms=["HS256"])
        if "tools:add" not in decoded.get("scopes", []):
            raise RuntimeError("Unauthorized: missing 'add' scope")
        return a + b

    @mcp.tool()
    def subtract(a: float, b: float) -> float:
        """
        Subtract two numbers.

        Args:
            a: The first number to be subtracted
            b: The second number to be subtracted
        
            Returns:
                The difference of the two numbers
        
        """

        access_token = get_access_token()
        decoded = jwt.decode(access_token.token, "your_secret", algorithms=["HS256"])
        if "tools:subtract" not in decoded.get("scopes", []):
            raise RuntimeError("Unauthorized: missing 'subtract' scope")
        return a - b

    @mcp.tool()
    def multiply(a: float, b: float) -> float:
        """
        Multiply two numbers
        
        Args: 
            a: The first number to be multiplied
            b: The second number to be multiplied

        Returns:
            The product of the two numbers
        """
        access_token = get_access_token()
        decoded = jwt.decode(access_token.token, "your_secret", algorithms=["HS256"])
        if "tools:multiply" not in decoded.get("scopes", []):
            raise RuntimeError("Unauthorized: missing 'multiply' scope")
        return a * b

    @mcp.tool()
    def divide(a: float, b: float) -> float:
        """
        Divide two numbers.
        
        Args:
            a: The numerator
            b: The denominator
        
        Returns:
            The quotient of the two numbers        
        """
        access_token = get_access_token()
        decoded = jwt.decode(access_token.token, "your_secret", algorithms=["HS256"])
        if "tools:divide" not in decoded.get("scopes", []):
            raise RuntimeError("Unauthorized: missing 'divide' scope")
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b