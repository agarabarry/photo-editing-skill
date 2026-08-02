"""
Photo Editing Skill - Core module for image manipulation using ImageMagick.
"""

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import os
from pathlib import Path
from typing import Optional, Tuple, List, Dict


class PhotoEditor:
    """Main class for photo editing operations using ImageMagick."""

    def __init__(self, quality: int = 95):
        """
        Initialize PhotoEditor.

        Args:
            quality: JPEG/WebP quality (1-100). Default: 95
        """
        self.quality = quality

    def _validate_input(self, input_path: str) -> None:
        """Validate that input file exists and is readable."""
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

    def _ensure_output_dir(self, output_path: str) -> None:
        """Ensure output directory exists."""
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

    # ==================== BASIC OPERATIONS ====================

    def resize(
        self,
        input_path: str,
        output_path: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        maintain_aspect: bool = True,
    ) -> None:
        """
        Resize an image.

        Args:
            input_path: Path to input image
            output_path: Path to output image
            width: Target width in pixels
            height: Target height in pixels
            maintain_aspect: Keep aspect ratio (default: True)
        """
        self._validate_input(input_path)
        self._ensure_output_dir(output_path)

        with Image(filename=input_path) as img:
            if maintain_aspect:
                img.transform(resize=f"{width or ''}x{height or ''}")
            else:
                if width and height:
                    img.resize(width=width, height=height)
                elif width:
                    img.resize(width=width)
                elif height:
                    img.resize(height=height)

            img.compression_quality = self.quality
            img.save(filename=output_path)

    def crop(
        self, input_path: str, output_path: str, x: int, y: int, width: int, height: int
    ) -> None:
        """
        Crop an image.

        Args:
            input_path: Path to input image
            output_path: Path to output image
            x: X coordinate of crop region
            y: Y coordinate of crop region
            width: Width of crop region
            height: Height of crop region
        """
        self._validate_input(input_path)
        self._ensure_output_dir(output_path)

        with Image(filename=input_path) as img:
            img.crop(left=x, top=y, right=x + width, bottom=y + height)
            img.compression_quality = self.quality
            img.save(filename=output_path)

    def rotate(self, input_path: str, output_path: str, degrees: float) -> None:
        """
        Rotate an image.

        Args:
            input_path: Path to input image
            output_path: Path to output image
            degrees: Rotation angle in degrees (positive = clockwise)
        """
        self._validate_input(input_path)
        self._ensure_output_dir(output_path)

        with Image(filename=input_path) as img:
            img.rotate(-degrees)  # Negative because ImageMagick uses opposite convention
            img.compression_quality = self.quality
            img.save(filename=output_path)

    def flip(self, input_path: str, output_path: str, direction: str = "horizontal") -> None:
        """
        Flip an image.

        Args:
            input_path: Path to input image
            output_path: Path to output image
            direction: 'horizontal' or 'vertical'
        """
        self._validate_input(input_path)
        self._ensure_output_dir(output_path)

        with Image(filename=input_path) as img:
            if direction.lower() == "horizontal":
                img.flop()
            elif direction.lower() == "vertical":
                img.flip()
            else:
                raise ValueError("Direction must be 'horizontal' or 'vertical'")

            img.compression_quality = self.quality
            img.save(filename=output_path)

    # ==================== COLOR ADJUSTMENTS ====================

    def adjust_colors(
        self,
        input_path: str,
        output_path: str,
        brightness: float = 0,
        contrast: float = 0,
        saturation: float = 0,
        hue: float = 0,
    ) -> None:
        """
        Adjust image colors.

        Args:
            input_path: Path to input image
            output_path: Path to output image
            brightness: Brightness adjustment (-100 to 100)
            contrast: Contrast adjustment (-100 to 100)
            saturation: Saturation adjustment (-100 to 100)
            hue: Hue shift in degrees (-360 to 360)
        """
        self._validate_input(input_path)
        self._ensure_output_dir(output_path)

        with Image(filename=input_path) as img:
            if brightness != 0:
                # Convert -100 to 100 range to 0 to 200 scale
                img.brightness = (brightness / 100 + 1) * 100
            if contrast != 0:
                # Convert -100 to 100 range to 0 to 200 scale
                img.contrast = (contrast / 100 + 1) * 100
            if saturation != 0:
                img.modulate(saturation=(saturation + 100))
            if hue != 0:
                img.modulate(hue=(hue % 360))

            img.compression_quality = self.quality
            img.save(filename=output_path)

    def convert_to_grayscale(self, input_path: str, output_path: str) -> None:
        """
        Convert image to grayscale.

        Args:
            input_path: Path to input image
            output_path: Path to output image
        """
        self._validate_input(input_path)
        self._ensure_output_dir(output_path)

        with Image(filename=input_path) as img:
            img.type = "grayscale"
            img.compression_quality = self.quality
            img.save(filename=output_path)

    # ==================== FILTERS & EFFECTS ====================

    def apply_filter(
        self, input_path: str, output_path: str, filter_type: str, **kwargs
    ) -> None:
        """
        Apply a filter to an image.

        Args:
            input_path: Path to input image
            output_path: Path to output image
            filter_type: Type of filter ('blur', 'sharpen', 'sepia', 'emboss', 'edge', 'oil_paint')
            **kwargs: Additional filter-specific parameters
        """
        self._validate_input(input_path)
        self._ensure_output_dir(output_path)

        with Image(filename=input_path) as img:
            if filter_type == "blur":
                radius = kwargs.get("radius", 2)
                sigma = kwargs.get("sigma", 1)
                img.blur(radius=radius, sigma=sigma)

            elif filter_type == "sharpen":
                radius = kwargs.get("radius", 1)
                sigma = kwargs.get("sigma", 0.5)
                img.sharpen(radius=radius, sigma=sigma)

            elif filter_type == "sepia":
                threshold = kwargs.get("threshold", "80%")
                img.sepia_tone(threshold=threshold)

            elif filter_type == "emboss":
                radius = kwargs.get("radius", 1)
                img.emboss(radius=radius)

            elif filter_type == "edge":
                radius = kwargs.get("radius", 2)
                img.edge(radius=radius)

            elif filter_type == "oil_paint":
                radius = kwargs.get("radius", 4)
                img.oil_paint(radius=radius)

            elif filter_type == "charcoal":
                radius = kwargs.get("radius", 2)
                img.charcoal(radius=radius)

            elif filter_type == "solarize":
                threshold = kwargs.get("threshold", 50000)
                img.solarize(threshold=threshold)

            else:
                raise ValueError(f"Unknown filter type: {filter_type}")

            img.compression_quality = self.quality
            img.save(filename=output_path)

    # ==================== IMAGE COMPOSITION ====================

    def add_text(
        self,
        input_path: str,
        output_path: str,
        text: str,
        font_size: int = 20,
        x: int = 10,
        y: int = 10,
        color: str = "white",
        font_path: Optional[str] = None,
    ) -> None:
        """
        Add text to an image.

        Args:
            input_path: Path to input image
            output_path: Path to output image
            text: Text to add
            font_size: Font size in points
            x: X coordinate for text
            y: Y coordinate for text
            color: Text color (color name or hex)
            font_path: Path to custom font file
        """
        self._validate_input(input_path)
        self._ensure_output_dir(output_path)

        with Image(filename=input_path) as img:
            with Drawing() as draw:
                draw.font_size = font_size
                draw.fill_color = Color(color)
                if font_path and os.path.exists(font_path):
                    draw.font = font_path
                draw.text(x, y, text)
                draw(img)

            img.compression_quality = self.quality
            img.save(filename=output_path)

    def composite(
        self, background_path: str, overlay_path: str, output_path: str, x: int = 0, y: int = 0
    ) -> None:
        """
        Composite an overlay image onto a background.

        Args:
            background_path: Path to background image
            overlay_path: Path to overlay image
            output_path: Path to output image
            x: X offset for overlay
            y: Y offset for overlay
        """
        self._validate_input(background_path)
        self._validate_input(overlay_path)
        self._ensure_output_dir(output_path)

        with Image(filename=background_path) as bg:
            with Image(filename=overlay_path) as overlay:
                bg.composite(overlay, left=x, top=y)
                bg.compression_quality = self.quality
                bg.save(filename=output_path)

    # ==================== FORMAT CONVERSION ====================

    def convert_format(self, input_path: str, output_path: str, format: str = None) -> None:
        """
        Convert image to a different format.

        Args:
            input_path: Path to input image
            output_path: Path to output image
            format: Target format (jpg, png, webp, gif, tiff, etc.). If None, inferred from output_path
        """
        self._validate_input(input_path)
        self._ensure_output_dir(output_path)

        with Image(filename=input_path) as img:
            if format:
                img.format = format
            img.compression_quality = self.quality
            img.save(filename=output_path)

    # ==================== BATCH OPERATIONS ====================

    def batch_resize(
        self, input_dir: str, output_dir: str, width: int, height: int, maintain_aspect: bool = True
    ) -> List[str]:
        """
        Resize all images in a directory.

        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            width: Target width
            height: Target height
            maintain_aspect: Keep aspect ratio

        Returns:
            List of processed file paths
        """
        if not os.path.isdir(input_dir):
            raise ValueError(f"Input directory not found: {input_dir}")

        os.makedirs(output_dir, exist_ok=True)
        processed = []

        for filename in os.listdir(input_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)

                try:
                    self.resize(input_path, output_path, width, height, maintain_aspect)
                    processed.append(output_path)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

        return processed

    # ==================== METADATA ====================

    def get_image_info(self, input_path: str) -> Dict:
        """
        Get image metadata.

        Args:
            input_path: Path to input image

        Returns:
            Dictionary with image properties
        """
        self._validate_input(input_path)

        with Image(filename=input_path) as img:
            return {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "colorspace": img.colorspace,
                "depth": img.depth,
                "density": img.density,
            }