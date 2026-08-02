# Photo Editing Skill for Claude

A comprehensive photo editing skill that enables Claude to perform advanced image manipulations using ImageMagick as the underlying engine.

## Features

- **Basic Operations**: Crop, resize, rotate, flip, and scale images
- **Color Adjustments**: Brightness, contrast, saturation, hue, and color grading
- **Filters & Effects**: Blur, sharpen, grayscale, sepia, emboss, and more
- **Image Composition**: Layer images, add text, apply overlays
- **Advanced**: Batch processing, format conversion, metadata handling

## Requirements

- Python 3.8+
- ImageMagick 6.9+ (with Ghostscript for PDF support)
- Wand (Python wrapper for ImageMagick)

## Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install ImageMagick (macOS)
brew install imagemagick

# Install ImageMagick (Ubuntu/Debian)
sudo apt-get install imagemagick

# Install ImageMagick (Windows)
# Download from https://imagemagick.org/script/download.php
```

## Quick Start

```python
from photo_editor import PhotoEditor

editor = PhotoEditor()

# Resize an image
editor.resize('input.jpg', 'output.jpg', width=800, height=600)

# Adjust brightness and contrast
editor.adjust_colors('input.jpg', 'output.jpg', brightness=20, contrast=15)

# Apply a filter
editor.apply_filter('input.jpg', 'output.jpg', filter_type='sepia')
```

## Usage with Claude

This skill is designed to be called as a tool function by Claude. See the `claude_integration.py` for examples of how to integrate with Claude's tool use feature.

## API Reference

See [API.md](./API.md) for complete documentation of all available functions.

## Directory Structure

```
photo-editing-skill/
├── photo_editor.py          # Core photo editing module
├── claude_integration.py     # Claude tool integration
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── API.md                   # Complete API documentation
├── examples/                # Usage examples
└── tests/                   # Test suite
```

## License

MIT