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