import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
#каждый раз, когда мы пишем код, который обращается к серверу - нужно смотреть наличие бибилиотеки и читать мануал, где написано каким способом мы можем сделать Update (КББТ)
#CommandHandler - класс, который создали разработчики python-telegram-bot, который обрабатывает введенные от пользователя команды (КББТ)

import settings #импортируем данные из файла settings - далее везде, где есть ссылки на этот файл - заменяем значения переменными из settings

logging.basicConfig(filename='bot.log', format='%(asctime)s-%(message)s', level=logging.INFO) #обозначаем куда будут записываться логи, дату, время и номер сообщения. И показывает уровень важности сообщений, которые будут выведены


PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}
#обходим блокировку proxy. Можно менять t2 на t1 или t3 - в зависимости от загрузки сервера

#определяем функцию greet_user
def greet_user(update, context):
    print("Вызван /start") #выводит в консоль сообщение, какую команду ввел пользователь
    update.message.reply_text('Привет!') #выводит сообщение пользователю непосредственно в боте (КББТ)
    print(update) #выводит информацию о пользователе
#greet_user запускает 2 переменные: update - информация, которая нам пришла с платформы Телеграм - команда старт, информация о пользователе, который ввел команду. context - функция, с помощью которой мы отдаем команды боту, который нас вызвал

def talk_to_me(update, context):
    text = update.message.text #здесь хранятся входящие сообщения от пользователя
    print(text)
    update.message.reply_text(text)
#talk_to_me 1. назначаем в text принимает  входящее сообщение update.message.text (КББТ) 2. Печатаем сообщение в консоль 3. с помощью update.message.reply_text(text)(КББТ) отправляем пользователю его же сообщение

def word_count(update, context):
  update.message.reply_text('Введите предложение:')
  print("Вызван /word_count")

def word_find(update, context):
    text = update.message.text
    if text.strip():
        text_split=text.split()
        count=len(text_split)
        if count%10 == 1 and count!=11 and count%100 != 11:
            update.message.reply_text(f"{count} слово")
        elif count%10 == 2 and count!=12 and count%100!=12:  
            update.message.reply_text(f"{count} слова")
        elif count%10 == 3 and count!=13 and count%100!=13:  
            update.message.reply_text(f"{count} слова")
        elif count%10 == 4 and count!=14 and count%100!=14:
            update.message.reply_text(f"{count} слова")
        else:
            update.message.reply_text(f"{count} слов")
    else:
        update.message.reply_text(f"Пустая строка")
    print(update) #выводит информацию о пользователе


#1. Запускаем бота
def main():
#определяем функцию main
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    #тут бот с помощью ключа от BotFather из поиска в Телеграме авторизуется на сервере телеграм. use_context=True - команда для обновления библиотеки - дело в самой этой библиотеке, так сделали разработчики
    #request_kwargs=PROXY обращается к прокси

    dp = mybot.dispatcher
    #определяем переменной dp диспетчера, который ищет определен ли CommandHandler к введенной пользователем команде, и если находит, то передает эту задачу обработчику, который эту функцию (действие) выполняет (КББТ)
    dp.add_handler(CommandHandler("start", greet_user))
    #добавляем к диспетчеру бота обработчик - Commandhandler, которому в скобках прописываем действие на введенную команду - в данном случае - на start функцией greet_user. Команду start пишем без косой черточки /, так как так указано в библиотеке разработчиками, эти вещи нужно уточнить(КББТ)
    dp.add_handler(CommandHandler("wordcount", word_count))
    dp.add_handler(MessageHandler(Filters.text, word_find))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    logging.info("The bot was launched") #залогирует в файле bot.log, что бот запущен в строке "INFO:root:The bot was launched"
    mybot.start_polling()
    #регулярные частые обращения за обновлением - бот несколько раз в секунду посылает сообщение на сервер Телеграм, чтоб узнать - написал ли ему кто-то, на что он может выдать ответ в соответствии с кодом (КББТ)
    mybot.idle()
    #эта команда для того, чтоб бот работал постоянно, крутил программу, которая в него заложена (типа цикла while True) (КББТ)

if __name__ == "__main__":
    main()
#вызываем функцию main