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
   
    return len(faces)

```

3. Создаем и оформляем базу данных:

__models.py__

```python

from sqlalchemy import Column, Integer, DateTime, MetaData, Sequence, create_engine
import datetime
from sqlalchemy.sql.schema import Table
from sqlalchemy.orm import sessionmaker



engine = create_engine('sqlite:///./my_database.db')

meta = MetaData()

image_table = Table ('image_table', meta,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('faces', Integer, autoincrement=False),
    Column('datetime', DateTime, default=datetime.datetime.utcnow) 
    )


meta.create_all(engine)
SessionLocal = sessionmaker()

```
4. Создаем функции, которые добавляют/отдают значения из post, get, del - запросов в/из бд:

__write_value.py__

```python

from sqlalchemy import func, select
from models import *



def create_image(faces: int):    
    with engine.begin() as conn:            
        result = conn.execute(image_table.insert(),{"faces": faces}).inserted_primary_key 
        print(f'В базу добавлено фото c id: {result[0]}')
    return result[0]

def get_image (id: int):
    select_image = select(image_table).where(image_table.c.id == id)
    with engine.begin() as conn: 
        for row in conn.execute(select_image):
            print(f'Выбрано фото c id: {row[0]}')
            return row

def del_image(id: int):    
    result_del = image_table.delete().where(image_table.c.id == id)
    with engine.begin() as conn:
        conn.execute(result_del)
        print(f'Удалено фото c id: {id}')
        return id
   
def count_image_id(id: int):
    count_table = [func.count('*').label('count'), image_table.c.id]
    select_count = select(count_table).where(image_table.c.id == id)
    with engine.begin() as conn:
        result = conn.execute(select_count)
        result_count = result.fetchall()                
    return result_count[0][0] 

def count_image_faces(faces: int):
    count_table = [func.count('*').label('count'), image_table.c.faces]
    select_count = select(count_table).where(image_table.c.faces == faces)
    with engine.begin() as conn:
        result = conn.execute(select_count)
        result_count = result.fetchall()                
    return result_count[0][0]

```
5. Обновляем main, чтоб данные из FastAPI запросов автоматически записывались в бд при их вызове:

__main.py__

```python

from fastapi import FastAPI, File, HTTPException, Path
import uvicorn
from detect_faces import detect
from write_value import count_image_faces, count_image_id, create_image, get_image, del_image
from models import *


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


@app.post('/images/')
async def create_item(image: bytes = File(...)) -> dict:
    faces = detect(image)
    item = create_image(faces=faces)    
    return {"image_id" : item, "faces": faces}

@app.get('/images/count/image_id/{image_id}')
async def count_item_id(image_id: int = Path(..., title="The ID of the image to get", gt=0))-> dict:
    db_image = count_image_id(id = image_id)
    return db_image

@app.get('/images/count/faces/{faces}')
async def count_item_faces(faces: int = Path(..., title="The faces on the image to get", gt=0))-> dict:
    db_image = count_image_faces(faces = faces)
    return db_image


@app.get('/images/{image_id}')
async def get_item(image_id: int = Path(..., gt=0))-> dict:
    db_image = get_image(id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

@app.delete('/images/{image_id}')
async def del_item(image_id: int = Path(..., gt=0))-> dict:
    db_image = del_image(id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"delete image_id": db_image}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")

```