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
    #detect of detect_faces.py
    item = create_image(faces=faces)    
    # puts value faces with int in (faces: int)
    # models.py takes value faces from write_value and put faces to value faces of Column in models.py
    return {"image_id" : item, "faces": faces}
    # image_id return value from db, generated from autoincrement

@app.get('/images/count/image_id/{image_id}')
async def count_item_id(image_id: int = Path(..., title="The ID of the image to get", gt=0))-> dict:
    db_image = count_image_id(id = image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

@app.get('/images/count/faces/{faces}')
async def count_item_faces(faces: int = Path(..., title="The faces on the image to get", gt=0))-> dict:
    db_image = count_image_faces(faces = faces)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image


@app.get('/images/{image_id}')
async def get_item(image_id: int = Path(..., gt=0))-> dict:
    db_image = get_image(id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found, id was be deleted")
    return db_image

@app.delete('/images/{image_id}')
async def del_item(image_id: int = Path(..., gt=0))-> dict:
    db_image = del_image(id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"delete image_id": db_image}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")
