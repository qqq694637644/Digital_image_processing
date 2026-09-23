from email.mime import image
from pathlib import Path
import sys
import cv2

def main():
    if len(sys.argv)!=2:
        print("usage: python main.py image.jpg")
        raise SystemExit(1)
    image_path =Path(sys.argv[1])
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"failed to read image:{image_path}")
    print("shape:",image.shape)
    print("dtype:",image.dtype)
    print("pixel[0,0]:",image[0,0])

if __name__ =="__main__":
    main()