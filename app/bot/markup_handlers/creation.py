from typing import Any

from telebot.types import CallbackQuery

from app.bot import bot, contexts, replies, utils
from app.bot.keyboard import cd, markups
from app.models import CardType
from app.models.Card import Card
from app.models.Deck import Deck
from app.models.User import User
from app.models.utils import humanize_title


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.add_card()))
@utils.log_pressed_button
def add_card_markup_handler(deck_id: int, **_: Any) -> utils.handler_return:
    deck = Deck.get(deck_id)
    deck_title = humanize_title(deck.title)

    reply = replies.CHOOSE_CARD_TYPE.format(deck_title.upper())
    keyboard = markups.choose_card_type_markup(deck_id)

    return keyboard, reply


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.card_type()))
@utils.log_pressed_button
def card_type_markup_handler(
    deck_id: int, card_type: int, user: User, **_: Any
) -> utils.handler_return:
    if int(card_type) == 0:
        reply = replies.SEND_FACT
    else:
        reply = replies.SEND_QUESTION.format(card_type)
        if int(card_type) == CardType.GAPS:
            reply = replies.Reply(
                text=f"{reply}{replies.NOTE_GAPS_FOR_TYPE_2}",
                parse_mode=(
                    replies.SEND_QUESTION.parse_mode
                    or replies.NOTE_GAPS_FOR_TYPE_2.parse_mode
                ),
            )

    keyboard = markups.question_await_markup(deck_id)

    command = (
        contexts.ExpectedCommands.SEND_FACT
        if card_type == CardType.FACT
        else contexts.ExpectedCommands.SEND_QUESTION
    )
    contexts.set_context(
        user=user, command=command, card_type=card_type, deck_id=deck_id
    )

    return keyboard, reply


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.no_correct_answers())
)
@utils.log_pressed_button
def no_correct_answers_markup_handler(
    callback: CallbackQuery, **_: Any
) -> utils.handler_return:
    context = contexts.get_context(callback)
    context.correct_answers = []
    context.command = contexts.ExpectedCommands.SEND_WRONG_ANSWERS

    deck = Deck.get(context.deck_id)

    reply = replies.Reply(
        f"{replies.THERE_ARE_NO_CORRECT_ANSWERS}\n"
        f"{replies.SEND_WRONG_ANSWERS.format(question=context.question)}"
    )

    keyboard = markups.cancel_markup(deck.id)

    return keyboard, reply


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.no_wrong_answers())
)
@utils.log_pressed_button
def no_wrong_answers_markup_handler(
    callback: CallbackQuery, user: User, **_: Any
) -> utils.handler_return:
    context = contexts.get_context(callback)
    deck = Deck.get(context.deck_id)

    card = Card(deck, context.card_type, context.question, context.correct_answers)
    contexts.forget_context(user)

    keyboard = markups.card_created_markup(card.id, deck.id)
    reply = replies.CARD_WITH_CHOICE_CREATED.format(
        type=context.card_type,
        question=context.question,
        correct_answers=context.correct_answers,
        wrong_answers=replies.THERE_ARE_NO_WRONG_ANSWERS,
    )
    return keyboard, reply
