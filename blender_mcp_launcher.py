import subprocess
import sys
import os

BLENDER_EXE = r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"

args = [
    BLENDER_EXE,
    "--background",
    "--factory-startup",
    "--noaudio",
    "--python",
    "blender_mcp_server.py",
]

# IMPORTANT:
# stdout → stderr
# so MCP sees ONLY JSON from Python MCP server
process = subprocess.Popen(
    args,
    stdout=sys.stderr,
    stderr=sys.stderr,
)

process.wait()
sys.exit(process.returncode)
