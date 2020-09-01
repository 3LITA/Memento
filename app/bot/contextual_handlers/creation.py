from typing import Any

from telebot.types import Message

from app import exceptions, settings
from app.bot import bot, contexts, replies, utils
from app.bot.keyboard import markups
from app.models import CardType
from app.models.Card import Card
from app.models.Deck import Deck
from app.models.User import User
from app.models.utils import humanize_title


@bot.message_handler(
    func=lambda message: contexts.command_expected(
        message, contexts.ExpectedCommands.CREATE_NEW_DECK
    )
)
@utils.log_message
def new_deck_handler(message: Message, user: User) -> utils.handler_return:
    title = message.text.lower()

    keyboard = markups.new_deck_markup()
    try:
        Deck(user, deck_title=title)
    except exceptions.TooLongError:
        reply = replies.TOO_LONG_DECK_TITLE
    except exceptions.IncorrectCharacters:
        reply = replies.INCORRECT_CHARACTERS_IN_DECK_TITLE
    except exceptions.NotUnique:
        reply = replies.DECK_TITLE_ALREADY_EXISTS.format(title=title.upper())
    else:
        contexts.forget_context(user)
        reply = replies.DECK_CREATED.format(title=title.upper())
        keyboard = markups.main_menu_markup(user.has_decks())

    return keyboard, reply


@bot.message_handler(
    func=lambda message: contexts.command_expected(
        message, contexts.ExpectedCommands.RENAME_USER_DECK
    )
)
@utils.log_message
def rename_user_deck_handler(message: Message, user: User) -> utils.handler_return:
    title = message.text.lower()

    context = contexts.get_context(message)
    deck = Deck.get(context.deck_id)
    ex_title = humanize_title(deck.title)

    keyboard = markups.cancel_to_deck_menu_markup(deck.id)
    try:
        deck.rename(deck_title=title)
    except exceptions.TooLongError:
        reply = replies.TOO_LONG_DECK_TITLE
    except exceptions.IncorrectCharacters:
        reply = replies.INCORRECT_CHARACTERS_IN_DECK_TITLE
    except exceptions.NotUnique:
        reply = replies.DECK_TITLE_ALREADY_EXISTS.format(title=title.upper())
    else:
        contexts.forget_context(user)
        reply = replies.DECK_RENAMED.format(
            previous_deck_title=ex_title.upper(), new_deck_title=title.upper()
        )
        keyboard = markups.deck_menu_markup(deck.id, deck.has_cards())

    return keyboard, reply


@bot.message_handler(
    func=lambda message: contexts.command_expected(
        message, contexts.ExpectedCommands.SEND_FACT
    )
)
@utils.log_message
def send_fact_handler(message: Message, user: User) -> utils.handler_return:
    fact = message.text

    context = contexts.get_context(message)
    deck = Deck.get(context.deck_id)

    if len(fact) > settings.MAX_QUESTION_LENGTH:
        reply = replies.QUESTION_TOO_LONG
        keyboard = markups.cancel_to_deck_menu_markup(deck.id)
    else:
        card = Card(deck, context.card_type, fact)
        reply = replies.FACT_CREATED.format(fact=fact)
        keyboard = markups.card_created_markup(card.id, deck.id)
        contexts.forget_context(user)

    return keyboard, reply


@bot.message_handler(
    func=lambda message: contexts.command_expected(
        message, contexts.ExpectedCommands.SEND_QUESTION
    )
)
@utils.log_message
def send_question_handler(message: Message, **_: Any) -> utils.handler_return:
    question = message.text

    context = contexts.get_context(message)
    deck = Deck.get(context.deck_id)

    keyboard = markups.cancel_to_deck_menu_markup(deck.id)

    if len(question) > settings.MAX_QUESTION_LENGTH:
        reply = replies.QUESTION_TOO_LONG
    else:
        if context.card_type == CardType.SIMPLE:
            reply = replies.SEND_CORRECT_ANSWERS.format(question=question)
            context.command = contexts.ExpectedCommands.SEND_CORRECT_ANSWERS_ONLY
            context.question = question
        elif context.card_type == CardType.GAPS:
            gaps = utils.count_gaps(question)
            if gaps == 0:
                context.command = contexts.ExpectedCommands.SEND_QUESTION
                reply = replies.NO_GAPS_IN_TYPE_2
            else:
                context.gaps = gaps
                reply = replies.SEND_EXACT_NUMBER_CORRECT_ANSWERS.format(
                    number=gaps, question=question
                )
                context.command = contexts.ExpectedCommands.SEND_CORRECT_ANSWERS_ONLY
                context.question = question
        elif context.card_type == CardType.MULTIPLE_CHOICE:
            keyboard = markups.correct_answers_await_markup(deck.id)
            reply = replies.SEND_CORRECT_ANSWERS.format(question=question)
            context.command = contexts.ExpectedCommands.SEND_CORRECT_ANSWERS
            context.question = question
        elif context.card_type == CardType.RADIOBUTTON:
            reply = replies.SEND_CORRECT_ANSWER.format(question=question)
            context.command = contexts.ExpectedCommands.SEND_CORRECT_ANSWERS
            context.question = question
        else:
            raise AttributeError(f"Unknown card type {context.card_type} was chosen")

    return keyboard, reply


@bot.message_handler(
    func=lambda message: contexts.command_expected(
        message, contexts.ExpectedCommands.SEND_CORRECT_ANSWERS_ONLY
    )
)
@utils.log_message
def correct_answers_only_handler(message: Message, user: User) -> utils.handler_return:
    context = contexts.get_context(message)
    deck = Deck.get(context.deck_id)

    correct_answers = [
        answer.strip().lower()
        for answer in message.text.split(',')
        if answer.strip() != ''
    ]

    keyboard = markups.cancel_markup(deck.id)
    if len(correct_answers) == 0 and context.card_type == CardType.SIMPLE:
        reply = replies.INADEQUATE_CORRECT_ANSWERS_SENT.format(
            question=context.question
        )
    elif context.card_type == CardType.GAPS and len(correct_answers) != context.gaps:
        reply = replies.INCORRECT_GAPS_NUMBER_IN_ANSWER.format(
            expected=context.gaps, actual=len(correct_answers)
        )
    else:
        contexts.forget_context(user)
        card = Card(deck, context.card_type, context.question, correct_answers)
        reply = replies.CARD_CREATED.format(
            type=context.card_type,
            question=context.question,
            correct_answers=', '.join(correct_answers),
        )
        keyboard = markups.card_created_markup(card.id, deck.id)

    return keyboard, reply


@bot.message_handler(
    func=lambda message: contexts.command_expected(
        message, contexts.ExpectedCommands.SEND_CORRECT_ANSWERS
    )
)
@utils.log_message
def correct_answers_handler(message: Message, **_: Any) -> utils.handler_return:
    context = contexts.get_context(message)
    deck = Deck.get(context.deck_id)

    correct_answers = [
        answer.strip().lower()
        for answer in message.text.split(',')
        if answer.strip() != ''
    ]
    keyboard = markups.cancel_markup(deck.id)

    if context.card_type == CardType.MULTIPLE_CHOICE:
        if len(correct_answers) > 0:  # when it's 0, button shall be pressed
            context.correct_answers = correct_answers
            context.command = contexts.ExpectedCommands.SEND_WRONG_ANSWERS

            reply = replies.SEND_WRONG_ANSWERS.format(question=context.question)
            keyboard = (
                markups.cancel_markup(deck.id)
                if len(correct_answers) == 0
                else markups.wrong_answers_await_markup(deck.id)
            )
        else:
            reply = replies.INADEQUATE_CORRECT_ANSWERS_SENT.format(
                question=context.question
            )
    else:
        if len(correct_answers) != 1:
            reply = replies.INADEQUATE_CORRECT_ANSWER_SENT.format(
                question=context.question
            )
        else:
            context.correct_answers = correct_answers
            context.command = contexts.ExpectedCommands.SEND_WRONG_ANSWERS

            reply = replies.SEND_WRONG_ANSWERS.format(question=context.question)
            keyboard = markups.cancel_to_deck_menu_markup(deck.id)
    return keyboard, reply


@bot.message_handler(
    func=lambda message: contexts.command_expected(
        message, contexts.ExpectedCommands.SEND_WRONG_ANSWERS
    )
)
@utils.log_message
def wrong_answers_handler(message: Message, user: User) -> utils.handler_return:
    context = contexts.get_context(message)

    wrong_answers = [
        answer.strip().lower()
        for answer in message.text.split(',')
        if answer.strip() != ''
    ]

    deck = Deck.get(context.deck_id)

    if len(wrong_answers) == 0:  # when it's 0, button shall be pressed
        reply = replies.INADEQUATE_WRONG_ANSWERS_SENT.format(question=context.question)
        keyboard = markups.cancel_markup(deck.id)
    else:
        card = Card(
            deck,
            context.card_type,
            context.question,
            context.correct_answers,
            wrong_answers,
        )
        keyboard = markups.card_created_markup(card.id, deck.id)

        correct_answers = (
            ', '.join(context.correct_answers)
            if len(context.correct_answers) > 0
            else replies.THERE_ARE_NO_CORRECT_ANSWERS
        )

        reply = replies.CARD_WITH_CHOICE_CREATED.format(
            type=context.card_type,
            question=context.question,
            correct_answers=correct_answers,
            wrong_answers=', '.join(wrong_answers),
        )
        contexts.forget_context(user)

    return keyboard, reply
