import subprocess
import sys
import os
import json

BLENDER_EXE = r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"

args = [
    BLENDER_EXE,
    "--background",
    "--factory-startup",
    "--log-level", "0",
    "--python",
    "blender_mcp_server.py",
]

# Start Blender process
process = subprocess.Popen(
    args,
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,  # Discard Blender's stderr
    text=True,
    bufsize=1,
)

# Filter and forward only JSON-RPC messages
try:
    for line in process.stdout:
        line = line.strip()
        if line:
            # Try to parse as JSON - only forward valid JSON
            try:
                json.loads(line)
                print(line, flush=True)
            except json.JSONDecodeError:
                # Skip non-JSON lines (Blender startup messages)
                pass
except KeyboardInterrupt:
    process.terminate()

process.wait()
sys.exit(process.returncode)
