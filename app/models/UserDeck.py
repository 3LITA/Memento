import typing
from random import random, shuffle

from app.run import db
from app import settings

from . import Card, PublicDeck, User, utils


class UserDeck(db.Model):  # type: ignore

    # title is unique inside the User namespace

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(
        db.String(settings.MAX_DECK_TITLE_LENGTH), nullable=False, unique=True
    )
    version = db.Column(db.Integer)
    public_id = db.Column(
        db.Integer, db.ForeignKey(PublicDeck.PublicDeck.id)
    )  # M-O to PublicDeck
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False
    )  # M-O to User
    cards = db.relationship('Card', backref='user_deck', lazy=True, cascade='all, delete-orphan')  # O-M to UserCard

    def __repr__(self) -> str:
        return '<UserDeck %r>' % self.title

    def __init__(self, user: User.User, deck_title: str) -> None:
        search = self.search_by_title(user, deck_title)

        if search:
            raise ValueError('this title is already in use')
        if not utils.is_title_correct(deck_title):
            raise AttributeError('deck title contains incorrect symbols')
        if (
            len(utils.generate_title(user.id, deck_title))
            > settings.MAX_DECK_TITLE_LENGTH
        ):
            raise ValueError('deck title is too long')
        else:
            self.title = utils.generate_title(user.id, deck_title)
            self.user = user
            db.session.add(self)
            db.session.commit()

    def rename(self: 'UserDeck', deck_title: str) -> 'UserDeck':

        if not utils.is_title_correct(deck_title):
            raise ValueError('deck title contains incorrect symbols')

        proper_title = utils.generate_title(self.user.id, deck_title)

        if len(proper_title) > settings.MAX_DECK_TITLE_LENGTH:
            raise ValueError('deck title is too long')

        search = UserDeck.query.filter_by(title=proper_title).first()

        if search:
            raise ValueError('deck title must be unique inside a user namespace')

        else:
            self.title = proper_title
            db.session.add(self)
            db.session.commit()
            return self

    def pull_card(self: 'UserDeck') -> 'Card.Card':

        if not self.cards or len(self.cards) == 0:
            raise ValueError('UserDeck is empty')

        num = random()

        if num < 0.6:
            knowledge = 1
        elif num < 0.9:
            knowledge = 2
        else:
            knowledge = 3

        cards = Card.Card.query.filter_by(knowledge=knowledge, user_deck=self).all()

        if len(cards) == 0:
            cards = self.cards
            shuffle(cards)
        else:
            cards.sort()
        return cards[0]

    def delete(self: 'UserDeck') -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def search_by_title(
        cls, user: User.User, user_deck_title: str
    ) -> typing.Optional['UserDeck']:
        proper_title = utils.generate_title(user.id, user_deck_title)
        return cls.query.filter_by(title=proper_title).first()

    @classmethod
    def get_by_id(cls, card_id: str) -> 'UserDeck':
        deck = cls.query.filter_by(id=card_id).first()
        if not deck:
            raise AttributeError('Deck not found')
        return deck
