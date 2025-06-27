import asyncio
import json
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional

import nest_asyncio
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from openai import AsyncOpenAI

nest_asyncio.apply()
load_dotenv()


class MCPOpenAIClient:
    """Client for interacting with OpenAI models using MCP tools."""

    def __init__(self, model: str = "gpt-4o"):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai_client = AsyncOpenAI()
        self.model = model
        self.stdio: Optional[Any] = None
        self.write: Optional[Any] = None
        self.available_tools: List[Dict[str, Any]] = []
        self.excluded_tools: set = set()
        self.chat_history: List[Dict[str, str]] = []

    async def connect_to_server(self, server_script_path: str = "server.py"):
        """Connect to an MCP server."""
        url = "http://127.0.0.1:8000/mcp"
        http_transport = await self.exit_stack.enter_async_context(
            streamablehttp_client(url)
        )
        self.stdio, self.write, _ = http_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        tools_result = await self.session.list_tools()
        self.available_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            for tool in tools_result.tools
        ]
        print("\nConnected to server with tools:")
        for tool in tools_result.tools:
            print(f"  - {tool.name}: {tool.description}")
        self.reconfigure_tools()

    def reconfigure_tools(self) -> None:
        """Prompt user to update tool exclusion list."""
        print("\nAvailable tools:")
        for tool in self.available_tools:
            print(f"- {tool['function']['name']}")
        res = input("Enter tool names to EXCLUDE (comma-separated), or leave blank for none: ")
        self.excluded_tools = {tool.strip() for tool in res.split(",") if tool.strip()}

    def get_specific_tools(self) -> List[Dict[str, Any]]:
        if not self.excluded_tools:
            return self.available_tools
        return [
            tool
            for tool in self.available_tools
            if tool["function"]["name"] not in self.excluded_tools
        ]

    async def process_query(self, query: str) -> str:
        """Process a user query with persistent memory."""
        tools = self.get_specific_tools()
        self.chat_history.append({"role": "user", "content": query})

        response = await self.openai_client.chat.completions.create(
            model=self.model,
            messages=self.chat_history,
            tools=tools,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message
        self.chat_history.append(assistant_message)

        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                print(f"\nUsing tool: `{tool_name}` with arguments:\n{json.dumps(arguments, indent=2)}")
                result = await self.session.call_tool(tool_name, arguments=arguments)
                print(f"Tool `{tool_name}` returned:\n{result.content[0].text}")

                self.chat_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result.content[0].text,
                })

            final_response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=self.chat_history,
                tools=tools,
                tool_choice="none",
            )

            final_msg = final_response.choices[0].message
            self.chat_history.append(final_msg)
            return final_msg.content

        return assistant_message.content

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    client = MCPOpenAIClient()
    await client.connect_to_server("server.py")

    while True:
        query = input("\nEnter your query (or type RECONFIGURE / RESET / QUIT): ").strip()

        if query.upper() == "QUIT":
            break
        elif query.upper() == "RESET":
            client.chat_history = []
            print("Chat history cleared.")
            continue
        elif query.upper() == "RECONFIGURE":
            client.reconfigure_tools()
            continue

        response = await client.process_query(query)
        print(f"\nResponse: {response}")


if __name__ == "__main__":
    asyncio.run(main())
