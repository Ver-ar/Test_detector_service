from fastapi import FastAPI, File, HTTPException, Path
from detect_faces import detect
from crud import count_image_faces, create_image, get_image, del_image, get_db, get_notify_users
from models import *

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from mytelegrambot.settings import API_KEY
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from mytelegrambot import handlers_
import logging
import asyncio


app = FastAPI()

#app.bot = bot

    
@app.on_event("startup")
async def launch_bot():
    bot = Bot(token=API_KEY)
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)       
    logging.basicConfig(filename='bot.log', format='%(asctime)s-%(message)s', level=logging.DEBUG)
    #logger = logging.getLogger(__name__)
    handlers_.register_handlers_client(dp)
    asyncio.create_task(dp.start_polling(dp,))
    await asyncio.sleep(1)
logger = logging.getLogger(__name__)


@app.post('/images/')
async def create_item(image: bytes = File(...)) -> dict:
    faces = detect(image)
    item = create_image(faces=faces)    
    return {"image_id" : item, "faces": faces}
  
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