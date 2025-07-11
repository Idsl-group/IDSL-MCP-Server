from fastmcp.server import FastMCP 
from fastmcp.server.auth import BearerAuthProvider
import tools
from fastapi import FastAPI
from customListingMiddleware import CustomListingMiddleware

class MCPServer:
    def __init__(self, name: str = "IDSL MCP Server"):
        print(f"Initializing MCP Server with name: {name}")

        auth = BearerAuthProvider(
            algorithm="HS256",
            public_key="your_secret"
        )

        self.name = name
        self.mcp = FastMCP(
            name=self.name,
            auth=auth
        )
        self.mcp.add_middleware(CustomListingMiddleware())
        self._register_tools()

    def _register_tools(self):
        print("Registering tools...")
        tools.register_all_tools(self.mcp)

    def get_app(self) -> FastAPI:
        app = self.mcp.http_app()
        return app



server = MCPServer()
app = server.get_app()

