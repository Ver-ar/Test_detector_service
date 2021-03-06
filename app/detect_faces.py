import cv2
import numpy as np


def detect(img):

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    jpg_as_np = np.frombuffer(
        img, dtype=np.uint8
    )  # takes bytes from buffer. uint8 - integers from 0 to 255 (size: 1 byte).
    img = cv2.imdecode(jpg_as_np, flags=1)  # return image in the form buffer image

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 7)

    return len(faces)
