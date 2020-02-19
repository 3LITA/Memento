from sqlalchemy.dialects.postgresql import ARRAY

from ..config import (
    MAX_ANSWER_LENGTH,
    MAX_DECK_TITLE_LENGTH,
    MAX_QUESTION_LENGTH,
    MAX_SLUG_LENGTH,
)
from ..main import db
from .mutable import MutableList


class PublicDeck(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(MAX_DECK_TITLE_LENGTH), nullable=False)
    version = db.Column(db.Integer, default=0, nullable=False)
    slug = db.Column(db.String(MAX_SLUG_LENGTH), nullable=False)
    password = db.Column(db.LargeBinary)
    questions = db.relationship(
        'Question', backref='public_deck', lazy=True
    )  # O-M to PublicCard
    user_decks = db.relationship('UserDeck', backref='public_deck')  # O-M to UserDeck
    admins = db.relationship('Admin', backref='public_deck', lazy=True)  # O-M to Admin
    invite = db.relationship(
        'Invite', backref='public_deck', lazy=True
    )  # O-M to Invite

    def __repr__(self):
        return '<PublicDeck %r>' % self.slug


class Question(db.Model):
    """
    <-- Notes for future coding -->

    If card_type == 0:
        question can be anything;
        answer is None

    If card_type == 1:
        question can be anything;
        there are many correct answers for the question;
        answer cannot be None

    If card_type == 2:
        question is to contain one or many '___' as an answer field;
        there is only one correct answer for the type_in question

    If card_type == 3:
        question can be anything;
        there can be any number of correct answers

    if card_type == 4:
        question can be anything;
        there is exactly one correct answer and others are incorrect
    """

    id = db.Column(db.Integer, primary_key=True)
    card_type = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(MAX_QUESTION_LENGTH), nullable=False)
    correct_answers = db.Column(ARRAY(db.String(MAX_ANSWER_LENGTH)))
    wrong_answers = db.Column(ARRAY(db.String(MAX_ANSWER_LENGTH)))
    deck_id = db.Column(
        db.Integer, db.ForeignKey('public_deck.id')
    )  # M-O to PublicDeck
    cards = db.relationship('Card', backref='question', lazy=True)  # O-M to UserCard

    def __repr__(self):
        return '<Question %r>' % self.id


class UserDeck(db.Model):

    # title unique inside the User namespace

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(MAX_DECK_TITLE_LENGTH), nullable=False, unique=True)
    version = db.Column(db.Integer)
    public_id = db.Column(
        db.Integer, db.ForeignKey('public_deck.id')
    )  # M-O to PublicDeck
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False
    )  # M-O to User
    cards = db.relationship('Card', backref='user_deck', lazy=True)  # O-M to UserCard

    def __repr__(self):
        return '<UserDeck %r>' % self.title


class Card(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    attempts_number = db.Column(db.Integer, default=0, nullable=False)
    attempts_list = db.Column(
        MutableList.as_mutable(ARRAY(db.String(50))), default=[], nullable=False
    )
    # success:timestamp => T:123456789
    knowledge = db.Column(db.Integer, default=1, nullable=False)
    question_id = db.Column(
        db.Integer, db.ForeignKey('question.id'), nullable=False
    )  # M-O to PublicCard
    user_deck_id = db.Column(
        db.Integer, db.ForeignKey('user_deck.id'), nullable=False
    )  # M-O to UserDeck

    def __gt__(self, other):
        return self.attempts_number > other.attempts_number

    def __lt__(self, other):
        return self.attempts_number < other.attempts_number

    def __repr__(self):
        return '<Card %r>' % self.id


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True)
    inline_keyboard_id = db.Column(db.Integer)
    decks = db.relationship('UserDeck', backref='user', lazy=True)  # O-M to UserDeck
    administrations = db.relationship(
        'Admin', backref='user', lazy=True
    )  # O-M to Admin
    invites = db.relationship('Invite', backref='user', lazy=True)  # O-M to Invite

    def __repr__(self):
        return '<User %r>' % self.chat_id


class Admin(db.Model):

    """
    rights: 1: admin
            2: creator
    """

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # M-O
    public_deck_id = db.Column(
        db.Integer, db.ForeignKey('public_deck.id'), primary_key=True
    )  # M-O
    rights = db.Column(db.Integer)


class Invite(db.Model):

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # M-O
    public_deck_id = db.Column(
        db.Integer, db.ForeignKey('public_deck.id'), primary_key=True
    )  # M-O
    invite_code = db.Column(db.String(100))
