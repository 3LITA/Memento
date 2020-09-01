import logging
from random import choice
from typing import Any

from telebot.types import Message

from app.bot import bot, contexts, replies, utils
from app.bot.keyboard import markups
from app.models import CardType
from app.models.Card import Card
from app.models.User import User


@bot.message_handler(
    func=lambda message: contexts.command_expected(
        message, contexts.ExpectedCommands.LEARN
    )
)
@utils.log_message
def learn_contextual_handler(message: Message, **_: Any) -> utils.handler_return:
    context = contexts.get_context(message)
    card = Card.get(context.card_id)

    answer = (
        message.text.lower()
        if card.type == CardType.SIMPLE
        else [ans.strip().lower() for ans in message.text.split(',')]
    )

    if card.add_attempt(answer).success:
        text = replies.RATE_KNOWLEDGE
        keyboard = markups.rate_knowledge_markup(card.id)
        reply_list = replies.CORRECT_REPLIES
    else:
        text = card.question
        keyboard = markups.basic_learn_markup(card.id, card.deck_id)
        reply_list = replies.WRONG_REPLIES
    reply = replies.Reply(f"{choice(reply_list)}\n\n{text}")

    return keyboard, reply


@bot.message_handler(func=lambda message: True)
@utils.log_message
def wtf_handler(user: User, **_: Any) -> utils.handler_return:
    logging.warning("%s sent an unexpected message", user.chat_id)
    answers = replies.WTF_MESSAGES
    reply = choice(answers)
    return None, reply
