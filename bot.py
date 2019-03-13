"""Calvin(n5) telegram bot © n05tr0m0"""

import locale
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import bot_hendlers

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
    dp.add_handler(CommandHandler('start', bot_hendlers.start_msg))
    dp.add_handler(CommandHandler('help', bot_hendlers.help_msg))
    dp.add_handler(CommandHandler('planet', bot_hendlers.planet_info, pass_args=True))
    dp.add_handler(CommandHandler('next_full_moon', bot_hendlers.get_next_full_moon, pass_args=True))
    dp.add_handler(CommandHandler('wordcount', bot_hendlers.word_counter, pass_args=True))
    dp.add_handler(CommandHandler('cities', bot_hendlers.cities_game, pass_args=True))
    dp.add_handler(CommandHandler('calc', bot_hendlers.calc, pass_args=True))
    dp.add_handler(CommandHandler('weather', bot_hendlers.get_weather, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, bot_hendlers.calvin_talk))

    calvin_bot.start_polling()
    calvin_bot.idle()


if __name__ == '__main__':
    bot_worker()
