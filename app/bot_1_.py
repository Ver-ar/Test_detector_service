import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentType
from aiogram.utils import executor
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from write_value import get_image_from_faces, get_image, del_image, get_db
from mytelegrambot.bot import Track, Get, Del, GetID
from models import *
from detect_faces import *
import string
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import text

bot = Bot(token="5096933168:AAGk0iiOi4U3ZeUib74Kq1KkOpZlZCpUQN0",)
storage = MemoryStorage()

dp = Dispatcher(bot=bot, storage=storage)


async def on_startup(_):
    print("Вызван бот")

conn = engine.connect()


logging.basicConfig(filename='bot.log', format='%(asctime)s-%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


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




@dp.message_handler(commands=['help'])
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


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply('Привет! С моей помощью ты можешь отслеживать состояние базы данных с определением количества лиц на фото. Вывести меню команд - /help')
    user_id = message.chat.id
    with engine.begin() as conn: 
        conn.execute(bot_table.insert(),{'user_id': user_id})
    print(user_id)
    await help_menu(message=message)


################################################

@dp.message_handler(commands=['view'])
async def wiew_all(message: types.Message):
    list_db = get_db()
    await message.reply('Список фото из базы:' 'list_db')

################################################

@dp.message_handler(commands=['faces'])
async def write_value_from_user(message: types.Message):
    await Track.faces.set()
    await message.reply("Введи количество лиц, которое ты хочешь отслеживать:")


@dp.message_handler(state=Track.faces)
async def value_send(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    for i in message.text.split(' '):
        i = i.lower().translate(str.maketrans('', '', string.punctuation))
        if i.isnumeric():
            i = int(i)            
            with engine.begin() as conn: 
                conn.execute(bot_table.insert(),{'face_from_user': i,'user_id': user_id})
            print('faces')
            await state.finish()


################################################

@dp.message_handler(commands=['getface'])
async def send_images(message: types.Message):
    await Get.get_faces.set()
    await message.reply('Введи нужное количество лиц на фото:')

@dp.message_handler(state=Get.get_faces)
async def value_send(message: types.Message, state: FSMContext):
    for i in message.text.split(' '):
        i = i.lower().translate(str.maketrans('', '', string.punctuation))
        if i.isnumeric():
            i = int(i)            
        print(get_image_from_faces(i))
        print('get')
        await message.reply(get_image_from_faces(i))

        await state.finish()

################################################

@dp.message_handler(commands=['getid'])
async def send_images(message: types.Message):
    await GetID.get_id.set()
    await message.reply('Введи интересующий id фото:')

@dp.message_handler(state=GetID.get_id)
async def value_send(message: types.Message, state: FSMContext):
    if message.text != "/cancel":
        for i in message.text.split(' '):
            i = i.lower().translate(str.maketrans('', '', string.punctuation))
            if i.isnumeric():
                i = int(i)
                if i != None:
                    print(get_image(i))
                    await message.reply(get_image(i))
                else:
                    await message.reply('Такого id нет в базе')
                    return
            else:
                await message.reply('Введи целое число:')
                return
    await state.finish()

################################################

@dp.message_handler(commands=['del'])
async def del_images(message: types.Message):
    await Del.del_id.set()
    await message.reply('Введи нужный id:')

@dp.message_handler(state=Del.del_id)
async def value_send(message: types.Message, state: FSMContext):
    for i in message.text.split(' '):
        i = i.lower().translate(str.maketrans('', '', string.punctuation))
        if i.isnumeric():
            i = int(i)            
        print(del_image(i))
        message.text = text('hgf{i}')
        await message.reply(text)

        await state.finish()

################################################
  
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')

###############################################
@dp.message_handler(content_types = ContentType.ANY)
async def unknown_message(message: types.Message):
    await message.answer("Ничего не понятно, но очень интересно:) Введи /help, чтоб посмотреть интересующую тебя команду")

'''
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(write_value_from_user, commands=['faces'])  
    dp.register_message_handler(send_images, commands=['getid'])    
    dp.register_message_handler(del_images, commands=['del'])
    dp.register_message_handler(help_menu, commands=['help'])
    dp.register_message_handler(wiew_all, commands=['view'])
    dp.register_message_handler(cancel_handler, commands=['cancel'])

register_handlers_client(dp)
'''
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


'''
if not db_image:
        raise HTTPException(status_code=404, detail="Image not found, id was be deleted")
    else:
        return {"delete image_id": db_image}
'''