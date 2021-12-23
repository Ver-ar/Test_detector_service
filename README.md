# Test_detector_service
## Детектор очередей на кассе
____

*Сделано в виртуальной среде*

1. Создаем FastAPI и делаем POST-запрос: 
   
 __main.py__ *(начальный вариант)*

```python

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/items/")
async def create_item(image: bytes) -> dict:
    return {"image_id" :  1}
```

2. Добавляем детекор лиц на фото:

__detect_faces.py__

```python

import cv2
import numpy as np


def detect(img):
        
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    jpg_as_np = np.frombuffer(img, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
   
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
    faces = face_cascade.detectMultiScale(gray, 1.1, 7)
   
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return len(faces)

```

3. Создаем базу данных:
   
__create_database.py__
   
```python

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./my_database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

```
4. Оформляем базу данных:

__models.py__

```python

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
import datetime

from create_database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    faces = Column(Integer, autoincrement=False)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)

```
5. Создаем функцию, которая добавляет значения из post-запроса в бд:

__write_value.py__

```python

from sqlalchemy.orm import Session
import models

def create_image(db: Session, faces: int):
    db_image = models.Image(faces=faces)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image.id

```
6. Обновляем main, чтоб данные из post-запроса автоматически записывались в бд при создании запроса:

__main.py__

```python

from fastapi import FastAPI, File, Depends
from requests.api import request
from requests.sessions import Request
from sqlalchemy.orm import Session
import uvicorn

from detect_faces import detect
from write_value import create_image
from models import Base
from create_database import SessionLocal, engine


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post('/images/')
async def create_item(image: bytes = File(...), db: Session = Depends(get_db)) -> dict:
    faces = detect(image)
    db_image = create_image(db, faces=faces)    
    return {"image_id" : db_image, "faces" : faces}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")
```