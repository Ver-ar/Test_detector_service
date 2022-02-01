from fastapi import FastAPI, File, HTTPException, Path
import uvicorn
from detect_faces import detect
from database_process.crud import count_image_faces, create_image, get_image_with_id, del_image, get_db, get_notify_users
from aiogram import Bot
from aiogram import Dispatcher
from mytelegrambot.settings import API_KEY
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from mytelegrambot import handlers_
import asyncio
import concurrent.futures
from database_process.models import engine, meta

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()

@app.on_event("startup")
async def launch_bot():
    storage = MemoryStorage()     
    bot = Bot(token=API_KEY)
    app.bot = bot        
    dp = Dispatcher(bot=bot, storage=storage)       
    handlers_.register_handlers_client(dp)
    app.state.polling_task = asyncio.create_task(dp.start_polling(dp))

@app.on_event("startup")
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)


@app.on_event("shutdown")
async def cancel_me():
    app.state.polling_task.cancel()    
     

@app.on_event("shutdown")
async def close_db():
    await engine.dispose()

@app.post('/images/')
async def create_item(image: bytes = File(...)) -> dict:
    loop = asyncio.get_running_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        faces = await loop.run_in_executor(pool, detect, image)
    item = await create_image(faces=faces)
    users_id = await get_notify_users(faces=faces)
    await asyncio.gather(*[app.bot.send_message(id, f"В базу добавлено фото с id: {item}, количество лиц: {faces}") for id in users_id])  
    return {"image_id" : item, "faces": faces}

@app.get('/images/count/faces/{faces}')
async def count_item_faces(faces: int = Path(..., title="The faces on the image to get"))-> dict:
    images_db = await count_image_faces(faces = faces)
    if images_db == None:
        raise HTTPException(status_code=404, detail="Image not found")
    else:
        return {"Фото с таким количеством лиц": images_db}

@app.get('/images/{image_id}')
async def get_item(image_id: int = Path(..., gt=0))-> dict:
    images_db = await get_image_with_id(id=image_id)
    if images_db is None:
        raise HTTPException(status_code=404, detail="Image not found, id was be deleted")
    else:
        return images_db

@app.get('/images/all/')
async def get_items():
    images_db = await get_db()
    if len(images_db) == 0:
        raise HTTPException(status_code=404, detail="Table empty")
    else:
        return images_db


@app.delete('/images/{image_id}')
async def del_item(image_id: int = Path(..., gt=0))-> dict:
    images_db = await del_image(id=image_id)
    if not images_db:
        raise HTTPException(status_code=404, detail="Image not found, id was be deleted")
    else:
        return {"delete image_id": image_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, loop = "asyncio")
