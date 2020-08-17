from typing import Optional, Union


class CallbackData:

    _MAIN_MENU = 'main_menu'

    _ADD_DECK = 'add_deck'

    _CREATE_NEW_DECK = 'new_deck'

    _ADD_CARD = 'add_card'

    _LANGUAGE = 'choose_language'

    _MY_DECKS = 'decks_list'

    _DECK_MENU = 'deck_menu'

    _EDIT_USER_DECK = 'edit_deck'

    _EDIT_CARD = 'edit_card'

    _EDIT_QUESTION = 'change_card_question'

    _EDIT_CORRECT_ANSWERS = 'change_card_correct_answers'

    _EDIT_WRONG_ANSWERS = 'change_card_wrong_answers'

    _DELETE_USER_CARD = 'delete_user_card'

    _DELETE_USER_DECK = 'delete_user_deck'

    _SURE_DELETE_USER_DECK = 'sure_delete_user_deck'

    _RENAME_USER_DECK = 'rename_user_deck'

    _LEARN_USER_DECK = 'learn'

    _CARD_TYPE = 'card_type'

    _TIP = 'tip'

    _SHOW_ANSWER = 'show_answer'

    _RATE_KNOWLEDGE = 'rate_knowledge'

    _SET_LANGUAGE = 'set_language'

    _PICK_ANSWER = 'pick_answer'

    _SUBMIT = 'submit'

    _RADIO_ANSWER = 'radio_answer'

    _NO_CORRECT_ANSWERS = 'no_correct_answers'

    _NO_WRONG_ANSWERS = 'no_wrong_answers'

    __instance = None

    def __new__(cls) -> 'CallbackData':
        if not cls.__instance:
            cls.__instance = super(CallbackData, cls).__new__(cls)
        return cls.__instance

    @staticmethod
    def _get_callback(command: str, **kwargs: Optional[Union[str, int]]) -> dict:
        return dict(command=command, **kwargs)

    def main_menu(self) -> dict:
        return self._get_callback(self._MAIN_MENU)

    def add_deck(self) -> dict:
        return self._get_callback(self._ADD_DECK)

    def create_new_deck(self) -> dict:
        return self._get_callback(self._CREATE_NEW_DECK)

    def add_card(self, deck_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._ADD_CARD, deck_id=deck_id)

    def language(self) -> dict:
        return self._get_callback(self._LANGUAGE)

    def my_decks(self) -> dict:
        return self._get_callback(self._MY_DECKS)

    def deck_menu(self, deck_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._DECK_MENU, deck_id=deck_id)

    def edit_user_deck(self, deck_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._EDIT_USER_DECK, deck_id=deck_id)

    def edit_card(self, card_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._EDIT_CARD, card_id=card_id)

    def edit_question(self, card_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._EDIT_QUESTION, card_id=card_id)

    def edit_correct_answers(self, card_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._EDIT_CORRECT_ANSWERS, card_id=card_id)

    def edit_wrong_answers(self, card_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._EDIT_WRONG_ANSWERS, card_id=card_id)

    def delete_user_card(self, card_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._DELETE_USER_CARD, card_id=card_id)

    def delete_user_deck(self, deck_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._DELETE_USER_DECK, deck_id=deck_id)

    def sure_delete_user_deck(self, deck_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._SURE_DELETE_USER_DECK, deck_id=deck_id)

    def rename_user_deck(self, deck_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._RENAME_USER_DECK, deck_id=deck_id)

    def learn_user_deck(self, deck_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._LEARN_USER_DECK, deck_id=deck_id)

    def card_type(
        self,
        deck_id: Optional[Union[int, str]] = None,
        card_type: Optional[Union[int, str]] = None,
    ) -> dict:
        return self._get_callback(self._CARD_TYPE, deck_id=deck_id, card_type=card_type)

    def tip(self, card_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._TIP, card_id=card_id)

    def show_answer(self, card_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._SHOW_ANSWER, card_id=card_id)

    def rate_knowledge(
        self,
        card_id: Optional[Union[int, str]] = None,
        knowledge: Optional[Union[int, str]] = None,
    ) -> dict:
        return self._get_callback(
            self._RATE_KNOWLEDGE, card_id=card_id, knowledge=knowledge
        )

    def set_language(self, language: Optional[str] = None) -> dict:
        return self._get_callback(self._SET_LANGUAGE, language=language)

    def pick_answer(self, option: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._PICK_ANSWER, option=option)

    def submit(self, card_id: Optional[Union[int, str]] = None) -> dict:
        return self._get_callback(self._SUBMIT, card_id=card_id)

    def radio_answer(
        self, card_id: Optional[Union[int, str]] = None, mark: Optional[str] = None
    ) -> dict:
        return self._get_callback(self._RADIO_ANSWER, card_id=card_id, mark=mark)

    def no_correct_answers(self) -> dict:
        return self._get_callback(self._NO_CORRECT_ANSWERS)

    def no_wrong_answers(self) -> dict:
        return self._get_callback(self._NO_WRONG_ANSWERS)
