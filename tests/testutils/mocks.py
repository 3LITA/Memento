import random
from functools import partial
from typing import Any, Callable, List, Optional, Sequence

import app.models.User
import app.models.Deck


def get_or_create(
        chat_id: int,
        username: Optional[str] = None,
        id: Optional[int] = None,
) -> app.models.User.User:
    user = app.models.User.User(chat_id, username)
    user._id = id if id else random.randint(1, 10000)
    return user


def dummy_func(*args, **kwargs) -> None:
    pass


def true_func(*args, **kwargs) -> bool:
    return True


def get_decks(*deck_ids: int) -> List[app.models.Deck.Deck]:
    decks = []
    for deck_id in deck_ids:
        deck = app.models.Deck.Deck(user=random_user(),
                                    deck_title=f'deck{deck_id}')
        deck._id = deck_id
        decks.append(deck)

    return decks


def random_user() -> app.models.User.User:
    return app.models.User.User(random.randint(1, 10000))


def deck_get_by_id(
        deck_id: int, deck_title: Optional[str] = None
) -> app.models.Deck.Deck:
    user = random_user()
    deck_title = deck_title if deck_title else f'deck{deck_id}'
    deck = app.models.Deck.Deck(user=user, deck_title=deck_title)
    deck._id = deck_id
    return deck


def user_deck_init(self, deck_title: str, deck_id: int = 9, **kwargs) -> None:
    self.title = deck_title
    self.id = deck_id


def _card_get_by_id(
        card_id: int, deck_id: Optional[int] = None, **kwargs: Any
) -> app.models.Card.Card:
    if not deck_id:
        deck_id = random.randint(1, 10000)
    deck = deck_get_by_id(deck_id)
    card = app.models.Card.Card(deck=deck, **kwargs)
    card.deck = deck
    card._deck_id = deck_id
    card._id = card_id
    return card


def card_get_by_id(
        card_type: int,
        question: str,
        correct_answers: Sequence[str] = (),
        wrong_answers: Sequence[str] = (),
        tips: Sequence[str] = (),
        deck_id: Optional[int] = None,
) -> Callable:
    return partial(
        _card_get_by_id,
        card_type=card_type,
        question=question,
        correct_answers=correct_answers,
        wrong_answers=wrong_answers,
        tips=tips,
        deck_id=deck_id,
    )


def raise_attribute_error(*args, **kwargs):
    raise AttributeError


def raise_value_error(*args, **kwargs):
    raise ValueError


app.models.utils.ActiveRecordMixin.delete = dummy_func
app.models.utils.ActiveRecordMixin.save = dummy_func

app.models.Deck.Deck.search_by_title = dummy_func
app.models.User.User.get_or_create_by_chat_id = get_or_create
app.models.User.User.preferred_language = None
