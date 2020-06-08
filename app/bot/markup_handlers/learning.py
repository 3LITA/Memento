from random import choice

from telebot.types import CallbackQuery

from app.bot import replies, utils
from app.bot.keyboard import cd, markups
from app.bot.main import bot
from app.models.Card import Card
from app.models.UserDeck import UserDeck


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.learn_user_deck())
)
def learn_markup_handler(callback: CallbackQuery) -> None:
    user = utils.get_user(callback)
    markup_message_id = user.inline_keyboard_id

    deck_id = callback.data.split('.')[-1]
    user_deck = UserDeck.get_by_id(deck_id)

    card = user_deck.pull_card()

    text, keyboard = utils.build_learn_text_and_keyboard(user, card)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.rate_knowledge())
)
def set_knowledge_markup_handler(callback: CallbackQuery) -> None:
    user = utils.get_user(callback)
    markup_message_id = user.inline_keyboard_id

    card_id, knowledge = callback.data.split('.')[1:]
    card = Card.get_by_id(card_id)

    card.set_knowledge(int(knowledge))
    deck = card.user_deck
    new_card = deck.pull_card()
    text, keyboard = utils.build_learn_text_and_keyboard(user, new_card)

    bot.delete_message(user.chat_id, markup_message_id)
    message_id = bot.send_message(user.chat_id, text, reply_markup=keyboard).message_id
    user.set_inline_keyboard(message_id)


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.tip()))
def tip_markup_handler(callback: CallbackQuery) -> None:
    user = utils.get_user(callback)
    markup_message_id = user.inline_keyboard_id

    card_id = callback.data.split('.')[1]
    card = Card.get_by_id(card_id)

    tip = replies.TIP + card.get_tip() if card.has_tips() else replies.NO_TIPS_REPLY
    reply = callback.message.text + '\n\n' + tip

    prev_keyboard = utils.get_prev_keyboard(callback.message.json)
    keyboard = markups.tip_markup(prev_keyboard, card_id)

    bot.edit_message_text(
        text=reply,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


# @bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.tip()))
# def tip_markup_handler(message: types.Message) -> None:
#     # TODO: make show handler from this
#
#     user = utils.get_user(message)
#     markup_message_id = user.inline_keyboard_id
#
#     card_id, correct = message.data.split('.')[1:]
#     card = Card.get_by_id(card_id)
#
#     js = message.message.json
#
#     if card.question.card_type == 3:
#         text = correct.replace(',', ', ')
#         text += '\n\n' + message.message.text
#     else:
#         if len(card.question.correct_answers) > 0:
#             text = replies.CORRECT_ANSWER_IS_REPLY
#         else:
#             text = replies.CORRECT_ANSWERS_ARE_REPLY
#         for ans in card.question.correct_answers:
#             text += ans + ', '
#         text = text[:-2]
#         text += '\n\n' + message.message.text
#
#     keyboard = utils.repeat_keyboard(js, exclude=[button_texts.TIP])
#
#     bot.edit_message_text(
#         text=text,
#         chat_id=user.chat_id,
#         message_id=markup_message_id,
#         reply_markup=keyboard,
#     )


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.submit()))
def submit_answer_markup_handler(callback: CallbackQuery) -> None:
    user = utils.get_user(callback)
    markup_message_id = user.inline_keyboard_id

    card_id = callback.data.split('.')[1]

    try:
        chosen = [int(num) for num in utils.parse_chosen_nums(callback.message.json)]
    except ValueError:
        chosen = []
    answers = utils.convert_chosen_to_answers(callback.message.json, chosen)

    card = Card.get_by_id(card_id)

    if card.add_attempt(answers):
        reply = ''
        keyboard = markups.rate_knowledge_markup(card)
        reply_list = replies.CORRECT_REPLIES
    else:
        reply = f'{card.question.text}\n\n'
        keyboard = markups.multiple_choice_markup(
            card.id,
            card.user_deck.id,
            card.question.correct_answers,
            card.question.wrong_answers,
        )
        reply_list = replies.WRONG_REPLIES

    reply += choice(reply_list)

    bot.edit_message_text(
        text=reply,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.answer()))
def answer_sheet_markup_handler(callback: CallbackQuery) -> None:
    user = utils.get_user(callback)
    markup_message_id = user.inline_keyboard_id

    card_id, correct_numbers, num = callback.data.split('.')[1:]
    card = Card.get_by_id(card_id)

    if card.question.card_type == 3:
        text = callback.message.text
        js = callback.message.json
        keyboard = utils.repeat_keyboard(js)
        if text.endswith(replies.USER_CHOSEN_REPLY):
            text += ' ' + num
        else:
            chosen_nums = utils.parse_chosen_nums(js)
            if num in chosen_nums:
                chosen_nums.remove(num)
            else:
                chosen_nums.append(num)
                chosen_nums = sorted(chosen_nums)
            text = utils.build_chosen_answers_reply(card) + ', '.join(chosen_nums)
    elif card.question.card_type == 4:
        if num == correct_numbers:
            text = ''
            reply_list = replies.CORRECT_REPLIES
            keyboard = markups.rate_knowledge_markup(card)
        else:
            card.inc_attempt()
            text = f'{card.question.text}\n\n'
            reply_list = replies.WRONG_REPLIES
            keyboard = markups.radiobutton_markup(
                card.id,
                card.user_deck.id,
                card.question.correct_answers[0],
                card.question.wrong_answers,
            )
        text += choice(reply_list)
    else:
        raise ValueError

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )
