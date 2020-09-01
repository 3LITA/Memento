from time import time

from . import Card, db, utils


class Attempt(db.Model, utils.ActiveRecordMixin):  # type: ignore

    _id = db.Column(db.Integer, primary_key=True, name='id')
    _success = db.Column(db.Boolean, nullable=False, name='success')
    _timestamp = db.Column(db.Integer, nullable=False, name='timestamp')
    _card_id = db.Column(
        db.Integer, db.ForeignKey('card.id'), nullable=False, name='card_id'
    )  # M-O to Card

    def __init__(self, success: bool, card: 'Card.Card') -> None:
        timestamp = int(time())
        self._success = success
        self._timestamp = timestamp
        self._card = card
        self.save()

    @property
    def id(self) -> int:
        return self.id

    @property
    def success(self) -> bool:
        return self._success

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def card(self) -> 'Card.Card':
        return self._card

    @property
    def card_id(self) -> int:
        return self._card_id
