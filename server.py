from fastmcp.server import FastMCP 
from fastmcp.server.auth import BearerAuthProvider
import tools
from fastapi import FastAPI
from customListingMiddleware import CustomListingMiddleware
import jwt
from dotenv import load_dotenv, dotenv_values

load_dotenv()
CONFIG = dotenv_values(".env")

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



mcp = MCPServer()
mcp_app = mcp.get_app()
app = FastAPI(lifespan=mcp_app.lifespan)
app.mount("/mcp", mcp_app)

@app.get("/jwt/{agentName}")
def generateJwt(agentName):
    payload = {
        "agentName": agentName,
        "scopes": ["tools:add", "tools:subtract", "tools:divide"]
    }

    token = jwt.encode(payload, CONFIG["SECRET"], algorithm="HS256")
    return token

@app.get("/url-list")
def get_all_urls():
    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
    return url_list