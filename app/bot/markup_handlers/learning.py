from random import shuffle

from telebot import types

from app.bot import markups, utils
from app.bot.main import bot
from app.locale import replies, buttons
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

    card.set_knowledge(knowledge)
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

    if card.question.card_type == 3 or card.question.card_type == 4:
        text = correct.replace(',', ', ')
        text += '\n\n' + message.message.text
    else:
        if len(card.question.correct_answers) > 0:
            text = 'Правильный ответ: '
        else:
            text = 'Правильные ответы: '
        for ans in card.question.correct_answers:
            text += ans + ', '
        text = text[:-2]
        text += '\n\n' + message.message.text
        # print(message.message.text)

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

    card_id, correct_answers, chosen = message.data.split('.')[1:]

    card = Card.get_by_id(card_id)

    if chosen == correct_answers:
        texts = replies.CORRECT_REPLIES
        shuffle(texts)
        text = texts[0]
        keyboard = markups.create_set_knowledge_markup(card)
    else:
        card.inc_attempt()
        texts = replies.WRONG_REPLIES
        shuffle(texts)
        text = texts[0]
        text += '\n\n' + utils.build_chosen_answers_reply(card)
        keyboard = markups.create_answer_sheet_markup(card)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('answer'))
def answer_sheet_markup_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id
    print('In answer_sheet_markup_handler')

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
            print(text)
    else:
        if num == correct_numbers:
            texts = replies.CORRECT_REPLIES
            shuffle(texts)
            text = texts[0]
            keyboard = markups.create_set_knowledge_markup(card)
        else:
            card.inc_attempt()
            texts = replies.WRONG_REPLIES
            shuffle(texts)
            text = texts[0]
            keyboard = markups.create_answer_sheet_markup(card)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )
