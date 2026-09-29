from pathlib import Path
import sys
import cv2
import matplotlib.pyplot as plt



def main():
    if len(sys.argv) != 2:
        print("usage: python main.py image.jpg")
        raise SystemExit(1)

    image_path = Path(sys.argv[1])
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"failed to read image:{image_path}")
    print("shape:",image.shape)
    print("dtype:",image.dtype)
    print("min:",image.min())
    print("max:",image.max())
    print("mean:",image.mean())
    print("std:",image.std())
    bgr = image
    rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )
    print("BGR shape",bgr.shape)
    print("RGB shape:",rgb.shape)
    print("Gray shape:",gray.shape)
    figure,axes = plt.subplots(1,3,figsize= (15,5))
    #第一张,故意出错
    axes[0].imshow(bgr)
    axes[0].set_title("BGR shwown as RGB(wroong)")
    axes[0].axis("off")

    #第二张,正确RGB
    axes[1].imshow(rgb)
    axes[1].set_title("RBG (correct)")
    axes[1].axis("off")

    #第三张 灰度图
    axes[2].imshow(gray,cmap="gray")
    axes[2].set_title("Gray")
    axes[2].axis("off")

    plt.tight_layout()
    plt.show()
    
