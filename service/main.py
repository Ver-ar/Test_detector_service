from fastapi import FastAPI, File, Depends, HTTPException
from requests.api import request
from requests.sessions import Request
from sqlalchemy.orm import Session
import uvicorn
#import base64
from detect_faces import detect
from write_value import create_image, get_image, del_image, count_image
from models import *
#from create_database import SessionLocal, engine



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post('/images/')
async def create_item(image: bytes = File(...), db: Session = Depends(get_db)) -> dict:
    
    #now create_image does 2 actions: 
    faces = detect(image)
    #detect of detect_faces.py
    item = create_image(db, faces=faces)    
    # puts value faces with int in (db: Session, faces: int) in file write_value.py: db_image = models.Image(faces=faces)
    # value faces assign to value model in class Image (models.Image(faces=faces))
    # models.py takes value faces from write_value(class Image) and put faces to value faces of Column in models.py
    
    return {"image_id" : item, "faces": faces}
    # image_id return value from db, generated from autoincrement

@app.get('/images/{image_id}')
async def get_item(image_id: int, db: Session = Depends(get_db))-> dict:
    db_image = get_image(db, id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

@app.delete('/images/{image_id}')
async def del_item(image_id: int, db: Session = Depends(get_db))-> dict:
    db_image = del_image(db, id=image_id)
    return {"delete image_id": image_id}

@app.get('/images/count/{info}')
async def count_item(image_id: int, faces: int, time: str, db: Session = Depends(get_db))-> dict:
    db_image_count = count_image(db, id = image_id, faces = faces, time = time)
    return {"count": db_image_count}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")
