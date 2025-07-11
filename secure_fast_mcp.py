from fastmcp.server import FastMCP
from fastmcp.server.dependencies import get_access_token, AccessToken
from mcp.types import Tool
from typing import List, Optional, Any
from fastapi import HTTPException
from fastmcp.tools.tool import Tool
import jwt
import logging
logging.basicConfig(level=logging.INFO)

class SecureFastMCP(FastMCP):
    async def list_tools(self) -> List[Tool]:
        logging.info("list_tools called")

        try:
            access_token: AccessToken = get_access_token()
            token = access_token.token
            logging.info(f"Token from access_token: {token}")
            
            all_tools = await super().list_tools()
            logging.info("All available tools:", [tool.name for tool in all_tools])
            
            authorized_tools = [
                tool for tool in all_tools if check_scope(tool.name, token)
            ]
            logging.info("Returning tools:", [tool.name for tool in authorized_tools])
            return authorized_tools
            
        except Exception as e:
            logging.info(f"Error in list_tools: {e}")
            return []

    async def call_tool(self, key: str, arguments: dict[str, Any], context: Optional[dict] = None):
        print(f"call_tool invoked for '{key}'")
        print("Context:", context)

        token = context.get("access_token") if context else None
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")

        if not check_scope(key, token):
            raise HTTPException(status_code=403, detail=f"Tool '{key}' is not authorized for your token")

        return await super().call_tool(key, arguments)

def check_scope(tool_name: str, token: str) -> bool:
    print(f"check_scope called for tool '{tool_name}'")
    print(f"Raw token: {token}")

    try:
        payload = jwt.decode(token, "your_secret", algorithms=["HS256"])
        print("Decoded payload:", payload)

        scopes = payload.get("scopes", []) 
        print(f"Allowed scopes from token: {scopes}")

        authorized = tool_name in scopes
        print(f"Is tool '{tool_name}' authorized? {authorized}")
        return authorized

    except jwt.PyJWTError as e:
        print("Token decode failed:", str(e))
        return False