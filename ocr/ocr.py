from PIL import Image
import pytesseract
import argparse
import cv2
import os
import base64
import numpy as np

def convertImage2Text(image_encode)  :
    image = base64.b64decode(image_encode)
    #gray = cv2.cvtColor(np.float32(image), cv2.COLOR_BGR2GRAY)


    #gray = cv2.threshold(gray, 0, 255,
     #                    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    text = "haha"
    cv2.imshow("Output", image)
    # Ghi tạm ảnh xuống ổ cứng để sau đó apply OCR
    # filename = "{}.png".format(os.getpid())
    # cv2.imwrite(filename, gray)
    #
    # # Load ảnh và apply nhận dạng bằng Tesseract OCR
    # text = pytesseract.image_to_string(Image.open(filename), lang='vie')
    #
    # # Xóa ảnh tạm sau khi nhận dạng
    # os.remove(filename)
    # print('da vao')



    return text