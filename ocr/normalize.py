import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def adjust_highlight(image, percent=30, value=30):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    lim = 255 * percent / 100
    v[v > lim] -= value
    v[v <= lim] = 0

    final_hsv = cv2.merge((h, s, v))
    image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return image


def normalize(image):
    image = np.asarray(image)
    rgb_planes = cv2.split(image)
    result_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
    img_result = cv2.merge(result_planes)
    img_result = adjust_highlight(img_result)
    return Image.fromarray(np.uint8(img_result))
