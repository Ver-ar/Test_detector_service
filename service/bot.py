import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

import telegram
import settings 
import sys
import os
from sqlalchemy import create_engine, MetaData
from models import *

conn = engine.connect()

logging.basicConfig(filename='bot.log', format='%(asctime)s-%(message)s', level=logging.INFO) #обозначаем куда будут записываться логи, дату, время и номер сообщения. И показывает уровень важности сообщений, которые будут выведены

logger = logging.getLogger(__name__)

#определяем функцию greet_user
def greet_user(update, context):
    print("Вызван /start")
    update.message.reply_text('Привет! С моей помощью ты можешь отслеживать количество лиц на фото в базе данных с помощью команды /face_track')
    user_id = update.message.chat.id
    with engine.begin() as conn: 
        result = conn.execute(bot_table.insert(),{'user_id': user_id})
        return result
    #user = update.message.from_user
    #user_data = context.user_data
    

    print(update)

def talk_to_me(update, context):
    text = update.message.text 
    print(text)
    update.message.reply_text(text)

def face_track(update, context):
  update.message.reply_text('Введите количество лиц, которое Вы хотите отслеживать:')
  print("Вызван /word_count")

def sentence_check(update, context):
    text = update.message.text
    if text.strip():
        text_split=text.split()
        count=len(text_split)
        if count == 0:
            update.message.reply_text(f"Пустая строка, введите значение:")
    print(update)

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! Hope to see you again next time.')
    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


#1. Запускаем бота
def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("wordcount", face_track))
    dp.add_handler(MessageHandler(Filters.text, sentence_check))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    logging.info("The bot was launched") 
    mybot.polling(none_stop = True)
    mybot.idle()

if __name__ == "__main__":
    main()
