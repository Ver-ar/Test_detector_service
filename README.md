# Детектор очередей
## Python 3.9.10, Windows 10
____

1. Находясь в папке с проектом, создаем виртуальное окружение:

python 3 -m venv env

3. Активируем и работаем в нем далее:

\env\Scripts\activate

3. Устанавливаем внешние пакеты:

pip install -r requirements.txt

4. Создаем бота в телеграм с помощью BotFather, сохраняем token

5. В \app\mytelegrambot создаем settings.py

```python
API_KEY = "token"
```
6. Запускаем main из cmd:

\app>python main.py

7. Через Postman отправляем фото в get-запросе, получаем ответ, создается БД, с которой далее будет происходить работа, в которой мы можем, с помощью прямых запросов к БД, либо с помощью созданного Telegram бота отслеживать состояние БД, а так же через бота подписаться на рассылку сообщений о пополнении БД новыми фотографиями с необходимым количеством лиц.