# 🎬 Automated MP4 Rendering - Quick Guide

## ✨ New Feature: AI-Powered Video Rendering

You can now ask the AI to render your animations to MP4 video files **completely automatically** - no Blender knowledge required!

## 🚀 How to Use

### Simple Prompt (Recommended)

Just ask the AI to create and render your animation in one go:

```
create a bouncing ball animation and render it to MP4 at C:/Users/aswin/Videos/bouncing_ball.mp4
```

### Step-by-Step Prompts

Or break it down:

1. **Create the animation:**
   ```
   create a red ball bouncing on a blue platform
   ```

2. **Render to MP4:**
   ```
   render this animation to MP4 at C:/Users/aswin/Videos/my_animation.mp4
   ```

## 📝 Example Prompts

### Basic Bouncing Ball
```
create a bouncing ball animation and render it as MP4 to C:/Users/aswin/Videos/ball.mp4
```

### Custom Animation
```
create a blue circle moving from left to right over 3 seconds, then render it to MP4 at C:/Users/aswin/Videos/circle_motion.mp4 in 720p
```

### Fix and Re-render
```
the render was blank, please add a sun light and adjust the camera to show everything, then render to MP4 at C:/Users/aswin/Videos/fixed_animation.mp4
```

## 🎯 What the AI Will Do Automatically

1. ✅ Clear the scene
2. ✅ Create objects (ball, platform, etc.)
3. ✅ Apply colors/materials
4. ✅ Set up camera
5. ✅ Add animation keyframes
6. ✅ Add lighting (if requested or needed)
7. ✅ Configure render settings for MP4
8. ✅ Start rendering
9. ✅ Save to your specified path

## 📹 Output Settings

The AI will automatically use these settings:
- **Format:** MP4 (H.264 codec)
- **Resolution:** 1920×1080 (Full HD) by default
- **Frame Rate:** 24 fps (cinematic)
- **Quality:** Medium (good balance of size and quality)

You can customize by asking:
```
render in 720p HD
render at 30 fps
render in 4K resolution
```

## 📂 Recommended Output Paths

Use these paths for easy access:

- **Videos folder:** `C:/Users/aswin/Videos/animation.mp4`
- **Desktop:** `C:/Users/aswin/Desktop/animation.mp4`
- **Documents:** `C:/Users/aswin/Documents/animation.mp4`
- **Project folder:** `C:/Development/Ai-agents/blender-mcp/output/animation.mp4`

## ⏱️ Rendering Time

- **48 frames (2 seconds):** ~30-60 seconds
- **120 frames (5 seconds):** ~1-2 minutes
- **240 frames (10 seconds):** ~2-4 minutes

The AI will tell you when rendering starts. You can check Blender's progress bar or wait for the completion message.

## 🔧 Troubleshooting

### "Blank render" or "Can't see objects"
```
add a sun light and adjust camera ortho_scale to 15, then render again
```

### "Permission denied" error
Use a different folder like your Videos or Documents folder instead of C:\ root.

### Want to preview before rendering?
```
create the animation and save it, but don't render yet
```
Then check it in Blender, and when ready:
```
now render it to MP4 at C:/Users/aswin/Videos/final.mp4
```

## 🎨 Complete Example

**You:** 
```
create a red ball bouncing on a gray platform with a white background, 
add proper lighting, and render it to MP4 at C:/Users/aswin/Videos/bouncing_ball.mp4
```

**AI will:**
1. Clear scene
2. Create 2D camera
3. Create red circle (ball)
4. Create gray rectangle (platform)
5. Animate ball with bounce keyframes
6. Set white background
7. Add sun light
8. Configure MP4 render settings
9. Start rendering
10. Save video to your Videos folder

**Result:** A complete MP4 video file ready to watch! 🎉

---

**No Blender knowledge needed - just tell the AI what you want!** 🚀
