from fastapi import FastAPI, File, Depends
from requests.api import request
from requests.sessions import Request
from sqlalchemy.orm import Session
import uvicorn

from detect_faces import detect
from write_value import create_image, get_image, del_image
from count_value import count_image
from models import Base
from create_database import SessionLocal, engine



Base.metadata.create_all(bind=engine) #запускаем базу данных на основе созданной в create_database.py базы данных с примененным видом "таблицы" из models.py

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post('/images/')
async def create_item(image: bytes = File(...), db: Session = Depends(get_db)) -> dict:
    #теперь create_image делает 2 действия: 
    faces = detect(image)
    #detect of detect_faces.py
    db_image = create_image(db, faces=faces)    
    # puts value faces with int in (db: Session, faces: int) in file write_value.py: db_image = models.Image(faces=faces)
    # value faces assign to value model in class Image (models.Image(faces=faces))
    # models.py takes value faces from write_value(class Image) and put faces to value faces of Column in models.py
    
    return {"image_id" : db_image, "faces" : faces}
    # теперь image_id возвращает значение из бд, которое генерируется с autoincrement

@app.get('/images/{image_id}')
async def get_item(image_id: int, db: Session = Depends(get_db))-> dict:
    db_image = get_image(db, id=id)
    return {"image_id" : db_image}

@app.delete('/images/{image_id}')
async def del_item(image_id: int, db: Session = Depends(get_db))-> dict:
    db_image = del_image(db, id=id)
    return db_image

@app.det('/images/count')
async def del_item(image_id: int, faces: int, time: str, db: Session = Depends(get_db))-> dict:
    db_image_count = count_image(db, id = id, faces = faces, time = time)
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")
