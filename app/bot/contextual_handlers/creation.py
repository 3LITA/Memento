from telebot import types

from app.bot import utils, replies
from app.bot.main import bot
from app.bot.keyboard import markups
from app.models.Card import Card
from app.models.UserDeck import UserDeck
from app.models.utils import humanize_title
from app.settings import dist


@bot.message_handler(func=lambda message: utils.get_expected(message) == 'new')
def new_deck_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    title = message.text.lower()

    keyboard = markups.new_deck_markup()
    try:
        UserDeck(user, deck_title=title)
    except ValueError as err:
        text = str(err)
    except AttributeError as err:
        text = str(err)
    else:
        text = replies.USER_DECK_CREATED_REPLY.format(title=title.upper())
        utils.forget_context(user)
        keyboard = markups.main_menu_markup(user)
    bot.delete_message(user.chat_id, markup_message_id)
    message_id = bot.send_message(
        user.chat_id, text, reply_markup=keyboard, parse_mode='Markdown',
    ).message_id
    user.set_inline_keyboard(message_id)


@bot.message_handler(
    func=lambda message: utils.get_expected(message) == 'rename_user_deck'
)
def rename_user_deck_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    title = message.text.lower()

    context = utils.get_context(message)
    deck_id = context['deck_id']
    deck = UserDeck.get_by_id(deck_id)
    ex_title = humanize_title(deck.title)

    try:
        deck.rename(title)
    except ValueError as err:
        text = str(err)
        keyboard = markups.cancel_to_deck_menu_markup(deck)
    else:
        text = replies.USER_DECK_RENAMED_REPLY.format(
            ex_deck_title=ex_title.upper(), new_deck_title=title.upper(),
        )
        keyboard = markups.deck_menu_markup(deck.id, deck.has_cards())

    bot.delete_message(user.chat_id, markup_message_id)
    message_id = bot.send_message(
        chat_id=user.chat_id, text=text, reply_markup=keyboard, parse_mode='Markdown'
    ).message_id

    user.set_inline_keyboard(message_id)


@bot.message_handler(
    func=lambda message: utils.get_expected(message) == 'send_question'
)
def send_question_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    question = message.text

    context = utils.get_context(message)
    card_type = context['card_type']
    user_deck = UserDeck.get_by_id(context['user_deck_id'])

    keyboard = markups.cancel_to_deck_menu_markup(user_deck.id)

    if len(question) > dist.MAX_QUESTION_LENGTH:
        text = replies.CARD_QUESTION_TOO_LONG_REPLY
    else:
        if card_type == 0:
            user_card = Card.fromQuestion(user_deck, card_type, question)
            text = replies.FACT_CREATED_REPLY.format(question)

            keyboard = markups.card_created_markup(user_card.id, user_deck.id)

            utils.forget_context(user)
        else:
            metadata = {
                'card_type': card_type,
                'user_deck_id': user_deck.id,
                'question': question,
            }
            if card_type == 1:
                text = replies.SEND_ANSWERS_REPLY.format(
                    f"{replies.ALL_POSSIBLE} ", replies.CORRECT_ANSWERS, question
                )
            elif card_type == 2:
                gaps = utils.count_gaps(question)
                if gaps == 0:
                    text = replies.NO_GAPS_IN_TYPE_2_REPLY
                    try:
                        bot.delete_message(user.chat_id, markup_message_id)
                    except Exception as err:
                        print(err)
                    message_id = bot.send_message(
                        chat_id=user.chat_id,
                        text=text,
                        parse_mode='Markdown',
                        reply_markup=keyboard,
                    ).message_id
                    user.set_inline_keyboard(message_id)
                    return
                metadata['gaps'] = gaps
                text = replies.SEND_ANSWERS_REPLY.format(
                    f"{gaps} ", replies.CORRECT_ANSWERS, question
                )
            elif card_type == 3:
                keyboard = markups.correct_answers_await_markup(user_deck.id)
                text = replies.SEND_ANSWERS_REPLY.format(
                    "", replies.CORRECT_ANSWERS, question,
                )
            elif card_type == 4:
                text = replies.SEND_CORRECT_ANSWER_REPLY.format(question)
            else:
                text = 'Card type out of range'
            utils.set_context(user, command='correct_answers', metadata=metadata)
    bot.delete_message(user.chat_id, markup_message_id)
    message_id = bot.send_message(
        chat_id=user.chat_id, text=text, reply_markup=keyboard
    ).message_id

    user.set_inline_keyboard(message_id)


@bot.message_handler(
    func=lambda message: utils.get_expected(message) == 'correct_answers'
)
def correct_answers_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    context = utils.get_context(message)
    question = context['question']

    card_type = context['card_type']
    user_deck = UserDeck.get_by_id(context['user_deck_id'])

    keyboard = markups.cancel_markup(user_deck.id)

    if card_type != 4:
        correct_answers = [
            answer.strip().lower()
            for answer in message.text.split(',')
            if answer.strip() != ''
        ]

        if len(correct_answers) == 0:
            text = replies.INCORRECT_NUMBER_OF_REPLY.format(
                replies.CORRECT_ANSWERS, question
            )
            keyboard = markups.cancel_markup(user_deck.id)
        else:
            if card_type == 2 and len(correct_answers) != context.get('gaps'):
                gaps = context.get('gaps')
                text = replies.INCORRECT_GAPS_NUMBER_IN_ANSWER_REPLY.format(
                    expected=gaps, actual=len(correct_answers),
                )
            elif card_type == 3:
                metadata = context
                metadata['correct_answers'] = correct_answers
                metadata.pop('command')
                utils.set_context(user, command='wrong_answers', metadata=metadata)

                text = replies.SEND_ANSWERS_REPLY.format(
                    "", replies.WRONG_ANSWERS, question,
                )
                keyboard = markups.wrong_answers_await_markup(user_deck.id)
            else:
                utils.forget_context(user)

                user_card = Card.fromQuestion(
                    user_deck, card_type, question, correct_answers
                )

                text = replies.CARD_CREATED_REPLY.format(
                    type=card_type, question=question, correct_answers=correct_answers
                )

                keyboard = markups.card_created_markup(user_card.id, user_deck.id)
    else:
        metadata = context
        metadata['correct_answers'] = [message.text.strip().lower()]
        metadata.pop('command')
        utils.set_context(user, command='wrong_answers', metadata=metadata)

        text = replies.SEND_ANSWERS_REPLY.format("", replies.WRONG_ANSWERS, question)

    bot.delete_message(user.chat_id, markup_message_id)
    message_id = bot.send_message(
        chat_id=user.chat_id, text=text, reply_markup=keyboard
    ).message_id
    user.set_inline_keyboard(message_id)


@bot.message_handler(
    func=lambda message: utils.get_expected(message) == 'wrong_answers'
)
def wrong_answers_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    context = utils.get_context(message)
    if not isinstance(context, dict):
        raise AttributeError(f'context must be dict, not {type(context)}')

    wrong_answers = [
        answer.strip().lower()
        for answer in message.text.split(',')
        if answer.strip() != ''
    ]

    user_deck = UserDeck.get_by_id(context['user_deck_id'])
    question = context.get('question')
    correct_answers = context.get('correct_answers')

    if len(wrong_answers) == 0:
        text = replies.INCORRECT_NUMBER_OF_REPLY.format(replies.WRONG_ANSWERS, question)
        keyboard = markups.cancel_markup(user_deck.id)
        if correct_answers and len(correct_answers) > 0:
            keyboard = markups.wrong_answers_await_markup(user_deck.id)
    else:
        card_type = context.get('card_type')
        if not isinstance(card_type, int) or not isinstance(question, str):
            raise AttributeError(f'{card_type} is not int or {question} is not str')

        user_card = Card.fromQuestion(
            user_deck, card_type, question, correct_answers, wrong_answers
        )

        keyboard = markups.card_created_markup(user_card.id, user_deck.id)

        if correct_answers and len(correct_answers) == 0:
            correct_answers = replies.THERE_ARE_NO_REPLY.format(replies.CORRECT_ANSWERS)

        text = replies.CARD_WITH_CHOICE_CREATED_REPLY.format(
            type=card_type,
            question=question,
            correct_answers=correct_answers,
            wrong_answers=wrong_answers,
        )
        utils.forget_context(user)

    bot.delete_message(user.chat_id, markup_message_id)

    message_id = bot.send_message(
        chat_id=user.chat_id, text=text, reply_markup=keyboard
    ).message_id
    user.set_inline_keyboard(message_id)
