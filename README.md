# Test_detector_service
## Детектор очередей на кассе
____

*Сделано в виртуальной среде*

1. Создаем FastAPI и делаем POST-запрос: 

```python

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/items/")
async def create_item(image: bytes) -> dict:
    return {"image_id" :  1}
```

2. Проверяем запрос:

```python

import requests

filename = "E:\projects_python\iStock_87827713_LARGE_9.02.01_AM-1024x640-696x435.jpg"


url = 'http://127.0.0.1:8000/images'


files = {'my_file': (filename, open(filename, 'rb'))}

response = requests.post(url,files=files)

print(response.json())

```

3. Добавляем детекор лиц на фото:

```python

import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

img = cv2.imread('test.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 


def viewImage(image, name_of_window):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)

viewImage(gray, 'gray_image') 

faces = face_cascade.detectMultiScale(gray, 1.1, 7) 

print(f'Высота изображения: {str(img.shape[0])}')
print(f'Ширина изображения: {str(img.shape[1])}')
 


for (x, y, w, h) in faces:
    cv2.rectangle (img, (x, y), (x+w, y+h), (0, 255, 0), 2)


def count_faces():    
    count = len(faces)
    return(count)

print(f'Количество лиц на фото: {count_faces()}')

cv2.imshow('img', img)

cv2.waitKey(0)

```