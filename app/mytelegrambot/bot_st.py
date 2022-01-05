from aiogram.utils import executor
import client, admin, other
from create_bot import dp


async def on_startup(_):
    print("Вызван бот")





client.register_handlers_client(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)