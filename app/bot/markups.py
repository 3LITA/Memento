from random import shuffle

from telebot import types

from app import settings
from app.localization import buttons
from app.models.Card import Card
from app.models.User import User
from app.models.UserDeck import UserDeck


def create_menu_markup(user: User) -> types.InlineKeyboardMarkup:

    keyboard = types.InlineKeyboardMarkup()

    decks_btn = types.InlineKeyboardButton(text=buttons.MY_DECKS, callback_data='decks')
    add_deck_btn = types.InlineKeyboardButton(
        text=buttons.ADD_DECK, callback_data='add_deck'
    )
    language_btn = types.InlineKeyboardButton(
        text=buttons.LANGUAGE, callback_data='language'
    )
    if user.decks and len(user.decks) > 0:
        keyboard.add(decks_btn)
    keyboard.add(add_deck_btn)
    keyboard.add(language_btn)

    return keyboard


def create_edit_card_markup(card: Card) -> types.InlineKeyboardMarkup:
    inline_keyboard = types.InlineKeyboardMarkup()

    change_question_btn = types.InlineKeyboardButton(
        text=buttons.QUESTION, callback_data=f'change_card_question.{card.id}'
    )
    change_correct_answers_btn = types.InlineKeyboardButton(
        text=buttons.CORRECT, callback_data=f'change_card_correct_answers.{card.id}'
    )
    change_wrong_answers_btn = types.InlineKeyboardButton(
        text=buttons.WRONG, callback_data=f'change_card_wrong_answers.{card.id}'
    )
    delete_card_btn = types.InlineKeyboardButton(
        text=buttons.DELETE, callback_data=f'delete_user_card.{card.id}'
    )
    cancel_btn = types.InlineKeyboardButton(
        text=buttons.CANCEL, callback_data=f'deck.{card.user_deck.id}'
    )

    first_row = [change_question_btn, change_correct_answers_btn]
    second_row = [delete_card_btn, cancel_btn]

    if card.question.card_type == 3 or card.question.card_type == 4:
        first_row.append(change_wrong_answers_btn)

    inline_keyboard.add(*first_row)
    inline_keyboard.add(*second_row)

    return inline_keyboard


def create_edit_user_deck_markup(deck: UserDeck) -> types.InlineKeyboardMarkup:
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)

    rename_btn = types.InlineKeyboardButton(
        text=buttons.RENAME, callback_data=f'rename_user_deck.{deck.id}'
    )
    delete_btn = types.InlineKeyboardButton(
        text=buttons.DELETE, callback_data=f'delete_user_deck.{deck.id}'
    )
    back_btn = types.InlineKeyboardButton(
        text=buttons.BACK, callback_data=f'deck.{deck.id}'
    )

    inline_keyboard.add(rename_btn, delete_btn, back_btn)
    return inline_keyboard


def create_rename_user_deck_markup(deck: UserDeck) -> types.InlineKeyboardMarkup:
    inline_keyboard = types.InlineKeyboardMarkup()

    inline_keyboard.add(
        types.InlineKeyboardButton(text=buttons.CANCEL, callback_data=f'deck.{deck.id}')
    )

    return inline_keyboard


def create_delete_user_deck_markup(deck: UserDeck) -> types.InlineKeyboardMarkup:
    inline_keyboard = types.InlineKeyboardMarkup()

    sure_btn = types.InlineKeyboardButton(
        text=buttons.DELETE, callback_data=f'sure_delete_user_deck.{deck.id}'
    )
    cancel_btn = types.InlineKeyboardButton(
        text=buttons.CANCEL, callback_data=f'deck.{deck.id}'
    )

    inline_keyboard.add(sure_btn, cancel_btn)
    return inline_keyboard


def create_deck_menu_markup(user_deck: UserDeck) -> types.InlineKeyboardMarkup:

    keyboard = types.InlineKeyboardMarkup()

    add_card_btn = types.InlineKeyboardButton(
        text=buttons.ADD_CARD, callback_data=f'add_card.{user_deck.id}'
    )
    learn_btn = types.InlineKeyboardButton(
        text=buttons.LEARN, callback_data=f'learn.{user_deck.id}'
    )
    edit_btn = types.InlineKeyboardButton(
        text=buttons.EDIT, callback_data=f'edit_deck.{user_deck.id}'
    )
    back_btn = types.InlineKeyboardButton(text=buttons.BACK, callback_data='decks')

    first_row = [add_card_btn, edit_btn]
    if user_deck.cards and len(user_deck.cards) > 0:
        first_row.insert(1, learn_btn)

    second_row = [back_btn]
    keyboard.add(*first_row)
    keyboard.add(*second_row)

    return keyboard


def create_new_deck_markup() -> types.InlineKeyboardMarkup:

    keyboard = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton(text=buttons.BACK, callback_data='add_deck')

    keyboard.add(back_btn)

    return keyboard


def create_choose_card_type_markup(user_deck_id: int) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=settings.CARD_TYPES_RANGE)

    btns = [
        types.InlineKeyboardButton(
            text=f'{i}', callback_data=f'card_type.{user_deck_id}.{i}'
        )
        for i in range(settings.CARD_TYPES_RANGE)
    ]
    btns.append(
        types.InlineKeyboardButton(
            text=buttons.BACK, callback_data=f'deck.{user_deck_id}'
        )
    )

    keyboard.add(*btns)
    return keyboard


def create_created_card_markup(
    card: Card, user_deck: UserDeck
) -> types.InlineKeyboardMarkup:

    keyboard = types.InlineKeyboardMarkup(row_width=2)

    edit_btn = types.InlineKeyboardButton(
        text=buttons.EDIT, callback_data=f'edit_card.{card.id}'
    )
    next_btn = types.InlineKeyboardButton(
        text=buttons.ADD_CARD, callback_data=f'add_card.{user_deck.id}'
    )
    cancel_btn = types.InlineKeyboardButton(
        text=buttons.CANCEL, callback_data=f'deck.{user_deck.id}'
    )

    keyboard.add(edit_btn, next_btn, cancel_btn)

    return keyboard


def create_cancel_markup(user_deck: UserDeck) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    cancel_btn = types.InlineKeyboardButton(
        text=buttons.CANCEL, callback_data=f'deck.{user_deck.id}'
    )
    keyboard.add(cancel_btn)

    return keyboard


def create_basic_learn_markup(card: Card) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    show_btn = types.InlineKeyboardButton(
        text=buttons.TIP, callback_data=f'show.{card.id}.{card.question.card_type}'
    )
    cancel_btn = types.InlineKeyboardButton(
        text=buttons.CANCEL, callback_data=f'deck.{card.user_deck.id}'
    )
    keyboard.add(show_btn, cancel_btn)
    return keyboard


def create_answer_sheet_markup(card: Card) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    answers = [[ans, True] for ans in card.question.correct_answers]
    answers.extend([[ans, False] for ans in card.question.wrong_answers])

    shuffle(answers)

    corrects = [i for i in range(len(answers)) if answers[i][1]]

    cor = ''
    for num in corrects:
        cor += str(num + 1) + ','
    cor = cor[:-1]

    if cor == '':
        cor = '0'

    keyboard.add(
        *[
            types.InlineKeyboardButton(
                text=f'{i + 1}) ' + answers[i][0],
                callback_data=f'answer.{card.id}.{cor}.{i + 1}',
            )
            for i in range(len(answers))
        ]
    )

    if card.question.card_type == 3:
        keyboard.add(
            types.InlineKeyboardButton(
                text=buttons.SUBMIT, callback_data=f'submit.{card.id}.{cor}'
            )
        )

    show_btn = types.InlineKeyboardButton(
        text=buttons.TIP, callback_data=f'show.{card.id}.{cor}'
    )

    cancel_btn = types.InlineKeyboardButton(
        text=buttons.CANCEL, callback_data=f'deck.{card.user_deck.id}'
    )
    keyboard.add(show_btn, cancel_btn)

    return keyboard


def create_set_knowledge_markup(card: Card) -> types.InlineKeyboardMarkup:

    keyboard = types.InlineKeyboardMarkup()

    good_btn = types.InlineKeyboardButton(
        text=buttons.KNOWLEDGE_RATES[2], callback_data=f'set_knowledge.{card.id}.3'
    )
    ok_btn = types.InlineKeyboardButton(
        text=buttons.KNOWLEDGE_RATES[1], callback_data=f'set_knowledge.{card.id}.2'
    )
    bad_btn = types.InlineKeyboardButton(
        text=buttons.KNOWLEDGE_RATES[0], callback_data=f'set_knowledge.{card.id}.1'
    )

    edit_btn = types.InlineKeyboardButton(
        text=buttons.EDIT, callback_data=f'edit_card.{card.id}'
    )

    keyboard.add(good_btn, ok_btn, bad_btn)
    keyboard.add(edit_btn)

    return keyboard


def create_language_choice_markup(current_language: str) -> types.InlineKeyboardMarkup:

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    languages = settings.LANGUAGES
    keyboard.add(
        *[
            types.InlineKeyboardButton(
                text=languages[lang], callback_data=f"set_language.{lang}",
            )
            for lang in languages.keys()
            if lang != current_language
        ]
    )

    cancel_btn = types.InlineKeyboardButton(text=buttons.CANCEL, callback_data='menu')
    keyboard.add(cancel_btn)

    return keyboard
