from typing import Any

from telebot.types import Message

from app import support_bot
from app.bot import bot, contexts, replies, utils
from app.bot.keyboard import markups
from app.models.User import User


@bot.message_handler(
    func=lambda message: contexts.command_expected(
        message, contexts.ExpectedCommands.SEND_ISSUE
    )
)
@utils.log_message
def issue_contextual_handler(
    message: Message, user: User, **_: Any
) -> utils.handler_return:
    support_bot.report(message=message.text, customer=user)
    reply = replies.ISSUE_SENT.format(username=user.username, issue_text=message.text)
    keyboard = markups.main_menu_markup(user.has_decks())
    contexts.forget_context(user)

    return keyboard, reply
