"""Calvin(n5) telegram bot © n05tr0m0"""

import locale
import logging
import re
from datetime import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem

import utils
import cities

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
    
    /calc <мат. выражение> - Кельвин посчитает за вас :)
            help - вызывает справку по калькулятору
    /planet <имя планеты> - получите информацию по планете (доступна только Солнечная ситема)
    
    /next_full_moon <дата> - узнаете ближайшее полнолуние от введённой даты
                    help - подробная справка по команде
                    
    /wordcount <текст> - считает слова в ведъном вашем тексте
    /cities start - запускает игру в слова
            help - вызывает справку по игре
            

    PS.: Пока это всё, на что я способен, но я быстро учусь :).
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
    update.message.reply_text('Ты мне написал: {}'.format(user_text))


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
            
            вызов /next_full_moon - покажу ближайшее полнолуние
            вызов /next_full_moon <дата> - покажу ближайшее полнолуние от заданной даты.
            
            Формат даты для ввода: 2019-01-01 (год, месяц, число)
            """
        )

    elif input_date:
        try:
            input_date = datetime.strptime(input_date, '%Y-%m-%d')
        except ValueError:
            update.message.reply_text(
                    'Ты написал дату не так!\nНапиши в таком виде: 2019-01-01 (год-месяц-день)',
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
    user_text = ' '.join(args).lower()
    if update.message.text == '/wordcount':
        update.message.reply_text('Введи текст, а я посчитаю слова ;)')
    else:
        word_count = re.findall(r"[\w']+", user_text)
        update.message.reply_text('Ммм... Я насчитал: {} слов'.format(len(word_count)))


@utils.logging_user_input
def cities_game(bot, update, args):
    input_date = ' '.join(args)
    # todo: закончить модуль с игрой в города
    if update.message.text == '/cities start':
        full_moon_date = ephem.next_full_moon(datetime.now())
        update.message.reply_text(
            'Ближайшее полнолуние будет: {}'.format(
                datetime.strptime(str(full_moon_date), '%Y/%m/%d %X').strftime('%d %b %Y'),
            )
        )
    elif update.message.text == '/cities help':
        update.message.reply_text(
            """
            Справка по игре Города:
            
            в базе используется 332 города России.

            вызов /cities start - запускает игру в города
            вызов /cities stop - заканчивает игру в города
            вызов /cities scores - показывает сколько очков набрал пользователь, а сколько бот

            Когда игра запущена:
            
            ввод: /cities <Наименование города> - без угловых скобок (например /cities Москва)
            
            Выигрывает тот, кто назвал больше городов, подсчёт очков происходит после окончания игры.
            Вызвав команду score игра покажет последний результат.
            
            Игра заканчивается, когда вызвана команда stop или закончились города в базе на нужную букву.
            """
        )
    elif update.message.text == '/cities':
        update.message.reply_text('Игра в Города! (для справки вызовите /cities help')


@utils.logging_user_input
def calc(bot, update, args):
    user_input = ' '.join(args)
    if update.message.text == '/calc':
        update.message.reply_text('Если ты скажешь, что посчитать, я посчитаю за тебя :)')
    elif update.message.text == '/calc help':
        update.message.reply_text(
            """
            Справка по команде /calc:
            
            Напишите Кельвину любое математическое выражение и он его вычислит.
            
            Пример: /calc (8 + 4) * 2   # ответ: 24
                    /calc 2 + 3         # ответ: 5
                    /calc 27 * 8        # ответ: 216
                    /calc 315 / 4       # ответ: 78.75
            
            """
        )

    elif user_input:
        if len(user_input) < 3:
            return update.message.reply_text('Слишком коротко, таких математических выражений не быыает :)')

        for character in user_input:
            if character not in '0123456789-+/* ':
                return update.message.reply_text('Ты не ввёл цифры и хочешь, чтобы я посчитал :)')

        if user_input[0] in '/*+':
            return update.message.reply_text('Это не математическое выражение, мой друг :)')
        else:
            result = eval(user_input)
            update.message.reply_text('Я посчитал, это будет: {:.2f}  :)'.format(result))


def bot_worker():
    calvin_bot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    logging.info('Calvin launch from space station...')

    dp = calvin_bot.dispatcher
    dp.add_handler(CommandHandler('start', start_msg))
    dp.add_handler(CommandHandler('help', help_msg))
    dp.add_handler(CommandHandler('planet', planet_info, pass_args=True))
    dp.add_handler(CommandHandler('next_full_moon', get_next_full_moon, pass_args=True))
    dp.add_handler(CommandHandler('wordcount', word_counter, pass_args=True))
    dp.add_handler(CommandHandler('cities', cities_game, pass_args=True))
    dp.add_handler(CommandHandler('calc', calc, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, calvin_talk))

    calvin_bot.start_polling()
    calvin_bot.idle()


if __name__ == '__main__':
    bot_worker()
