"""
Example of integrating Photo Editing Skill with Claude.

This example demonstrates how to use the ClaudePhotoEditingTools class
to process tool calls from Claude's API.
"""

import json
from claude_integration import ClaudePhotoEditingTools

# Initialize Claude photo editing tools
tools = ClaudePhotoEditingTools(quality=95)

# Get tool definitions to pass to Claude API
tool_definitions = tools.get_tools_definition()

print("Available tools for Claude:")
for tool in tool_definitions:
    print(f"  - {tool['name']}: {tool['description']}")

print("\n" + "="*60)
print("Example: Processing tool calls from Claude")
print("="*60 + "\n")

# Example 1: Resize an image (simulating Claude tool call)
print("Example 1: Resize tool call")
resize_input = {
    "input_path": "photos/original.jpg",
    "output_path": "photos/resized.jpg",
    "width": 800,
    "height": 600,
    "maintain_aspect": True
}
result = tools.process_tool_call("resize_image", resize_input)
print(f"Input: {json.dumps(resize_input, indent=2)}")
print(f"Result: {result}\n")

# Example 2: Apply a filter
print("Example 2: Apply filter tool call")
filter_input = {
    "input_path": "photos/original.jpg",
    "output_path": "photos/sepia.jpg",
    "filter_type": "sepia"
}
result = tools.process_tool_call("apply_filter", filter_input)
print(f"Input: {json.dumps(filter_input, indent=2)}")
print(f"Result: {result}\n")

# Example 3: Add text overlay
print("Example 3: Add text tool call")
text_input = {
    "input_path": "photos/original.jpg",
    "output_path": "photos/labeled.jpg",
    "text": "Summer 2024",
    "font_size": 32,
    "x": 50,
    "y": 50,
    "color": "white"
}
result = tools.process_tool_call("add_text", text_input)
print(f"Input: {json.dumps(text_input, indent=2)}")
print(f"Result: {result}\n")

# Example 4: Adjust colors
print("Example 4: Adjust colors tool call")
colors_input = {
    "input_path": "photos/original.jpg",
    "output_path": "photos/vibrant.jpg",
    "brightness": 15,
    "contrast": 20,
    "saturation": 30
}
result = tools.process_tool_call("adjust_colors", colors_input)
print(f"Input: {json.dumps(colors_input, indent=2)}")
print(f"Result: {result}\n")

# Example 5: Get image info
print("Example 5: Get image info tool call")
info_input = {
    "input_path": "photos/original.jpg"
}
result = tools.process_tool_call("get_image_info", info_input)
print(f"Input: {json.dumps(info_input, indent=2)}")
print(f"Result: {result}\n")

print("="*60)
print("Integration Example Complete")
print("="*60)
print("\nTo use with Claude's API:")
print("1. Include tool_definitions in your API request")
print("2. When Claude returns tool use, call process_tool_call()")
print("3. Return the JSON result back to Claude")
