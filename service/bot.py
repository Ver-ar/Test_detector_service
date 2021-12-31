import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from sqlalchemy import select
import settings 
from models import *

conn = engine.connect()

logging.basicConfig(filename='bot.log', format='%(asctime)s-%(message)s', level=logging.INFO) #обозначаем куда будут записываться логи, дату, время и номер сообщения. И показывает уровень важности сообщений, которые будут выведены

logger = logging.getLogger(__name__)


def greet_user(update, context):
    print("Вызван /start")
    update.message.reply_text('Привет! С моей помощью ты можешь отслеживать количество лиц на фото в базе данных с помощью команды /face_track')
    user_id = update.message.chat.id
    with engine.begin() as conn: 
        result = conn.execute(bot_table.insert(),{'user_id': user_id})
        print(update)
        return result

def database_start(update, context):
    print("Вызван database_start")
    update.message.reply_text(f'Введите количество лиц, которое Вы хотите отслеживать:')
    return "number"

def database_value(update, context):
    msg_value = update.message.text
    if type(msg_value) != int:
        update.message.reply_text(f'Пожалуйста, введите целое число')
        return "number"  
    else:
        context.user_data["numbers"] = {"number": msg_value}      
        def count_image_faces(msg_value):
            photo_list = select([image_table]).where(image_table.c.faces == msg_value)
            with engine.begin() as conn:
                result = conn.execute(photo_list.fetchall())
                photo_count = sum([len(element) for element in photo_list])
                print_list = str(result).replace("[", "").replace("]", "").replace("'", "").replace("(')", "").replace(")", "")                           
            update.message.reply_text (f'Есть {photo_count} фото с указанным количеством лиц в списке. Список фото: {print_list}')
        count_image_faces(msg_value)

def request_incorrect(update, context):
    update.message.reply_text(f'Некорректный ввод, введите число')

'''
def cancel(update, context):
    user = update.message.from_user
    logger.info("Пользователь %s завершил общение.", user.first_name)
    update.message.reply_text('Пока!')
    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

'''

def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher

    
    database_request = ConversationHandler(
        entry_points=[
            (CommandHandler("face_track", database_start), database_start)],
        states={
            "number": [MessageHandler(Filters.text, database_value)]
            },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.audio | Filters.sticker | Filters.video | Filters.voice | Filters.location 
            | Filters.document | Filters.animation , request_incorrect)
        ]
    )

    dp.add_handler(database_request)

    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, greet_user))
   
    
    logging.info("The bot was launched") 
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
