from fastapi import FastAPI, File, HTTPException, Path
from sqlalchemy.sql import schema

from detect_faces import detect
from crud import count_image_faces, create_image, get_image, del_image, get_db, get_notify_users
from models import *
import asyncio

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from mytelegrambot.settings import API_KEY

from mytelegrambot import handlers_
import logging
from mytelegrambot import tg_bot

app = FastAPI()


@app.on_event("startup")
async def launch_bot():
    bot = Bot(token=API_KEY,)
    try:
        dp = tg_bot.dp       
        logging.basicConfig(filename='bot.log', format='%(asctime)s-%(message)s', level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        await dp.start_polling(dp, skip_updates=True)
    finally:
        await bot.close()

asyncio.run(launch_bot())


@app.post('/images/')
async def create_item(image: bytes = File(...)) -> dict:
    faces = detect(image)
    #detect of detect_faces.py
    item = create_image(faces=faces)    
    # puts value faces with int in file write_value.py: db_image = models.Image(faces=faces)
    # value faces assign to value model
    # models.py takes value faces from write_value(class Image) and put faces to value faces of Column in models.py
    return {"image_id" : item, "faces": faces}
    # image_id return value from db, generated from autoincrement

@app.post('/images/bot')
async def search_id(image: bytes = File(...)) -> dict:
    faces = detect(image)
    
    item = create_image(faces=faces)    
    
    id = get_notify_users(faces=faces)

    return {"image_id" : item, "faces": faces, "user_id": id}
    

@app.get('/images/count/faces/{faces}')
async def count_item_faces(faces: int = Path(..., title="The faces on the image to get"))-> dict:
    db_image = count_image_faces(faces = faces)
    if db_image == None:
        raise HTTPException(status_code=404, detail="Image not found")
    else:
        return {"Фото с таким количеством лиц": db_image}

@app.get('/images/{image_id}')
async def get_item(image_id: int = Path(..., gt=0))-> dict:
    db_image = get_image(id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found, id was be deleted")
    else:
        return db_image

@app.get('/images/all/')
async def get_items():
    db_image = get_db()
    if len(db_image) == 0:
        raise HTTPException(status_code=404, detail="Table empty")
    else:
        return db_image


@app.delete('/images/{image_id}')
async def del_item(image_id: int = Path(..., gt=0))-> dict:
    db_image = del_image(id=image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found, id was be deleted")
    else:
        return {"delete image_id": image_id}


