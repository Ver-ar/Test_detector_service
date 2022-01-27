from fastapi import FastAPI, File, HTTPException, Path
import uvicorn
from detect_faces import detect
from database_process.crud import count_image_faces, create_image, get_image, del_image, get_db, get_notify_users
from aiogram import Bot
from aiogram import Dispatcher
from mytelegrambot.settings import API_KEY
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from mytelegrambot import handlers_
import logging
import asyncio


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()

logging.basicConfig(filename = 'log.log', format = '%(asctime)s-%(message)s', level=logging.DEBUG)
logger = logging.getLogger()


@app.on_event("startup")
async def launch_bot():
    storage = MemoryStorage()     
    bot = Bot(token=API_KEY)
    app.bot = bot        
    dp = Dispatcher(bot=bot, storage=storage)       
    handlers_.register_handlers_client(dp)
    app.state.polling_task = asyncio.create_task(dp.start_polling(dp))


@app.on_event("shutdown")
async def cancel_me():
    try:
        app.state.polling_task.cancel()    
    finally:
        with open ('log.log', mode = "a") as log:
            log.write ("Application shutdown")       

@app.post('/images/')
async def create_item(image: bytes = File(...)) -> dict:
    faces = detect(image)
    item = create_image(faces=faces)
    users_id = get_notify_users(faces=faces)
    await asyncio.gather(*[app.bot.send_message(ids, f"В базу добавлено фото с id: {item}, количество лиц: {faces}") for ids in users_id])  
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, loop = "asyncio")

