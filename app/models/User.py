import logging
from typing import Optional, Sequence

from flask_login import UserMixin
from werkzeug.security import check_password_hash

from app import exceptions

from . import Deck, db, utils


class User(UserMixin, db.Model, utils.ActiveRecordMixin):  # type: ignore

    _id = db.Column(db.Integer, primary_key=True, name='id')
    _chat_id = db.Column(db.Integer, unique=True, nullable=True, name='chat_id')
    _email = db.Column(db.String(100), unique=True, nullable=False, name='email')
    _email_verified = db.Column(db.Boolean, default=False, name='email_verified')
    _password_hash = db.Column(db.String, nullable=False, name='password_hash')
    _username = db.Column(db.String(100), unique=True, nullable=False, name='username')
    _inline_keyboard_id = db.Column(db.Integer, name='inline_keyboard_id')
    _preferred_language = db.Column(db.String(2), name='preferred_language')
    _decks = db.relationship('Deck', backref='_user', lazy=True)  # O-M to Deck

    def __init__(
        self,
        email: str,
        raw_password: str,
        username: str,
        chat_id: Optional[int] = None,
    ):
        username = username.lower()
        email = email.lower()
        if User.get_by(_email=email):
            raise exceptions.EmailAlreadyUsed(f"User with email {email} already exists")
        elif not self._is_valid_username(username):
            raise exceptions.IncorrectCharacters(
                f"Username {username} contains incorrect characters"
            )
        elif User.get_by(_username=username):
            raise exceptions.UsernameAlreadyUsed(
                f"User with username {username} already exists"
            )
        password = utils.hash_password(raw_password)
        self._email = email
        self._username = username
        self._password_hash = password
        self._chat_id = chat_id
        self.save()

    def __repr__(self) -> str:
        return '<User %r>' % self.id

    @property
    def id(self) -> int:
        return self._id

    @property
    def chat_id(self) -> Optional[int]:
        return self._chat_id

    @property
    def email(self) -> str:
        return self._email

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @property
    def username(self) -> str:
        return self._username

    @property
    def inline_keyboard_id(self) -> Optional[int]:
        return self._inline_keyboard_id

    @property
    def preferred_language(self) -> Optional[str]:
        return self._preferred_language

    @property
    def decks(self) -> Sequence[Deck.Deck]:
        return self._decks

    @property
    def email_verified(self) -> bool:
        return self._email_verified

    def set_email_verified(self, email_verified: bool) -> None:
        self._email_verified = email_verified
        self.save()

    def set_password(self, raw_password: str) -> None:
        password = utils.hash_password(raw_password)
        self._password_hash = password
        self.save()

    def set_username(self, username: str) -> None:
        if User.get_by(_username=username):
            raise exceptions.NotUnique("user with username %s already exists")
        self._username = username
        self.save()

    def set_preferred_language(self, language: str) -> None:
        self._preferred_language = language
        self.save()

    def set_inline_keyboard_id(self, inline_keyboard_id: int) -> None:
        self._inline_keyboard_id = inline_keyboard_id
        self.save()

    def forget_keyboard(self) -> None:
        self._inline_keyboard_id = None
        self.save()

    def has_decks(self) -> bool:
        return bool(self.decks and len(self.decks) > 0)

    @classmethod
    def search_by_username(cls, username: str) -> Optional['User']:
        return cls.query.filter_by(username=username).first()

    @classmethod
    def search_by_chat_id(cls, chat_id: int) -> Optional['User']:
        user = cls.query.filter_by(chat_id=chat_id).first()
        return user

    @staticmethod
    def _is_valid_username(username: str) -> bool:
        return username.isalnum()

    @staticmethod
    def login(email: str, raw_password: str) -> 'User':
        email = email.lower()
        user: Optional[User] = User.get_by(_email=email)
        if not user:
            raise exceptions.NotFound(
                "User with email %s not found in database", utils.generate_hash(email)
            )
        if not check_password_hash(user.password_hash, raw_password):
            logging.warning("User %s tried to login with a wrong password", user.id)
            raise exceptions.PasswordError("Wrong password for user %s", user.id)
        return user
