from random import choice

from telebot import types

from app.bot import utils, replies
from app.bot.keyboard import markups
from app.bot.main import bot
from app.models.Card import Card


@bot.message_handler(func=lambda message: utils.get_expected(message) == 'learn')
def learn_contextual_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    context = utils.get_context(message)

    card_id = context['card_id']
    card = Card.get_by_id(card_id)

    answer = (
        message.text
        if card.question.card_type == 1
        else [ans.strip() for ans in message.text.split(',')]
    )

    if card.add_attempt(answer):
        reply = ''
        keyboard = markups.create_set_knowledge_markup(card)
        reply_list = replies.CORRECT_REPLIES
    else:
        reply = f'{card.question.text}\n\n'
        keyboard = markups.create_basic_learn_markup(card)
        reply_list = replies.WRONG_REPLIES
    reply += choice(reply_list)

    bot.delete_message(user.chat_id, markup_message_id)
    message_id = bot.send_message(user.chat_id, reply, reply_markup=keyboard).message_id
    user.set_inline_keyboard(message_id)


@bot.message_handler(func=lambda message: True)
def wtf_handler(message: types.Message) -> None:
    answers = replies.WTF_MESSAGES
    text = choice(answers)
    bot.send_message(message.chat.id, text)
