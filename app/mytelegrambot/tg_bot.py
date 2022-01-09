from aiogram.dispatcher import Dispatcher
from mytelegrambot import handlers_
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from main import bot

storage = MemoryStorage()


dp = Dispatcher(bot=bot, storage=storage)       
handlers_.register_handlers_client(dp)