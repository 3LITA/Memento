import importlib
import logging

import telebot

from app import settings
from app.bot.keyboard import markups
from app.models.User import User

from . import replies


bot = telebot.TeleBot(settings.BOT_TOKEN, threaded=False)


def process_update(raw_update: str) -> None:
    importlib.import_module('app.bot.main')
    importlib.import_module('app.bot.contextual_handlers')
    importlib.import_module('app.bot.markup_handlers')

    logging.debug("Message handlers number: %s", len(bot.message_handlers))
    logging.debug("CallbackQuery handlers number: %s", len(bot.callback_query_handlers))

    update = telebot.types.Update.de_json(raw_update)
    logging.debug("Proceeding update: %s", update.update_id)
    bot.process_new_updates([update])


def send_greetings(user: User) -> None:
    reply = replies.AFTER_SIGN_UP.format(username=user.username)
    inline_keyboard_id = bot.send_message(
        chat_id=user.chat_id,
        text=reply.text(),
        reply_markup=markups.main_menu_markup(user.has_decks()),
        parse_mode=reply.parse_mode,
    ).message_id
    user.set_inline_keyboard_id(inline_keyboard_id)


__all__ = ['bot', 'contexts', 'main', 'replies', 'utils', 'send_greetings']
