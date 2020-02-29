import typing
from random import random, shuffle

from app import errors
from app.models import models
from .utils import generate_title


def get_decks(user: models.User) -> typing.Optional[typing.List[models.UserDeck]]:
    try:
        return user.decks
    except AttributeError:
        return None


def get_user_deck_by_id(user_deck_id: str) -> typing.Optional[models.UserDeck]:
    return models.UserDeck.query.filter_by(id=user_deck_id).first()


def search_user_deck_by_title(user: models.User, user_deck_title: str) -> typing.Optional[models.UserDeck]:

    proper_title = generate_title(user.chat_id, user_deck_title)

    return models.UserDeck.query.filter_by(title=proper_title).first()


def search_public_deck_by_slug(slug: str) -> typing.Optional[models.PublicDeck]:
    return models.PublicDeck.query.filter_by(slug=slug).first()


def get_public_deck_by_id(public_deck_id: str) -> typing.Optional[models.PublicDeck]:
    return models.PublicDeck.query.filter_by(id=public_deck_id).first()


def get_card_by_id(card_id: str) -> typing.Optional[models.Card]:
    return models.Card.query.filter_by(id=card_id).first()


def search_user_by_username(username: str) -> typing.Optional[models.User]:
    return models.User.query.filter_by(username=username).first()


def pull_card(user_deck: models.UserDeck) -> models.Card:

    if user_deck.cards is None or len(user_deck.cards) == 0:
        raise errors.EmptyDeckError('UserDeck is empty')

    num = random()

    if num < 0.6:
        knowledge = 1
    elif num < 0.9:
        knowledge = 2
    else:
        knowledge = 3

    cards = models.Card.query.filter_by(knowledge=knowledge, user_deck=user_deck).all()

    if len(cards) == 0:
        cards = user_deck.cards
        shuffle(cards)
    else:
        cards.sort()
    return cards[0]
