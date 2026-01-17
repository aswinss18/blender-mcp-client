# Blender AI Agent 🎨🤖

Create beautiful 2D animations in Blender using natural language!

## Quick Start

### 1. Add Your OpenAI API Key

Edit `.env` file:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### 2. Run the Agent

```powershell
uv run agent_blender.py
```

### 3. Start Creating!

```
💬 You: Create a bouncing ball animation with a red ball

🤖 Agent: I'll create that for you!
[Agent automatically uses Blender tools]
✅ Done! Saved to output/bouncing_ball.blend
```

## Example Prompts

- "Create a bouncing ball animation"
- "Make a simple stick figure waving"
- "Draw a spinning square that changes color"
- "Create a 5-second looping background animation"
- "Make the ball bigger and change it to green"

## Features

✨ **Natural Language**: Just describe what you want  
🤖 **AI-Powered**: GPT-4o plans and executes  
🎨 **2D Animation**: Full Grease Pencil support  
💬 **Conversational**: Modify and refine your work  
📁 **Auto-Save**: Everything saved to .blend files  

## What You Can Create

- Bouncing balls with physics
- Character animations
- Logo reveals
- Abstract motion graphics
- Shape morphing
- Text animations
- Background loops
- And much more!

## Documentation

- **[Agent Guide](file:///C:/Users/aswin/.gemini/antigravity/brain/195a444a-f077-454c-aee2-f32c558cb2ee/agent_guide.md)** - Complete usage guide
- **[2D Animation Guide](file:///C:/Users/aswin/.gemini/antigravity/brain/195a444a-f077-454c-aee2-f32c558cb2ee/2d_animation_guide.md)** - Tool reference
- **[Walkthrough](file:///C:/Users/aswin/.gemini/antigravity/brain/195a444a-f077-454c-aee2-f32c558cb2ee/walkthrough.md)** - Setup walkthrough

## How It Works

```
Your Description → OpenAI GPT-4o → Blender MCP Tools → 2D Animation
```

The AI agent:
1. Understands your natural language request
2. Plans which Blender tools to use
3. Executes them in the correct order
4. Saves your animation to a .blend file

## Requirements

- Python 3.11+
- Blender 5.0+
- OpenAI API key
- All dependencies (installed via `uv`)

## Project Structure

```
blender-mcp/
├── agent_blender.py          # Main agent (run this!)
├── mcp_agent_wrapper.py      # OpenAI + MCP integration
├── tool_definitions.py       # Function schemas
├── blender_mcp_server.py     # Blender MCP server
├── blender_mcp_launcher.py   # Blender launcher
├── .env                      # Configuration
└── output/                   # Your animations
```

## Troubleshooting

**"Error: Please set your OPENAI_API_KEY"**
- Open `.env` and add your API key

**Connection errors**
- Ensure Blender is installed
- Run `uv sync` to install dependencies

**Agent doesn't understand**
- Be more specific in your description
- Check example prompts for inspiration

## Examples

### Simple Animation
```
You: Create a bouncing ball
Agent: [Creates ball animation]
```

### Multi-Step
```
You: Create a red ball
Agent: [Creates red ball]

You: Now make it bounce
Agent: [Adds bouncing animation]

You: Change it to blue
Agent: [Updates color]
```

## Cost

Uses OpenAI API:
- ~$0.01-0.05 per animation
- GPT-4o recommended
- Can use GPT-4o-mini for lower cost

## Support

See the [Agent Guide](file:///C:/Users/aswin/.gemini/antigravity/brain/195a444a-f077-454c-aee2-f32c558cb2ee/agent_guide.md) for detailed help!

---

**Ready to create?** Run `uv run agent_blender.py` and start animating! 🚀
