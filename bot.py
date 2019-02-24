import logging
from datetime import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='calvin_bot.log'
)


def start_msg(bot, update):
    text = 'Привет мой друг, я Кельвин, виртуальный образец инопланетного существа из фильма "Живое".'
    logging.info(text)
    update.message.reply_text(text)


def calvin_talk(bot, update):
    t_user = {
        'username': update.message.chat.username,
        'first_name': update.message.chat.first_name,
        'last_name': update.message.chat.last_name,
        'full_name': update.message.chat.first_name + ' ' + update.message.chat.last_name
    }
    user_text = update.message.text
    print('{} - {} пишет: {}'.format(update.message.date, t_user.get('full_name'), update.message.text))
    logging.info(
        "User: %s(%s), Chat ID: %s, Message: %s",
        t_user.get('username'), t_user.get('full_name'), update.message.chat.id, update.message.text
    )
    update.message.reply_text('Вы написали: {}'.format(user_text))


def bot_worker():
    calvin_bot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    logging.info('Calvin launch from space station...')

    dp = calvin_bot.dispatcher
    dp.add_handler(CommandHandler('start', start_msg))
    dp.add_handler(MessageHandler(Filters.text, calvin_talk))

    calvin_bot.start_polling()
    calvin_bot.idle()


bot_worker()
