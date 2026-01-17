import sys
import site
import os

# Add user site-packages to path so Blender can find mcp
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.insert(0, user_site)

# Add all pywin32 directories to sys.path for pywintypes
win32_dir = os.path.join(user_site, "win32")
win32lib_dir = os.path.join(user_site, "win32", "lib")
pywin32_dll_dir = os.path.join(user_site, "pywin32_system32")

# Add all pywin32 paths
for path in [win32_dir, win32lib_dir, pywin32_dll_dir]:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)

# Add pywin32 DLL directory to PATH and DLL search path
if os.path.exists(pywin32_dll_dir):
    os.environ["PATH"] = pywin32_dll_dir + os.pathsep + os.environ.get("PATH", "")
    if hasattr(os, 'add_dll_directory'):
        os.add_dll_directory(pywin32_dll_dir)
    
    # Preload the DLLs using ctypes
    import ctypes
    try:
        pywintypes_dll = os.path.join(pywin32_dll_dir, "pywintypes311.dll")
        if os.path.exists(pywintypes_dll):
            ctypes.WinDLL(pywintypes_dll)
        pythoncom_dll = os.path.join(pywin32_dll_dir, "pythoncom311.dll")
        if os.path.exists(pythoncom_dll):
            ctypes.WinDLL(pythoncom_dll)
    except Exception:
        pass  # If preloading fails, continue anyway

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

@mcp.tool()
def save_file(filepath: str):
    """Save the current Blender scene to a file"""
    bpy.ops.wm.save_as_mainfile(filepath=filepath)
    return f"Scene saved to {filepath}"

# IMPORTANT:
# - No print()
# - No logging
# - Only MCP JSON goes to stdout
if __name__ == "__main__":
    mcp.run()
