from random import shuffle
from typing import Dict, Optional, Sequence

from telebot.types import InlineKeyboardMarkup

from app import settings
from app.models import CardType

from . import button_texts, buttons, cd


class _Markup:
    def __init__(self, *rows: Sequence[buttons.Button]) -> None:
        row_width = len(max(rows, key=len))
        self._keyboard = InlineKeyboardMarkup(row_width)
        for row in rows:
            btns = [btn.button for btn in row]
            self._keyboard.add(*btns)

    @property
    def keyboard(self) -> InlineKeyboardMarkup:
        return self._keyboard


def sign_up_markup(chat_id: int) -> InlineKeyboardMarkup:
    sign_up_btn = buttons.SignUpButton(chat_id)
    markup = _Markup([sign_up_btn])
    return markup.keyboard


def repeat_keyboard(
    prev_keyboard: dict, exclude_text: Sequence[str], *add_btns: buttons.Button
) -> InlineKeyboardMarkup:
    rows = []
    for row in range(len(prev_keyboard)):
        new_row = []
        for btn in prev_keyboard[row]:
            text = btn.get('text')
            callback_data = btn.get('callback_data')
            if text not in exclude_text:
                new_row.append(buttons.Button(text, callback_data))
        rows.append(new_row)
    for btn in add_btns:
        rows.append([btn])

    markup = _Markup(*rows)
    return markup.keyboard


def main_menu_markup(has_decks: bool) -> InlineKeyboardMarkup:
    decks_btn = buttons.DecksButton()
    add_deck_btn = buttons.AddDeckButton()
    language_btn = buttons.LanguageButton()

    support_btn = buttons.SupportButton()

    first_row = [add_deck_btn, language_btn]
    if has_decks:
        first_row.insert(0, decks_btn)

    second_row = [support_btn]

    markup = _Markup(first_row, second_row)
    return markup.keyboard


def support_markup() -> InlineKeyboardMarkup:
    back_btn = buttons.BackButton(cd.main_menu())
    markup = _Markup([back_btn])
    return markup.keyboard


def decks_markup(decks_map: Dict[int, str]) -> InlineKeyboardMarkup:
    decks_btns = [
        [buttons.DeckButton(decks_map[deck_id], deck_id)]
        for deck_id in decks_map.keys()
    ]
    back_btn = buttons.BackButton(cd.main_menu())

    markup = _Markup(*decks_btns, [back_btn])
    return markup.keyboard


def add_deck_markup() -> InlineKeyboardMarkup:
    create_deck_btn = buttons.CreateNewDeckButton()

    back_btn = buttons.BackButton(cd.main_menu())

    markup = _Markup([create_deck_btn], [back_btn])
    return markup.keyboard


def edit_card_markup(
    card_id: int, deck_id: int, card_type: int
) -> InlineKeyboardMarkup:
    edit_question_btn = buttons.EditQuestionButton(card_id)
    edit_correct_btn = buttons.EditCorrectAnswersButton(card_id)
    edit_wrong_btn = buttons.EditWrongAnswersButton(card_id)

    delete_user_card_btn = buttons.DeleteUserCardButton(card_id)
    cancel_btn = buttons.CancelButton(cd.deck_menu(deck_id))

    first_row = [edit_question_btn]
    second_row = [delete_user_card_btn, cancel_btn]
    if card_type != CardType.FACT:
        first_row.append(edit_correct_btn)  # type: ignore
    if card_type in (CardType.MULTIPLE_CHOICE, CardType.RADIOBUTTON):
        first_row.append(edit_wrong_btn)  # type: ignore

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


def cancel_to_deck_menu_markup(deck_id: int) -> InlineKeyboardMarkup:
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


def correct_answers_await_markup(deck_id: int) -> InlineKeyboardMarkup:
    no_correct_answers_btn = buttons.NoCorrectAnswersButton()
    cancel_btn = buttons.CancelButton(cd.deck_menu(deck_id))

    markup = _Markup([no_correct_answers_btn], [cancel_btn])
    return markup.keyboard


def wrong_answers_await_markup(deck_id: int) -> InlineKeyboardMarkup:
    no_wrong_answers_btn = buttons.NoWrongAnswersButton()
    cancel_btn = buttons.CancelButton(cd.deck_menu(deck_id))

    markup = _Markup([no_wrong_answers_btn], [cancel_btn])
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
    card_id: int,
    deck_id: int,
    correct_answers: Sequence[str],
    wrong_answers: Sequence[str],
) -> InlineKeyboardMarkup:
    answers = list(correct_answers) + list(wrong_answers)
    shuffle(answers)

    answers_btns = [
        [buttons.AnswerButton(i + 1, answer)] for i, answer in enumerate(answers)
    ]

    submit_btn = buttons.SubmitButton(card_id)

    tip_btn = buttons.TipButton(card_id)
    cancel_btn = buttons.CancelButton(cd.deck_menu(deck_id))

    markup = _Markup(*answers_btns, [submit_btn], [tip_btn], [cancel_btn])
    return markup.keyboard


def radiobutton_markup(
    card_id: int, deck_id: int, correct_answer: str, wrong_answers: Sequence[str]
) -> InlineKeyboardMarkup:
    answers = [(ans, False) for ans in wrong_answers]
    answers.append((correct_answer, True))

    shuffle(answers)
    answers_btns = [
        [buttons.RadioAnswerButton(answer[0], card_id, answer[1])] for answer in answers
    ]

    tip_btn = buttons.TipButton(card_id)
    cancel_btn = buttons.CancelButton(cd.deck_menu(deck_id))

    markup = _Markup(*answers_btns, [tip_btn], [cancel_btn])
    return markup.keyboard


def rate_knowledge_markup(card_id: int) -> InlineKeyboardMarkup:
    first_row = [
        buttons.RateKnowledgeButton(card_id, knowledge)
        for knowledge in range(len(button_texts.knowledge_rates()))
    ]
    edit_btn = buttons.EditCardButton(card_id)

    markup = _Markup(first_row, [edit_btn])
    return markup.keyboard


def language_choice_markup(
    current_language: Optional[str] = None,
) -> InlineKeyboardMarkup:
    languages = [
        [buttons.SetLanguageButton(lang)]
        for lang in settings.LANGUAGES.keys()
        if lang != current_language
    ]
    cancel_btn = buttons.CancelButton(cd.main_menu())

    markup = _Markup(*languages, [cancel_btn])
    return markup.keyboard


def tip_markup(prev_keyboard: dict, card_id: int) -> InlineKeyboardMarkup:
    show_btn = buttons.ShowAnswerButton(card_id)
    return repeat_keyboard(prev_keyboard, [button_texts.tip()], show_btn)
