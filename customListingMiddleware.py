from fastmcp.server.middleware import Middleware, MiddlewareContext, ListToolsResult
import logging
from fastmcp.server.dependencies import get_access_token, AccessToken
from scope import check_scope

logging.basicConfig(level=logging.INFO)

class CustomListingMiddleware(Middleware):
    async def on_list_tools(self, context: MiddlewareContext, call_next):
        all_tools = await call_next(context)  
        
        logging.info("list_tools called")
        try:
            access_token: AccessToken = get_access_token()
            token = access_token.token
            logging.info(f"Token from access_token: {token}")

            
            tool_names = [tool.name for tool in all_tools]
            logging.info(f"All available tools: {tool_names}")

            authorized_tools = [
                tool for tool in all_tools
                if check_scope(tool.name, token)
            ]

            logging.info(f"Returning tools: {authorized_tools}")
            logging.info(f"List Tools Result: {ListToolsResult(tools=authorized_tools)}")
            return authorized_tools

        except Exception as e:
            logging.error(f"Error in list_tools: {e}")
            return ListToolsResult(tools={})
