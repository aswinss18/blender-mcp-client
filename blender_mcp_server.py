import sys
import site
import os

# Add user site-packages to path so Blender can find mcp
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.insert(0, user_site)

# Add all pywin32 directories to sys.path for pywintypes
win32_dir = os.path.join(user_site, "win32")
win32lib_dir = os.path.join(user_site, "win32", "lib")
pywin32_dll_dir = os.path.join(user_site, "pywin32_system32")

# Add all pywin32 paths
for path in [win32_dir, win32lib_dir, pywin32_dll_dir]:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)

# Add pywin32 DLL directory to PATH and DLL search path
if os.path.exists(pywin32_dll_dir):
    os.environ["PATH"] = pywin32_dll_dir + os.pathsep + os.environ.get("PATH", "")
    if hasattr(os, 'add_dll_directory'):
        os.add_dll_directory(pywin32_dll_dir)
    
    # Preload the DLLs using ctypes
    import ctypes
    try:
        pywintypes_dll = os.path.join(pywin32_dll_dir, "pywintypes311.dll")
        if os.path.exists(pywintypes_dll):
            ctypes.WinDLL(pywintypes_dll)
        pythoncom_dll = os.path.join(pywin32_dll_dir, "pythoncom311.dll")
        if os.path.exists(pythoncom_dll):
            ctypes.WinDLL(pythoncom_dll)
    except Exception:
        pass  # If preloading fails, continue anyway

import bpy
from mcp.server.fastmcp import FastMCP

# Create MCP server inside Blender
mcp = FastMCP("Blender MCP Server")

@mcp.tool()
def clear_scene():
    """Delete all objects in the current scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    return "Scene cleared"

@mcp.tool()
def add_cube(size: float = 2.0):
    """Add a cube to the scene"""
    bpy.ops.mesh.primitive_cube_add(size=size)
    return f"Cube added with size {size}"

@mcp.tool()
def save_file(filepath: str):
    """Save the current Blender scene to a file"""
    bpy.ops.wm.save_as_mainfile(filepath=filepath)
    return f"Scene saved to {filepath}"

# ========== 2D ANIMATION TOOLS ==========

@mcp.tool()
def create_grease_pencil(name: str = "GPencil"):
    """Create a new Grease Pencil object for 2D drawing"""
    try:
        # Try new Blender 4.0+ API first
        bpy.ops.object.grease_pencil_add()
        gp_obj = bpy.context.active_object
        gp_obj.name = name
        return f"Grease Pencil object '{name}' created"
    except AttributeError:
        # Fallback to legacy API for Blender < 4.0
        try:
            bpy.ops.object.gpencil_add(type='EMPTY')
            gp_obj = bpy.context.active_object
            gp_obj.name = name
            return f"Grease Pencil object '{name}' created"
        except Exception as e:
            return f"Error: Could not create Grease Pencil object - {str(e)}"

@mcp.tool()
def add_gp_stroke(layer_name: str = "Lines", points: list = None, frame: int = 1):
    """Add a stroke to the active Grease Pencil object
    
    Args:
        layer_name: Name of the layer to draw on
        points: List of [x, y, z] coordinates for the stroke
        frame: Frame number to add the stroke to
    """
    if points is None:
        points = [[0, 0, 0], [1, 1, 0], [2, 0, 0]]
    
    gp_obj = bpy.context.active_object
    if gp_obj.type not in ('GPENCIL', 'GREASEPENCIL'):
        return f"Error: Active object is not a Grease Pencil object (type: {gp_obj.type})"
    
    try:
        gp_data = gp_obj.data
        
        # Check if this is legacy Grease Pencil (has layers attribute)
        if hasattr(gp_data, 'layers') and hasattr(gp_data.layers, 'new'):
            # Legacy Grease Pencil API (Blender < 4.0)
            # Get or create layer
            if layer_name not in gp_data.layers:
                gp_layer = gp_data.layers.new(layer_name)
            else:
                gp_layer = gp_data.layers[layer_name]
            
            # Get or create frame
            gp_frame = gp_layer.frames.new(frame) if frame not in [f.frame_number for f in gp_layer.frames] else gp_layer.frames[frame]
            
            # Create stroke
            stroke = gp_frame.strokes.new()
            stroke.points.add(len(points))
            
            for i, point in enumerate(points):
                stroke.points[i].co = point
                stroke.points[i].pressure = 1.0
            
            return f"Added stroke with {len(points)} points to layer '{layer_name}' at frame {frame}"
        else:
            # New Grease Pencil v3 (Blender 4.0+)
            # The new system uses a different approach - we'll use drawing mode
            # For now, return a message indicating this needs manual drawing
            return f"Note: Blender 4.0+ Grease Pencil v3 detected. Programmatic stroke creation requires using the drawing operators. Object created successfully - please use Blender's Draw mode to add strokes manually."
    except Exception as e:
        return f"Error adding stroke: {str(e)}"

@mcp.tool()
def set_gp_material(name: str, color: list = None, alpha: float = 1.0):
    """Create and assign a material to the active Grease Pencil object
    
    Args:
        name: Material name
        color: RGB color as [r, g, b] (0-1 range)
        alpha: Transparency (0-1)
    """
    if color is None:
        color = [0.0, 0.0, 0.0]  # Black by default
    
    gp_obj = bpy.context.active_object
    if gp_obj.type not in ('GPENCIL', 'GREASEPENCIL'):
        return f"Error: Active object is not a Grease Pencil object (type: {gp_obj.type})"
    
    try:
        # Create material
        mat = bpy.data.materials.new(name)
        
        # Try legacy Grease Pencil API (Blender < 4.0)
        if hasattr(bpy.data.materials, 'create_gpencil_data'):
            bpy.data.materials.create_gpencil_data(mat)
            mat.grease_pencil.color = (*color, alpha)
        else:
            # New Grease Pencil v3 (Blender 4.0+) - use standard material
            mat.use_nodes = True
            if mat.node_tree:
                nodes = mat.node_tree.nodes
                # Clear default nodes
                nodes.clear()
                
                # Create Principled BSDF
                bsdf = nodes.new('ShaderNodeBsdfPrincipled')
                bsdf.inputs['Base Color'].default_value = (*color, 1.0)
                bsdf.inputs['Alpha'].default_value = alpha
                
                # Create output node
                output = nodes.new('ShaderNodeOutputMaterial')
                
                # Link nodes
                mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Assign to object
        gp_obj.data.materials.append(mat)
        
        return f"Material '{name}' created with color {color} and alpha {alpha}"
    except Exception as e:
        return f"Error creating material: {str(e)}"

@mcp.tool()
def setup_2d_camera(location: list = None, ortho_scale: float = 10.0):
    """Setup an orthographic camera for 2D animation
    
    Args:
        location: Camera location [x, y, z]
        ortho_scale: Orthographic scale (controls zoom)
    """
    if location is None:
        location = [0, 0, 10]
    
    # Create camera
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.active_object
    camera.rotation_euler = (0, 0, 0)
    
    # Set to orthographic
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = ortho_scale
    
    # Set as active camera
    bpy.context.scene.camera = camera
    
    return f"2D camera created at {location} with ortho scale {ortho_scale}"

@mcp.tool()
def set_keyframe(object_name: str, property_path: str, frame: int, value: float):
    """Set a keyframe for animation
    
    Args:
        object_name: Name of the object to animate
        property_path: Property path (e.g., 'location', 'rotation_euler', 'scale')
        frame: Frame number
        value: Value to set
    """
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return f"Error: Object '{object_name}' not found"
    
    bpy.context.scene.frame_set(frame)
    
    # Set the value
    if property_path == 'location':
        obj.location = value if isinstance(value, (list, tuple)) else [value, value, value]
    elif property_path == 'rotation_euler':
        obj.rotation_euler = value if isinstance(value, (list, tuple)) else [value, value, value]
    elif property_path == 'scale':
        obj.scale = value if isinstance(value, (list, tuple)) else [value, value, value]
    
    # Insert keyframe
    obj.keyframe_insert(data_path=property_path, frame=frame)
    
    return f"Keyframe set for '{object_name}.{property_path}' at frame {frame}"

@mcp.tool()
def set_animation_range(start_frame: int = 1, end_frame: int = 250):
    """Set the animation frame range"""
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame
    return f"Animation range set to {start_frame}-{end_frame}"

@mcp.tool()
def set_render_settings(resolution_x: int = 1920, resolution_y: int = 1080, fps: int = 24, output_path: str = "//render_", format: str = "PNG"):
    """Configure render settings for animation
    
    Args:
        resolution_x: Width in pixels
        resolution_y: Height in pixels
        fps: Frames per second
        output_path: Output file path pattern
        format: Output format - 'PNG' for image sequence, 'MP4' for video
    """
    scene = bpy.context.scene
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y
    scene.render.fps = fps
    scene.render.filepath = output_path
    
    # Set output format
    if format.upper() == 'MP4':
        scene.render.image_settings.file_format = 'FFMPEG'
        scene.render.ffmpeg.format = 'MPEG4'
        scene.render.ffmpeg.codec = 'H264'
        scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
        return f"Render settings: {resolution_x}x{resolution_y} @ {fps}fps, MP4 output: {output_path}"
    else:
        scene.render.image_settings.file_format = 'PNG'
        return f"Render settings: {resolution_x}x{resolution_y} @ {fps}fps, PNG output: {output_path}"

@mcp.tool()
def render_animation(output_path: str = None):
    """Render the animation to files (uses current render settings)
    
    Args:
        output_path: Optional output path to override current settings
    """
    if output_path:
        bpy.context.scene.render.filepath = output_path
    
    bpy.ops.render.render(animation=True)
    
    actual_path = bpy.context.scene.render.filepath
    return f"Animation rendering started! Output: {actual_path}"

@mcp.tool()
def add_light(light_type: str = "SUN", location: list = None, energy: float = 1.0):
    """Add a light to the scene
    
    Args:
        light_type: Type of light (SUN, POINT, SPOT, AREA)
        location: Light location [x, y, z]
        energy: Light strength
    """
    if location is None:
        location = [0, 0, 5]
    
    bpy.ops.object.light_add(type=light_type, location=location)
    light = bpy.context.active_object
    light.data.energy = energy
    
    return f"{light_type} light added at {location} with energy {energy}"

@mcp.tool()
def set_background_color(color: list = None):
    """Set the world background color
    
    Args:
        color: RGB color as [r, g, b] (0-1 range)
    """
    if color is None:
        color = [0.05, 0.05, 0.05]  # Dark gray
    
    world = bpy.context.scene.world
    if world.use_nodes:
        bg_node = world.node_tree.nodes.get('Background')
        if bg_node:
            bg_node.inputs[0].default_value = (*color, 1.0)
    
    return f"Background color set to {color}"

# ========== MESH-BASED 2D ANIMATION TOOLS (Alternative to Grease Pencil) ==========

@mcp.tool()
def create_2d_circle(name: str = "Circle", radius: float = 1.0, location: list = None):
    """Create a 2D circle mesh for animation
    
    Args:
        name: Object name
        radius: Circle radius
        location: Location [x, y, z]
    """
    if location is None:
        location = [0, 0, 0]
    
    bpy.ops.mesh.primitive_circle_add(radius=radius, location=location, fill_type='NGON')
    obj = bpy.context.active_object
    obj.name = name
    
    return f"2D circle '{name}' created at {location} with radius {radius}"

@mcp.tool()
def create_2d_rectangle(name: str = "Rectangle", width: float = 2.0, height: float = 1.0, location: list = None):
    """Create a 2D rectangle mesh for animation
    
    Args:
        name: Object name
        width: Rectangle width
        height: Rectangle height
        location: Location [x, y, z]
    """
    if location is None:
        location = [0, 0, 0]
    
    bpy.ops.mesh.primitive_plane_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = [width/2, height/2, 1]
    
    return f"2D rectangle '{name}' created at {location} with size {width}x{height}"

@mcp.tool()
def set_object_material(object_name: str, color: list = None, alpha: float = 1.0):
    """Create and assign a material to an object
    
    Args:
        object_name: Name of the object
        color: RGB color as [r, g, b] (0-1 range)
        alpha: Transparency (0-1)
    """
    if color is None:
        color = [0.8, 0.8, 0.8]
    
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return f"Error: Object '{object_name}' not found"
    
    # Create material
    mat_name = f"{object_name}_Material"
    mat = bpy.data.materials.new(mat_name)
    mat.use_nodes = True
    
    # Get the Principled BSDF node
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*color, 1.0)
        bsdf.inputs['Alpha'].default_value = alpha
        
        # Enable transparency if alpha < 1
        if alpha < 1.0:
            mat.blend_method = 'BLEND'
    
    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    
    return f"Material assigned to '{object_name}' with color {color}"

@mcp.tool()
def animate_object_location(object_name: str, keyframes: list):
    """Animate an object's location with keyframes
    
    Args:
        object_name: Name of the object to animate
        keyframes: List of [frame, x, y, z] values
    """
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return f"Error: Object '{object_name}' not found"
    
    for keyframe in keyframes:
        if len(keyframe) != 4:
            return f"Error: Each keyframe must have [frame, x, y, z]"
        
        frame, x, y, z = keyframe
        bpy.context.scene.frame_set(int(frame))
        obj.location = (x, y, z)
        obj.keyframe_insert(data_path="location", frame=int(frame))
    
    return f"Added {len(keyframes)} location keyframes to '{object_name}'"


# IMPORTANT:
# - No print()
# - No logging
# - Only MCP JSON goes to stdout
if __name__ == "__main__":
    mcp.run()
