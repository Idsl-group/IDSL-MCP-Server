from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

app.get("/")
async def root():
    return {"message":"MCP Server is running!"}

app.get("/add", operation_id="add_numbers")
def add_numbers(a: int, b: int):
    """
    Adds two numbers together.
    """
    return {"result": a + b}

mcp = FastApiMCP(
    app,
    name="IDSL MCP Server",
    include_operations="add_numbers"
    )
mcp.mount()

