import matplotlib.pyplot as plt
import base64
import io
from PIL import Image
import numpy as np


def display_image(rgb_array):
    plt.figure(figsize=(8, 8))
    plt.imshow(rgb_array)
    plt.axis("off")
    plt.show()


def rgb_array_to_base64_image(rgb_array):
    # Convert numpy array to PIL Image with high quality
    img = Image.fromarray(np.uint8(rgb_array))

    # Save image to bytes buffer with maximum quality settings
    buffer = io.BytesIO()
    img.save(buffer, format="PNG", optimize=False, quality=100, subsampling=0)

    # Encode to base64 and add markdown image prefix
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode(
        "utf-8"
    )


def base64_to_image_url_message(base_64_image, text=None):
    content = [
        {
            "type": "image_url",
            "image_url": {"url": base_64_image},
            "detail": "high",
        }
    ]
    if text is not None:
        content.append({"type": "text", "text": text})
    return {
        "role": "user",
        "content": content,
    }
