import typing
from time import time

from sqlalchemy.dialects.postgresql import ARRAY

from app.run import db
from app.settings import dist

from . import Question, UserDeck, utils


class Card(db.Model):  # type: ignore

    id = db.Column(db.Integer, primary_key=True)
    attempts_number = db.Column(db.Integer, default=0, nullable=False)
    attempts_list = db.Column(
        utils.MutableList.as_mutable(ARRAY(db.String(50))), default=[], nullable=False
    )
    # success:timestamp => T:123456789
    knowledge = db.Column(db.Integer, default=1, nullable=False)
    question_id = db.Column(
        db.Integer, db.ForeignKey('question.id'), nullable=False
    )  # M-O to PublicCard
    user_deck_id = db.Column(
        db.Integer, db.ForeignKey('user_deck.id'), nullable=False
    )  # M-O to UserDeck

    def __init__(
        self,
        deck: UserDeck.UserDeck,
        question: Question.Question,
        need_commit: bool = True,
    ) -> None:
        self.user_deck = deck
        self.question = question
        db.session.add(self)
        if need_commit:
            db.session.commit()

    def __gt__(self, other: 'Card') -> bool:
        return self.attempts_number > other.attempts_number

    def __lt__(self, other: 'Card') -> bool:
        return self.attempts_number < other.attempts_number

    def __repr__(self) -> str:
        return '<Card %r>' % self.id

    def add_attempt(self: 'Card', user_answer: typing.Union[str, typing.List]) -> bool:

        success = self._is_answer_correct(user_answer)
        timestamp = int(time())
        attempt = utils.generate_attempt(success, timestamp)
        self.attempts_number += 1
        attempts = self.attempts_list
        attempts.append(attempt)
        self.attempts_list = attempts

        db.session.add(self)
        db.session.commit()

        return success

    def inc_attempt(self) -> None:
        self.attempts_number += 1
        db.session.add(self)
        db.session.commit()

    def set_knowledge(self: 'Card', knowledge: int) -> typing.Union['Card', int]:
        if knowledge in range(1, dist.KNOWLEDGE_RANGE + 1):
            self.knowledge = knowledge
            db.session.add(self)
            db.session.commit()
            return self
        else:
            return knowledge

    def _is_answer_correct(self: 'Card', user_answer: typing.Union[str, typing.List]) -> bool:
        question = self.question

        if question.card_type == 1:
            return user_answer.lower() in question.correct_answers

        elif question.card_type == 2:
            return list(user_answer) == list(question.correct_answers)

        elif question.card_type == 3:
            return sorted(list(user_answer)) == sorted(list(question.correct_answers))

        return False  # mypy forced my to write it

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def fromQuestion(
        cls,
        deck: UserDeck.UserDeck,
        card_type: int,
        question_string: str,
        correct_answers: list = None,
        wrong_answers: list = None,
    ) -> 'Card':

        if card_type not in range(dist.CARD_TYPES_RANGE):
            raise AttributeError('card_type is out of available range')
        if len(question_string) > dist.MAX_QUESTION_LENGTH:
            raise ValueError('question is too long')
        else:
            deck.version = -1
            db.session.add(deck)

            if (
                card_type == 3
                and (not correct_answers or len(correct_answers) == 0)
                and (not correct_answers or len(correct_answers) == 0)
            ):
                raise ValueError(
                    'card with type 3 must have at least one answer in total'
                )

            elif card_type in (1, 2, 4) and (
                not correct_answers or len(correct_answers) == 0
            ):
                raise ValueError(
                    f'card with type {card_type} must have correct answers'
                )

            elif card_type == 4 and correct_answers and len(correct_answers) != 1:
                raise ValueError(
                    'card with type 4 must have exactly one correct answer'
                )

            question = Question.Question(
                card_type=card_type,
                text=question_string.lower(),
                correct_answers=correct_answers,
                wrong_answers=wrong_answers,
            )
            db.session.add(question)
            return cls(deck=deck, question=question)

    @classmethod
    def get_by_id(cls, card_id: str) -> 'Card':
        card = cls.query.filter_by(id=card_id).first()
        if not card:
            raise AttributeError('card not found')
        return card
