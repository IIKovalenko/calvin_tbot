"""Calvin(n5) telegram bot © n05tr0m0"""

import logging
from datetime import datetime
import locale
from collections import Counter

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem

import utils

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

HELP_TEXT = """
    Доспуные команды:

    /start - показывает приветственное сообщение
    /help - вызывает это сообщение
    /planet <имя планеты> - получите информацию по планете (доступна только Солнечная ситема)
    /next_full_moon <дата> - узнаете ближайшее полнолуние от введённой даты
                    help - подробная справка по команде
    /wordcount <текст> - считает слова в ведъном вашем тексте

    PS.: По мере добавления команд help будет пополняться.
    """


def start_msg(bot, update):
    text = 'Привет, мой друг, я - Кельвин, виртуальный образец инопланетного существа из фильма "Живое".'
    update.message.reply_text('{}\n{}'.format(text, HELP_TEXT))


def help_msg(bot, update):
    update.message.reply_text(HELP_TEXT)


@utils.logging_user_input
def calvin_talk(bot, update):
    """Зеркалирование ввода пользователя"""
    user_text = update.message.text
    update.message.reply_text('Вы написали: {}'.format(user_text))


@utils.logging_user_input
def planet_info(bot, update, args):
    """Получение информации о планете с помощью модуля ephem"""
    planets_list = [
        'Mercury',
        'Venus',
        'Mars',
        'Jupiter',
        'Saturn',
        'Uranus',
        'Neptune',
        'Pluto',
        'Sun',
        'Moon',
    ]
    call_planet = ' '.join(args).title()
    if update.message.text == '/planet':
        update.message.reply_text('Доступный список планет: \n' + '\n'.join(planets_list))
    elif call_planet not in planets_list:
        update.message.reply_text(
            '{} такой планеты нет в списке известных мне планет! \n'
            'Список планет можно посмотреть командой /planet'.format(call_planet)
        )
    elif len(call_planet) >= 2:
        planet = getattr(ephem, call_planet)()
        planet.compute()
        zodiac = ephem.constellation(planet)
        bot.send_message(
            chat_id=update.message.chat.id,
            text='Вы выбрали планету {}. \nОна находится в созвездии {}'.format(
                planet.name,
                zodiac[1],
            )
        )


@utils.logging_user_input
def get_next_full_moon(bot, update, args):
    """Показывает дату ближайшего полнолуния"""
    input_date = ' '.join(args)

    if update.message.text == '/next_full_moon':
        full_moon_date = ephem.next_full_moon(datetime.now())
        update.message.reply_text(
            'Ближайшее полнолуние будет: {}'.format(
                datetime.strptime(str(full_moon_date), '%Y/%m/%d %X').strftime('%d %b %Y'),
            )
        )
    elif update.message.text == '/next_full_moon help':
        update.message.reply_text(
            """
            Справка по команде next_full_moon:
            
            вызов /next_full_moon - показывает ближайшее полнолуние
            вызов /next_full_moon <дата> - показывает ближайшее полнолуние от заданной даты.
            
            Формат даты для ввода: 2019-01-01 (год, месяц, число)
            """
        )

    elif input_date:
        try:
            input_date = datetime.strptime(input_date, '%Y-%m-%d')
        except ValueError:
            update.message.reply_text(
                    'Вы ввели дату не правильно!\nВведите дату в формате 2019-01-01 (год-месяц-день)',
            )
        full_moon_date = ephem.next_full_moon(input_date)
        update.message.reply_text(
            'Полнолуние будет: {}'.format(
                datetime.strptime(str(full_moon_date), '%Y/%m/%d %X').strftime('%d %b %Y'),
            )
        )


@utils.logging_user_input
def word_counter(bot, update, args):
    """Подсчёт слов в отправленном сообщении (тексте)"""
    ignored_symbols = []
    user_text = ' '.join(args).lower().split()
    print(user_text)
    if update.message.text == '/wordcount':
        update.message.reply_text('Введи текст, а я посчитаю слова ;)')
    else:
        word_count = len(user_text)
        update.message.reply_text('Ммм... Я насчитал: {} слов'.format(word_count))


def bot_worker():
    calvin_bot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    logging.info('Calvin launch from space station...')

    dp = calvin_bot.dispatcher
    dp.add_handler(CommandHandler('start', start_msg))
    dp.add_handler(CommandHandler('help', help_msg))
    dp.add_handler(CommandHandler('planet', planet_info, pass_args=True))
    dp.add_handler(CommandHandler('next_full_moon', get_next_full_moon, pass_args=True))
    dp.add_handler(CommandHandler('wordcount', word_counter, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, calvin_talk))

    calvin_bot.start_polling()
    calvin_bot.idle()


if __name__ == '__main__':
    bot_worker()
