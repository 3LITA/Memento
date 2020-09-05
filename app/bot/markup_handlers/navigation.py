import logging
from typing import Any

from telebot.types import CallbackQuery

from app import i18n
from app.bot import bot, contexts, replies, utils
from app.bot.keyboard import cd, markups
from app.models.Deck import Deck
from app.models.User import User
from app.models.utils import humanize_title


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.delete_message())
)
def delete_message_markup_handler(callback: CallbackQuery) -> None:
    bot.delete_message(callback.from_user.id, callback.message.message_id)


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.main_menu()))
@utils.log_pressed_button
def menu_markup_handler(user: User, **_: Any) -> utils.handler_return:
    reply = replies.MAIN_MENU
    keyboard = markups.main_menu_markup(user.has_decks())

    return keyboard, reply


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.add_deck()))
@utils.log_pressed_button
def add_deck_markup_handler(user: User, **_: Any) -> utils.handler_return:
    contexts.forget_context(user)
    reply = replies.ADD_DECK
    keyboard = markups.add_deck_markup()

    return keyboard, reply


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.my_decks()))
@utils.log_pressed_button
def decks_markup_handler(user: User, **_: Any) -> utils.handler_return:
    decks_map = {deck.id: utils.humanize_title(deck.title) for deck in user.decks}
    keyboard = markups.decks_markup(decks_map)
    reply = replies.CHOOSE_DECK
    return keyboard, reply


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.deck_menu()))
@utils.log_pressed_button
def deck_menu_markup_handler(
    deck_id: int, user: User, **_: Any
) -> utils.handler_return:
    contexts.forget_context(user)

    deck = Deck.get(deck_id)

    reply = replies.DECK_MENU.format(title=humanize_title(deck.title).upper())
    keyboard = markups.deck_menu_markup(deck.id, deck.has_cards())

    return keyboard, reply


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.create_new_deck())
)
@utils.log_pressed_button
def new_markup_handler(user: User, **_: Any) -> utils.handler_return:
    reply = replies.CREATE_NEW_DECK
    keyboard = markups.new_deck_markup()

    contexts.set_context(user, command=contexts.ExpectedCommands.CREATE_NEW_DECK)

    return keyboard, reply


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.language()))
@utils.log_pressed_button
def language_markup_handler(user: User, **_: Any) -> utils.handler_return:
    reply = replies.CHANGE_LANGUAGE
    keyboard = markups.language_choice_markup(user.preferred_language)

    return keyboard, reply


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.set_language())
)
@utils.log_pressed_button
def set_language_markup_handler(
    language: str, user: User, **_: Any
) -> utils.handler_return:
    user.set_preferred_language(language)
    i18n.set_language(user)

    logging.info("Set '%s' language to user %s", language, user.id)

    reply = replies.LANGUAGE_WAS_CHANGED
    keyboard = markups.main_menu_markup(user.has_decks())

    return keyboard, reply


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.support()))
@utils.log_pressed_button
def support_markup_handler(user: User, **_: Any) -> utils.handler_return:
    reply = replies.SUPPORT.format(username=user.username)
    keyboard = markups.support_markup()
    contexts.set_context(user, contexts.ExpectedCommands.SEND_ISSUE)

    return keyboard, reply
