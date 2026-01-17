# 🎥 How to Save Animation as Video and View in Blender

## 🎯 Quick Solutions

### Option 1: Convert Existing PNG Images to MP4 (Easiest)

If you already have PNG images rendered (like your umbrella animation), convert them to MP4:

#### Step 1: Install FFmpeg (if not installed)

**Using winget (Windows 10/11):**
```bash
winget install ffmpeg
```

**Or download manually:**
1. Go to https://ffmpeg.org/download.html
2. Download Windows build
3. Extract and add to PATH

#### Step 2: Convert to MP4

```bash
python convert_to_mp4.py "C:/tmp/umbrella" "C:/Users/aswin/Videos/umbrella.mp4"
```

Replace paths with your actual PNG folder and desired output location.

---

### Option 2: Use Blender's Built-in Video Sequencer

1. **Open Blender** (the one running your MCP server)

2. **Switch to Video Editing workspace:**
   - Click "Video Editing" at the top menu bar

3. **Add Image Sequence:**
   - Press `Shift+A` → `Image/Sequence`
   - Navigate to your PNG folder
   - Select ALL images (Ctrl+A)
   - Click "Add Image Strip"

4. **Set Output to MP4:**
   - Go to Output Properties (printer icon)
   - File Format: `FFmpeg video`
   - Container: `MPEG-4`
   - Video Codec: `H.264`
   - Output path: `C:/Users/aswin/Videos/output.mp4`

5. **Render:**
   - Press `Ctrl+F12`
   - Wait for completion
   - Find your MP4 in the output folder!

---

### Option 3: Ask AI to Render Directly to MP4 (Best for New Animations)

**In your AI terminal, use this EXACT prompt:**

```
Clear the scene, create a simple bouncing ball animation, then configure render settings with format MP4 and output path C:/Users/aswin/Videos/test.mp4, and finally call render_animation
```

**Or more naturally:**

```
create a bouncing ball, set render format to MP4 with output C:/Users/aswin/Videos/ball.mp4, then render it
```

The key is to explicitly mention:
- ✅ "format MP4" or "format='MP4'"
- ✅ Full output path with `.mp4` extension
- ✅ "render" or "render_animation"

---

## 🎬 View Animation in Blender

### Method 1: Play Timeline Animation

1. **Open Blender** (the MCP server instance)
2. **Press `Numpad 0`** to view through camera
3. **Press `Spacebar`** to play animation
4. **Adjust view:**
   - `Home` to zoom to fit
   - `Scroll wheel` to zoom in/out

### Method 2: View Rendered Output

1. **After rendering completes:**
   - Press `F11` to view last render
   - Use arrow keys to navigate frames

2. **Or open the video file:**
   - Navigate to output folder
   - Double-click the MP4 file
   - Plays in your default video player

---

## 🎨 For Your Umbrella Animation

Since you already rendered the umbrella PNG images, here's what to do:

### Quick Convert to MP4:

```bash
# Find where the PNG files are (probably in C:/tmp/umbrella or similar)
# Then run:
python convert_to_mp4.py "C:/tmp/umbrella" "C:/Users/aswin/Videos/umbrella_rain.mp4"
```

### Or Use Blender Video Editor:

1. Open Blender
2. Switch to "Video Editing" workspace
3. Add your PNG sequence
4. Render to MP4

---

## 📋 Troubleshooting

### "AI still renders PNG images"

Make sure to explicitly say:
```
set render format to MP4, output path C:/Users/aswin/Videos/output.mp4, then render
```

### "Can't find PNG files"

Check these common locations:
- `C:/tmp/`
- `C:/Users/aswin/AppData/Local/Temp/`
- Your Blender project directory
- Look for folders named after your animation

### "FFmpeg not found"

Install it:
```bash
winget install ffmpeg
```

Or download from: https://ffmpeg.org/download.html

---

## 🎯 Best Workflow Going Forward

1. **For new animations, use this prompt:**
   ```
   create [your animation description], add lighting, 
   set render format to MP4 at C:/Users/aswin/Videos/[name].mp4, 
   then render it
   ```

2. **For existing PNG sequences:**
   ```bash
   python convert_to_mp4.py [png_folder] [output.mp4]
   ```

3. **To preview before rendering:**
   - Just create the animation
   - Check it in Blender (Spacebar to play)
   - Then ask AI to render when satisfied

---

## 💡 Pro Tips

- **Always specify full path** with `.mp4` extension
- **Add "format MP4"** explicitly in your prompt
- **Use Videos folder** for easy access: `C:/Users/aswin/Videos/`
- **Check Blender window** to see render progress
- **PNG sequences** can be converted later if needed

---

**Need help? Just ask the AI to render with these specific instructions!** 🚀
