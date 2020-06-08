from flask_babel import refresh
from telebot.types import CallbackQuery

from app.bot import replies, utils
from app.bot.keyboard import cd, markups
from app.bot.main import bot
from app.models.UserDeck import UserDeck
from app.models.utils import humanize_title


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.main_menu()))
def menu_markup_handler(callback: CallbackQuery) -> None:
    user = utils.get_user(callback)
    inline_keyboard_id = user.inline_keyboard_id

    text = replies.MENU_REPLY
    keyboard = markups.main_menu_markup(user)
    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=inline_keyboard_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.add_deck()))
def add_deck_markup_handler(callback: CallbackQuery) -> None:
    user = utils.get_user(callback)
    markup_message_id = user.inline_keyboard_id

    utils.forget_context(user)

    text = replies.ADD_DECK_REPLY

    keyboard = markups.add_deck_markup()

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.my_decks()))
def decks_markup_handler(callback: CallbackQuery) -> None:
    user = utils.get_user(callback)
    inline_keyboard_id = user.inline_keyboard_id

    decks_map = {deck.id: utils.humanize_title(deck.title) for deck in user.decks}
    keyboard = markups.decks_markup(decks_map)

    text = replies.CHOOSE_DECK_REPLY
    bot.edit_message_text(
        text, user.chat_id, message_id=inline_keyboard_id, reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.deck_menu()))
def deck_menu_markup_handler(callback: CallbackQuery) -> None:
    user = utils.get_user(callback)
    markup_message_id = user.inline_keyboard_id

    utils.forget_context(user)

    user_deck_id = callback.data.split('.')[-1]
    user_deck = UserDeck.get_by_id(user_deck_id)

    text = replies.DECK_MENU_REPLY.format(humanize_title(user_deck.title).upper())

    keyboard = markups.deck_menu_markup(user_deck.id, user.has_decks())

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        parse_mode='Markdown',
        reply_markup=keyboard,
    )


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.create_new_deck())
)
def new_markup_handler(callback: CallbackQuery) -> None:
    user = utils.get_user(callback)
    markup_message_id = user.inline_keyboard_id

    text = replies.CREATE_NEW_DECK_REPLY
    keyboard = markups.new_deck_markup()

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )
    utils.set_context(user, command='new')


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.language()))
def language_markup_handler(callback: CallbackQuery) -> None:
    user = utils.get_user(callback)
    markup_message_id = user.inline_keyboard_id

    text = replies.CHANGE_LANGUAGE_REPLY
    keyboard = markups.language_choice_markup(user.preferred_language)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.set_language())
)
def set_language_markup_handler(callback: CallbackQuery) -> None:
    user = utils.get_user(callback)
    markup_message_id = user.inline_keyboard_id

    language = callback.data.split('.')[1]
    user.set_preferred_language(language)

    refresh()  # TODO: make this work

    text = replies.LANGUAGE_WAS_CHANGED_REPLY
    keyboard = markups.main_menu_markup(user)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )
