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
        self.system_prompt = """You are a professional 2D animation assistant using Blender's Grease Pencil system.

Your capabilities:
- Create 2D drawings and animations
- Set up cameras and scenes for 2D work
- Animate objects with keyframes
- Configure rendering settings
- Save and manage Blender files

When creating animations:
1. Always start by clearing the scene
2. Set up a 2D camera with appropriate ortho_scale
3. Create Grease Pencil objects for drawing
4. Add materials with colors before drawing
5. Draw strokes with appropriate point coordinates
6. Set animation range based on the desired duration
7. Save the file with a descriptive name

For shapes:
- Circle: Use 16-32 points in a circular pattern (x = cos(angle), y = sin(angle))
- Square: 4 corner points plus closing point
- Line: 2 or more points in sequence

For animation:
- Consider frame rate (24 fps is standard)
- Use multiple frames for smooth motion
- Apply animation principles (squash & stretch, anticipation, etc.)

Always provide clear feedback about what you're doing and save the final result.
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
