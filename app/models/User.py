import typing

from app import db

from . import Admin, Invite, UserDeck


class User(db.Model):  # type: ignore

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True)
    inline_keyboard_id = db.Column(db.Integer)
    preferred_language = db.Column(db.String(2))
    decks = db.relationship('UserDeck', backref='user', lazy=True)  # O-M to UserDeck
    administrations = db.relationship(
        Admin.Admin, backref='user', lazy=True
    )  # O-M to Admin
    invites = db.relationship(Invite.Invite, backref='user', lazy=True)  # O-M to Invite

    def __init__(self, chat_id: int, username: typing.Optional[str] = None) -> None:
        self.chat_id = chat_id
        if username:
            self.username = username
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        return '<User %r>' % self.chat_id

    def set_inline_keyboard(self: 'User', inline_keyboard_id: int) -> None:
        self.inline_keyboard_id = inline_keyboard_id
        db.session.add(self)
        db.session.commit()

    def set_preferred_language(self, language: str) -> None:
        self.preferred_language = language
        db.session.add(self)
        db.session.commit()

    def forget_keyboard(self: 'User') -> None:
        self.inline_keyboard_id = None
        db.session.add(self)
        db.session.commit()

    def delete_user_deck(self: 'User', deck_title: str) -> bool:
        deck = UserDeck.UserDeck.search_by_title(self, deck_title)

        if deck:
            return self._delete_user_deck(deck)
        return False

    def get_decks(self: 'User') -> typing.List['UserDeck.UserDeck']:
        try:
            return self.decks
        except AttributeError:
            return []

    @classmethod
    def search_by_username(cls, username: str) -> 'User':
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_or_create(
        cls, chat_id: int, username: typing.Optional[str] = None
    ) -> 'User':
        if username:
            named_user = cls.query.filter_by(username=username).first()
            if named_user:
                if named_user.chat_id == chat_id:
                    # no fields have changed
                    return named_user
                else:
                    # another user used to have this username
                    named_user.username = None
                    db.session.add(named_user)

        unnamed_user = cls.query.filter_by(chat_id=chat_id).first()

        if not unnamed_user:
            # user is new
            unnamed_user = cls(chat_id=chat_id, username=username)
            db.session.add(unnamed_user)

        elif unnamed_user.username != username:
            # username was changed
            unnamed_user.username = username

        db.session.commit()
        return unnamed_user

    @classmethod
    def search_by_chat_id(cls, chat_id: str) -> typing.Optional['User']:
        user = cls.query.filter_by(chat_id=chat_id).first()
        return user

    @staticmethod
    def _delete_user_deck(deck: 'UserDeck.UserDeck') -> bool:
        db.session.delete(deck)
        db.session.commit()
        return True
