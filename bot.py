"""Calvin(n5) telegram bot © n05tr0m0"""

import locale
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import bot_handlers

try:
    import settings
except ImportError:
    raise ImportError(
        """
        Модуль settings, не импортирован, так как его нет в текущей директории.
        Создайте или скопируйте модуль с настройками в текую папку для запуска бота.
        """
    )

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='calvin_bot.log'
)

locale.setlocale(locale.LC_ALL, 'ru_RU')


def bot_worker():
    calvin_bot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    logging.info('Calvin launch from space station...')

    dp = calvin_bot.dispatcher
    dp.add_handler(CommandHandler('start', bot_handlers.start_msg))
    dp.add_handler(CommandHandler('help', bot_handlers.help_msg))
    dp.add_handler(CommandHandler('planet', bot_handlers.planet_info, pass_args=True))
    dp.add_handler(CommandHandler('next_full_moon', bot_handlers.get_next_full_moon, pass_args=True))
    dp.add_handler(CommandHandler('wordcount', bot_handlers.word_counter, pass_args=True))
    dp.add_handler(CommandHandler('cities', bot_handlers.cities_game, pass_args=True))
    dp.add_handler(CommandHandler('calc', bot_handlers.calc, pass_args=True))
    dp.add_handler(CommandHandler('weather', bot_handlers.get_weather, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, bot_handlers.calvin_talk))

    calvin_bot.start_polling()
    calvin_bot.idle()


if __name__ == '__main__':
    bot_worker()
