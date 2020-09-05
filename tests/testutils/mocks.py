import random
from functools import partial
from typing import Any, Callable, List, Optional, Sequence

import mock

import app.models.User
import app.models.Deck

from tests.testutils.utils import random_string


def dummy_func(*args, **kwargs) -> None:
    pass


def true_func(*args, **kwargs) -> bool:
    return True


def get_decks(*deck_ids: int) -> List[app.models.Deck.Deck]:
    decks = []
    for deck_id in deck_ids:
        deck = app.models.Deck.Deck(user=_get_user_by(),
                                    deck_title=f'deck{deck_id}')
        deck._id = deck_id
        decks.append(deck)

    return decks


def _get_user(
        id_: int, found: bool = True, has_decks: bool = False
) -> Optional[app.models.User.User]:
    if not found:
        return

    raw_password = (
        f"{random_string().lower()}"
        f"{random_string().upper()}"
        f"{random.randint(0, 1000)}"
    )
    email = f"{random_string()}@mail.com"
    username = random_string()
    user = app.models.User.User(
        email=email, raw_password=raw_password, username=username
    )
    user._id = id_
    return user


def _get_user_by(
        search_result_map: dict,
        has_decks: bool,
        deck_ids: Optional[Sequence[int]] = None,
        **kwargs: Any,
) -> Optional[app.models.User.User]:
    for k in kwargs.keys():
        if k.startswith('_') and search_result_map[k]:
            kwargs[k[1:]] = kwargs.pop(k)
            with mock.patch.object(app.models.User.User, 'get_by', dummy_func):
                user = app.models.User.User(**kwargs)
            user._id = random.randint(1, 1000)
            if has_decks:
                user.has_decks = true_func
            if deck_ids:
                user._decks = [get_deck(deck_id) for deck_id in deck_ids]
            return user


def get_user_by(
        by_chat_id: bool = False,
        by_email: bool = False,
        by_username: bool = False,
        has_decks: bool = False,
        email: Optional[str] = None,
        raw_password: Optional[str] = None,
        username: Optional[str] = None,
        deck_ids: Optional[Sequence[int]] = None,
) -> Callable:
    has_decks = True if deck_ids else has_decks
    search_result_map = {
        '_chat_id': by_chat_id,
        '_email': by_email,
        '_username': by_username,
    }
    if not raw_password:
        raw_password = (
            f"{random_string().lower()}"
            f"{random_string().upper()}"
            f"{random.randint(0, 1000)}"
        )
    return partial(
        _get_user_by,
        search_result_map,
        has_decks=has_decks,
        deck_ids=deck_ids,
        email=email if email else f"{random_string()}@mail.com",
        raw_password=raw_password,
        username=username if username else random_string(),
    )


def get_deck(
        id_: int, deck_title: Optional[str] = None
) -> app.models.Deck.Deck:
    user = _get_user(id_=random.randint(1, 1000), has_decks=True)
    deck_title = deck_title if deck_title else f'deck{id_}'
    deck = app.models.Deck.Deck(user=user, deck_title=deck_title)
    deck._id = id_
    return deck


def _card_get_by_id(
        card_id: int, deck_id: Optional[int] = None, **kwargs: Any
) -> app.models.Card.Card:
    if not deck_id:
        deck_id = random.randint(1, 10000)
    deck = get_deck(deck_id)
    card = app.models.Card.Card(deck=deck, **kwargs)
    card.deck = deck
    card._deck_id = deck_id
    card._id = card_id
    return card


def get_card(
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


def _raise_error(*args, error: Exception, **kwargs):
    raise error


def raise_error(error: Exception, *args, **kwargs):
    return partial(_raise_error, error=error)


def raise_attribute_error(*args, **kwargs):
    raise AttributeError


def raise_value_error(*args, **kwargs):
    raise ValueError


app.support_bot.report = dummy_func
app.support_bot.notify_critical_error = dummy_func

app.models.utils.ActiveRecordMixin.delete = dummy_func
app.models.utils.ActiveRecordMixin.save = dummy_func
app.models.utils.ActiveRecordMixin.get = dummy_func
app.models.utils.ActiveRecordMixin.get_by = dummy_func


app.models.Deck.Deck.search_by_title = dummy_func
