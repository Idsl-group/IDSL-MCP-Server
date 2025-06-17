from mcp.server.fastmcp import FastMCP
import tools

mcp = FastMCP("IDSL MCP Server")

tools.register_all_tools(mcp)

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http"
    )
