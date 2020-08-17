from typing import Any

import telebot
from telebot.types import Message

from app import settings
from app.app import logging
from app.bot.keyboard import markups
from app.models.User import User

from . import replies, utils


bot = telebot.TeleBot(settings.TOKEN)


@bot.message_handler(commands=settings.BotCommands.start_commands)
@utils.log_message
def start_handler(message: Message, user: User) -> utils.handler_return:
    if user.inline_keyboard_id:
        reply = replies.START_AGAIN.format(message.from_user.first_name)
    else:
        reply = replies.START.format(message.from_user.first_name)

    keyboard = markups.main_menu_markup(user.has_decks())
    return keyboard, reply


@bot.message_handler(commands=settings.BotCommands.help_commands)
@utils.log_message
def help_handler(**_: Any) -> utils.handler_return:
    reply = replies.HELP
    return None, reply


@bot.message_handler(commands=settings.BotCommands.menu_commands)
@utils.log_message
def menu_handler(user: User, **_: Any) -> utils.handler_return:
    reply = replies.MAIN_MENU
    keyboard = markups.main_menu_markup(user.has_decks())
    return keyboard, reply


@bot.message_handler(regexp=r'^/.*')
@utils.log_message
def unknown_command_handler(message: Message, **_: Any) -> utils.handler_return:
    reply = replies.UNKNOWN_COMMAND
    logging.warning(
        "%s tried to send a non-existing command %s", message.chat.id, message.text
    )
    return None, reply
