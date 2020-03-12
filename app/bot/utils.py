import re
import typing

from telebot import types

from app.logic.get import get_decks
from app.logic.utils import get_or_create, humanize_title
from app.models import models

from . import markups, replies


expectations: typing.Dict[int, typing.Dict[str, typing.Any]] = dict() # chat_id: {key: value}


def get_user(message: types.Message) -> models.User:
    return get_or_create(message.from_user.id, message.from_user.username)


def get_args(message: types.Message) -> typing.Optional[typing.List[str]]:
    pattern = r'(^/\w+)(\s(.*))?'
    search = re.search(pattern, message.text)
    if search:
        args = search.group(3)
    if args:
        args = args.strip()
        if args == '':
            args = None
    return args


def count_gaps(question: str) -> int:
    pattern = r'(_)'
    count = len(re.findall(pattern, question))
    return count


def create_learn_decks_inline_keyboard(user: models.User) -> typing.Optional[types.InlineKeyboardMarkup]:

    decks = get_decks(user)

    if decks and len(decks) > 0:
        markup = types.InlineKeyboardMarkup()
        for deck in decks:
            markup.add(
                types.InlineKeyboardButton(
                    text=humanize_title(user.chat_id, deck.title),
                    callback_data=f'learn_decks.{deck.id}',
                )
            )
        return markup
    return None  # probably it is wrong


def decks_inline_keyboard(user: models.User) -> typing.Optional[types.InlineKeyboardMarkup]:

    decks = get_decks(user)

    if decks and len(decks) > 0:
        markup = types.InlineKeyboardMarkup()
        markuped = [
            types.InlineKeyboardButton(
                text=humanize_title(user.chat_id, deck.title).upper(),
                callback_data=f'deck.{deck.id}',
            )
            for deck in decks
        ]
        markup.add(*markuped)
        markup.add(types.InlineKeyboardButton(text='Назад', callback_data='menu'))
        return markup
    return None  # probably it is wrong


def build_learn_text_and_keyboard(user: models.User, card: models.Card) -> types.InlineKeyboardMarkup:
    text = card.question.question
    if card.question.card_type == 0:
        text += '\n\n' + replies.SET_KNOWLEDGE_REPLY
        keyboard = markups.create_set_knowledge_markup(card)
    elif card.question.card_type == 3:
        text += '\n\n' + replies.USER_CHOSEN_REPLY
        keyboard = markups.create_answer_sheet_markup(card)
    elif card.question.card_type == 4:
        keyboard = markups.create_answer_sheet_markup(card)
    else:
        keyboard = markups.create_basic_learn_markup(card)
        metadata = {'card_id': card.id}
        set_context(user, 'learn', metadata)
    return text, keyboard


def repeat_keyboard(js: dict) -> types.InlineKeyboardMarkup:
    reply_markup = js.get('reply_markup')
    if reply_markup:
        reply_markup = reply_markup.get('inline_keyboard')
        if reply_markup:
            buttons = reply_markup[0]  
    # that's a total bullshit ^

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        *[
            types.InlineKeyboardButton(
                text=btn.get('text'), callback_data=btn.get('callback_data')
            )
            for btn in buttons
            if not btn.get('callback_data').startswith('show')
        ]
    )
    return keyboard


def forget_context(user: models.User) -> typing.Optional[typing.Dict[str, typing.Any]]:
    try:
        return expectations.pop(user.chat_id)
    except KeyError:
        return None


def set_context(user: models.User, command: str, metadata: dict = None) -> None:
    data = {'command': command}
    if metadata:
        data.update(metadata)
    expectations[user.chat_id] = data


def get_expected(message: types.Message) -> typing.Optional[str]:
    data = expectations.get(message.from_user.id)
    if data:
        return data.get('command')
    return None


def get_context(message: types.Message) -> typing.Optional[typing.Dict[str, typing.Any]]:
    data = expectations.get(message.from_user.id)
    return data
