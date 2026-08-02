"""
Claude Integration - Tool definitions for using PhotoEditor with Claude.
"""

import json
from typing import Any, Callable, Dict, List
from photo_editor import PhotoEditor


class ClaudePhotoEditingTools:
    """Provides Claude-compatible tool definitions for photo editing operations."""

    def __init__(self, quality: int = 95):
        """Initialize with a PhotoEditor instance."""
        self.editor = PhotoEditor(quality=quality)

    def get_tools_definition(self) -> List[Dict[str, Any]]:
        """
        Get tool definitions for Claude's tool use feature.

        Returns:
            List of tool definition dictionaries compatible with Claude's API
        """
        return [
            {
                "name": "resize_image",
                "description": "Resize an image to specified dimensions",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "input_path": {
                            "type": "string",
                            "description": "Path to the input image file",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Path for the output image file",
                        },
                        "width": {
                            "type": "integer",
                            "description": "Target width in pixels (optional)",
                        },
                        "height": {
                            "type": "integer",
                            "description": "Target height in pixels (optional)",
                        },
                        "maintain_aspect": {
                            "type": "boolean",
                            "description": "Keep aspect ratio (default: true)",
                            "default": True,
                        },
                    },
                    "required": ["input_path", "output_path"],
                },
            },
            {
                "name": "crop_image",
                "description": "Crop an image to a specified region",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "input_path": {
                            "type": "string",
                            "description": "Path to the input image file",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Path for the output image file",
                        },
                        "x": {"type": "integer", "description": "X coordinate of crop region"},
                        "y": {"type": "integer", "description": "Y coordinate of crop region"},
                        "width": {"type": "integer", "description": "Width of crop region"},
                        "height": {
                            "type": "integer",
                            "description": "Height of crop region",
                        },
                    },
                    "required": ["input_path", "output_path", "x", "y", "width", "height"],
                },
            },
            {
                "name": "rotate_image",
                "description": "Rotate an image by a specified angle",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "input_path": {
                            "type": "string",
                            "description": "Path to the input image file",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Path for the output image file",
                        },
                        "degrees": {
                            "type": "number",
                            "description": "Rotation angle in degrees (positive = clockwise)",
                        },
                    },
                    "required": ["input_path", "output_path", "degrees"],
                },
            },
            {
                "name": "flip_image",
                "description": "Flip an image horizontally or vertically",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "input_path": {
                            "type": "string",
                            "description": "Path to the input image file",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Path for the output image file",
                        },
                        "direction": {
                            "type": "string",
                            "enum": ["horizontal", "vertical"],
                            "description": "Flip direction (default: horizontal)",
                            "default": "horizontal",
                        },
                    },
                    "required": ["input_path", "output_path"],
                },
            },
            {
                "name": "adjust_colors",
                "description": "Adjust brightness, contrast, saturation, and hue",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "input_path": {
                            "type": "string",
                            "description": "Path to the input image file",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Path for the output image file",
                        },
                        "brightness": {
                            "type": "number",
                            "description": "Brightness adjustment (-100 to 100, default: 0)",
                            "default": 0,
                        },
                        "contrast": {
                            "type": "number",
                            "description": "Contrast adjustment (-100 to 100, default: 0)",
                            "default": 0,
                        },
                        "saturation": {
                            "type": "number",
                            "description": "Saturation adjustment (-100 to 100, default: 0)",
                            "default": 0,
                        },
                        "hue": {
                            "type": "number",
                            "description": "Hue shift in degrees (-360 to 360, default: 0)",
                            "default": 0,
                        },
                    },
                    "required": ["input_path", "output_path"],
                },
            },
            {
                "name": "convert_to_grayscale",
                "description": "Convert an image to grayscale",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "input_path": {
                            "type": "string",
                            "description": "Path to the input image file",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Path for the output image file",
                        },
                    },
                    "required": ["input_path", "output_path"],
                },
            },
            {
                "name": "apply_filter",
                "description": "Apply a visual filter to an image",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "input_path": {
                            "type": "string",
                            "description": "Path to the input image file",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Path for the output image file",
                        },
                        "filter_type": {
                            "type": "string",
                            "enum": [
                                "blur",
                                "sharpen",
                                "sepia",
                                "emboss",
                                "edge",
                                "oil_paint",
                                "charcoal",
                                "solarize",
                            ],
                            "description": "Type of filter to apply",
                        },
                        "radius": {
                            "type": "number",
                            "description": "Filter radius parameter (varies by filter)",
                        },
                        "sigma": {
                            "type": "number",
                            "description": "Sigma parameter for blur/sharpen (default: varies)",
                        },
                        "threshold": {
                            "type": "string",
                            "description": "Threshold for sepia (e.g., '80%') or solarize",
                        },
                    },
                    "required": ["input_path", "output_path", "filter_type"],
                },
            },
            {
                "name": "add_text",
                "description": "Add text overlay to an image",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "input_path": {
                            "type": "string",
                            "description": "Path to the input image file",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Path for the output image file",
                        },
                        "text": {"type": "string", "description": "Text to add to the image"},
                        "font_size": {
                            "type": "integer",
                            "description": "Font size in points (default: 20)",
                            "default": 20,
                        },
                        "x": {
                            "type": "integer",
                            "description": "X coordinate for text (default: 10)",
                            "default": 10,
                        },
                        "y": {
                            "type": "integer",
                            "description": "Y coordinate for text (default: 10)",
                            "default": 10,
                        },
                        "color": {
                            "type": "string",
                            "description": "Text color (color name or hex, default: white)",
                            "default": "white",
                        },
                        "font_path": {
                            "type": "string",
                            "description": "Path to custom font file (optional)",
                        },
                    },
                    "required": ["input_path", "output_path", "text"],
                },
            },
            {
                "name": "composite_images",
                "description": "Composite an overlay image onto a background image",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "background_path": {
                            "type": "string",
                            "description": "Path to the background image",
                        },
                        "overlay_path": {
                            "type": "string",
                            "description": "Path to the overlay image",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Path for the output image file",
                        },
                        "x": {
                            "type": "integer",
                            "description": "X offset for overlay (default: 0)",
                            "default": 0,
                        },
                        "y": {
                            "type": "integer",
                            "description": "Y offset for overlay (default: 0)",
                            "default": 0,
                        },
                    },
                    "required": ["background_path", "overlay_path", "output_path"],
                },
            },
            {
                "name": "convert_format",
                "description": "Convert an image to a different format",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "input_path": {
                            "type": "string",
                            "description": "Path to the input image file",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "Path for the output image file",
                        },
                        "format": {
                            "type": "string",
                            "description": "Target format (jpg, png, webp, gif, tiff, etc.). If omitted, inferred from output_path",
                        },
                    },
                    "required": ["input_path", "output_path"],
                },
            },
            {
                "name": "get_image_info",
                "description": "Get metadata about an image",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "input_path": {
                            "type": "string",
                            "description": "Path to the input image file",
                        },
                    },
                    "required": ["input_path"],
                },
            },
        ]

    def process_tool_call(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """
        Process a tool call from Claude.

        Args:
            tool_name: Name of the tool to execute
            tool_input: Input parameters for the tool

        Returns:
            JSON string with the result or error message
        """
        try:
            if tool_name == "resize_image":
                self.editor.resize(
                    tool_input["input_path"],
                    tool_input["output_path"],
                    width=tool_input.get("width"),
                    height=tool_input.get("height"),
                    maintain_aspect=tool_input.get("maintain_aspect", True),
                )
                return json.dumps(
                    {"status": "success", "message": f"Image resized and saved to {tool_input['output_path']}"}
                )

            elif tool_name == "crop_image":
                self.editor.crop(
                    tool_input["input_path"],
                    tool_input["output_path"],
                    tool_input["x"],
                    tool_input["y"],
                    tool_input["width"],
                    tool_input["height"],
                )
                return json.dumps(
                    {"status": "success", "message": f"Image cropped and saved to {tool_input['output_path']}"}
                )

            elif tool_name == "rotate_image":
                self.editor.rotate(
                    tool_input["input_path"],
                    tool_input["output_path"],
                    tool_input["degrees"],
                )
                return json.dumps(
                    {
                        "status": "success",
                        "message": f"Image rotated by {tool_input['degrees']}° and saved to {tool_input['output_path']}",
                    }
                )

            elif tool_name == "flip_image":
                self.editor.flip(
                    tool_input["input_path"],
                    tool_input["output_path"],
                    tool_input.get("direction", "horizontal"),
                )
                return json.dumps(
                    {
                        "status": "success",
                        "message": f"Image flipped and saved to {tool_input['output_path']}",
                    }
                )

            elif tool_name == "adjust_colors":
                self.editor.adjust_colors(
                    tool_input["input_path"],
                    tool_input["output_path"],
                    brightness=tool_input.get("brightness", 0),
                    contrast=tool_input.get("contrast", 0),
                    saturation=tool_input.get("saturation", 0),
                    hue=tool_input.get("hue", 0),
                )
                return json.dumps(
                    {
                        "status": "success",
                        "message": f"Colors adjusted and saved to {tool_input['output_path']}",
                    }
                )

            elif tool_name == "convert_to_grayscale":
                self.editor.convert_to_grayscale(
                    tool_input["input_path"],
                    tool_input["output_path"],
                )
                return json.dumps(
                    {
                        "status": "success",
                        "message": f"Image converted to grayscale and saved to {tool_input['output_path']}",
                    }
                )

            elif tool_name == "apply_filter":
                filter_kwargs = {}
                if "radius" in tool_input:
                    filter_kwargs["radius"] = tool_input["radius"]
                if "sigma" in tool_input:
                    filter_kwargs["sigma"] = tool_input["sigma"]
                if "threshold" in tool_input:
                    filter_kwargs["threshold"] = tool_input["threshold"]

                self.editor.apply_filter(
                    tool_input["input_path"],
                    tool_input["output_path"],
                    tool_input["filter_type"],
                    **filter_kwargs,
                )
                return json.dumps(
                    {
                        "status": "success",
                        "message": f"{tool_input['filter_type']} filter applied and saved to {tool_input['output_path']}",
                    }
                )

            elif tool_name == "add_text":
                self.editor.add_text(
                    tool_input["input_path"],
                    tool_input["output_path"],
                    tool_input["text"],
                    font_size=tool_input.get("font_size", 20),
                    x=tool_input.get("x", 10),
                    y=tool_input.get("y", 10),
                    color=tool_input.get("color", "white"),
                    font_path=tool_input.get("font_path"),
                )
                return json.dumps(
                    {
                        "status": "success",
                        "message": f"Text added and saved to {tool_input['output_path']}",
                    }
                )

            elif tool_name == "composite_images":
                self.editor.composite(
                    tool_input["background_path"],
                    tool_input["overlay_path"],
                    tool_input["output_path"],
                    x=tool_input.get("x", 0),
                    y=tool_input.get("y", 0),
                )
                return json.dumps(
                    {
                        "status": "success",
                        "message": f"Images composited and saved to {tool_input['output_path']}",
                    }
                )

            elif tool_name == "convert_format":
                self.editor.convert_format(
                    tool_input["input_path"],
                    tool_input["output_path"],
                    format=tool_input.get("format"),
                )
                return json.dumps(
                    {
                        "status": "success",
                        "message": f"Image converted and saved to {tool_input['output_path']}",
                    }
                )

            elif tool_name == "get_image_info":
                info = self.editor.get_image_info(tool_input["input_path"])
                return json.dumps({"status": "success", "data": info})

            else:
                return json.dumps({"status": "error", "message": f"Unknown tool: {tool_name}"})

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})