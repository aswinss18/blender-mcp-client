"""
Blender AI Agent - Interactive 2D Animation Assistant
Natural language interface for creating Blender animations
"""
import asyncio
import os
from dotenv import load_dotenv
from mcp_agent_wrapper import BlenderMCPAgent

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Example prompts
EXAMPLE_PROMPTS = """
📝 Example Prompts:

1. "Create a bouncing ball animation with a red ball"
2. "Make a simple stick figure waving animation"
3. "Create a logo reveal animation with a blue circle"
4. "Draw a bouncing ball that changes color from red to blue"
5. "Create a 5-second looping background animation with moving shapes"
6. "Make the ball bigger and change it to green" (after creating a ball)
7. "Add a yellow sun in the top right corner"
8. "Create text that writes itself letter by letter"

💡 Tips:
- Be specific about colors, sizes, and durations
- You can ask follow-up questions to modify existing work
- The agent will automatically figure out which tools to use
- All files are saved to the output directory
"""


async def main():
    """Main interactive loop"""
    
    # Check for API key
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
        print("❌ Error: Please set your OPENAI_API_KEY in the .env file")
        print("\n1. Open .env file")
        print("2. Replace 'your_openai_api_key_here' with your actual API key")
        print("3. Get your API key from: https://platform.openai.com/api-keys")
        return
    
    print("=" * 70)
    print("🎨 Blender AI Agent - 2D Animation Assistant")
    print("=" * 70)
    print(f"\nModel: {OPENAI_MODEL}")
    print("Type 'examples' to see example prompts")
    print("Type 'quit' or 'exit' to end the session")
    print("=" * 70)
    
    # Initialize agent
    async with BlenderMCPAgent(OPENAI_API_KEY, OPENAI_MODEL) as agent:
        
        while True:
            try:
                # Get user input
                print("\n" + "─" * 70)
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye! Your Blender files are saved in the output directory.")
                    break
                
                if user_input.lower() in ['examples', 'help', '?']:
                    print(EXAMPLE_PROMPTS)
                    continue
                
                # Send to agent
                print("\n🤖 Agent: ", end="", flush=True)
                response = await agent.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'quit' to exit.")


if __name__ == "__main__":
    asyncio.run(main())
