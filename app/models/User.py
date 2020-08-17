from typing import Optional, Sequence

from app.app import db

from . import Deck, utils


class User(db.Model, utils.ActiveRecordMixin):  # type: ignore

    _id = db.Column(db.Integer, primary_key=True, name='id')
    _chat_id = db.Column(db.Integer, unique=True, nullable=True, name='chat_id')
    _username = db.Column(db.String(100), unique=True, name='username')
    _inline_keyboard_id = db.Column(db.Integer, name='inline_keyboard_id')
    _preferred_language = db.Column(db.String(2), name='preferred_language')
    _decks = db.relationship('Deck', backref='_user', lazy=True)  # O-M to Deck

    def __init__(self, chat_id: int, username: Optional[str] = None) -> None:
        self._chat_id = chat_id
        if username:
            self._username = username
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
    def username(self) -> Optional[str]:
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
    def search_by_username(cls, username: str) -> 'User':
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_or_create_by_chat_id(cls, chat_id: int) -> 'User':
        user = cls.search_by_chat_id(chat_id)

        if not user:
            user = cls(chat_id=chat_id)

        return user

    @classmethod
    def search_by_chat_id(cls, chat_id: int) -> Optional['User']:
        user = cls.query.filter_by(chat_id=chat_id).first()
        return user
