from telebot import TeleBot

from app import settings
from app.bot.keyboard import markups
from app.models.User import User

from . import replies


bot = TeleBot(settings.TOKEN)


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
