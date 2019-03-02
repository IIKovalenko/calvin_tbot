import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem

import settings


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='calvin_bot.log'
)

HELP_TEXT = """
    Доспуные команды:

    /start - показывает приветственное сообщение
    /help - вызывает это сообщение
    /planet <имя планеты> - получите информацию по планете (доступна только Солнечная ситема)

    PS.: По мере добавления команд help будет пополняться.
    """


def start_msg(bot, update):
    text = 'Привет, мой друг, я - Кельвин, виртуальный образец инопланетного существа из фильма "Живое".'
    logging.info(text)
    update.message.reply_text('{}\n{}'.format(text, HELP_TEXT))


def help_msg(bot, update):
    logging.info('Вызвана команда /help')
    update.message.reply_text(HELP_TEXT)


def calvin_talk(bot, update):
    t_user = {
        'username': update.message.chat.username,
        'first_name': update.message.chat.first_name,
        'last_name': update.message.chat.last_name,
        'full_name': update.message.chat.first_name + ' ' + update.message.chat.last_name,
    }
    user_text = update.message.text
    logging.info(
        "User: %s(%s), Chat ID: %s, Message: %s",
        t_user['username'], t_user['full_name'], update.message.chat.id, update.message.text
    )
    update.message.reply_text('Вы написали: {}'.format(user_text))


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
    logging.info('Вызвана команда /planet')
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


def bot_worker():
    calvin_bot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    logging.info('Calvin launch from space station...')

    dp = calvin_bot.dispatcher
    dp.add_handler(CommandHandler('start', start_msg))
    dp.add_handler(CommandHandler('help', help_msg))
    dp.add_handler(CommandHandler('planet', planet_info, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, calvin_talk))

    calvin_bot.start_polling()
    calvin_bot.idle()


if __name__ == '__main__':
    bot_worker()
