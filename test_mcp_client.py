import asyncio
import sys
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession


async def test():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Tools from MCP Server:", [t.name for t in tools.tools])
            res = await session.call_tool("add", {"a": 10, "b": 25})
            print("Call tool add(10, 25):", res.content[0].text)
            res2 = await session.call_tool("multiply", {"a": 6, "b": 7})
            print("Call tool multiply(6, 7):", res2.content[0].text)


if __name__ == "__main__":
    asyncio.run(test())

