from telebot import types

from app.bot import utils, replies
from app.bot.main import bot
from app.bot.keyboard import button_texts, markups
from app.models.UserDeck import UserDeck
from app.models.utils import humanize_title


@bot.callback_query_handler(func=lambda message: message.data.startswith('menu'))
def menu_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    text = replies.MENU_REPLY
    keyboard = markups.create_menu_markup(user)
    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('add_deck'))
def add_deck_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    utils.forget_context(user)

    text = replies.ADD_DECK_REPLY

    # TODO: move keyboard generation to markups.py
    keyboard = types.InlineKeyboardMarkup()

    create_deck_btn = types.InlineKeyboardButton(
        text=button_texts.CREATE_NEW_DECK, callback_data='new'
    )
    add_existing_btn = types.InlineKeyboardButton(
        text=button_texts.ADD_EXISTING_DECK, callback_data='join'
    )
    back_btn = types.InlineKeyboardButton(text=button_texts.BACK, callback_data='menu')

    keyboard.add(create_deck_btn, add_existing_btn)
    keyboard.add(back_btn)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('decks'))
def decks_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    inline_keyboard = utils.decks_inline_keyboard(user)
    text = replies.CHOOSE_DECK_REPLY
    bot.edit_message_text(
        text, user.chat_id, message_id=markup_message_id, reply_markup=inline_keyboard
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('deck'))
def deck_menu_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    utils.forget_context(user)

    user_deck_id = message.data.split('.')[-1]
    user_deck = UserDeck.get_by_id(user_deck_id)

    text = replies.DECK_MENU_REPLY.format(humanize_title(user_deck.title).upper())

    keyboard = markups.create_deck_menu_markup(user_deck)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        parse_mode='Markdown',
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('new'))
def new_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    text = replies.CREATE_NEW_DECK_REPLY
    keyboard = markups.create_new_deck_markup()

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )
    utils.set_context(user, command='new')


@bot.callback_query_handler(func=lambda message: message.data.startswith('language'))
def language_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    text = replies.CHANGE_LANGUAGE_REPLY
    keyboard = markups.create_language_choice_markup(user.preferred_language)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(
    func=lambda message: message.data.startswith('set_language')
)
def set_language_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    language = message.data.split('.')[1]
    user.set_preferred_language(language)

    text = replies.LANGUAGE_WAS_CHANGED_REPLY
    keyboard = markups.create_menu_markup(user)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )
