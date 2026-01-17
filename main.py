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

            # List available tools
            tools = await session.list_tools()
            print(f"\n📋 Available tools: {[t.name for t in tools.tools]}")

            # Clear the scene
            print("\n🧹 Clearing scene...")
            result = await session.call_tool("clear_scene", arguments={})
            print(f"   {result.content[0].text}")

            # Add a cube
            print("\n📦 Adding cube with size 5.0...")
            result = await session.call_tool("add_cube", arguments={"size": 5.0})
            print(f"   {result.content[0].text}")

            # Save the file
            output_path = "C:\\Development\\Ai-agents\\blender-mcp\\output.blend"
            print(f"\n💾 Saving scene to {output_path}...")
            result = await session.call_tool("save_file", arguments={"filepath": output_path})
            print(f"   {result.content[0].text}")
            
            print("\n✅ Done! You can now open output.blend in Blender to see the result.")



asyncio.run(main())
