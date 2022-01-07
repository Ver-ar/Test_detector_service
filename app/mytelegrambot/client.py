from aiogram import types
from aiogram.dispatcher import FSMContext
from mytelegrambot.bot import Track, Get, Del, GetID
from .. import models
from create_bot import dp
from aiogram.types.message import ContentType
from write_value import get_image_from_faces, get_image, del_image, get_db
from models import *
from detect_faces import *
from aiogram.dispatcher import Dispatcher



conn = models.engine.connect()


#dp.message_handler(commands=['help'])
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
    with engine.begin() as conn: 
        conn.execute(bot_table.insert(),{'user_id': user_id})
    print(user_id)
    await help_menu(message=message)

#@dp.message_handler(state='*', commands='cancel')
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.finish()
    await message.reply('Выполнение команды прервано')
################################################

#@dp.message_handler(commands=['view'])
async def view_all(message: types.Message):
    photo_list = get_db()
    photo_list_view=[]
    count=len(photo_list)
    while count!=0:
        new_value = 'id фото: {photo_list[0][0]}, количество лиц: {photo_list[0][1]}'.format(photo_list=photo_list)
        photo_list_view.append(new_value)
        photo_list.pop(0)
        count-=1
        
    await message.reply('\n'.join(photo_list_view))
################################################

#@dp.message_handler(commands=['faces'])
async def write_value_from_user(message: types.Message):
    await Track.faces.set()
    await message.reply("Введи количество лиц, которое ты хочешь отслеживать:")

#@dp.message_handler(lambda message: not message.text.isdigit(), state=Track.faces)
async def value_send_invalid(message: types.Message):
    return await message.reply("Введи целое число:")


#@dp.message_handler(lambda message: message.text.isdigit(), state=Track.faces)
async def value_send(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    faces=int(message.text)
    with engine.begin() as conn: 
        conn.execute(bot_table.insert(),{'face_from_user': faces,'user_id': user_id})
        print(f'В базу бота внесены новые данные:user_id: {user_id} и количество отслеживаемых лиц: {faces}')
    await message.reply(f"Данные для отслеживания сохранены")
    await state.finish()



################################################

#@dp.message_handler(commands=['getface'])
async def send_images(message: types.Message):
    await Get.get_faces.set()
    await message.reply('Введи нужное количество лиц на фото:')


#@dp.message_handler(lambda message: not message.text.isdigit(), state=Get.get_faces)
async def value_send_invalid(message: types.Message):
    return await message.reply("Введи целое число:")

#@dp.message_handler(lambda message: message.text.isdigit(), state=Get.get_faces)
async def value_send(message: types.Message, state: FSMContext):
    id_image=int(message.text)
    photo_list = get_image_from_faces(id_image)
        
    if len(photo_list) !=0: 
        photo_list_view=[]
        count=len(photo_list)
        while count!=0:
            new_value = 'id фото: {photo_list[0][0]}, количество лиц: {photo_list[0][1]}'.format(photo_list=photo_list)
            photo_list_view.append(new_value)
            photo_list.pop(0)
            count-=1
            await message.reply(f"Найдено {len(photo_list_view)} фото с указанным количеством лиц: {photo_list_view}")
    else:
        await message.reply(f"Фото с таким id не найдено, возможно оно еще не добавлено или удалено")
    await state.finish()

################################################

#@dp.message_handler(commands=['getid'])
async def send_images(message: types.Message):
    await GetID.get_id.set()
    await message.reply('Введи интересующий id фото:')

#@dp.message_handler(lambda message: not message.text.isdigit(), state=GetID.get_id)
async def value_send_invalid(message: types.Message):
    return await message.reply("Введи целое число:")

#@dp.message_handler(lambda message: message.text.isdigit(), state=GetID.get_id)
async def value_send(message: types.Message, state: FSMContext):
    id_image=int(message.text)
    a = get_image(id_image)    
    if a is not None:
        await message.reply(f"id: {a[0]}, количество лиц: {a[1]}")
    else:
        await message.reply(f"Фото с таким id не найдено, возможно оно еще не добавлено или удалено")
    await state.finish()

################################################

#@dp.message_handler(commands=['del'])
async def del_images(message: types.Message):
    await Del.del_id.set()
    await message.reply('Введи нужный id:')

#@dp.message_handler(lambda message: not message.text.isdigit(), state=Del.del_id)
async def value_send_invalid(message: types.Message):
    return await message.reply("Введи целое число:")

#@dp.message_handler(lambda message: message.text.isdigit(), state=Del.del_id)
async def value_send(message: types.Message, state: FSMContext):
    id_image=int(message.text)
    a = del_image(id_image)    
    if a is not None: 
        await message.reply(f"Удалено фото с id: {id_image}") 
    else: #проверка не работает
        await message.reply(f"Фото с таким id не найдено, возможно оно еще не добавлено или удалено") 
    await state.finish()

###############################################
#@dp.message_handler(content_types = ContentType.ANY)
async def unknown_message(message: types.Message):
    await message.answer("Ничего не понятно, но очень интересно:) Введи /help, чтоб посмотреть интересующую тебя команду")



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(write_value_from_user, commands=['faces'])  
    dp.register_message_handler(send_images, commands=['getid'])    
    dp.register_message_handler(del_images, commands=['del'])
    dp.register_message_handler(help_menu, commands=['help'])
    dp.register_message_handler(view_all, commands=['view'])
    dp.register_message_handler(cancel_handler, commands=['cancel'])
    dp.register_message_handler(unknown_message, content_types = ContentType.ANY)

register_handlers_client(dp)
