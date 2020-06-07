import typing

from app.__init__ import db
from app.settings import MAX_SLUG_LENGTH


class PublicDeck(db.Model):  # type: ignore

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

    def __repr__(self) -> str:
        return '<PublicDeck %r>' % self.slug

    def delete(self: 'PublicDeck') -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def search_by_slug(cls, slug: str) -> typing.Optional['PublicDeck']:
        return cls.query.filter_by(slug=slug).first()

    @classmethod
    def get_by_id(cls, card_id: str) -> typing.Optional['PublicDeck']:
        return cls.query.filter_by(id=card_id).first()
