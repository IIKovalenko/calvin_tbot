import logging
from datetime import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem

import settings


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='calvin_bot.log'
)


def start_msg(bot, update):
    text = 'Привет, мой друг, я - Кельвин, виртуальный образец инопланетного существа из фильма "Живое".'
    logging.info(text)
    update.message.reply_text(text)


def help_msg(bot, update):
    help_text = """
    Доспуные команды:
    
    /help - вызывает это сообщение
    /planet <имя планеты> - получите информацию по планете (доступна только Солнечная ситема)
    /start - показывает приветственное сообщение
    
    
    PS.: По мере добавления команд help будет пополняться.
     """
    logging.info('Вызвана команда /help')
    update.message.reply_text(help_text)


def calvin_talk(bot, update):
    t_user = {
        'username': update.message.chat.username,
        'first_name': update.message.chat.first_name,
        'last_name': update.message.chat.last_name,
        'full_name': update.message.chat.first_name + ' ' + update.message.chat.last_name
    }
    user_text = update.message.text
    logging.info(
        "User: %s(%s), Chat ID: %s, Message: %s",
        t_user['username'], t_user['full_name'], update.message.chat.id, update.message.text
    )
    # для теста (на проде этот принт уйдёт)
    print('{} - {} пишет: {}'.format(update.message.date, t_user['full_name'], update.message.text))
    update.message.reply_text('Вы написали: {}'.format(user_text))


def planet_info(bot, update):
    """Получение информации о планете с помощью модуля ephem"""
    logging.info('Вызвана команда /planet')
    astro_obj = update.message.text.split()
    astro_obj = getattr(ephem, astro_obj[1])
    planet = astro_obj()
    planet.compute()
    zodiac = ephem.constellation(planet)
    bot.send_message(
        chat_id=update.message.chat.id,
        text='Вы выбрали планету {}. Она находится в созвездии {}'.format(
            planet.name,
            zodiac[1]
        )
    )


def bot_worker():
    calvin_bot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    logging.info('Calvin launch from space station...')

    dp = calvin_bot.dispatcher
    dp.add_handler(CommandHandler('start', start_msg))
    dp.add_handler(CommandHandler('help', help_msg))
    dp.add_handler(CommandHandler('planet', planet_info))
    dp.add_handler(MessageHandler(Filters.text, calvin_talk))

    calvin_bot.start_polling()
    calvin_bot.idle()


bot_worker()
