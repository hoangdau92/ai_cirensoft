import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

RED_MASK = {
    "low": np.array([0, 84, 0]),
    "high": np.array([179, 255, 243])
}
YELLOW_MASK = {
    "low": np.array([9, 0, 0]),
    "high": np.array([255, 255, 255])
}


def filter_color(img, mask=None):
    if mask is None:
        mask = RED_MASK
    img = img.convert("RGB")
    img = np.asarray(img, dtype=np.uint8)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, mask["low"], mask["high"])
    # mask_inv = cv2.bitwise_not(mask)
    fg = cv2.bitwise_and(img, img, mask=mask)
    # bg = cv2.bitwise_and(img, img, mask=mask_inv)
    return Image.fromarray(np.uint8(fg))