from aiogram import types, Dispatcher
from sqlalchemy import select
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from .. import write_value
from mytelegrambot.bot import Track, Get, Del, GetID
from .. import models

from ..detect_faces import *
from create_bot import dp
import string
import os.path as path



conn = models.engine.connect()

#@dp.message_handler(commands=['help'])
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


#@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Привет! С моей помощью ты можешь отслеживать состояние базы данных с определением количества лиц на фото. Вывести меню команд - /help')
    user_id = message.chat.id
    with models.engine.begin() as conn: 
        conn.execute(models.bot_table.insert(),{'user_id': user_id})
    print(user_id)
    await help_menu(message=message)


################################################

#@dp.message_handler(commands=['view'])
async def wiew_all(message: types.Message):
    await message.reply("Список фото из базы:{}")

################################################

#@dp.message_handler(commands=['faces'])
async def write_value_from_user(message: types.Message):
    await Track.faces.set()
    await message.reply("Введи количество лиц, которое ты хочешь отслеживать:")


#@dp.message_handler(state=Track.faces)
async def value_send(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    for i in message.text.split(' '):
        i = i.lower().translate(str.maketrans('', '', string.punctuation))
        if i.isnumeric():
            i = int(i)            
            with models.engine.begin() as conn: 
                conn.execute(models.bot_table.insert(),{'face_from_user': i,'user_id': user_id})
            print('faces')
            await state.finish()


################################################

#@dp.message_handler(commands=['getface'])
async def send_images(message: types.Message):
    await Get.get_faces.set()
    await message.reply('Введи нужное количество лиц на фото:')

#@dp.message_handler(state=Get.get_faces)
async def value_send(message: types.Message, state: FSMContext):
    for i in message.text.split(' '):
        i = i.lower().translate(str.maketrans('', '', string.punctuation))
        if i.isnumeric():
            i = int(i)            
        print(write_value.get_image_faces(i))
        print('get')
        await message.reply(write_value.get_image_faces(i))

        await state.finish()

################################################

#@dp.message_handler(commands=['getid'])
async def send_images(message: types.Message):
    await GetID.get_id.set()
    await message.reply('Введи нужное количество лиц на фото:')

#@dp.message_handler(state=GetID.get_id)
async def value_send(message: types.Message, state: FSMContext):
    for i in message.text.split(' '):
        i = i.lower().translate(str.maketrans('', '', string.punctuation))
        if i.isnumeric():
            i = int(i)            
        print(write_value.get_image(i))
        print('getid')
        await message.reply(write_value.get_image(i))

        await state.finish()

################################################

#@dp.message_handler(commands=['del'])
async def del_images(message: types.Message):
    await Del.del_id.set()
    await message.reply('Введи нужный id:')

#@dp.message_handler(state=Del.del_id)
async def value_send(message: types.Message, state: FSMContext):
    for i in message.text.split(' '):
        i = i.lower().translate(str.maketrans('', '', string.punctuation))
        if i.isnumeric():
            i = int(i)            
        print(write_value.del_image(i))
        await message.reply(write_value.del_image(i))

        await state.finish()

################################################
  
#@dp.message_handler(state='*', commands='cancel')
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')

###############################################



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(write_value_from_user, commands=['faces'])  
    dp.register_message_handler(send_images, commands=['getid'])    
    dp.register_message_handler(del_images, commands=['del'])
    dp.register_message_handler(help_menu, commands=['help'])
    dp.register_message_handler(wiew_all, commands=['view'])
    dp.register_message_handler(cancel_handler, commands=['cancel'])
