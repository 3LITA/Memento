from typing import Optional, Union


class CallbackData:

    _MAIN_MENU = 'menu'

    _ADD_DECK = 'add_deck'

    _CREATE_NEW_DECK = 'new_deck'

    _ADD_CARD = 'add_card.{deck_id}'

    _LANGUAGE = 'language'

    _MY_DECKS = 'decks'

    _DECK_MENU = 'deck.{deck_id}'

    _EDIT_USER_DECK = 'edit_deck.{deck_id}'

    _EDIT_CARD = 'edit_card.{card_id}'

    _EDIT_QUESTION = 'change_card_question.{card_id}'

    _EDIT_CORRECT_ANSWERS = 'change_card_correct_answers.{card_id}'

    _EDIT_WRONG_ANSWERS = 'change_card_wrong_answers.{card_id}'

    _DELETE_USER_CARD = 'delete_user_card.{card_id}'

    _DELETE_USER_DECK = 'delete_user_deck.{deck_id}'

    _SURE_DELETE_USER_DECK = 'sure_delete_user_deck.{deck_id}'

    _RENAME_USER_DECK = 'rename_user_deck.{deck_id}'

    _LEARN_USER_DECK = 'learn.{deck_id}'

    _CARD_TYPE = 'card_type.{deck_id}.{type}'

    _TIP = 'tip.{card_id}'

    _RATE_KNOWLEDGE = 'rate_knowledge.{card_id}.{knowledge}'

    _SET_LANGUAGE = 'set_language.{language}'

    _ANSWER = 'answer.{option_number}'

    _SUBMIT = 'submit.{card_id}'

    _RADIO_ANSWER = 'radio_answer.{card_id}.{mark}'

    _NO_CORRECT_ANSWERS = 'no_correct_answers'

    _NO_WRONG_ANSWERS = 'no_wrong_answers'

    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(CallbackData, cls).__new__(cls)
        return cls.__instance

    @staticmethod
    def _get_callback(callback: str, **kwargs: Union[str, int]) -> str:
        if kwargs and None not in kwargs.values():
            return callback.format_map(kwargs)
        return callback.split('.')[0]

    def main_menu(self) -> str:
        return self._get_callback(self._MAIN_MENU)

    def add_deck(self) -> str:
        return self._get_callback(self._ADD_DECK)

    def create_new_deck(self) -> str:
        return self._get_callback(self._CREATE_NEW_DECK)

    def add_card(self, deck_id: Optional[int] = None) -> str:
        return self._get_callback(self._ADD_CARD, deck_id=deck_id)

    def language(self) -> str:
        return self._get_callback(self._LANGUAGE)

    def my_decks(self) -> str:
        return self._get_callback(self._MY_DECKS)

    def deck_menu(self, deck_id: Optional[int] = None) -> str:
        return self._get_callback(self._DECK_MENU, deck_id=deck_id)

    def edit_user_deck(self, deck_id: Optional[int] = None) -> str:
        return self._get_callback(self._EDIT_USER_DECK, deck_id=deck_id)

    def edit_card(self, card_id: Optional[int] = None) -> str:
        return self._get_callback(self._EDIT_CARD, card_id=card_id)

    def edit_question(self, card_id: Optional[int] = None) -> str:
        return self._get_callback(self._EDIT_QUESTION, card_id=card_id)

    def edit_correct_answers(self, card_id: Optional[int] = None) -> str:
        return self._get_callback(self._EDIT_CORRECT_ANSWERS, card_id=card_id)

    def edit_wrong_answers(self, card_id: Optional[int] = None) -> str:
        return self._get_callback(self._EDIT_WRONG_ANSWERS, card_id=card_id)

    def delete_user_card(self, card_id: Optional[int] = None) -> str:
        return self._get_callback(self._DELETE_USER_CARD, card_id=card_id)

    def delete_user_deck(self, deck_id: Optional[int] = None) -> str:
        return self._get_callback(self._DELETE_USER_DECK, deck_id=deck_id)

    def sure_delete_user_deck(self, deck_id: Optional[int] = None) -> str:
        return self._get_callback(self._SURE_DELETE_USER_DECK, deck_id=deck_id)

    def rename_user_deck(self, deck_id: Optional[int] = None) -> str:
        return self._get_callback(self._RENAME_USER_DECK, deck_id=deck_id)

    def learn_user_deck(self, deck_id: Optional[int] = None) -> str:
        return self._get_callback(self._LEARN_USER_DECK, deck_id=deck_id)

    def card_type(
            self, deck_id: Optional[int] = None, card_type: Optional[int] = None
    ) -> str:
        return self._get_callback(self._CARD_TYPE, deck_id=deck_id, type=card_type)

    def tip(self, card_id: Optional[int] = None) -> str:
        return self._get_callback(self._TIP, card_id=card_id)

    def rate_knowledge(
            self, card_id: Optional[int] = None, knowledge: Optional[int] = None
    ) -> str:
        return self._get_callback(
            self._RATE_KNOWLEDGE, card_id=card_id, knowledge=knowledge
        )

    def set_language(self, language: Optional[str] = None) -> str:
        return self._get_callback(self._SET_LANGUAGE, language=language)

    def answer(self, option_number: Optional[int] = None) -> str:
        return self._get_callback(self._ANSWER, option_number=option_number)

    def submit(self, card_id: Optional[int] = None) -> str:
        return self._get_callback(self._SUBMIT, card_id=card_id)

    def radio_answer(
            self, card_id: Optional[int] = None, mark: Optional[str] = None) -> str:
        return self._get_callback(self._RADIO_ANSWER, card_id=card_id, mark=mark)

    def no_correct_answers(self) -> str:
        return self._get_callback(self._NO_CORRECT_ANSWERS)

    def no_wrong_answers(self) -> str:
        return self._get_callback(self._NO_WRONG_ANSWERS)
