from random import choice
from typing import List, Sequence, Union

from sqlalchemy.dialects.postgresql import ARRAY

from app import settings
from app.app import db, logging

from . import Attempt, CardType, Deck, utils


class Card(db.Model, utils.ActiveRecordMixin):  # type: ignore

    _id = db.Column(db.Integer, primary_key=True, name='id')
    _card_type = db.Column(db.Integer, nullable=False, name='type')
    _question = db.Column(
        db.String(settings.MAX_QUESTION_LENGTH), nullable=False, name='question'
    )
    _correct_answers = db.Column(
        ARRAY(db.String(settings.MAX_ANSWER_LENGTH)),
        nullable=False,
        name='correct_answers',
    )
    _wrong_answers = db.Column(
        ARRAY(db.String(settings.MAX_ANSWER_LENGTH)),
        nullable=False,
        name='wrong_answers',
    )
    _tips = db.Column(
        ARRAY(db.String(settings.MAX_ANSWER_LENGTH)), nullable=False, name='tips',
    )
    _knowledge = db.Column(db.Integer, default=1, nullable=False, name='knowledge')
    _deck_id = db.Column(
        db.Integer, db.ForeignKey('deck.id'), nullable=False, name='deck_id'
    )  # M-O to Deck
    _attempts = db.relationship(
        'Attempt', backref='card', lazy=True, cascade='all, delete-orphan'
    )  # O-M to Attempt

    def __init__(
        self,
        deck: 'Deck.Deck',
        card_type: int,
        question: str,
        correct_answers: Sequence[str] = (),
        wrong_answers: Sequence[str] = (),
        tips: Sequence[str] = (),
    ) -> None:
        self._deck = deck
        self._card_type = card_type
        self._question = question
        self._correct_answers = correct_answers
        self._wrong_answers = wrong_answers
        self._tips = tips
        self.save()

    def __gt__(self, other: 'Card') -> bool:
        return self.attempts_number > other.attempts_number

    def __lt__(self, other: 'Card') -> bool:
        return self.attempts_number < other.attempts_number

    def __repr__(self) -> str:
        return '<Card %r>' % self.id

    @property
    def id(self) -> int:
        return self._id

    @property
    def type(self) -> int:
        return self._card_type

    @property
    def knowledge(self) -> int:
        return self._knowledge

    @property
    def question(self) -> str:
        return self._question

    @property
    def correct_answers(self) -> Sequence[str]:
        return self._correct_answers

    @property
    def wrong_answers(self) -> Sequence[str]:
        return self._wrong_answers

    @property
    def tips(self) -> Sequence[str]:
        return self._tips

    @property
    def deck(self) -> 'Deck.Deck':
        return self._deck

    @property
    def deck_id(self) -> int:
        return self._deck_id

    def set_tips(self, tips: Sequence[str]) -> None:
        self._tips = tips
        self.save()

    def set_question(self, question: str) -> None:
        self._question = question
        self.save()

    def set_correct_answers(self, correct_answers: Sequence[str]) -> None:
        self._correct_answers = correct_answers
        self.save()

    def set_wrong_answers(self, wrong_answers: Sequence[str]) -> None:
        self._wrong_answers = wrong_answers
        self.save()

    def has_tips(self) -> bool:
        return len(self.tips) > 0

    def get_tip(self, prev_tip: str = '') -> str:
        tips = set(self.tips) - {prev_tip}
        return choice(list(tips))

    def add_attempt(self, user_answer: Union[str, List[str]]) -> 'Attempt.Attempt':
        success = (
            True if self.type == CardType.FACT else self._is_answer_correct(user_answer)
        )
        attempt = Attempt.Attempt(success, self)
        return attempt

    def set_knowledge(self, knowledge: int) -> None:
        logging.info("Setting knowledge %s to card %s", knowledge, self.id)
        if knowledge not in range(1, settings.KNOWLEDGE_RANGE + 1):
            raise AttributeError('Knowledge is out of available range')
        self._knowledge = knowledge
        self.save()

    def _is_answer_correct(self, user_answer: Union[str, List[str]]) -> bool:
        if self.type == CardType.SIMPLE:
            if not isinstance(user_answer, str):
                raise AttributeError(
                    f"{user_answer} is {type(user_answer)} instead of str"
                )
            return user_answer.lower() in self.correct_answers

        elif self.type == CardType.RADIOBUTTON:
            if not isinstance(user_answer, str):
                raise AttributeError(
                    f"{user_answer} is {type(user_answer)} instead of str"
                )
            return user_answer.lower() == self.correct_answers[0]

        answer = user_answer if isinstance(user_answer, list) else [user_answer]
        if self.type == CardType.GAPS:
            return sorted(answer) == sorted(list(self.correct_answers))

        elif self.type == CardType.MULTIPLE_CHOICE:
            return sorted(answer) == sorted(list(self.correct_answers))

        raise AttributeError("Unknown card type %s", self.type)
