from random import choice
from typing import Any

from telebot.types import CallbackQuery

from app import exceptions
from app.bot import bot, replies, utils
from app.bot.keyboard import CORRECT_MARK, button_texts, cd, markups
from app.models import CardType
from app.models.Card import Card
from app.models.Deck import Deck
from app.models.User import User


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.learn_deck()))
@utils.log_pressed_button
def learn_markup_handler(deck_id: int, user: User, **_: Any) -> utils.handler_return:
    deck = Deck.get(deck_id)

    try:
        card = deck.pull_card()
    except exceptions.EmptyDeck:
        title = utils.humanize_title(deck.title).upper()
        reply = replies.DECK_IS_EMPTY.format(title=title)
        keyboard = markups.deck_menu_markup(deck_id, False)
    else:
        reply, keyboard = utils.build_learn_text_and_keyboard(user, card)

    return keyboard, reply


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.rate_knowledge())
)
@utils.log_pressed_button
def set_knowledge_markup_handler(
    card_id: int, knowledge: int, user: User, **_: Any
) -> utils.handler_return:
    card = Card.get(card_id)

    card.set_knowledge(int(knowledge))
    deck = card.deck
    new_card = deck.pull_card()
    reply, keyboard = utils.build_learn_text_and_keyboard(user, new_card)

    return keyboard, reply


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.tip()))
@utils.log_pressed_button
def tip_markup_handler(
    callback: CallbackQuery, card_id: int, **_: Any
) -> utils.handler_return:
    card = Card.get(card_id)

    tip = f'{replies.TIP}{card.get_tip()}' if card.has_tips() else replies.NO_TIPS
    reply = replies.Reply(text=f'{callback.message.text}\n\n{tip}')

    prev_keyboard = utils.get_previous_keyboard(callback.message.json)
    keyboard = markups.tip_markup(prev_keyboard, card_id)

    return keyboard, reply


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.show_answer())
)
@utils.log_pressed_button
def show_answers_markup_handler(
    callback: CallbackQuery, card_id: int, **_: Any
) -> utils.handler_return:
    card = Card.get(card_id)

    if card.type == CardType.MULTIPLE_CHOICE and not card.correct_answers:
        text = replies.THERE_ARE_NO_CORRECT_ANSWERS
    else:
        if len(card.correct_answers) == 1:
            text = replies.CORRECT_ANSWER_IS
        else:
            text = replies.CORRECT_ANSWERS_ARE
        text = replies.Reply(f"{text}{', '.join(card.correct_answers)}")

    keyboard = utils.repeat_keyboard(callback, exclude=[button_texts.SHOW_ANSWER])
    reply = replies.Reply(f"{card.question}\n\n{text}")

    return keyboard, reply


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.radio_answer())
)
@utils.log_pressed_button
def radio_button_markup_handler(
    card_id: int, mark: str, **_: Any
) -> utils.handler_return:
    # TODO: use number instead of mark
    card = Card.get(card_id)

    if mark == CORRECT_MARK:
        text = ''
        card.add_attempt(card.correct_answers[0])
        reply_list = replies.CORRECT_REPLIES
        keyboard = markups.rate_knowledge_markup(card.id)
    else:
        card.add_attempt('')
        text = f'{card.question}\n\n'
        reply_list = replies.WRONG_REPLIES
        keyboard = markups.radiobutton_markup(
            card.id, card.deck_id, card.correct_answers[0], card.wrong_answers
        )
    reply = replies.Reply(f'{text}{choice(reply_list)}')

    return keyboard, reply


@bot.callback_query_handler(
    func=lambda msg: utils.button_pressed(msg, cd.pick_answer())
)
@utils.log_pressed_button
def answer_sheet_markup_handler(
    callback: CallbackQuery, option: int, **_: Any
) -> utils.handler_return:
    text = callback.message.text

    keyboard = utils.repeat_keyboard(callback)
    if text.endswith(replies.USER_CHOSEN.text):
        reply = replies.Reply(f"{text} {option}")
    else:
        chosen_nums = utils.parse_chosen_nums(callback)
        if option in chosen_nums:
            chosen_nums.remove(option)
        else:
            chosen_nums.append(option)
            chosen_nums.sort()
        question = utils.parse_question(text)
        reply = replies.Reply(
            f"{question}"
            f"{replies.USER_CHOSEN} {', '.join(str(num) for num in chosen_nums)}"
        )

    return keyboard, reply


@bot.callback_query_handler(func=lambda msg: utils.button_pressed(msg, cd.submit()))
@utils.log_pressed_button
def submit_answer_markup_handler(
    callback: CallbackQuery, card_id: int, **_: Any
) -> utils.handler_return:
    card = Card.get(card_id)

    try:
        chosen = [num for num in utils.parse_chosen_nums(callback)]
    except ValueError:
        chosen = []
    answers = utils.convert_chosen_to_answers(callback, chosen)

    if card.add_attempt(answers).success:
        text = ''
        keyboard = markups.rate_knowledge_markup(card.id)
        reply_list = replies.CORRECT_REPLIES
    else:
        text = f'{card.question}\n\n'
        keyboard = markups.multiple_choice_markup(
            card.id, card.deck_id, card.correct_answers, card.wrong_answers
        )
        reply_list = replies.WRONG_REPLIES

    reply = replies.Reply(f"{text}{choice(reply_list)}")

    return keyboard, reply
