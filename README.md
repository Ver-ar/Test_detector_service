# Test_detector_service
## Детектор очередей на кассе
____


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

__crud.py__

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
        result = conn.execute(select_image)
        result_image = result.fetchone() 
        print(f'Выбрано фото c id: {result_image}')
        return result_image

def del_image(id: int):    
    result_del = image_table.delete().where(image_table.c.id == id)
    with engine.begin() as conn:
        result = conn.execute(result_del)
        if result.rowcount == 1:
            print(f'Удалено фото c id: {id}')
            return result
        else:
            return
   
def count_image_faces(faces: int):
    count_table = [func.count('*').label('count'), image_table.c.faces]
    select_count = select(count_table).where(image_table.c.faces == faces)
    with engine.begin() as conn:
        result = conn.execute(select_count)
        result_count = result.fetchone()                             
    return result_count[1]

def get_image_from_faces (faces: int):
    select_image = select(image_table).where(image_table.c.faces == faces)
    with engine.begin() as conn: 
        result = conn.execute(select_image)
        result_image = result.fetchall() 
        print(f'Выбрано фото c количеством лиц: {result_image}')
        return result_image

def get_db():
    select_image = select([image_table])
    with engine.begin() as conn: 
        result = conn.execute(select_image).fetchall()             
        return result    

```
5. Обновляем main, чтоб данные из FastAPI запросов автоматически записывались в бд при их вызове:

__main.py__

```python

from fastapi import FastAPI, File, HTTPException, Path
import uvicorn
from detect_faces import detect
from crud import count_image_faces, count_image_id, create_image, get_image, del_image
from models import *


app = FastAPI()


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
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="debug")

```
5. Добавляем бота aiogram, который будет отвечать пользователю на запросы к бд:

Запуск бота из __main.py__

```python

@app.on_event("startup")
async def launch_bot():
    storage = MemoryStorage()     
    bot = Bot(token=API_KEY)
    app.bot = bot        
    dp = Dispatcher(bot=bot, storage=storage)       
    logging.basicConfig(filename='bot.log', format='%(asctime)s-%(message)s', level=logging.DEBUG)
    handlers_.register_handlers_client(dp)
    asyncio.create_task(dp.start_polling(dp))
    
logger = logging.getLogger(__name__)

```
Добавяем функцию рассылки ботом уведомлений пользователям об обновлении бд по ранее введенным запросам от пользователей

```python

@app.post('/images/')
async def create_item(image: bytes = File(...)) -> dict:

    faces = detect(image)
    item = create_image(faces=faces)
    users_id = get_notify_users(faces=faces)
    for ids in users_id:
        await app.bot.send_message(ids, f"В базу добавлено фото с id: {item}, количество лиц: {faces}")
    return {"image_id" : item, "faces": faces}

```
Обновляем модули __models.py__ и __crud.py__:
  
+ Добавляем бд для бота, в которой он будет хранить id пользователей и их запросы к нему:

```python

bot_table = Table ('bot_users', meta,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('user_id', Integer, autoincrement=False),
    Column('face_from_user', Integer, autoincrement=False)
    )
```
+ Добавляем функции подсчета id пользователей из бд бота и извлечениия и добавления id пользователей для дальнейшей рассылки сообщений по запросам:

```python

def get_notify_users(faces: int):
    select_image = select(bot_table).where(bot_table.c.face_from_user == faces)
    with engine.begin() as conn:
        result = conn.execute(select_image)
        result_id = result.fetchall()
        list_users_id = []
        for a in result_id:
            list_users_id.append(a[1])
        return list_users_id

def create_users(faces, user_id):
    exist = select(bot_table).where(bot_table.c.face_from_user == faces, bot_table.c.user_id == user_id)
    print(exist)

    with engine.begin() as conn:
        result = conn.execute(exist)
        result_ex = result.fetchone()
        if result_ex == None:
            res = conn.execute(bot_table.insert(),{'face_from_user': faces,'user_id': user_id})     
            print(res)
            return (f'В базу бота внесены новые данные:user_id: {user_id} и количество отслеживаемых лиц: {faces}')            
        else:
            return(f'В базе уже есть это значение, попробуй ввести другое с командой /faces')

```

6. Модуль с функциями бота aiogram __handlers.py__:

```python

from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from models import *
from aiogram.types.message import ContentType
from crud import get_image_from_faces, get_image, del_image, get_db, get_notify_users, create_users
from detect_faces import *
from aiogram.dispatcher.filters.state import State, StatesGroup


conn = engine.connect()

class Track(StatesGroup):
    faces = State()

class Get(StatesGroup):
    get_faces = State()

class View(StatesGroup):
    view_faces = State()

class Del(StatesGroup):
    del_id = State()

class GetID(StatesGroup):
    get_id = State()

#help
async def help_menu(message: types.Message):
    await message.reply(
        text='''
    Мои команды:
    /view - показать всю базу с фото
    /faces - ввести количество лиц для отслеживания
    /getface - получить данные по количеству лиц
    /getid - получить данные по фото-id
    /del - удалить фото с необходимым id
    /cancel - выйти из цикла команды
    ''',
            reply=False,
    )

#start
async def send_welcome(message: types.Message):
    await message.reply('Привет! С моей помощью ты можешь отслеживать состояние базы данных с определением количества лиц на фото. Вывести меню команд - /help')
    await help_menu(message=message)

async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Выполнение команды прервано')

#view
async def view_all(message: types.Message):
    photo_list = get_db()
    await message.reply("\n".join(f'id: {a[0]}, количество лиц: {a[1]}, дата и время: {a[2]}' for a in photo_list))

#faces
async def write_value_from_user(message: types.Message):
    await Track.faces.set()
    await message.reply("Введи количество лиц, которое ты хочешь отслеживать:")

async def value_send_func_faces(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.reply("Введи целое число:")
    else:
        user_id = message.chat.id
        faces=int(message.text)
        
    await message.reply(create_users(faces, user_id))

    await state.finish()

async def send_images_faces(message: types.Message):
    await Get.get_faces.set()
    await message.reply('Введи нужное количество лиц на фото:')

async def value_send_func_getface(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.reply("Введи целое число:")
    else:
        faces=int(message.text)
        photo_list = get_image_from_faces(faces)
    if len(photo_list) !=0: 
        await message.reply("\n".join(f'id: {a[0]}, количество лиц: {a[1]}, дата и время: {a[2]}' for a in photo_list))
    else:
        await message.reply(f"Фото с таким количеством лиц не найдено, возможно оно еще не добавлено или удалено")
    await state.finish()         

#getid
async def send_images_id(message: types.Message):
    await GetID.get_id.set()
    await message.reply('Введи интересующий id фото:')

async def value_send_func_getid(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.reply("Введи целое число:")
    else:
        id_image=int(message.text)
        a = get_image(id_image) 
        if a is not None:
            await message.reply(f"id: {a[0]}, количество лиц: {a[1]}")
        else:
            await message.reply(f"Фото с таким id не найдено, возможно оно еще не добавлено или удалено")
        await state.finish()

#del
async def del_images(message: types.Message):    
    await message.reply('Введи нужный id:')
    await Del.del_id.set()

async def value_send_func_del(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.reply("Введи целое число:")
    else:
        id_image=int(message.text)
        a = del_image(id_image)    
        if a is not None: 
            await message.reply(f"Удалено фото с id: {id_image}") 
        else: 
            await message.reply(f"Фото с таким id не найдено, возможно оно еще не добавлено или удалено") 
        await state.finish()

#ContentType.ANY
async def unknown_message(message: types.Message):
    await message.answer("Ничего не понятно, но очень интересно:) Введи /help, чтоб посмотреть интересующую тебя команду")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])

    dp.register_message_handler(write_value_from_user, commands=['faces'],  state="*")
    dp.register_message_handler(value_send_func_faces, state = Track.faces)
  
    dp.register_message_handler(send_images_faces, commands=['getface'],  state="*")
    dp.register_message_handler(value_send_func_getface, state = Get.get_faces)

    dp.register_message_handler(send_images_id, commands=['getid'], state="*")
    dp.register_message_handler(value_send_func_getid, state = GetID.get_id)
    
    dp.register_message_handler(del_images, commands=['del'], state="*")
    dp.register_message_handler(value_send_func_del, state = Del.del_id)

    dp.register_message_handler(help_menu, commands=['help'])

    dp.register_message_handler(view_all, commands=['view'])

    dp.register_message_handler(cmd_cancel, commands=['cancel'], state="*")

    dp.register_message_handler(unknown_message, content_types = ContentType.ANY)

```