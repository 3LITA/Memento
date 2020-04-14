from telebot import types

from app.bot import markups, utils
from app.bot.main import bot
from app.locale import replies
from app.models.Card import Card
from app.models.UserDeck import UserDeck
from app.models.utils import humanize_title


@bot.callback_query_handler(func=lambda message: message.data.startswith('edit_card'))
def edit_card_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    card_id = message.data.split('.')[-1]
    card = Card.get_by_id(card_id)

    keyboard = markups.create_edit_card_markup(card)

    question_text = card.question.text
    if card.question.correct_answers and len(card.question.correct_answers) > 0:
        answers = 'Правильные ответы: '
        for ans in card.question.correct_answers:
            answers += ans + ', '
        answers = answers[:-2]
    else:
        answers = 'Правильных ответов нет'
    answers += '\n\n'
    if card.question.wrong_answers and len(card.question.wrong_answers) > 0:
        answers += 'Неправильные ответы: '
        for ans in card.question.wrong_answers:
            answers += ans + ', '
        answers = answers[:-2]
    elif card.question.card_type == 3 or card.question.card_type == 4:
        answers += 'Неправильных ответов нет'

    text = replies.EDIT_CARD_REPLY.format(question_text, answers)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('edit_deck'))
def edit_deck_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    deck_id = message.data.split('.')[-1]
    deck = UserDeck.get_by_id(deck_id)

    text = replies.EDIT_USER_DECK_REPLY.format(
        deck_title=humanize_title(user.chat_id, deck.title).upper()
    )
    keyboard = markups.create_edit_user_deck_markup(deck)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
        parse_mode='Markdown',
    )


@bot.callback_query_handler(
    func=lambda message: message.data.startswith('rename_user_deck')
)
def rename_user_deck_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    deck_id = message.data.split('.')[-1]
    deck = UserDeck.get_by_id(deck_id)

    text = replies.RENAME_USER_DECK_REPLY.format(
        deck_title=humanize_title(user.chat_id, deck.title).upper()
    )
    keyboard = markups.create_rename_user_deck_markup(deck)

    metadata = {'deck_id': deck.id}
    utils.set_context(user, 'rename_user_deck', metadata)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
        parse_mode='Markdown',
    )


@bot.callback_query_handler(
    func=lambda message: message.data.startswith('delete_user_deck')
)
def delete_user_deck_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    deck_id = message.data.split('.')[-1]
    deck = UserDeck.get_by_id(deck_id)

    text = replies.DELETE_USER_DECK_REPLY.format(
        humanize_title(user.chat_id, deck.title).upper()
    )
    keyboard = markups.create_delete_user_deck_markup(deck)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
        parse_mode='Markdown',
    )


@bot.callback_query_handler(
    func=lambda message: message.data.startswith('sure_delete_user_deck')
)
def ensure_delete_user_deck_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    deck_id = message.data.split('.')[-1]
    deck = UserDeck.get_by_id(deck_id)

    if deck:
        deck.delete()

        text = replies.USER_DECK_DELETED_REPLY.format(
            deck_title=humanize_title(user.chat_id, deck.title).upper()
        )
    else:
        text = replies.USER_DECK_NOT_FOUND_REPLY
    keyboard = markups.create_menu_markup(user)
    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
        parse_mode='Markdown',
    )
