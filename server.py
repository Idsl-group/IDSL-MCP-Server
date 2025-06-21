from mcp.server.fastmcp import FastMCP
import tools

# Creating FastMCP Instance
mcp = FastMCP(name="IDSL MCP Server")

# Registering tools on the FastMCP instance
tools.register_all_tools(mcp)

# Running the FastMCP Server with a transport type of streamable-http
app = mcp.streamable_http_app()
