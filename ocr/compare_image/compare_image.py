import cv2
from skimage.metrics import structural_similarity, peak_signal_noise_ratio
import numpy as np
from PIL import Image

img_path = 'samples/'
img_base_portrait = 'blank_portrait.png'
img_base_landscape = 'blank_landscape.png'

img_a4_portrait = cv2.imread(img_path + img_base_portrait)
height = int(img_a4_portrait.shape[0])
width = int(img_a4_portrait.shape[1])
dim_portrait = (width, height)
img_a4_landscape = cv2.imread(img_path + img_base_landscape)
height = int(img_a4_landscape.shape[0])
width = int(img_a4_landscape.shape[1])
dim_landscape = (width, height)


def check_blank_image(img):
    w, h = img.size
    img = img.convert("RGB")
    img = np.asarray(img, dtype=np.uint8)
    if w > h:
        img = cv2.resize(img, dim_landscape, interpolation=cv2.INTER_AREA)
        similar = structural_similarity(img_a4_landscape, img, multichannel=True)
        mse = peak_signal_noise_ratio(img_a4_landscape, img)
        print(similar, mse)
        if similar > 0.938:
            return True
        return False
    else:
        img = cv2.resize(img, dim_portrait, interpolation=cv2.INTER_AREA)
        similar = structural_similarity(img_a4_portrait, img, multichannel=True)
        mse = peak_signal_noise_ratio(img_a4_portrait, img)
        print(similar, mse)
        if similar > 0.938:
            return True
        return False

