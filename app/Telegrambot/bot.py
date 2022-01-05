from aiogram.utils import executor
from aiogram.bot import api
import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
import handlers.client, handlers.admin, handlers.other

logging.basicConfig(filename='bot.log', format='%(asctime)s-%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def on_startup(_):
    print("Вызван бот")



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

handlers.client.register_handlers_client(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)