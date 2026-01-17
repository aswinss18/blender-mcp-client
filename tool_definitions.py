"""
OpenAI function definitions for Blender MCP tools.
These definitions allow the AI agent to understand and use Blender tools.
"""

BLENDER_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "clear_scene",
            "description": "Delete all objects in the current Blender scene to start fresh",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_grease_pencil",
            "description": "Create a new Grease Pencil object for 2D drawing and animation",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name for the Grease Pencil object (e.g., 'Character', 'Ball', 'Background')"
                    }
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_gp_stroke",
            "description": "Draw a stroke (line or shape) on the active Grease Pencil object at a specific frame",
            "parameters": {
                "type": "object",
                "properties": {
                    "layer_name": {
                        "type": "string",
                        "description": "Name of the layer to draw on (e.g., 'Lines', 'Fill', 'Outline')"
                    },
                    "points": {
                        "type": "array",
                        "description": "List of [x, y, z] coordinate points that define the stroke path",
                        "items": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 3,
                            "maxItems": 3
                        }
                    },
                    "frame": {
                        "type": "integer",
                        "description": "Frame number to add the stroke to (1-based)"
                    }
                },
                "required": ["layer_name", "points", "frame"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_gp_material",
            "description": "Create and assign a colored material to the active Grease Pencil object",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Material name (e.g., 'Red', 'Blue', 'Outline')"
                    },
                    "color": {
                        "type": "array",
                        "description": "RGB color values in 0-1 range [r, g, b]. Examples: [1.0, 0.0, 0.0] for red, [0.0, 0.0, 1.0] for blue",
                        "items": {"type": "number", "minimum": 0, "maximum": 1},
                        "minItems": 3,
                        "maxItems": 3
                    },
                    "alpha": {
                        "type": "number",
                        "description": "Transparency: 0.0 = fully transparent, 1.0 = fully opaque",
                        "minimum": 0,
                        "maximum": 1
                    }
                },
                "required": ["name", "color", "alpha"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "setup_2d_camera",
            "description": "Setup an orthographic camera optimized for 2D animation viewing",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "array",
                        "description": "Camera position [x, y, z]. For 2D, typically [0, 0, 10]",
                        "items": {"type": "number"},
                        "minItems": 3,
                        "maxItems": 3
                    },
                    "ortho_scale": {
                        "type": "number",
                        "description": "Orthographic scale (zoom level). Larger = more zoomed out. Typical: 8-12"
                    }
                },
                "required": ["location", "ortho_scale"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_background_color",
            "description": "Set the world background color for the scene",
            "parameters": {
                "type": "object",
                "properties": {
                    "color": {
                        "type": "array",
                        "description": "RGB color values in 0-1 range [r, g, b]",
                        "items": {"type": "number", "minimum": 0, "maximum": 1},
                        "minItems": 3,
                        "maxItems": 3
                    }
                },
                "required": ["color"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_light",
            "description": "Add a light source to the scene",
            "parameters": {
                "type": "object",
                "properties": {
                    "light_type": {
                        "type": "string",
                        "enum": ["SUN", "POINT", "SPOT", "AREA"],
                        "description": "Type of light to add"
                    },
                    "location": {
                        "type": "array",
                        "description": "Light position [x, y, z]",
                        "items": {"type": "number"},
                        "minItems": 3,
                        "maxItems": 3
                    },
                    "energy": {
                        "type": "number",
                        "description": "Light strength/intensity"
                    }
                },
                "required": ["light_type", "location", "energy"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_keyframe",
            "description": "Set a keyframe to animate an object's property over time",
            "parameters": {
                "type": "object",
                "properties": {
                    "object_name": {
                        "type": "string",
                        "description": "Name of the object to animate"
                    },
                    "property_path": {
                        "type": "string",
                        "enum": ["location", "rotation_euler", "scale"],
                        "description": "Property to animate"
                    },
                    "frame": {
                        "type": "integer",
                        "description": "Frame number for the keyframe"
                    },
                    "value": {
                        "description": "Value to set (number for single value, array [x,y,z] for vector)",
                    }
                },
                "required": ["object_name", "property_path", "frame", "value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_animation_range",
            "description": "Set the start and end frame numbers for the animation timeline",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_frame": {
                        "type": "integer",
                        "description": "First frame of the animation"
                    },
                    "end_frame": {
                        "type": "integer",
                        "description": "Last frame of the animation"
                    }
                },
                "required": ["start_frame", "end_frame"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_render_settings",
            "description": "Configure render output settings for the animation (supports PNG image sequence or MP4 video)",
            "parameters": {
                "type": "object",
                "properties": {
                    "resolution_x": {
                        "type": "integer",
                        "description": "Width in pixels (e.g., 1920 for Full HD)"
                    },
                    "resolution_y": {
                        "type": "integer",
                        "description": "Height in pixels (e.g., 1080 for Full HD)"
                    },
                    "fps": {
                        "type": "integer",
                        "description": "Frames per second (24 for cinematic, 30 for video)"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "File path for output. For MP4: full path with .mp4 extension (e.g., 'C:/Videos/animation.mp4'). For PNG: path pattern (e.g., 'C:/Frames/frame_')"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["PNG", "MP4"],
                        "description": "Output format: 'MP4' for video file, 'PNG' for image sequence"
                    }
                },
                "required": ["resolution_x", "resolution_y", "fps", "output_path", "format"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "render_animation",
            "description": "Start rendering the animation using current render settings (call set_render_settings first to configure output format and path)",
            "parameters": {
                "type": "object",
                "properties": {
                    "output_path": {
                        "type": "string",
                        "description": "Optional: Override output path. If not provided, uses path from set_render_settings"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_file",
            "description": "Save the current Blender scene to a .blend file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Full path where to save the .blend file"
                    }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_2d_circle",
            "description": "Create a 2D circle mesh object for animation (RECOMMENDED for 2D work, works in all Blender versions)",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name for the circle object (e.g., 'Ball', 'Sun', 'Wheel')"
                    },
                    "radius": {
                        "type": "number",
                        "description": "Circle radius in Blender units"
                    },
                    "location": {
                        "type": "array",
                        "description": "Position [x, y, z] where to create the circle",
                        "items": {"type": "number"},
                        "minItems": 3,
                        "maxItems": 3
                    }
                },
                "required": ["name", "radius", "location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_2d_rectangle",
            "description": "Create a 2D rectangle mesh object for animation (RECOMMENDED for 2D work, works in all Blender versions)",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name for the rectangle object (e.g., 'Platform', 'Wall', 'Ground')"
                    },
                    "width": {
                        "type": "number",
                        "description": "Rectangle width in Blender units"
                    },
                    "height": {
                        "type": "number",
                        "description": "Rectangle height in Blender units"
                    },
                    "location": {
                        "type": "array",
                        "description": "Position [x, y, z] where to create the rectangle",
                        "items": {"type": "number"},
                        "minItems": 3,
                        "maxItems": 3
                    }
                },
                "required": ["name", "width", "height", "location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_object_material",
            "description": "Create and assign a colored material to any mesh object",
            "parameters": {
                "type": "object",
                "properties": {
                    "object_name": {
                        "type": "string",
                        "description": "Name of the object to apply material to"
                    },
                    "color": {
                        "type": "array",
                        "description": "RGB color values in 0-1 range [r, g, b]. Examples: [1.0, 0.0, 0.0] for red, [0.0, 1.0, 0.0] for green",
                        "items": {"type": "number", "minimum": 0, "maximum": 1},
                        "minItems": 3,
                        "maxItems": 3
                    },
                    "alpha": {
                        "type": "number",
                        "description": "Transparency: 0.0 = fully transparent, 1.0 = fully opaque",
                        "minimum": 0,
                        "maximum": 1
                    }
                },
                "required": ["object_name", "color", "alpha"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "animate_object_location",
            "description": "Animate an object's position with multiple keyframes (RECOMMENDED for simple animations)",
            "parameters": {
                "type": "object",
                "properties": {
                    "object_name": {
                        "type": "string",
                        "description": "Name of the object to animate"
                    },
                    "keyframes": {
                        "type": "array",
                        "description": "List of keyframes, each as [frame, x, y, z]. Example: [[1, 0, 3, 0], [12, 0, -1.5, 0], [24, 0, 2, 0]]",
                        "items": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 4,
                            "maxItems": 4
                        }
                    }
                },
                "required": ["object_name", "keyframes"]
            }
        }
    }
]

