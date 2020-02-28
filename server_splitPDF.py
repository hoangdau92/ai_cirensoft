# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import io
import os
import base64
import pytesseract
from flask import request
from flask_cors import CORS, cross_origin
from splitPDF import pdf_processing
import json as JSON

import re

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

@app.route("/split", methods=["POST"])
@cross_origin() # allow all origins all methods
def split():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}

	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		print("Start processing ...")
		json = request.get_json()
		fileContents = json.get('contentbase64')
		# #imgstring = request.form.get('image')
		pdf = base64.b64decode(fileContents)
		fileName = json.get('fileName')
		with open("tempfiles\\" + fileName, "wb") as f:
			f.write(pdf)
		xoay180 = json.get('xoay180')
		result = pdf_processing(fileName, xoay180)

		data["data"] = str(result)
		data["success"] = True

		f.close()
		os.remove("tempfiles\\" + fileName)
	# return the data dictionary as a JSON response
	return flask.jsonify(data)

@app.route("/setConfig", methods=["POST"])
@cross_origin() # allow all origins all methods
def setConfig():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}
	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		print("Start processing ...")
		json = request.get_json()
		fileContents = json.get('config')
		temp = JSON.dumps(fileContents)
		with open("config\\config.json", "w") as f:
			f.write(temp)

		data["success"] = True
	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# for debugging purposes, it's helpful to start the Flask testing
# server (don't use this for production
if __name__ == "__main__":
	PORT = os.getenv("PORT", 6792)
	HOST = os.getenv("HOST", "10.151.137.202")
	print("* Starting web service at http://{host}:{port}...".format(host=HOST, port=PORT))
	app.run(host=HOST, port=PORT)


