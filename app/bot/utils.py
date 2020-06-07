import re
import typing

from telebot import types

from . import replies
from .keyboard import button_texts, markups
from app.models import utils
from app.models.Card import Card
from app.models.User import User

expectations: typing.Dict[
    int, typing.Dict[str, typing.Any]
] = dict()  # chat_id: {key: value}


def get_user(message: types.Message) -> User:
    return User.get_or_create(message.from_user.id, message.from_user.username)


def button_pressed(message, callback_data: str) -> bool:
    return message.data.startswith(callback_data)


def get_args(message: types.Message) -> typing.Optional[typing.List[str]]:
    pattern = r'(^/\w+)(\s(.*))?'
    search = re.search(pattern, message.text)
    args = None
    if search:
        args = search.group(3)
        if args and args.strip() != '':
            args = args.strip()
    return args


def count_gaps(question: str) -> int:
    pattern = r'(_)'
    count = len(re.findall(pattern, question))
    return count


def create_learn_decks_inline_keyboard(
    user: User,
) -> typing.Optional[types.InlineKeyboardMarkup]:

    decks = user.get_decks()

    if decks and len(decks) > 0:
        markup = types.InlineKeyboardMarkup()
        for deck in decks:
            markup.add(
                types.InlineKeyboardButton(
                    text=utils.humanize_title(deck.title),
                    callback_data=f'learn_decks.{deck.id}',
                )
            )
        return markup
    return None  # probably it is wrong


def decks_inline_keyboard(user: User) -> typing.Optional[types.InlineKeyboardMarkup]:

    decks = User.get_decks(user)

    if decks and len(decks) > 0:
        # TODO: move to replies.py
        markup = types.InlineKeyboardMarkup()
        markuped = [
            types.InlineKeyboardButton(
                text=utils.humanize_title(deck.title).upper(),
                callback_data=f'deck.{deck.id}',
            )
            for deck in decks
        ]
        markup.add(*markuped)
        markup.add(types.InlineKeyboardButton(text=button_texts.BACK, callback_data='menu'))
        return markup
    return None  # probably it is wrong


def build_learn_text_and_keyboard(
    user: User, card: Card
) -> typing.Tuple[str, types.InlineKeyboardMarkup]:
    text = card.question.text
    if card.question.card_type == 0:
        text += '\n\n' + replies.SET_KNOWLEDGE_REPLY
        keyboard = markups.rate_knowledge_markup(card)
    elif card.question.card_type == 3:
        text += '\n\n' + replies.USER_CHOSEN_REPLY
        keyboard = markups.multiple_choice_markup(card)
    elif card.question.card_type == 4:
        keyboard = markups.multiple_choice_markup(card)
    else:
        keyboard = markups.basic_learn_markup(card)
        metadata = {'card_id': card.id}
        set_context(user, 'learn', metadata)
    return text, keyboard


def repeat_keyboard(
    js: dict, exclude: typing.Optional[typing.List] = None, delete_btn: bool = False
) -> types.InlineKeyboardMarkup:
    if exclude is None:
        exclude = []
    inline_keyboard = js.get('reply_markup', {}).get('inline_keyboard')

    keyboard = types.InlineKeyboardMarkup()
    for row in range(len(inline_keyboard)):
        for btn in inline_keyboard[row]:
            text = btn.get('text')
            callback_data = btn.get('callback_data')
            if text not in exclude:
                keyboard.add(
                    types.InlineKeyboardButton(text=text, callback_data=callback_data,)
                )
    if delete_btn:
        keyboard.add(types.InlineKeyboardButton(text=button_texts.DELETE, callback_data=f'delete_user_card.{card.id}'))
    return keyboard


def forget_context(user: User) -> typing.Optional[typing.Dict[str, typing.Any]]:
    try:
        return expectations.pop(user.chat_id)
    except KeyError:
        return None


def set_context(user: User, command: str, metadata: dict = None) -> None:
    data = {'command': command}
    if metadata:
        data.update(metadata)
    expectations[user.chat_id] = data


def get_expected(message: types.Message) -> typing.Optional[str]:
    data = expectations.get(message.from_user.id)
    if data:
        return data.get('command')
    return None


def get_context(message: types.Message,) -> typing.Dict[str, typing.Any]:
    data = expectations[message.from_user.id]
    return data


def build_chosen_answers_reply(card: Card) -> str:
    return card.question.text + '\n\n' + replies.USER_CHOSEN_REPLY + ' '


def parse_chosen_nums(js: dict) -> typing.List[str]:
    text = js['text'].split(replies.USER_CHOSEN_REPLY)
    chosen_nums = sorted([num.strip() for num in text[-1].split(',')])

    return chosen_nums


def convert_chosen_to_answers(js: dict, chosen: typing.List[int]) -> typing.List[str]:
    inline_keyboard = js.get('reply_markup', {}).get('inline_keyboard')
    answers = []
    for num in chosen:
        num_part_length = len(f'{num - 1}) ')
        answer = inline_keyboard[num - 1][0]['text'][num_part_length:]
        answers.append(answer)
    return answers
