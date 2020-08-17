from random import random, shuffle
from typing import Sequence

from app import settings
from app.app import db, logging

from . import Card, User, utils


class Deck(db.Model, utils.ActiveRecordMixin):  # type: ignore

    _id = db.Column(db.Integer, primary_key=True, name='id')
    _title = db.Column(
        db.String(settings.MAX_DECK_TITLE_LENGTH),
        nullable=False,
        unique=True,
        name='title',
    )  # title is unique inside a User's namespace
    _user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False, name='user_id'
    )  # M-O to User
    _cards = db.relationship(
        'Card', backref='deck', lazy=True, cascade='all, delete-orphan'
    )  # O-M to Card

    def __repr__(self) -> str:
        return '<Deck %r>' % self.title

    def __init__(self, user: 'User.User', deck_title: str) -> None:
        if not utils.is_title_correct(deck_title):
            logging.error("Deck title %s contains incorrect symbols", deck_title)
            raise AttributeError(f'deck title contains incorrect symbols: {deck_title}')
        if (
            len(utils.generate_title(user.id, deck_title))
            > settings.MAX_DECK_TITLE_LENGTH
        ):
            logging.error("Too long deck title %s", deck_title)
            raise ValueError(f'deck title is too long: {deck_title}')

        deck_title = utils.generate_title(user.id, deck_title)
        search = Deck.search_by_title(user, deck_title)

        if search:
            logging.error("Tried to create deck with non unique title %s", deck_title)
            raise ValueError(f'this title is already in use: {deck_title}')

        self._title = deck_title
        self._user = user
        self.save()

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def user(self) -> 'User.User':
        return self._user

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def cards(self) -> Sequence['Card.Card']:
        return self._cards

    def has_cards(self) -> bool:
        return bool(self.cards and len(self.cards) > 0)

    def rename(self, deck_title: str) -> None:

        if not utils.is_title_correct(deck_title):
            logging.error("Deck title %s contains incorrect symbols", deck_title)
            raise ValueError(f'deck title contains incorrect symbols: {deck_title}')

        proper_title = utils.generate_title(self.user.id, deck_title)

        if len(proper_title) > settings.MAX_DECK_TITLE_LENGTH:
            logging.error("Too long deck title %s", deck_title)
            raise ValueError(f'deck title is too long: {deck_title}')

        search = Deck.get_by(title=proper_title)

        if search:
            logging.error("Tried to create deck with non unique title %s", proper_title)
            raise ValueError(
                f'deck title must be unique inside a user namespace: {proper_title}'
            )

        else:
            self._title = proper_title
            self.save()

    def pull_card(self) -> 'Card.Card':
        if not self.cards or len(self.cards) == 0:
            logging.error("Deck with id %s is empty", self.id)
            raise ValueError('UserDeck is empty')

        num = random()

        if num < 0.6:
            knowledge = 1
        elif num < 0.9:
            knowledge = 2
        else:
            knowledge = 3

        cards = Card.Card.query.filter_by(knowledge=knowledge, deck=self).all()
        if len(cards) == 0:
            cards = list(self.cards)

        shuffle(cards)
        return cards[0]
