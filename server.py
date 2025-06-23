from mcp.server.fastmcp import FastMCP
import tools

class MCPServer:
    def __init__(self, name: str = "IDSL MCP Server"):
        self.name = name
        self.mcp = FastMCP(name=self.name)
        self._register_tools()

    def _register_tools(self):
        tools.register_all_tools(self.mcp)

    def get_app(self):
        return self.mcp.streamable_http_app()

server = MCPServer()
app = server.get_app()
