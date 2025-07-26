from fastmcp.server import FastMCP 
from fastmcp.server.auth import BearerAuthProvider
import tools
from fastapi import FastAPI, Query
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
            public_key=CONFIG["SECRET"]
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
app = FastAPI(title="IDSL Server", lifespan=mcp_app.lifespan)
app.mount("/mcp", mcp_app, name="mcp_app")

@app.get("/jwt")
def generate_jwt(
    agentName: str = Query(description="Name of the agent"),
    tools: list[str] = Query( 
        alias="tools", 
        description="List of tool names you want scopes for"
        )
    ):
    """
    Example request:
      GET /jwt?agentName=HadiAgent&tools=add&tools=subtract&tools=divide
    """
    scopes = [f"tools:{t}" for t in tools]

    payload = {
        "agentName": agentName,
        "scopes": scopes
    }

    token = jwt.encode(payload, CONFIG["SECRET"], algorithm="HS256")
    return {"token": token}

@app.get("/url-list")
def get_all_urls():
    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
    return url_list