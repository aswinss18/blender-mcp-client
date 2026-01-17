# Example prompts for the Blender AI Agent

## Using Mesh-Based 2D Animation (Recommended)

### Bouncing Ball Animation
```
Create a bouncing ball animation:
1. Clear the scene
2. Setup a 2D camera at [0, 0, 10] with ortho scale 12
3. Create a 2D circle named "Ball" with radius 0.5 at location [0, 3, 0]
4. Set the ball's material to red color [1.0, 0.0, 0.0]
5. Create a 2D rectangle named "Platform" with width 8 and height 0.5 at location [0, -2, 0]
6. Set the platform's material to gray color [0.3, 0.3, 0.3]
7. Animate the ball's location with these keyframes:
   - Frame 1: [0, 3, 0] (start high)
   - Frame 12: [0, -1.5, 0] (bounce on platform)
   - Frame 24: [0, 2, 0] (bounce back up)
   - Frame 36: [0, -1.5, 0] (second bounce)
   - Frame 48: [0, 1, 0] (smaller bounce)
8. Set animation range to 1-48 frames
9. Set background color to white [1.0, 1.0, 1.0]
```

### Simple User Prompt
```
create a red ball bouncing on a gray platform
```

## Using Grease Pencil (Legacy - Blender < 4.0)

Note: Grease Pencil tools may not work fully in Blender 4.0+ due to API changes.
Use the mesh-based tools above for better compatibility.

### Example
```
create a grease pencil animation with a bouncing ball
```
