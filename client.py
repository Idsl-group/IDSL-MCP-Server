import asyncio
import nest_asyncio
from mcp import ClientSession
from fastmcp import Client
nest_asyncio.apply()  

client = Client("http://localhost:8000/mcp")
async def main():
    async with client:
        tools = await client.list_tools()
        for tool in tools:
            print(f"=============== {tool.name} ===============\n- Description: {tool.description}\n")
        print("\n\n\n\n\n")
        result = await client.call_tool("add", arguments={"a": 5, "b": 3})
        print("\n\n\n\n\n")
        print(f"Result of add tool: {result[0].text}")

if __name__ == "__main__":
    asyncio.run(main())