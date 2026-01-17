# Blender MCP Server - Fixes and Improvements

## Summary

Fixed Blender 4.0+ compatibility issues and added new mesh-based 2D animation tools that work reliably across all Blender versions.

## Issues Fixed

### 1. Grease Pencil Creation Error
**Problem:** `bpy.ops.object.gpencil_add` operator not found in Blender 4.0+

**Root Cause:** Blender 4.0+ replaced the old Grease Pencil system with Grease Pencil v3, which uses different operators and data structures.

**Solution:** 
- Updated `create_grease_pencil()` to try the new API (`bpy.ops.object.grease_pencil_add()`) first
- Falls back to legacy API for older Blender versions
- Added error handling for better diagnostics

### 2. Type Checking Issues
**Problem:** Functions checking for `'GPENCIL'` type failed with new Grease Pencil objects

**Root Cause:** Blender 4.0+ uses `'GREASEPENCIL'` (no underscore) as the object type

**Solution:**
- Updated `add_gp_stroke()` and `set_gp_material()` to accept both types
- Added better error messages showing the actual object type

### 3. Material Creation Incompatibility
**Problem:** `bpy.data.materials.create_gpencil_data()` doesn't exist in Blender 4.0+

**Solution:**
- Updated `set_gp_material()` to detect API version
- Uses legacy API for Blender < 4.0
- Uses standard material nodes for Blender 4.0+

### 4. Stroke Drawing Limitations
**Problem:** New Grease Pencil v3 has a completely different data structure for layers/frames/strokes

**Solution:**
- Updated `add_gp_stroke()` to detect the data structure
- Works with legacy API when available
- Returns informative message for Blender 4.0+ (manual drawing required)

## New Features

### Mesh-Based 2D Animation Tools (Recommended)

Added four new tools that work reliably across ALL Blender versions:

1. **`create_2d_circle(name, radius, location)`**
   - Creates a filled circle mesh perfect for balls, wheels, etc.
   - Example: `create_2d_circle("Ball", 0.5, [0, 3, 0])`

2. **`create_2d_rectangle(name, width, height, location)`**
   - Creates a rectangular plane for platforms, walls, etc.
   - Example: `create_2d_rectangle("Platform", 8, 0.5, [0, -2, 0])`

3. **`set_object_material(object_name, color, alpha)`**
   - Assigns colored materials to any mesh object
   - Works with standard Blender materials (compatible with all versions)
   - Example: `set_object_material("Ball", [1.0, 0.0, 0.0], 1.0)`

4. **`animate_object_location(object_name, keyframes)`**
   - Simplified animation with batch keyframe creation
   - Example: `animate_object_location("Ball", [[1, 0, 3, 0], [12, 0, -1.5, 0], [24, 0, 2, 0]])`

### Updated AI Agent Behavior

- **System prompt** now recommends mesh-based tools over Grease Pencil
- Includes specific guidance for bouncing ball animations
- Provides example keyframe patterns
- **Tool definitions** updated to mark mesh-based tools as "RECOMMENDED"

## Files Modified

1. **`blender_mcp_server.py`**
   - Fixed `create_grease_pencil()` for Blender 4.0+
   - Updated `add_gp_stroke()` with version detection
   - Updated `set_gp_material()` with version detection
   - Added 4 new mesh-based animation tools

2. **`mcp_agent_wrapper.py`**
   - Updated system prompt to prefer mesh-based tools
   - Added specific bouncing ball animation guidance

3. **`tool_definitions.py`**
   - Added definitions for 4 new mesh-based tools
   - Marked them as "RECOMMENDED" in descriptions

4. **`EXAMPLES.md`** (new file)
   - Example prompts for using the new tools
   - Both detailed and simple prompt examples

## Testing

To test the fixes:

1. **Restart the server:**
   ```bash
   # Stop current server (Ctrl+C or type 'quit')
   uv run main.py
   ```

2. **Try a simple prompt:**
   ```
   create a red ball bouncing on a gray platform
   ```

3. **Expected behavior:**
   - Scene clears
   - 2D camera created
   - Circle created for ball (using `create_2d_circle`)
   - Rectangle created for platform (using `create_2d_rectangle`)
   - Materials applied with colors
   - Animation keyframes set
   - File saved

## Compatibility

- ✅ **Blender 2.8-2.9x:** Legacy Grease Pencil tools work
- ✅ **Blender 3.x:** Legacy Grease Pencil tools work
- ✅ **Blender 4.0+:** Mesh-based tools work perfectly
- ⚠️ **Blender 4.0+ Grease Pencil:** Object creation works, but stroke drawing requires manual work

## Recommendations

1. **For new projects:** Use mesh-based tools (`create_2d_circle`, `create_2d_rectangle`)
2. **For Blender 4.0+ users:** Avoid Grease Pencil tools until full v3 API support is added
3. **For complex 2D work:** Consider using the mesh-based approach with shape keys for deformation

## Future Improvements

- [ ] Full Blender 4.0+ Grease Pencil v3 API support
- [ ] Add more shape primitives (triangle, polygon, star)
- [ ] Add scale and rotation animation helpers
- [ ] Add easing curve support for smoother animations
- [ ] Add shape key animation for squash & stretch effects
