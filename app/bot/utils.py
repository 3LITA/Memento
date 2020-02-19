import re

from telebot import types

from app.logic.utils import humanize_title, get_or_create
from app.logic.get import get_decks

from . import replies
from . import markups


expectations = dict()  # chat_id: {key: value}


def get_user(message):
    return get_or_create(message.from_user.id, message.from_user.username)


def get_args(message):
    pattern = r'(^/\w+)(\s(.*))?'
    args = re.search(pattern, message.text).group(3)
    if args:
        args = args.strip()
        if args == '':
            args = None
    return args


def count_gaps(question):
    pattern = r'(_)'
    count = len(re.findall(pattern, question))
    return count


#
#
# def ask_question(user, user_deck):
#     # return [question, reply_keyboard, inline_keyboard]
#
#     card = pull_card(user_deck)
#     public_card = card.public_card
#
#     reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=False,
#                                                resize_keyboard=True)
#     inline_keyboard = None
#
#     show_btn = types.KeyboardButton(text='/show')
#     cancel_btn = types.KeyboardButton(text='/cancel')
#
#     reply_keyboard.add(show_btn, cancel_btn)
#
#     if public_card.card_type == 0:
#
#         expectations[user.chat_id] = ['set_knowledge', {'user_deck_id': user_deck.id,
#                                                         'user_card_id': card.id,
#                                                         'public_card_id': public_card.id}]
#
#         inline_keyboard = create_set_knowledge_inline_keyboard(card)
#         text = public_card.question + '\n\n' + replies.SET_KNOWLEDGE_REPLY
#
#     elif public_card.card_type == 1 or public_card.card_type == 2:
#
#         expectations[user.chat_id] = ['learn', {'user_deck_id': user_deck.id,
#                                                 'user_card_id': card.id,
#                                                 'public_card_id': public_card.id,
#                                                 'correct_answers': public_card.correct_answers}]
#         text = public_card.question
#
#     elif public_card.card_type == 3 or public_card.card_type == 4:
#
#         inline_keyboard, correct_numbers = create_answer_sheet(card)
#
#         if public_card.card_type == 3:
#             text = public_card.question + '\n\n' + replies.CHOOSE_MANY_REPLY
#         else:
#             text = public_card.question + '\n\n' + replies.CHOOSE_ONE_REPLY
#
#         expectations[user.chat_id] = ['learn_markup', {'user_deck_id': user_deck.id,
#                                                        'user_card_id': card.id,
#                                                        'public_card_id': public_card.id,
#                                                        'correct_answers': correct_numbers}]
#
#     else:
#         print(f'Unknown card type: {public_card.card_type}')
#         return
#
#     return text, reply_keyboard, inline_keyboard


def create_learn_decks_inline_keyboard(user):

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


def decks_inline_keyboard(user):

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


# def parse_answers(js):
#     buttons = js.get('reply_markup').get('inline_keyboard')
#     chosen = buttons[-3][0]['callback_data'].split('.')[-1]

#     # if chosen ==

#     print('printing buttons')
#     print(buttons)

#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     keyboard.add(
#         *[
#             types.InlineKeyboardButton(
#                 text=btn[0].get('text'), callback_data=btn[0].get('callback_data')
#             )
#             for btn in buttons
#         ]
#     )
#     return keyboard


def build_learn_text_and_keyboard(user, card):
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


def repeat_keyboard(js):
    buttons = js.get('reply_markup').get('inline_keyboard')[0]

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


#
#
# def give_card(user, user_deck):
#     try:
#         pull_card(user_deck)
#     except errors.EmptyDeckError:
#         text = replies.EMPTY_DECK_REPLY
#         reply_keyboard = None
#         inline_keyboard = None
#     else:
#         text, reply_keyboard, inline_keyboard = ask_question(user, user_deck)
#     return text, reply_keyboard, inline_keyboard


def forget_context(user):
    try:
        return expectations.pop(user.chat_id)
    except KeyError:
        return


def set_context(user, command, metadata: dict = None):
    data = {'command': command}
    if metadata:
        data.update(metadata)
    expectations[user.chat_id] = data


def get_expected(message):
    data = expectations.get(message.from_user.id)
    if data:
        return data.get('command')


def get_context(message):
    data = expectations.get(message.from_user.id)
    return data
