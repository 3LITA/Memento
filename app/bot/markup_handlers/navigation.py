from telebot import types

from app.bot import markups, utils
from app.bot.main import bot
from app.locale import replies
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

    keyboard = types.InlineKeyboardMarkup()

    create_deck_btn = types.InlineKeyboardButton(
        text='Создать новую колоду', callback_data='new'
    )
    add_existing_btn = types.InlineKeyboardButton(
        text='Добавить уже имеющуюся', callback_data='join'
    )
    back_btn = types.InlineKeyboardButton(text='В главное меню', callback_data='menu')

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

    text = replies.DECK_MENU_REPLY.format(
        humanize_title(user.chat_id, user_deck.title).upper()
    )

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
