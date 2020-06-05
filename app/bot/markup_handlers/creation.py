from telebot import types

from app.bot import markups, utils
from app.bot.main import bot
from app.bot.messages import buttons, replies
from app.models.Card import Card
from app.models.User import User
from app.models.UserDeck import UserDeck
from app.models.utils import humanize_title


@bot.callback_query_handler(func=lambda message: message.data.startswith('add_card'))
def deck_menu_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    utils.forget_context(user)

    user_deck_id = message.data.split('.')[-1]
    user_deck = UserDeck.get_by_id(user_deck_id)
    deck_title = humanize_title(user_deck.title)

    text = replies.CHOOSE_CARD_TYPE_REPLY.format(deck_title.upper())

    keyboard = markups.create_choose_card_type_markup(user_deck_id)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
        parse_mode='Markdown',
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('card_type'))
def card_type_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    user_deck_id, card_type = message.data.split('.')[1:]

    if int(card_type) == 0:
        text = replies.SEND_FACT_REPLY
    else:
        text = replies.SEND_QUESTION_REPLY.format(card_type)
        if int(card_type) == 2:
            text += replies.NOTE_GAPS_FOR_TYPE_2_REPLY
    # TODO: move to markups.py
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text=buttons.BACK, callback_data=f'add_card.{user_deck_id}'
        )
    )
    metadata = {'card_type': int(card_type), 'user_deck_id': int(user_deck_id)}

    utils.set_context(user=user, command='send_question', metadata=metadata)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        parse_mode='Markdown',
        reply_markup=keyboard,
    )


@bot.callback_query_handler(
    func=lambda message: message.data.startswith('no_correct_answers')
)
def no_correct_answers_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    context = utils.get_context(message)
    if context:
        context.pop('command')

    context['correct_answers'] = []

    user_deck = UserDeck.get_by_id(context['user_deck_id'])

    text = replies.THERE_ARE_NO_REPLY.format(
        replies.CORRECT_ANSWERS
    ) + replies.SEND_ANSWERS_REPLY.format(
        "", replies.WRONG_ANSWERS, context['question'],
    )

    keyboard = markups.create_cancel_markup(user_deck=user_deck)

    utils.set_context(user, command='wrong_answers', metadata=context)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(
    func=lambda message: message.data.startswith('no_wrong_answers')
)
def no_wrong_answers_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    context = utils.get_context(message)
    user_deck = UserDeck.get_by_id(context['user_deck_id'])
    card_type = context['card_type']  # seems like it's always 3, but still
    question = context['question']
    correct_answers = context['correct_answers']

    card = Card.fromQuestion(user_deck, card_type, question, correct_answers, [])

    keyboard = markups.create_created_card_markup(card, user_deck)

    utils.forget_context(user)

    text = replies.CARD_WITH_CHOICE_CREATED_REPLY.format(
        type=card_type,
        question=question,
        correct_answers=correct_answers,
        wrong_answers=replies.THERE_ARE_NO_REPLY.format(replies.WRONG_ANSWERS),
    )

    bot.delete_message(user.chat_id, markup_message_id)
    message_id = bot.send_message(
        chat_id=user.chat_id, text=text, reply_markup=keyboard
    ).message_id
    User.set_inline_keyboard(user, message_id)
