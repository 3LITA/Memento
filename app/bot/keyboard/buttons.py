from typing import Optional, Union

from telebot.types import InlineKeyboardButton

from app.settings import LANGUAGES, URLS, WEBSITE

from . import CORRECT_MARK, WRONG_MARK, button_texts, cd


class Button:
    def __init__(
        self, text: str, callback: Optional[str] = None, url: Optional[str] = None
    ) -> None:
        self._button = InlineKeyboardButton(text, callback_data=callback, url=url)

    @property
    def button(self) -> InlineKeyboardButton:
        return self._button


class SignUpButton(Button):
    def __init__(self, chat_id: int) -> None:
        text = button_texts.sign_up()
        url = f"{WEBSITE}{URLS.LOGIN}?chat_id={chat_id}"
        super().__init__(text, callback=cd.delete_message(), url=url)


class SupportButton(Button):
    def __init__(self) -> None:
        text = button_texts.support()
        super().__init__(text, callback=cd.support())


class DecksButton(Button):
    def __init__(self) -> None:
        text = button_texts.my_decks()
        super().__init__(text, cd.my_decks())


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
        text = button_texts.create_new_deck()
        super().__init__(text, cd.create_new_deck())


class AddDeckButton(Button):
    def __init__(self) -> None:
        text = button_texts.add_deck()
        super().__init__(text, cd.add_deck())


class AddCardButton(Button):
    def __init__(self, deck_id: Union[int, str]) -> None:
        text = button_texts.add_card()
        super().__init__(text, cd.add_card(deck_id))


class LanguageButton(Button):
    def __init__(self) -> None:
        text = button_texts.language()
        super().__init__(text, cd.language())


class EditQuestionButton(Button):
    def __init__(self, card_id: Union[int, str]) -> None:
        text = button_texts.question()
        super().__init__(text, cd.edit_question(card_id))


class EditCorrectAnswersButton(Button):
    def __init__(self, card_id: Union[int, str]) -> None:
        text = button_texts.correct()
        super().__init__(text, cd.edit_correct_answers(card_id))


class EditWrongAnswersButton(Button):
    def __init__(self, card_id: Union[int, str]) -> None:
        text = button_texts.wrong()
        super().__init__(text, cd.edit_wrong_answers(card_id))


class _DeleteButton(Button):
    def __init__(self, callback: str) -> None:
        text = button_texts.delete()
        super().__init__(text, callback)


class DeleteUserCardButton(_DeleteButton):
    def __init__(self, card_id: Union[int, str]) -> None:
        super().__init__(cd.delete_card(card_id))


class DeleteUserDeckButton(_DeleteButton):
    def __init__(self, deck_id: Union[int, str]) -> None:
        super().__init__(cd.delete_deck(deck_id))


class SureDeleteDeckButton(_DeleteButton):
    def __init__(self, deck_id: Union[int, str]) -> None:
        super().__init__(cd.sure_delete_deck(deck_id))


class CancelButton(Button):
    def __init__(self, callback: str) -> None:
        text = button_texts.cancel()
        super().__init__(text, callback)


class RenameUserDeckButton(Button):
    def __init__(self, deck_id: Union[int, str]) -> None:
        text = button_texts.rename()
        super().__init__(text, cd.rename_deck(deck_id))


class LearnButton(Button):
    def __init__(self, deck_id: Union[int, str]) -> None:
        text = button_texts.learn()
        super().__init__(text, cd.learn_deck(deck_id))


class _EditButton(Button):
    def __init__(self, callback: str) -> None:
        text = button_texts.edit()
        super().__init__(text, callback)


class EditDeckButton(_EditButton):
    def __init__(self, deck_id: Union[int, str]) -> None:
        super().__init__(cd.edit_deck(deck_id))


class EditCardButton(_EditButton):
    def __init__(self, card_id: Union[int, str]) -> None:
        super().__init__(cd.edit_card(card_id))


class BackButton(Button):
    def __init__(self, callback: str) -> None:
        text = button_texts.back()
        super().__init__(text, callback)


class CardTypeButton(Button):
    def __init__(self, deck_id: Union[int, str], card_type: int) -> None:
        text = str(card_type)
        super().__init__(text, cd.card_type(deck_id, card_type))


class TipButton(Button):
    def __init__(self, card_id: Union[int, str]) -> None:
        text = button_texts.tip()
        super().__init__(text, cd.tip(card_id))


class ShowAnswerButton(Button):
    def __init__(self, card_id: Union[int, str]) -> None:
        text = button_texts.show_answer()
        super().__init__(text, cd.show_answer(card_id))


class RateKnowledgeButton(Button):
    def __init__(self, card_id: Union[int, str], knowledge: int) -> None:
        text = button_texts.knowledge_rates()[knowledge]
        super().__init__(text, cd.rate_knowledge(card_id, knowledge))


class SetLanguageButton(Button):
    def __init__(self, language: str) -> None:
        text = LANGUAGES[language]
        super().__init__(text, cd.set_language(language))


class AnswerButton(Button):
    def __init__(self, option_number: int, option_text: str) -> None:
        text = f'{option_number}: {option_text}'
        super().__init__(text, cd.pick_answer(option_number))


class SubmitButton(Button):
    def __init__(self, card_id: int) -> None:
        text = button_texts.submit()
        super().__init__(text, cd.submit(card_id))


class RadioAnswerButton(Button):
    def __init__(
        self, option_text: str, card_id: int, is_correct: bool = False
    ) -> None:
        text = option_text
        correct_mark = CORRECT_MARK if is_correct else WRONG_MARK
        super().__init__(text, cd.radio_answer(card_id, correct_mark))


class NoCorrectAnswersButton(Button):
    def __init__(self) -> None:
        text = button_texts.no_correct_answers()
        super().__init__(text, cd.no_correct_answers())


class NoWrongAnswersButton(Button):
    def __init__(self) -> None:
        text = button_texts.no_wrong_answers()
        super().__init__(text, cd.no_wrong_answers())
