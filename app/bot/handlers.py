from random import shuffle

import telebot
from telebot import types

from .. import config, errors
from ..local import TOKEN
from ..logic.change import (
    inc_attempt,
    rename_user_deck,
    set_inline_keyboard,
    set_knowledge,
)
from ..logic.create import create_new_card, create_new_user_deck
from ..logic.delete import (
    delete_user_deck,
    forget_keyboard,
    remove_public_deck,
    remove_user_card,
    remove_user_deck,
)
from ..logic.get import (
    get_card_by_id,
    get_public_deck_by_id,
    get_user_deck_by_id,
    pull_card,
    search_public_deck_by_slug,
    search_user_deck_by_title,
)
from ..logic.share import get_rights, merge_user_deck_with_public, update_user_deck
from ..logic.utils import humanize_title
from . import commands, markups, replies, utils


# from app.bot.commands import *
# import app.bot.replies as replies
# import app.bot.utils as utils
# import app.bot.markups as markups


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=commands.start_commands)
def start_handler(message):
    user = utils.get_user(message)
    keyboard = markups.create_menu_markup(user)
    if user.inline_keyboard_id:
        text = replies.START_AGAIN.format(message.from_user.first_name)
        bot.delete_message(user.chat_id, user.inline_keyboard_id)
    else:
        text = replies.START_REPLY.format(message.from_user.first_name)
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard)


@bot.message_handler(commands=commands.help_commands)
def help_handler(message):
    utils.get_user(message)
    text = replies.HELP_REPLY
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=commands.delete_commands)
def delete_handler(user, title=None):

    if title is None:  # it means we're gonna delete user_card

        expected = utils.expectations.get(user.chat_id)

        if expected is None or (
            expected[0] != '/just_created' and expected[0] != '/learn'
        ):
            text = replies.NOTHING_TO_DELETE_MESSAGE
            bot.send_message(user.chat_id, text)

        else:

            data = expected[1]

            # looking for card
            user_card_id = data.get('user_card_id')
            if user_card_id:
                user_card = get_card_by_id(user_card_id)
                remove_user_card(user_card)

            # looking for public_deck
            public_deck_id = data.get('public_deck_id')
            if public_deck_id:
                public_deck = get_public_deck_by_id(public_deck_id)
                remove_public_deck(public_deck)
            cancel_handler(user)

            text = replies.CARD_DELETED_MESSAGE
            bot.send_message(user.chat_id, text)

    else:
        result = remove_user_deck(user, title)
        if result is None:
            text = replies.DELETE_DECK_NOT_FOUND_MESSAGE
        else:
            cancel_handler(user)
            text = replies.DECK_DELETED_REPLY.format(title)
        bot.send_message(user.chat_id, text)


@bot.message_handler(commands=commands.cancel_commands)
def cancel_handler(message, text_required=False):
    try:
        utils.expectations.pop(message.chat.id)
    except KeyError:
        if text_required:
            text = replies.NOTHING_TO_CANCEL_MESSAGE
            bot.send_message(message.chat.id, text)
    else:
        if text_required:
            text = replies.CANCEL_MESSAGE
            bot.send_message(message.chat.id, text)


@bot.message_handler(commands=commands.expectations_commands)
def expectations_handler(message):
    print(utils.expectations)


@bot.message_handler(commands=commands.share_commands)
def share_handler(user, user_deck_title):

    user_deck = search_user_deck_by_title(user, user_deck_title)
    if user_deck is None:
        text = replies.USER_DECK_NOT_FOUND_REPLY
    else:
        utils.expectations[user.chat_id] = [
            '/share_slug',
            {'user_deck_id': user_deck.id},
        ]
        text = replies.SHARE_MESSAGE
    bot.send_message(user.chat_id, text)


@bot.message_handler(commands=commands.join_commands)
def join_handler(user, slug):

    slug = slug.lower()
    public_deck = search_public_deck_by_slug(slug)
    if public_deck is None:
        text = replies.PUBLIC_DECK_NOT_FOUND_MESSAGE
    else:
        if public_deck.password:
            utils.expectations[user.chat_id] = [
                '/join_password',
                {'public_deck_id': public_deck.id},
            ]
            text = replies.ASK_PASSWORD_MESSAGE
        else:
            utils.expectations[user.chat_id] = [
                '/join_title',
                {'public_deck_id': public_deck.id},
            ]
            text = replies.JOIN_SET_TITLE_MESSAGE
    bot.send_message(user.chat_id, text)


@bot.message_handler(commands=commands.delete_public_commands)
def delete_public_deck_handler(user, slug):

    public_deck = search_public_deck_by_slug(slug)
    if public_deck is None:
        text = replies.NO_PUBLIC_DECK_INSTANCE_MESSAGE
    else:
        rights = get_rights(user, public_deck)
        if rights == 2:
            remove_public_deck(public_deck)
            text = replies.DECK_DELETED_REPLY
        else:
            text = replies.PERMISSION_DENIED_MESSAGE
    bot.send_message(user.chat_id, text)


@bot.message_handler(commands=commands.update_commands)
def update_handler(user, user_deck_title):

    user_deck = search_user_deck_by_title(user, user_deck_title)
    if user_deck is None:
        text = replies.USER_DECK_NOT_FOUND_REPLY
    else:
        try:
            update = update_user_deck(user_deck)
        except errors.NoPublicDeckError:
            text = replies.NO_PUBLIC_DECK_INSTANCE_MESSAGE
        else:
            if update:
                text = replies.DECK_UPDATED_MESSAGE
            else:
                text = replies.DECK_UP_TO_DATE_MESSAGE
    bot.send_message(user.chat_id, text)


@bot.message_handler(commands=commands.merge_commands)
def merge_handler(user, user_deck_title):

    user_deck = search_user_deck_by_title(user, user_deck_title)
    if user_deck is None:
        text = replies.USER_DECK_NOT_FOUND_REPLY
    else:
        try:
            merge = merge_user_deck_with_public(user, user_deck_title)
        except errors.NoPublicDeckError:
            text = replies.NO_PUBLIC_DECK_INSTANCE_MESSAGE
        except errors.RightsError:
            text = replies.PERMISSION_DENIED_MESSAGE
        else:
            if merge:
                text = replies.DECK_UPDATED_MESSAGE
            else:
                text = replies.DECK_UP_TO_DATE_MESSAGE
    bot.send_message(user.chat_id, text)


@bot.message_handler(commands=commands.hire_commands)
def hire_handler(user, slug):

    public_deck = search_public_deck_by_slug(slug)
    if public_deck is None:
        text = replies.PUBLIC_DECK_NOT_FOUND_MESSAGE
    elif get_rights(user, public_deck) != 2:
        text = replies.PERMISSION_DENIED_MESSAGE
    else:
        utils.expectations[user.chat_id] = ['/hire', {'public_deck_id': public_deck.id}]
        text = replies.HIRE_MESSAGE
    bot.send_message(user.chat_id, text)


@bot.message_handler(commands=commands.fire_commands)
def fire_handler(user, slug):

    public_deck = search_public_deck_by_slug(slug)
    if public_deck is None:
        text = replies.PUBLIC_DECK_NOT_FOUND_MESSAGE
    elif get_rights(user, public_deck) != 2:
        text = replies.PERMISSION_DENIED_MESSAGE
    else:
        utils.expectations[user.chat_id] = ['/fire', {'public_deck_id': public_deck.id}]
        text = replies.FIRE_MESSAGE
    bot.send_message(user.chat_id, text)


@bot.message_handler(commands=commands.menu_commands)
def menu_handler(message):
    user = utils.get_user(message)
    if user.inline_keyboard_id:
        try:
            bot.delete_message(message.chat.id, user.inline_keyboard_id)
        except telebot.apihelper.ApiException:
            forget_keyboard(user)

    text = replies.MENU_REPLY
    keyboard = markups.create_menu_markup(user)

    message_id = bot.send_message(
        message.chat.id, text, reply_markup=keyboard
    ).message_id
    set_inline_keyboard(user, message_id)


@bot.callback_query_handler(func=lambda message: message.data.startswith('menu'))
def menu_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    text = replies.MENU_REPLY
    keyboard = markups.create_menu_markup(user)
    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('add_deck'))
def add_deck_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    utils.forget_context(user)

    text = replies.ADD_DECK_REPLY

    keyboard = types.InlineKeyboardMarkup()

    create_deck_btn = types.InlineKeyboardButton(
        text='Создать новую колоду', callback_data='new'
    )
    add_existing_btn = types.InlineKeyboardButton(
        text='Добавить уже имеющуюся 🎱', callback_data='join'
    )
    back_btn = types.InlineKeyboardButton(text='В главное меню', callback_data='menu')

    keyboard.add(create_deck_btn, add_existing_btn)
    keyboard.add(back_btn)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('new'))
def new_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    text = replies.CREATE_NEW_DECK_REPLY
    keyboard = markups.create_new_deck_markup()

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )

    utils.set_context(user, command='new')


@bot.callback_query_handler(func=lambda message: message.data.startswith('decks'))
def decks_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    inline_keyboard = utils.decks_inline_keyboard(user)
    text = replies.CHOOSE_DECK_REPLY
    bot.edit_message_text(
        text, user.chat_id, message_id=markup_message_id, reply_markup=inline_keyboard
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('add_card'))
def deck_menu_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    utils.forget_context(user)

    user_deck_id = message.data.split('.')[-1]
    user_deck = get_user_deck_by_id(user_deck_id)
    deck_title = humanize_title(user.chat_id, user_deck.title)

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
def card_type_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    user_deck_id, card_type = message.data.split('.')[1:]

    if int(card_type) == 0:
        text = replies.SEND_FACT_REPLY
    elif int(card_type) == 2:
        text = replies.SEND_QUESTION_TYPE_2_REPLY
    else:
        text = replies.SEND_QUESTION_REPLY.format(card_type)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text='Назад', callback_data=f'add_card.{user_deck_id}'
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
def no_correct_answers_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    context = utils.get_context(message)
    context.pop('command')

    context['correct_answers'] = []

    user_deck = get_user_deck_by_id(context.get('user_deck_id'))

    text = replies.NO_CORRECT_ANSWERS_REPLY + replies.SEND_WRONG_ANSWERS_REPLY.format(
        context.get('question')
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
def no_wrong_answers_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    context = utils.get_context(message)
    user_deck = get_user_deck_by_id(context.get('user_deck_id'))
    card_type = context.get('card_type')  # seems like it's always 3, but still
    question = context.get('question')
    correct_answers = context.get('correct_answers')

    card = create_new_card(user_deck, card_type, question, correct_answers, [])

    keyboard = markups.create_created_card_markup(card, user_deck)

    utils.forget_context(user)

    text = replies.CARD_WITH_CHOICE_CREATED_REPLY.format(
        card_type, question, correct_answers, replies.NO_WRONG_ANSWERS_REPLY
    )

    bot.delete_message(user.chat_id, markup_message_id)
    message_id = bot.send_message(
        chat_id=user.chat_id, text=text, reply_markup=keyboard
    ).message_id
    set_inline_keyboard(user, message_id)


@bot.callback_query_handler(func=lambda message: message.data.startswith('edit_card'))
def edit_card_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    card_id = message.data.split('.')[-1]
    card = get_card_by_id(card_id)

    keyboard = markups.create_edit_card_markup(card)

    question = card.question.question
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

    text = replies.EDIT_CARD_REPLY.format(question, answers)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('edit_deck'))
def edit_deck_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    deck_id = message.data.split('.')[-1]
    deck = get_user_deck_by_id(deck_id)

    text = replies.EDIT_USER_DECK_REPLY.format_map(
        {'deck_title': humanize_title(user.chat_id, deck.title).upper()}
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
def rename_user_deck_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    deck_id = message.data.split('.')[-1]
    deck = get_user_deck_by_id(deck_id)

    text = replies.RENAME_USER_DECK_REPLY.format_map(
        {'deck_title': humanize_title(user.chat_id, deck.title).upper()}
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
def delete_user_deck_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    deck_id = message.data.split('.')[-1]
    deck = get_user_deck_by_id(deck_id)

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
def sure_delete_user_deck_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    deck_id = message.data.split('.')[-1]
    deck = get_user_deck_by_id(deck_id)

    delete_user_deck(deck)

    text = replies.USER_DECK_DELETED_REPLY.format_map(
        {'deck_title': humanize_title(user.chat_id, deck.title).upper()}
    )
    keyboard = markups.create_menu_markup(user)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
        parse_mode='Markdown',
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('learn'))
def learn_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    deck_id = message.data.split('.')[-1]
    user_deck = get_user_deck_by_id(deck_id)

    card = pull_card(user_deck)

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
def set_knowledge_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    card_id, knowledge = message.data.split('.')[1:]
    card = get_card_by_id(card_id)

    inc_attempt(card)

    set_knowledge(card, knowledge)

    new_card = pull_card(card.user_deck)

    text, keyboard = utils.build_learn_text_and_keyboard(user, new_card)

    bot.delete_message(user.chat_id, markup_message_id)
    message_id = bot.send_message(user.chat_id, text, reply_markup=keyboard).message_id
    set_inline_keyboard(user, message_id)


@bot.callback_query_handler(func=lambda message: message.data.startswith('show'))
def show_answers_markup_handler(message):
    # TODO: show answer has to work properly
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    card_id, cor = message.data.split('.')[1:]
    card = get_card_by_id(card_id)

    js = message.message.json
    # print(message.message.text)

    if card.question.card_type == 3 or card.question.card_type == 4:
        text = cor.replace(',', ', ')
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
        print(message.message.text)

    keyboard = utils.repeat_keyboard(js)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('submit'))
def submit_answer_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    card_id, correct_answers, chosen = message.data.split('.')[1:]

    card = get_card_by_id(card_id)

    if chosen == correct_answers:
        texts = replies.CORRECT_REPLIES
        shuffle(texts)
        text = texts[0]
        keyboard = markups.create_set_knowledge_markup(card)
    else:
        inc_attempt(card)
        texts = replies.WRONG_REPLIES
        shuffle(texts)
        text = texts[0]
        text += '\n\n' + card.question.question + '\n\n' + replies.USER_CHOSEN_REPLY
        keyboard = markups.create_answer_sheet_markup(card)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda message: message.data.startswith('answer'))
def answer_sheet_markup_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    card_id, correct_numbers, num = message.data.split('.')[1:]
    card = get_card_by_id(card_id)

    if card.question.card_type == 3:

        text = message.message.text

        if text.endswith(replies.USER_CHOSEN_REPLY):
            text += num
        else:
            answers = utils.parse_answers(message.message.json)
            if num in answers:
                answers.pop(num)
            else:
                answers.append(num)

            text += ', ' + num
    else:
        if num == correct_numbers:
            texts = replies.CORRECT_REPLIES
            shuffle(texts)
            text = texts[0]
            keyboard = markups.create_set_knowledge_markup(card)
        else:
            inc_attempt(card)
            texts = replies.ANSWER_INCORRECT_MESSAGE
            shuffle(texts)
            text = texts[0]
            keyboard = markups.create_answer_sheet_markup(card)

    bot.edit_message_text(
        text=text,
        chat_id=user.chat_id,
        message_id=markup_message_id,
        reply_markup=keyboard,
    )
    text = 'Nocheinmal das Selbe'


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


@bot.message_handler(regexp=r'^/.*')
def unknown_handler(message):
    text = replies.UNKNOWN_COMMAND_REPLY
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: utils.get_expected(message) == 'new')
def new_deck_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    title = message.text.lower()

    keyboard = markups.create_new_deck_markup()
    try:
        create_new_user_deck(user, deck_title=title)
    except errors.NonUniqueTitleError:
        text = replies.USER_DECK_TITLE_NOT_UNIQUE_REPLY.format(title.upper())
    except ValueError:
        text = replies.TOO_LONG_DECK_TITLE_REPLY
    except AttributeError:
        text = replies.USER_DECK_WRONG_TITLE_FORMATTING_REPLY
    else:
        text = replies.USER_DECK_CREATED_REPLY.format(title.upper())
        utils.forget_context(user)
        keyboard = markups.create_menu_markup(user)
    bot.delete_message(user.chat_id, markup_message_id)
    message_id = bot.send_message(user.chat_id, text, reply_markup=keyboard).message_id
    set_inline_keyboard(user, message_id)


@bot.message_handler(
    func=lambda message: utils.get_expected(message) == 'rename_user_deck'
)
def rename_user_deck_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    title = message.text.lower()

    context = utils.get_context(message)
    deck_id = context.get('deck_id')
    deck = get_user_deck_by_id(deck_id)
    ex_title = humanize_title(user.chat_id, deck.title)

    try:
        rename_user_deck(user, deck, title)
    except errors.NonUniqueTitleError:
        text = replies.USER_DECK_TITLE_NOT_UNIQUE_REPLY.format(title.upper())
        keyboard = markups.create_rename_user_deck_markup(deck)
    except ValueError:
        text = replies.USER_DECK_WRONG_TITLE_FORMATTING_REPLY
        keyboard = markups.create_rename_user_deck_markup(deck)
    else:
        text = replies.USER_DECK_RENAMED_REPLY.format_map(
            {'ex_deck_title': ex_title.upper(), 'new_deck_title': title.upper()}
        )
        keyboard = markups.create_deck_menu_markup(deck)

    bot.delete_message(user.chat_id, markup_message_id)
    message_id = bot.send_message(
        chat_id=user.chat_id, text=text, reply_markup=keyboard, parse_mode='Markdown'
    ).message_id

    set_inline_keyboard(user, message_id)


@bot.message_handler(
    func=lambda message: utils.get_expected(message) == 'send_question'
)
def send_question_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    question = message.text

    context = utils.get_context(message)
    card_type = context.get('card_type')
    user_deck_id = context.get('user_deck_id')

    keyboard = types.InlineKeyboardMarkup()
    cancel_btn = types.InlineKeyboardButton(
        text='Отмена', callback_data=f'deck.{user_deck_id}'
    )
    keyboard.add(cancel_btn)

    if len(question) > config.MAX_QUESTION_LENGTH:
        text = replies.CARD_QUESTION_TOO_LONG_MESSAGE
    else:
        user_deck = get_user_deck_by_id(user_deck_id)
        if card_type == 0:
            user_card = create_new_card(user_deck, card_type, question)
            text = replies.FACT_CREATED_REPLY.format(question)

            keyboard = markups.create_created_card_markup(user_card, user_deck)

            utils.forget_context(user)
        else:
            metadata = {
                'card_type': card_type,
                'user_deck_id': user_deck_id,
                'question': question,
            }
            if card_type == 1:
                text = replies.SEND_ANSWERS_TYPE_1_REPLY.format(question)
            elif card_type == 2:
                gaps = utils.count_gaps(question)
                if gaps == 0:
                    text = replies.INCORRECT_GAPS_NUMBER_IN_QUESTION_REPLY
                    try:
                        bot.delete_message(user.chat_id, markup_message_id)
                    except Exception:
                        pass
                    message_id = bot.send_message(
                        chat_id=user.chat_id,
                        text=text,
                        parse_mode='Markdown',
                        reply_markup=keyboard,
                    ).message_id
                    set_inline_keyboard(user, message_id)
                    return
                metadata['gaps'] = gaps
                text = replies.SEND_ANSWERS_TYPE_2_REPLY.format(gaps, question)
            elif card_type == 3:
                keyboard.add(
                    types.InlineKeyboardButton(
                        text='Правильных ответов нет',
                        callback_data=f'no_correct_answers',
                    )
                )
                text = replies.SEND_CORRECT_ANSWERS_REPLY.format(question)
            elif card_type == 4:
                text = replies.SEND_CORRECT_ANSWER_REPLY.format(question)
            else:
                text = 'Card type out of range'
            utils.set_context(user, command='correct_answers', metadata=metadata)
    bot.delete_message(user.chat_id, markup_message_id)
    message_id = bot.send_message(
        chat_id=user.chat_id, text=text, reply_markup=keyboard
    ).message_id

    set_inline_keyboard(user, message_id)


@bot.message_handler(
    func=lambda message: utils.get_expected(message) == 'correct_answers'
)
def correct_answers_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    context = utils.get_context(message)
    question = context.get('question')

    card_type = context.get('card_type')
    user_deck = get_user_deck_by_id(context.get('user_deck_id'))

    keyboard = markups.create_cancel_markup(user_deck)

    if card_type != 4:
        correct_answers = [
            answer.strip().lower()
            for answer in message.text.split(',')
            if answer.strip() != ''
        ]

        if len(correct_answers) == 0:
            text = replies.INCORRECT_CORRECT_ANSWERS_REPLY.format(question)
            keyboard = markups.create_cancel_markup(user_deck)
        else:
            if card_type == 2 and len(correct_answers) != context.get('gaps'):
                gaps = context.get('gaps')
                text = replies.INCORRECT_GAPS_NUMBER_IN_ANSWER_REPLY.format(
                    gaps, len(correct_answers)
                )
            elif card_type == 3:
                metadata = context
                metadata['correct_answers'] = correct_answers
                metadata.pop('command')
                utils.set_context(user, command='wrong_answers', metadata=metadata)

                text = replies.SEND_WRONG_ANSWERS_REPLY.format(question)
                keyboard.add(
                    types.InlineKeyboardButton(
                        text='Неправильных ответов нет',
                        callback_data='no_wrong_answers',
                    )
                )
            else:
                utils.forget_context(user)

                user_card = create_new_card(
                    user_deck, card_type, question, correct_answers
                )

                text = replies.CARD_CREATED_REPLY.format(
                    card_type, question, correct_answers
                )

                keyboard = markups.create_created_card_markup(user_card, user_deck)
    else:
        metadata = context
        metadata['correct_answers'] = [message.text.strip().lower()]
        metadata.pop('command')
        utils.set_context(user, command='wrong_answers', metadata=metadata)

        text = replies.SEND_WRONG_ANSWERS_REPLY.format(question)

    bot.delete_message(user.chat_id, markup_message_id)
    message_id = bot.send_message(
        chat_id=user.chat_id, text=text, reply_markup=keyboard
    ).message_id
    set_inline_keyboard(user, message_id)


@bot.message_handler(
    func=lambda message: utils.get_expected(message) == 'wrong_answers'
)
def wrong_answers_handler(message):
    user = utils.get_user(message)
    markup_message_id = user.inline_keyboard_id

    context = utils.get_context(message)

    wrong_answers = [
        answer.strip().lower()
        for answer in message.text.split(',')
        if answer.strip() != ''
    ]

    user_deck = get_user_deck_by_id(context.get('user_deck_id'))
    question = context.get('question')
    correct_answers = context.get('correct_answers')

    if len(wrong_answers) == 0:
        text = replies.INCORRECT_WRONG_ANSWERS_REPLY.format(question)
        keyboard = markups.create_cancel_markup(user_deck)
        if len(correct_answers) > 0:
            keyboard.add(
                types.InlineKeyboardButton(
                    text='Неправильных ответов нет', callback_data='no_wrong_answers'
                )
            )
    else:
        card_type = context.get('card_type')

        user_card = create_new_card(
            user_deck, card_type, question, correct_answers, wrong_answers
        )

        keyboard = markups.create_created_card_markup(user_card, user_deck)

        if len(correct_answers) == 0:
            correct_answers = replies.NO_CORRECT_ANSWERS_REPLY

        text = replies.CARD_WITH_CHOICE_CREATED_REPLY.format(
            card_type, question, correct_answers, wrong_answers
        )
        utils.forget_context(user)

    bot.delete_message(user.chat_id, markup_message_id)

    message_id = bot.send_message(
        chat_id=user.chat_id, text=text, reply_markup=keyboard
    ).message_id
    set_inline_keyboard(user, message_id)


@bot.message_handler(func=lambda message: True)
def check_answer_handler(message):
    answers = replies.WTF_MESSAGES
    shuffle(answers)
    text = answers[0]
    bot.send_message(message.chat.id, text)


# TODO: add answer check if card_type == 1
