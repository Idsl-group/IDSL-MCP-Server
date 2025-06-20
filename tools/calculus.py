from mcp.server.fastmcp import FastMCP
import sympy as sp
from typing import Literal

def register_tools(mcp: FastMCP):
    """Register calculus tools with the MCP server."""

    x = sp.Symbol("x") 

    @mcp.tool()
    def derivative(expression: str) -> str:
        """Compute the derivative of an expression with respect to x.

        Args:
            expression: A string like "x**2 + sin(x)"

        Returns:
            The symbolic derivative as a string.
        """
        expr = sp.sympify(expression)
        deriv = sp.diff(expr, x)
        return str(deriv)

    @mcp.tool()
    def indefinite_integral(expression: str) -> str:
        """Compute the indefinite integral of an expression with respect to x.

        Args:
            expression: A string like "x**2 + sin(x)"

        Returns:
            The symbolic indefinite integral as a string.
        """
        expr = sp.sympify(expression)
        integral = sp.integrate(expr, x)
        return str(integral) + " + C"

    @mcp.tool()
    def definite_integral(expression: str, lower: float, upper: float) -> float:
        """Compute the definite integral of an expression from lower to upper.

        Args:
            expression: A string like "x**2 + sin(x)"
            lower: The lower limit of integration
            upper: The upper limit of integration

        Returns:
            The numeric result of the definite integral.
        """
        expr = sp.sympify(expression)
        result = sp.integrate(expr, (x, lower, upper))
        return float(result)
