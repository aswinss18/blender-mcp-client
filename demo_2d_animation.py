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


async def create_bouncing_ball_animation():
    """Create a simple 2D bouncing ball animation"""
    async with stdio_client(BlenderServer) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ Connected to Blender MCP\n")

            # 1. Clear the scene
            print("🧹 Clearing scene...")
            await session.call_tool("clear_scene", arguments={})

            # 2. Setup 2D camera
            print("📷 Setting up 2D camera...")
            await session.call_tool("setup_2d_camera", arguments={
                "location": [0, 0, 10],
                "ortho_scale": 8.0
            })

            # 3. Set background color (light blue)
            print("🎨 Setting background color...")
            await session.call_tool("set_background_color", arguments={
                "color": [0.5, 0.7, 1.0]  # Light blue
            })

            # 4. Create Grease Pencil object
            print("✏️  Creating Grease Pencil object...")
            await session.call_tool("create_grease_pencil", arguments={
                "name": "Ball"
            })

            # 5. Add material (red ball)
            print("🎨 Adding red material...")
            await session.call_tool("set_gp_material", arguments={
                "name": "Red",
                "color": [1.0, 0.2, 0.2],  # Red
                "alpha": 1.0
            })

            # 6. Draw circle strokes at different positions (simulating bounce)
            print("🎾 Drawing bouncing ball frames...")
            
            # Create circle points (simplified circle)
            import math
            circle_points = []
            num_points = 16
            radius = 0.5
            for i in range(num_points + 1):
                angle = (i / num_points) * 2 * math.pi
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                circle_points.append([x, y, 0])

            # Frame 1: Ball at top
            await session.call_tool("add_gp_stroke", arguments={
                "layer_name": "Ball",
                "points": [[p[0], p[1] + 3, p[2]] for p in circle_points],
                "frame": 1
            })

            # Frame 10: Ball falling
            await session.call_tool("add_gp_stroke", arguments={
                "layer_name": "Ball",
                "points": [[p[0], p[1] + 1.5, p[2]] for p in circle_points],
                "frame": 10
            })

            # Frame 20: Ball at bottom (squashed)
            squashed_points = [[p[0] * 1.3, p[1] * 0.7, p[2]] for p in circle_points]
            await session.call_tool("add_gp_stroke", arguments={
                "layer_name": "Ball",
                "points": squashed_points,
                "frame": 20
            })

            # Frame 30: Ball bouncing back up
            await session.call_tool("add_gp_stroke", arguments={
                "layer_name": "Ball",
                "points": [[p[0], p[1] + 2, p[2]] for p in circle_points],
                "frame": 30
            })

            # Frame 40: Ball at top again
            await session.call_tool("add_gp_stroke", arguments={
                "layer_name": "Ball",
                "points": [[p[0], p[1] + 3, p[2]] for p in circle_points],
                "frame": 40
            })

            # 7. Set animation range
            print("⏱️  Setting animation range...")
            await session.call_tool("set_animation_range", arguments={
                "start_frame": 1,
                "end_frame": 40
            })

            # 8. Configure render settings
            print("🎬 Configuring render settings...")
            await session.call_tool("set_render_settings", arguments={
                "resolution_x": 1280,
                "resolution_y": 720,
                "fps": 24,
                "output_path": "C:\\Development\\Ai-agents\\blender-mcp\\output\\frame_"
            })

            # 9. Save the file
            output_file = "C:\\Development\\Ai-agents\\blender-mcp\\bouncing_ball.blend"
            print(f"💾 Saving to {output_file}...")
            await session.call_tool("save_file", arguments={
                "filepath": output_file
            })

            print("\n✅ Done! Animation created successfully!")
            print(f"\n📂 Open '{output_file}' in Blender to see the bouncing ball animation")
            print("   Press SPACEBAR in Blender to play the animation")


asyncio.run(create_bouncing_ball_animation())
