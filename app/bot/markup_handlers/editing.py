from typing import Any

from app.bot import contexts, replies, utils
from app.bot.keyboard import button_texts, cd, markups
from app.bot.main import bot
from app.models import CardType
from app.models.Card import Card
from app.models.Deck import Deck
from app.models.User import User
from app.models.utils import humanize_title


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.edit_card()))
@utils.log_pressed_button
def edit_card_markup_handler(card_id: int, **_: Any) -> utils.handler_return:
    card = Card.get(card_id)

    keyboard = markups.edit_card_markup(card.id, card.deck_id, card.type)

    if card.type == CardType.FACT:
        reply = replies.EDIT_FACT.format(question=card.question)
    else:
        if card.correct_answers:
            answers = (
                f"{replies.CORRECT_ANSWERS_ARE}" f"{', '.join(card.correct_answers)}"
            )
        else:
            answers = button_texts.NO_CORRECT_ANSWERS
        if card.wrong_answers:
            answers = (
                f"{answers}\n\n{replies.WRONG_ANSWERS_ARE}"
                f"{', '.join(card.wrong_answers)}"
            )
        elif card.type in (CardType.MULTIPLE_CHOICE, CardType.RADIOBUTTON):
            answers = f"{answers}\n\n{button_texts.NO_WRONG_ANSWERS}"

        reply = replies.EDIT_CARD.format(question=card.question, answers=answers)

    return keyboard, reply


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.edit_user_deck())
)
@utils.log_pressed_button
def edit_deck_markup_handler(deck_id: int, **_: Any) -> utils.handler_return:
    deck = Deck.get(deck_id)

    reply = replies.EDIT_DECK.format(deck_title=humanize_title(deck.title).upper())
    keyboard = markups.edit_user_deck_markup(deck.id)

    return keyboard, reply


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.rename_user_deck())
)
@utils.log_pressed_button
def rename_deck_markup_handler(
    deck_id: int, user: User, **_: Any
) -> utils.handler_return:
    deck = Deck.get(deck_id)

    reply = replies.RENAME_DECK.format(deck_title=humanize_title(deck.title).upper())
    keyboard = markups.cancel_to_deck_menu_markup(deck.id)

    contexts.set_context(
        user, contexts.ExpectedCommands.RENAME_USER_DECK, deck_id=deck_id
    )

    return keyboard, reply


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.delete_user_deck())
)
@utils.log_pressed_button
def delete_deck_markup_handler(deck_id: int, **_: Any) -> utils.handler_return:
    deck = Deck.get(deck_id)

    reply = replies.DELETE_DECK.format(title=humanize_title(deck.title).upper())
    keyboard = markups.delete_user_deck_markup(deck.id)

    return keyboard, reply


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.sure_delete_user_deck())
)
@utils.log_pressed_button
def confirm_delete_user_deck_markup_handler(
    deck_id: int, user: User, **_: Any
) -> utils.handler_return:
    try:
        deck = Deck.get(deck_id)
    except AttributeError:
        reply = replies.DECK_NOT_FOUND
    else:
        deck.delete()

        reply = replies.DECK_DELETED.format(
            deck_title=humanize_title(deck.title).upper()
        )
    keyboard = markups.main_menu_markup(user.has_decks())

    return keyboard, reply


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.delete_user_card())
)
@utils.log_pressed_button
def delete_card_markup_handler(
    card_id: int, user: User, **_: Any
) -> utils.handler_return:
    try:
        card = Card.get(card_id)
    except AttributeError:
        reply = replies.CARD_ALREADY_DELETED
        keyboard = markups.main_menu_markup(user.has_decks())
    else:
        card.delete()
        deck = card.deck
        text = replies.DECK_MENU.format(title=humanize_title(deck.title).upper())
        reply = replies.Reply(
            text=f"{replies.CARD_DELETED}\n\n{text}",
            parse_mode=(
                replies.DECK_MENU.parse_mode or replies.CARD_DELETED.parse_mode
            ),
        )
        keyboard = markups.deck_menu_markup(deck.id, deck.has_cards())

    return keyboard, reply
