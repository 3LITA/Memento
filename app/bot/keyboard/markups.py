from random import shuffle
from typing import List

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from app import settings
from app.bot.keyboard import button_texts
from app.models.Card import Card
from app.models.User import User
from app.models.UserDeck import UserDeck


class Markup:

    def __init__(self, row_width: int = 3, *btns: List[InlineKeyboardMarkup]):
        self._markup = InlineKeyboardMarkup(row_width)

    # def add_button(self):


class Button:

    def __init__(self, text, callback_data):
        self._text = text
        self._callback_data = callback_data


class MenuButton(Button):
    pass


class DecksButton(Button):
    pass


class AddDeckButton(Button):
    pass


class LanguageButton(Button):
    pass


class EditQuestionButton(Button):
    pass


class EditCorrectAnswersButton(Button):
    pass


class EditWrongAnswersButton(Button):
    pass


class DeleteButton(Button):
    pass


class CancelButton(Button):
    pass


class RenameButton(Button):
    pass


class LearnButton(Button):
    pass


class EditDeckButton(Button):
    pass


class CancelButton(Button):
    pass


class RenameButton(Button):
    pass


def create_menu_markup(user: User) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup()

    decks_btn = InlineKeyboardButton(text=button_texts.MY_DECKS, callback_data='decks')
    add_deck_btn = InlineKeyboardButton(
        text=button_texts.ADD_DECK, callback_data='add_deck'
    )
    language_btn = InlineKeyboardButton(
        text=button_texts.LANGUAGE, callback_data='language'
    )
    if user.decks and len(user.decks) > 0:
        keyboard.add(decks_btn)
    keyboard.add(add_deck_btn)
    keyboard.add(language_btn)

    return keyboard


def create_edit_card_markup(card: Card) -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup()

    change_question_btn = InlineKeyboardButton(
        text=button_texts.QUESTION, callback_data=f'change_card_question.{card.id}'
    )
    change_correct_answers_btn = InlineKeyboardButton(
        text=button_texts.CORRECT, callback_data=f'change_card_correct_answers.{card.id}'
    )
    change_wrong_answers_btn = InlineKeyboardButton(
        text=button_texts.WRONG, callback_data=f'change_card_wrong_answers.{card.id}'
    )
    delete_card_btn = InlineKeyboardButton(
        text=button_texts.DELETE, callback_data=f'delete_user_card.{card.id}'
    )
    cancel_btn = InlineKeyboardButton(
        text=button_texts.CANCEL, callback_data=f'deck.{card.user_deck.id}'
    )

    first_row = [change_question_btn, change_correct_answers_btn]
    second_row = [delete_card_btn, cancel_btn]

    if card.question.card_type == 3 or card.question.card_type == 4:
        first_row.append(change_wrong_answers_btn)

    inline_keyboard.add(*first_row)
    inline_keyboard.add(*second_row)

    return inline_keyboard


def create_edit_user_deck_markup(deck: UserDeck) -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(row_width=2)

    rename_btn = InlineKeyboardButton(
        text=button_texts.RENAME, callback_data=f'rename_user_deck.{deck.id}'
    )
    delete_btn = InlineKeyboardButton(
        text=button_texts.DELETE, callback_data=f'delete_user_deck.{deck.id}'
    )
    back_btn = InlineKeyboardButton(
        text=button_texts.BACK, callback_data=f'deck.{deck.id}'
    )

    inline_keyboard.add(rename_btn, delete_btn, back_btn)
    return inline_keyboard


def create_rename_user_deck_markup(deck: UserDeck) -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup()

    inline_keyboard.add(
        InlineKeyboardButton(text=button_texts.CANCEL, callback_data=f'deck.{deck.id}')
    )

    return inline_keyboard


def create_delete_user_deck_markup(deck: UserDeck) -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup()

    sure_btn = InlineKeyboardButton(
        text=button_texts.DELETE, callback_data=f'sure_delete_user_deck.{deck.id}'
    )
    cancel_btn = InlineKeyboardButton(
        text=button_texts.CANCEL, callback_data=f'deck.{deck.id}'
    )

    inline_keyboard.add(sure_btn, cancel_btn)
    return inline_keyboard


def create_deck_menu_markup(user_deck: UserDeck) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup()

    add_card_btn = InlineKeyboardButton(
        text=button_texts.ADD_CARD, callback_data=f'add_card.{user_deck.id}'
    )
    learn_btn = InlineKeyboardButton(
        text=button_texts.LEARN, callback_data=f'learn.{user_deck.id}'
    )
    edit_btn = InlineKeyboardButton(
        text=button_texts.EDIT, callback_data=f'edit_deck.{user_deck.id}'
    )
    back_btn = InlineKeyboardButton(text=button_texts.BACK, callback_data='decks')

    first_row = [add_card_btn, edit_btn]
    if user_deck.cards and len(user_deck.cards) > 0:
        first_row.insert(1, learn_btn)

    second_row = [back_btn]
    keyboard.add(*first_row)
    keyboard.add(*second_row)

    return keyboard


def create_new_deck_markup() -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup()
    back_btn = InlineKeyboardButton(text=button_texts.BACK, callback_data='add_deck')

    keyboard.add(back_btn)

    return keyboard


def create_choose_card_type_markup(user_deck_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=settings.CARD_TYPES_RANGE)

    btns = [
        InlineKeyboardButton(
            text=f'{i}', callback_data=f'card_type.{user_deck_id}.{i}'
        )
        for i in range(settings.CARD_TYPES_RANGE)
    ]
    btns.append(
        InlineKeyboardButton(
            text=button_texts.BACK, callback_data=f'deck.{user_deck_id}'
        )
    )

    keyboard.add(*btns)
    return keyboard


def create_created_card_markup(
    card: Card, user_deck: UserDeck
) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(row_width=2)

    edit_btn = InlineKeyboardButton(
        text=button_texts.EDIT, callback_data=f'edit_card.{card.id}'
    )
    next_btn = InlineKeyboardButton(
        text=button_texts.ADD_CARD, callback_data=f'add_card.{user_deck.id}'
    )
    cancel_btn = InlineKeyboardButton(
        text=button_texts.CANCEL, callback_data=f'deck.{user_deck.id}'
    )

    keyboard.add(edit_btn, next_btn, cancel_btn)

    return keyboard


def create_cancel_markup(user_deck: UserDeck) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    cancel_btn = InlineKeyboardButton(
        text=button_texts.CANCEL, callback_data=f'deck.{user_deck.id}'
    )
    keyboard.add(cancel_btn)

    return keyboard


def create_basic_learn_markup(card: Card) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    show_btn = InlineKeyboardButton(
        text=button_texts.TIP, callback_data=f'show.{card.id}.{card.question.card_type}'
    )
    cancel_btn = InlineKeyboardButton(
        text=button_texts.CANCEL, callback_data=f'deck.{card.user_deck.id}'
    )
    keyboard.add(show_btn, cancel_btn)
    return keyboard


def create_answer_sheet_markup(card: Card) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
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
            InlineKeyboardButton(
                text=f'{i + 1}) ' + answers[i][0],
                callback_data=f'answer.{card.id}.{cor}.{i + 1}',
            )
            for i in range(len(answers))
        ]
    )

    if card.question.card_type == 3:
        keyboard.add(
            InlineKeyboardButton(
                text=button_texts.SUBMIT, callback_data=f'submit.{card.id}.{cor}'
            )
        )

    show_btn = InlineKeyboardButton(
        text=button_texts.TIP, callback_data=f'show.{card.id}.{cor}'
    )

    cancel_btn = InlineKeyboardButton(
        text=button_texts.CANCEL, callback_data=f'deck.{card.user_deck.id}'
    )
    keyboard.add(show_btn, cancel_btn)

    return keyboard


def create_set_knowledge_markup(card: Card) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup()

    good_btn = InlineKeyboardButton(
        text=button_texts.KNOWLEDGE_RATES[2], callback_data=f'set_knowledge.{card.id}.3'
    )
    ok_btn = InlineKeyboardButton(
        text=button_texts.KNOWLEDGE_RATES[1], callback_data=f'set_knowledge.{card.id}.2'
    )
    bad_btn = InlineKeyboardButton(
        text=button_texts.KNOWLEDGE_RATES[0], callback_data=f'set_knowledge.{card.id}.1'
    )

    edit_btn = InlineKeyboardButton(
        text=button_texts.EDIT, callback_data=f'edit_card.{card.id}'
    )

    keyboard.add(good_btn, ok_btn, bad_btn)
    keyboard.add(edit_btn)

    return keyboard


def create_language_choice_markup(current_language: str) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(row_width=1)

    languages = settings.LANGUAGES
    keyboard.add(
        *[
            InlineKeyboardButton(
                text=languages[lang], callback_data=f"set_language.{lang}",
            )
            for lang in languages.keys()
            if lang != current_language
        ]
    )

    cancel_btn = InlineKeyboardButton(text=button_texts.CANCEL, callback_data='menu')
    keyboard.add(cancel_btn)

    return keyboard
