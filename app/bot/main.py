import logging
from typing import Any

from telebot.types import Message

from app.bot.keyboard import markups
from app.models.User import User
from app.settings import BotCommands

from . import bot, replies, utils


@bot.message_handler(commands=BotCommands.start_commands)
@utils.log_message
def start_handler(user: User, **_: Any) -> utils.handler_return:
    reply = replies.START_AGAIN.format(user.username)
    keyboard = markups.main_menu_markup(user.has_decks())
    return keyboard, reply


@bot.message_handler(commands=BotCommands.help_commands)
@utils.log_message
def help_handler(**_: Any) -> utils.handler_return:
    reply = replies.HELP
    return None, reply


@bot.message_handler(commands=BotCommands.menu_commands)
@utils.log_message
def menu_handler(user: User, **_: Any) -> utils.handler_return:
    reply = replies.MAIN_MENU
    has_decks = user.has_decks()
    keyboard = markups.main_menu_markup(has_decks)
    return keyboard, reply


@bot.message_handler(regexp=r'^/.*')
@utils.log_message
def unknown_command_handler(message: Message, **_: Any) -> utils.handler_return:
    reply = replies.UNKNOWN_COMMAND
    logging.warning(
        "%s tried to send a non-existing command %s", message.chat.id, message.text
    )
    return None, reply


def send_greetings(user: User) -> None:
    reply = replies.AFTER_SIGN_UP.format(username=user.username)
    inline_keyboard_id = bot.send_message(
        chat_id=user.chat_id,
        text=reply.text,
        reply_markup=markups.main_menu_markup(user.has_decks()),
        parse_mode=reply.parse_mode,
    ).message_id
    user.set_inline_keyboard_id(inline_keyboard_id)
