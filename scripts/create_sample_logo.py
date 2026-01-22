#!/usr/bin/env python3
"""
Create a sample Recrui8 logo for testing
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_recrui8_logo(output_path='assets/recrui8_logo.png', width=200, height=60):
    """
    Create a simple Recrui8 logo

    Args:
        output_path: Path to save the logo
        width: Logo width in pixels
        height: Logo height in pixels
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Create image with white background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Draw a simple logo with text
    # Background rectangle
    draw.rectangle([(0, 0), (width, height)], fill='#2563eb', outline='#1e40af', width=2)

    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()

    # Draw text "Recrui8"
    text = "Recrui8"
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center the text
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    draw.text((x, y), text, fill='white', font=font)

    # Save the image
    img.save(output_path)
    print(f"Logo created at: {output_path}")
    print(f"Size: {width}x{height}")

if __name__ == '__main__':
    create_recrui8_logo()
    print("Sample logo created successfully!")
