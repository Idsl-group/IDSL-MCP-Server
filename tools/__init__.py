import importlib
import pkgutil
from mcp.server.fastmcp import FastMCP

def register_all_tools(mcp: FastMCP) -> None:
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{__name__}.{module_name}")
        if hasattr(module, 'register_tools'):
            module.register_tools(mcp)