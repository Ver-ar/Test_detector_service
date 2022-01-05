from aiogram import Bot, Dispatcher
from aiogram.dispatcher import Dispatcher
from settings import API_KEY
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=API_KEY,)
storage = MemoryStorage()

dp = Dispatcher(bot=bot, storage=storage)