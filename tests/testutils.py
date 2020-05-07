from typing import List, Optional

from app.models.Card import Card
from app.models.User import User
from app.models.UserDeck import UserDeck


def create_user() -> User:
    chat_id = 0
    username = 'durov'
    return User(chat_id, username)


def create_deck() -> UserDeck:
    user = create_user()
    deck_title = 'testing_deck'
    return UserDeck(user, deck_title)


def create_card(
        card_type: int = 0,
        question: str = 'test fact',
        correct: Optional[List[str]] = None,
        wrong: Optional[List[str]] = None,
) -> Card:
    deck = create_deck()
    return Card.fromQuestion(deck, card_type, question, correct, wrong)
