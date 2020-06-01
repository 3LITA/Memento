from sqlalchemy.dialects.postgresql import ARRAY

from app import db
from app.settings import MAX_ANSWER_LENGTH, MAX_QUESTION_LENGTH


class Question(db.Model):  # type: ignore
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
    text = db.Column(db.String(MAX_QUESTION_LENGTH), nullable=False)
    correct_answers = db.Column(ARRAY(db.String(MAX_ANSWER_LENGTH)))
    wrong_answers = db.Column(ARRAY(db.String(MAX_ANSWER_LENGTH)))
    deck_id = db.Column(
        db.Integer, db.ForeignKey('public_deck.id')
    )  # M-O to PublicDeck
    cards = db.relationship('Card', backref='question', lazy=True)  # O-M to UserCard

    def __repr__(self) -> str:
        return '<Question %r>' % self.id
