from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

print("Loading environment...")
load_dotenv("../.env")
print("Importing tools...")
import tools

print("Creating FastMCP instance...")
mcp = FastMCP(
    name="IDSL MCP Server",
)

print("Registering tools...")
tools.register_all_tools(mcp)
print("Tools registered!")

mcp.run(transport="streamable-http")