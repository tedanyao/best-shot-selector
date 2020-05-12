import cv2
from flask import jsonify
import numpy as np
import urllib.request

def classify(file_names):
    # Load the cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Read the input image
    #img = cv2.imread('images/aaa.png')
    result = {}
    for filename in file_names:
        # img = cv2.imread(filename)
        req = urllib.request.urlopen(filename)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw rectangle around the faces
        # print (filename, faces, type(list(faces)))
        if list(faces):
            result[filename] = "people"
        else:
            result[filename] = "landscape"
    return result
