import cv2
import numpy as np


def detect(img):
        
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    jpg_as_np = np.frombuffer(img, dtype=np.uint8) #из буфера берем байты. uint8 - целые числа в диапазоне от 0 по 255 (числа размером 1 байт).
    img = cv2.imdecode(jpg_as_np, flags=1) #возвращаем изображение в виде буфера изображения
   
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
    faces = face_cascade.detectMultiScale(gray, 1.1, 7)
   
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return len(faces)