# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import io
import os
from ocr import convertImage2Text
import base64
import cv2
import pytesseract
import argparse
from flask import request
from flask_cors import CORS, cross_origin

# initialize our Flask application and Redis server
app = flask.Flask(__name__)


def prepare_image(image, target):
    # if the image mode is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image


@app.route("/")
def homepage():
    return "Welcome to the Keras REST API!"


@app.route("/predict", methods=["POST"])
@cross_origin()  # allow all origins all methods
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        print("Start convert ...")

        # imgstring = request.form.get('image')
        json = request.get_json()
        images = json.get('image')

        # Convert multiples images
        # text = "\n"
        # for i in images:
        #     img_data = base64.urlsafe_b64decode(i)
        #     image = Image.open(io.BytesIO(img_data))
        #     text = pytesseract.image_to_string(image, lang='vie') + text

        img_data = base64.urlsafe_b64decode(images)
        image = Image.open(io.BytesIO(img_data))
        text = pytesseract.image_to_string(image, lang='vie')

        print(text)
        # Response
        data["text"] = text
        # indicate that the request was a success
        data["success"] = True
    # return the data dictionary as a JSON response
    return flask.jsonify(data)


# for debugging purposes, it's helpful to start the Flask testing
# server (don't use this for production
if __name__ == "__main__":
    PORT = os.getenv("PORT", 6790)
    HOST = os.getenv("HOST", "10.151.137.221")
    print("* Starting web service at http://{host}:{port}...".format(host=HOST, port=PORT))
    app.run(host=HOST, port=PORT)
