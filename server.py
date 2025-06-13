import os
from mcp.server.fastmcp import FastMCP
import tools

mcp = FastMCP("My MCP Server")
tools.register_all_tools(mcp)

if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT")
    if transport:
        mcp.run(transport=transport)
    else:
        mcp.run()