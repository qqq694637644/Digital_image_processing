from pathlib import Path
import sys

import cv2


def load_image(image_path):
    """Read an image with OpenCV and fail clearly if loading fails."""
    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"failed to read image: {image_path}")

    return image


def print_image_stats(image):
    """Print the basic image information required by the current checkpoint."""
    print("shape:", image.shape)
    print("dtype:", image.dtype)
    print("min:", image.min())
    print("max:", image.max())
    print("mean:", image.mean())
    print("std:", image.std())


def main():
    if len(sys.argv) != 2:
        print("usage: python main.py image.jpg")
        raise SystemExit(1)

    image_path = Path(sys.argv[1])
    image = load_image(image_path)
    print_image_stats(image)
