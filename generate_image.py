from PIL import Image, ImageDraw
import os

def generate_platform_image(width=100, height=20, color=(139, 69, 19)):
    """
    Generate a simple platform image.
    """
    # Create a new image with RGBA mode for transparency if needed
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(image)

    # Draw the platform as a filled rectangle with the given color
    draw.rectangle([0, 0, width-1, height-1], fill=color)

    # Add a simple border for definition
    border_color = (101, 67, 33)  # Darker brown
    draw.rectangle([0, 0, width-1, height-1], outline=border_color, width=2)

    return image

if __name__ == "__main__":
    # Define the path
    path = "pict/ground/platform.png"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Generate the image
    platform_img = generate_platform_image()

    # Save the image
    platform_img.save(path)

    print(f"Platform image saved to {path}")