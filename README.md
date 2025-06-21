# MCP SERVER

## What it is
This is an MCP server made for the IDSL agentic ecosystem

## How to run it
To run it, run these commands

**Windows**
```
> python -m venv .venv
> .venv\Scripts\Activate
> pip install -r requirements.txt
> uvicorn server:app --reload --host 127.0.0.1 --port 8000
```

**Linux/Mac**
```
> python -m venv .venv
> source .venv\bin\activate
> pip install -r requirements.txt
> uvicorn server:app --reload --host 127.0.0.1 --port 8000
```

## How to add tools
To add tools, create a new python script in the tools.py. Import the following dependency
```
from mcp.server.fastmcp import FastMCP
```

Then, define a register_tools function with the signature defined below:
```
def register_tools(mcp: FastMCP):
```

Create the functions that you wish to be tools, and give them a docstring explaining the functionality, the arguments, and the returns. Then, annotate the functions with `@mcp.tool`. 
