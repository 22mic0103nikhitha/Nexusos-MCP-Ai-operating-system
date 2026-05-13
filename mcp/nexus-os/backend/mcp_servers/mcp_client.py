from mcp.client.stdio import stdio_client
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters
import asyncio
import sys

async def run():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_servers/filesystem_server.py"]
    )

    async with stdio_client(server_params) as streams:
        async with ClientSession(
            streams[0],
            streams[1]
        ) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Discovered tools:", tools)

            result = await session.call_tool(
                "list_files",
                arguments={"path": "."}
            )
            print("Tool result:", result)

if __name__ == "__main__":
    asyncio.run(run())
