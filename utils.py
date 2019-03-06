"""Extended utils for Calvin(n5) telegram bot"""

import logging


def logging_user_input(bot_func):
    """Логирование пользовательского ввода"""
    def logging_wrapper(*args, **kwargs):
        update = args[1]
        t_user = {
            'username': update.message.chat.username,
            'first_name': update.message.chat.first_name,
            'last_name': update.message.chat.last_name,
            'full_name': update.message.chat.first_name + ' ' + update.message.chat.last_name,
        }
        logging.info(
            "User: %s(%s), Chat ID: %s, Message: %s",
            t_user['username'], t_user['full_name'], update.message.chat.id, update.message.text,
        )

        return bot_func(*args, **kwargs)
    return logging_wrapper
