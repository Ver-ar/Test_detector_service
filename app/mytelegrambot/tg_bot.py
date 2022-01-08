from aiogram.dispatcher import Dispatcher
import handlers_
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()


dp = Dispatcher(bot=bot, storage=storage)       
handlers_.register_handlers_client(dp)