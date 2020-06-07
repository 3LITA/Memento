from random import shuffle
from typing import List

from telebot.types import InlineKeyboardMarkup

from app import settings

from . import buttons, button_texts, cd


class _Markup:

    def __init__(self, *rows: List[buttons.Button]) -> None:
        rows = list(rows)
        row_width = max(rows, key=len)
        self._keyboard = InlineKeyboardMarkup(row_width)
        for row in rows:
            btns = [btn.button for btn in row]
            self._keyboard.add(*btns)

    @property
    def keyboard(self):
        return self._keyboard


def main_menu_markup(has_decks: bool) -> InlineKeyboardMarkup:
    decks_btn = buttons.DecksButton()
    add_deck_btn = buttons.AddDeckButton()
    language_btn = buttons.LanguageButton()

    first_row = [decks_btn] if has_decks else []
    first_row += [add_deck_btn, language_btn]

    markup = _Markup(first_row)
    return markup.keyboard


def edit_card_markup(card_id: int, deck_id: int, card_type: int) -> InlineKeyboardMarkup:
    edit_question_btn = buttons.EditQuestionButton(card_id)
    edit_correct_btn = buttons.EditCorrectAnswersButton(card_id)
    change_wrong_answers_btn = buttons.EditWrongAnswersButton(card_id)

    delete_user_card_btn = buttons.DeleteUserCardButton(card_id)
    cancel_btn = buttons.CancelButton(cd.deck_menu(deck_id))

    first_row = [edit_question_btn, edit_correct_btn]
    second_row = [delete_user_card_btn, cancel_btn]
    if card_type == 3 or card_type == 4:
        first_row.append(change_wrong_answers_btn)

    markup = _Markup(first_row, second_row)
    return markup.keyboard


def edit_user_deck_markup(deck_id: int) -> InlineKeyboardMarkup:
    rename_btn = buttons.RenameUserDeckButton(deck_id)
    delete_btn = buttons.DeleteUserDeckButton(deck_id)

    back_btn = buttons.BackButton(cd.deck_menu(deck_id))

    first_row = [rename_btn, delete_btn]
    second_row = [back_btn]

    markup = _Markup(first_row, second_row)
    return markup.keyboard


def rename_user_deck_markup(deck_id: int) -> InlineKeyboardMarkup:
    cancel_btn = buttons.CancelButton(cd.deck_menu(deck_id))

    markup = _Markup([cancel_btn])
    return markup.keyboard


def delete_user_deck_markup(deck_id: int) -> InlineKeyboardMarkup:
    sure_btn = buttons.SureDeleteDeckButton(deck_id)
    cancel_btn = buttons.CancelButton(cd.deck_menu(deck_id))

    markup = _Markup([sure_btn, cancel_btn])
    return markup.keyboard


def deck_menu_markup(deck_id: int, has_cards: bool) -> InlineKeyboardMarkup:
    add_card_btn = buttons.AddCardButton(deck_id)
    learn_btn = buttons.LearnButton(deck_id)
    edit_btn = buttons.EditDeckButton(deck_id)

    back_btn = buttons.BackButton(cd.my_decks())

    first_row = [add_card_btn, edit_btn]
    if has_cards:
        first_row.insert(1, learn_btn)

    markup = _Markup(first_row, [back_btn])
    return markup.keyboard


def new_deck_markup() -> InlineKeyboardMarkup:
    back_btn = buttons.BackButton(cd.add_deck())
    markup = _Markup([back_btn])
    return markup.keyboard


def choose_card_type_markup(deck_id: int) -> InlineKeyboardMarkup:
    first_row = [
        buttons.CardTypeButton(deck_id, card_type)
        for card_type in range(settings.CARD_TYPES_RANGE)
    ]
    back_btn = buttons.BackButton(cd.deck_menu(deck_id))

    markup = _Markup(first_row, [back_btn])
    return markup.keyboard


def question_await_markup(deck_id: int) -> InlineKeyboardMarkup:
    back_btn = buttons.BackButton(cd.add_card(deck_id))
    markup = _Markup([back_btn])
    return markup.keyboard


def card_created_markup(card_id: int, deck_id: int) -> InlineKeyboardMarkup:
    edit_btn = buttons.EditCardButton(card_id)
    next_btn = buttons.AddCardButton(deck_id)

    cancel_btn = buttons.CancelButton(cd.deck_menu(deck_id))

    markup = _Markup([edit_btn, next_btn], [cancel_btn])
    return markup.keyboard


def cancel_markup(deck_id: int) -> InlineKeyboardMarkup:
    cancel_btn = buttons.CancelButton(cd.deck_menu(deck_id))
    markup = _Markup([cancel_btn])
    return markup.keyboard


def basic_learn_markup(card_id: int, deck_id: int) -> InlineKeyboardMarkup:
    tip_btn = buttons.TipButton(card_id)
    cancel_btn = buttons.CancelButton(cd.deck_menu(deck_id))

    markup = _Markup([tip_btn, cancel_btn])
    return markup.keyboard


def multiple_choice_markup(
        card_id: int, deck_id: int, correct_answers: List[str], wrong_answers: List[str]
) -> InlineKeyboardMarkup:
    answers = [(ans, True) for ans in correct_answers]
    answers.extend([(ans, False) for ans in wrong_answers])

    shuffle(answers)
    answers_btns = [
        buttons.AnswerButton(i + 1, answers[i][0]) for i in range(len(answers))
    ]

    correct_options = [i + 1 for i in range(len(answers)) if answers[i][1]]
    submit_btn = buttons.SubmitButton(card_id, correct_options)

    tip_btn = buttons.TipButton(card_id)
    cancel_btn = buttons.CancelButton(cd.deck_menu(deck_id))

    markup = _Markup(*answers_btns, [submit_btn], [tip_btn], [cancel_btn])
    return markup.keyboard


def radiobutton_markup(
        card_id: int, deck_id: int, correct_answer: str, wrong_answers: List[str]
) -> InlineKeyboardMarkup:
    answers = [(ans, False) for ans in wrong_answers]
    answers.append((correct_answer, True))

    shuffle(answers)
    answers_btns = [
        buttons.RadioAnswerButton(i + 1, answers[i][0], card_id, answers[i][1])
        for i in range(len(answers))
    ]

    tip_btn = buttons.TipButton(card_id)
    cancel_btn = buttons.CancelButton(cd.deck_menu(deck_id))

    markup = _Markup(*answers_btns, [tip_btn], [cancel_btn])
    return markup.keyboard


def rate_knowledge_markup(card_id: int) -> InlineKeyboardMarkup:
    first_row = [
        buttons.RateKnowledgeButton(card_id, knowledge)
        for knowledge in range(len(button_texts.KNOWLEDGE_RATES))
    ]
    edit_btn = buttons.EditCardButton(card_id)

    markup = _Markup(first_row, [edit_btn])
    return markup.keyboard


def language_choice_markup(current_language: str) -> InlineKeyboardMarkup:
    languages = [
        [buttons.SetLanguageButton(lang)]
        for lang in settings.LANGUAGES.keys()
        if lang != current_language
    ]
    cancel_btn = buttons.CancelButton(cd.menu())

    markup = _Markup(*languages, [cancel_btn])
    return markup.keyboard
