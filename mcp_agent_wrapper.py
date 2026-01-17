"""
MCP Agent Wrapper - Connects OpenAI Agent with Blender MCP Server
"""
import sys
import asyncio
import json
from typing import Any, Dict, List
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI
from tool_definitions import BLENDER_TOOLS


class BlenderServer:
    """Configuration for Blender MCP server"""
    command = sys.executable
    args = ["blender_mcp_launcher.py"]
    env = None
    cwd = None
    encoding = "utf-8"
    encoding_error_handler = "replace"


class BlenderMCPAgent:
    """Agentic AI wrapper for Blender MCP tools"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.mcp_session = None
        self.conversation_history = []
        
        # System prompt for the agent
        self.system_prompt = """You are a professional 2D animation assistant using Blender.

Your capabilities:
- Create 2D shapes and animations using mesh objects
- Set up cameras and scenes for 2D work
- Animate objects with keyframes
- Configure rendering settings
- Render animations to MP4 video files automatically
- Save and manage Blender files

IMPORTANT: For 2D animations, ALWAYS use mesh-based tools (create_2d_circle, create_2d_rectangle) instead of Grease Pencil tools, as they work reliably across all Blender versions including 4.0+.

When creating animations:
1. Always start by clearing the scene with clear_scene()
2. Set up a 2D camera with setup_2d_camera() - use appropriate ortho_scale (8-15 for most scenes)
3. Create shapes using create_2d_circle() or create_2d_rectangle()
4. Apply materials with set_object_material() to add colors
5. Animate using animate_object_location() with keyframe data
6. Set animation range with set_animation_range()
7. Optionally set background color with set_background_color()
8. Add lighting with add_light() for better visibility in renders
9. Save the file with save_file()

For rendering to MP4 video:
1. After creating the animation, call set_render_settings() with format='MP4'
2. Specify a full path with .mp4 extension (e.g., 'C:/Users/Username/Videos/animation.mp4')
3. Then call render_animation() to start the render
4. The video will be saved automatically to the specified path

For bouncing ball animations:
- Start ball high (y = 2 to 4)
- Platform at y = -2 to -3
- Use keyframes to create bounce motion (ball should reach platform level minus ball radius)
- Typical animation: 48 frames at 24fps = 2 seconds

Example keyframes for bouncing ball at [0, 3, 0]:
- Frame 1: [0, 3, 0] (start)
- Frame 12: [0, -1.5, 0] (hit platform)
- Frame 24: [0, 2, 0] (bounce up)
- Frame 36: [0, -1.5, 0] (second bounce)
- Frame 48: [0, 1, 0] (smaller bounce)

Common render settings:
- Resolution: 1920x1080 for Full HD, 1280x720 for HD
- FPS: 24 for cinematic, 30 for smooth video
- Format: 'MP4' for video files, 'PNG' for image sequences

Always provide clear feedback about what you're doing and inform the user when rendering starts and where the output will be saved.
"""
    
    async def __aenter__(self):
        """Initialize MCP connection"""
        self.stdio_context = stdio_client(BlenderServer)
        self.read, self.write = await self.stdio_context.__aenter__()
        
        self.session_context = ClientSession(self.read, self.write)
        self.mcp_session = await self.session_context.__aenter__()
        
        await self.mcp_session.initialize()
        print("✅ Connected to Blender MCP Server\n")
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup MCP connection"""
        if self.session_context:
            await self.session_context.__aexit__(exc_type, exc_val, exc_tb)
        if self.stdio_context:
            await self.stdio_context.__aexit__(exc_type, exc_val, exc_tb)
    
    async def call_blender_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Execute a Blender MCP tool"""
        try:
            result = await self.mcp_session.call_tool(tool_name, arguments=arguments)
            
            # Extract text from result
            if hasattr(result, 'content') and len(result.content) > 0:
                return result.content[0].text
            return str(result)
            
        except Exception as e:
            return f"Error calling {tool_name}: {str(e)}"
    
    async def process_tool_calls(self, tool_calls: List) -> List[Dict]:
        """Process OpenAI tool calls and execute them via MCP"""
        results = []
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            print(f"🔧 Calling: {function_name}({json.dumps(arguments, indent=2)})")
            
            # Execute the tool via MCP
            result = await self.call_blender_tool(function_name, arguments)
            print(f"   ✓ {result}\n")
            
            results.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": result
            })
        
        return results
    
    async def chat(self, user_message: str) -> str:
        """Send a message to the agent and get a response"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare messages with system prompt
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history
        
        # Call OpenAI with tools
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=BLENDER_TOOLS,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        
        # Handle tool calls
        while assistant_message.tool_calls:
            # Add assistant message with tool calls to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            })
            
            # Execute tools
            tool_results = await self.process_tool_calls(assistant_message.tool_calls)
            
            # Add tool results to history
            self.conversation_history.extend(tool_results)
            
            # Get next response
            messages = [
                {"role": "system", "content": self.system_prompt}
            ] + self.conversation_history
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=BLENDER_TOOLS,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
        
        # Add final assistant message to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message.content
        })
        
        return assistant_message.content
