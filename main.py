import sys
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client


class BlenderServer:
    # Use the current Python (uv) to run the launcher
    command = sys.executable
    args = ["blender_mcp_launcher.py"]

    env = None
    cwd = None
    encoding = "utf-8"
    encoding_error_handler = "replace"


async def main():
    async with stdio_client(BlenderServer) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ Connected to Blender MCP")

            tools = await session.list_tools()
            print("Tools:", tools)

            result = await session.call_tool(
                "add_cube",
                arguments={"size": 3}
            )
            print(result)


asyncio.run(main())
