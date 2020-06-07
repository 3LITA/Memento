from typing import Union

from telebot.types import InlineKeyboardButton

from app.settings import LANGUAGES

from . import button_texts, cd, CORRECT_MARK, WRONG_MARK


class Button:

    def __init__(self, text: str, callback: str) -> None:
        self._text = text
        self._callback_data = callback
        self._button = InlineKeyboardButton(text, callback_data=self._callback_data)

    @property
    def button(self):
        return self._button


class DecksButton(Button):

    def __init__(self) -> None:
        text = button_texts.MY_DECKS
        super().__init__(text, cd.add_deck())


class DeckButton(Button):

    def __init__(self, humanized_title: str, deck_id: int) -> None:
        text = humanized_title.upper()
        super().__init__(text, cd.deck_menu(deck_id))


class DeckMenuButton(Button):

    def __init__(self, deck_title: str, deck_id: Union[int, str]) -> None:
        text = deck_title
        super().__init__(text, cd.deck_menu(deck_id))


class CreateNewDeckButton(Button):

    def __init__(self) -> None:
        text = button_texts.CREATE_NEW_DECK
        super().__init__(text, cd.create_new_deck())


class AddDeckButton(Button):

    def __init__(self) -> None:
        text = button_texts.ADD_DECK
        super().__init__(text, cd.add_deck())


class AddCardButton(Button):

    def __init__(self, deck_id: Union[int, str]) -> None:
        text = button_texts.ADD_CARD
        super().__init__(text, cd.add_card(deck_id))


class LanguageButton(Button):

    def __init__(self) -> None:
        text = button_texts.LANGUAGE
        super().__init__(text, cd.language())


class EditQuestionButton(Button):

    def __init__(self, card_id: Union[int, str]) -> None:
        text = button_texts.QUESTION
        super().__init__(text, cd.edit_question(card_id))


class EditCorrectAnswersButton(Button):

    def __init__(self, card_id: Union[int, str]) -> None:
        text = button_texts.CORRECT
        super().__init__(text, cd.edit_correct_answers(card_id))


class EditWrongAnswersButton(Button):

    def __init__(self, card_id: Union[int, str]) -> None:
        text = button_texts.WRONG
        super().__init__(text, cd.edit_wrong_answers(card_id))


class _DeleteButton(Button):

    def __init__(self, callback: str) -> None:
        text = button_texts.DELETE
        super().__init__(text, callback)


class DeleteUserCardButton(_DeleteButton):

    def __init__(self, card_id: Union[int, str]) -> None:
        super().__init__(cd.delete_user_card(card_id))


class DeleteUserDeckButton(_DeleteButton):

    def __init__(self, deck_id: Union[int, str]) -> None:
        super().__init__(cd.delete_user_deck(deck_id))


class SureDeleteDeckButton(_DeleteButton):

    def __init__(self, deck_id: Union[int, str]) -> None:
        super().__init__(cd.sure_delete_user_deck(deck_id))


class CancelButton(Button):

    def __init__(self, callback: str) -> None:
        text = button_texts.CANCEL
        super().__init__(text, callback)


class RenameUserDeckButton(Button):

    def __init__(self, deck_id: Union[int, str]) -> None:
        text = button_texts.RENAME
        super().__init__(text, cd.rename_user_deck(deck_id))


class LearnButton(Button):

    def __init__(self, deck_id: Union[int, str]) -> None:
        text = button_texts.LEARN
        super().__init__(text, cd.learn_user_deck(deck_id))


class _EditButton(Button):

    def __init__(self, callback: str) -> None:
        text = button_texts.EDIT
        super().__init__(text, callback)


class EditDeckButton(_EditButton):

    def __init__(self, deck_id: Union[int, str]) -> None:
        super().__init__(cd.edit_user_deck(deck_id))


class EditCardButton(_EditButton):

    def __init__(self, card_id: Union[int, str]) -> None:
        super().__init__(cd.edit_card(card_id))


class BackButton(Button):

    def __init__(self, callback: str) -> None:
        text = button_texts.BACK
        super().__init__(text, callback)


class CardTypeButton(Button):

    def __init__(self, deck_id: Union[int, str], card_type: int) -> None:
        text = str(card_type)
        super().__init__(text, cd.card_type(deck_id, card_type))


class TipButton(Button):

    def __init__(self, card_id: Union[int, str]) -> None:
        text = button_texts.TIP
        super().__init__(text, cd.tip(card_id))


class RateKnowledgeButton(Button):

    def __init__(self, card_id: Union[int, str], knowledge: int) -> None:
        text = button_texts.KNOWLEDGE_RATES[knowledge]
        super().__init__(text, cd.rate_knowledge(card_id, knowledge))


class SetLanguageButton(Button):

    def __init__(self, language: str) -> None:
        text = LANGUAGES[language]
        super().__init__(text, cd.set_language(language))


class AnswerButton(Button):

    def __init__(self, option_number: int, option_text: str) -> None:
        text = _render_option(option_number, option_text)
        super().__init__(text, cd.answer(option_number))


class SubmitButton(Button):

    def __init__(self, card_id: int) -> None:
        text = button_texts.SUBMIT
        super().__init__(text, cd.submit(card_id))


class RadioAnswerButton(Button):

    def __init__(
            self,
            option_number: int,
            option_text: str,
            card_id: int,
            is_correct: bool = False,
    ) -> None:
        text = _render_option(option_number, option_text)
        correct_mark = CORRECT_MARK if is_correct else WRONG_MARK
        super().__init__(text, cd.radio_answer(card_id, correct_mark))


def _render_option(option_number: int, option_text: str) -> str:
    return f'{option_number}: {option_text}'
