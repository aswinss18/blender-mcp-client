import bpy
from mcp.server.fastmcp import FastMCP

# Create MCP server inside Blender
mcp = FastMCP("Blender MCP Server")

@mcp.tool()
def clear_scene():
    """Delete all objects in the current scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    return "Scene cleared"

@mcp.tool()
def add_cube(size: float = 2.0):
    """Add a cube to the scene"""
    bpy.ops.mesh.primitive_cube_add(size=size)
    return f"Cube added with size {size}"

# IMPORTANT:
# - No print()
# - No logging
# - Only MCP JSON goes to stdout
if __name__ == "__main__":
    mcp.run()
