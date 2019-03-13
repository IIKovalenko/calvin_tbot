"""All hadlers function of Calvin(n5) bot"""

import re
from datetime import datetime
from random import choice

import ephem
import requests


import cities
import settings
import utils

HELP_TEXT = """
    Доспуные команды:

    /start - показывает приветственное сообщение

    /help - вызывает это сообщение

    /calc <мат. выражение> - Кельвин посчитает за вас :)
            help - вызывает справку по калькулятору
            
    /planet <имя планеты> - Кельвин скажет в каком созвездии планета (доступна только Солнечная ситема)

    /next_full_moon <дата> - узнаете ближайшее полнолуние от введённой даты
                    help - подробная справка по команде

    /wordcount <текст> - считает слова в ведъном вашем тексте
    /weather <имя города> - показывает текущую погоду в выбраном городе
             help - справка по команде погоды

    /cities start - запускает игру в слова
            help - вызывает справку по игре


    PS.: Пока это всё, на что я способен, но я быстро учусь :).
    """


def start_msg(bot, update):
    text = 'Привет, мой друг, я - Кельвин, виртуальный образец инопланетного существа из фильма "Живое".'
    update.message.reply_text('{}\n{}'.format(text, HELP_TEXT), reply_markup=utils.get_keyboard())


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
    input_data = ' '.join(args)
    # todo: закончить модуль с игрой в города
    user_data = {}

    if update.message.text == '/cities start':
        update.message.reply_text('Так начнётся же игра...')
        user_data.update(id=update.message.chat.id, cities=[])
        city = choice(list(cities.cities_base.keys()))
        update.message.reply_text('Город: {} \nТы называешь города на: {}'.format(city, city[-1]))
        chat_id = getattr(user_data, str(update.message.chat.id))
        print(chat_id)
        print(user_data)

        if chat_id == update.message.chat.id:
            if input_data.startswith(city[-1]) == city[-1]:
                update.message.reply_text('Город: {} \nТы называешь города на: {}'.format(city, city[-1]))

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

            Напишите Кельвину любое математическое выражение
            и он его вычислит.

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


@utils.logging_user_input
def get_weather(bot, update, args):
    city_name = ' '.join(args)
    if update.message.text == '/weather':
        update.message.reply_text('Я расскажу про погоду, если скажешь мне в каком городе хочешь узнать погодку :)')
    elif update.message.text == '/weather help' or city_name == 'help':
        update.message.reply_text(
            """
            Показывает текущую погоду в выбраном городе.

            вызов /weather <наименование города>

            Наименование города надо вводить на английском.
            Для точности лучше указать имя города и через запятую страну, без пробела
            Например: /weather Mosсow,Russia
            """
        )

    else:
        weather_url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'
        params = {
            'key': settings.API_KEY_WEATHER,
            'q': city_name,
            'format': 'json',
            'num_of_days': 1,
            'showlocaltime': 'yes',
            'lang': 'ru',
        }

        try:
            result = requests.get(weather_url, params=params)
            result.raise_for_status()
            weather = result.json()
            if 'data' in weather:
                if 'current_condition' in weather['data']:
                    try:
                        cur_weather = weather['data']['current_condition'][0]
                        update.message.reply_text(
                            'Погода {}. \n{}\nТемпература: {}\nОщущается как: {}\nСкорость ветра: {} км/ч'.format(
                                city_name,
                                cur_weather['lang_ru'][0]['value'],
                                cur_weather['temp_C'],
                                cur_weather['FeelsLikeC'],
                                cur_weather['windspeedKmph'],
                            )
                        )

                    except (TypeError, IndexError):
                        return update.message.reply_text('Ошибка сети, попробуй позже, вдруг получится :)')

        except (requests.RequestException, ValueError):
            return update.message.reply_text('Ошибка сети, попробуй позже, вдруг получится :)')
