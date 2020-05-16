from random import shuffle

from telebot import types

from app.bot import markups, utils
from app.bot.main import bot
from app.localization import buttons, replies
from app.models.Card import Card
from app.models.UserDeck import UserDeck


@bot.callback_query_handler(func=lambda message: message.data.startswith('learn'))
def learn_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    deck_id = message.data.split('.')[-1]
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
    func=lambda message: message.data.startswith('set_knowledge')
)
def set_knowledge_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    card_id, knowledge = message.data.split('.')[1:]
    card = Card.get_by_id(card_id)

    card.set_knowledge(int(knowledge))
    deck = card.user_deck
    new_card = deck.pull_card()
    text, keyboard = utils.build_learn_text_and_keyboard(user, new_card)

    bot.delete_message(user.chat_id, markup_message_id)
    message_id = bot.send_message(user.chat_id, text, reply_markup=keyboard).message_id
    user.set_inline_keyboard(message_id)


@bot.callback_query_handler(func=lambda message: message.data.startswith('show'))
def show_answers_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    card_id, correct = message.data.split('.')[1:]
    card = Card.get_by_id(card_id)

    js = message.message.json

    if card.question.card_type == 3:
        text = correct.replace(',', ', ')
        text += '\n\n' + message.message.text
    else:
        if len(card.question.correct_answers) > 0:
            text = replies.CORRECT_ANSWER_IS_REPLY
        else:
            text = replies.CORRECT_ANSWERS_ARE_REPLY
        for ans in card.question.correct_answers:
            text += ans + ', '
        text = text[:-2]
        text += '\n\n' + message.message.text

    keyboard = utils.repeat_keyboard(js, exclude=[buttons.TIP])

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('submit'))
def submit_answer_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    card_id, correct_answers = message.data.split('.')[1:]

    try:
        chosen = [int(num) for num in utils.parse_chosen_nums(message.message.json)]
    except ValueError:
        chosen = []
    answers = utils.convert_chosen_to_answers(message.message.json, chosen)

    card = Card.get_by_id(card_id)

    if card.add_attempt(answers):
        reply = ''
        keyboard = markups.create_set_knowledge_markup(card)
        reply_list = replies.CORRECT_REPLIES
    else:
        reply = f'{card.question.text}\n\n'
        keyboard = markups.create_answer_sheet_markup(card)
        reply_list = replies.WRONG_REPLIES
    shuffle(reply_list)
    reply += reply_list[0]

    bot.edit_message_text(
        text=reply,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('answer'))
def answer_sheet_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    card_id, correct_numbers, num = message.data.split('.')[1:]
    card = Card.get_by_id(card_id)

    if card.question.card_type == 3:
        text = message.message.text
        js = message.message.json
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
    else:
        if num == correct_numbers:
            text = ''
            reply_list = replies.CORRECT_REPLIES
            keyboard = markups.create_set_knowledge_markup(card)
        else:
            card.inc_attempt()
            text = f'{card.question.text}\n\n'
            reply_list = replies.WRONG_REPLIES
            keyboard = markups.create_answer_sheet_markup(card)
        shuffle(reply_list)
        text += reply_list[0]

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )
