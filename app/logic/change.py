import typing
from time import time

from app import config, errors
from app.models import models
from .utils import generate_attempt, generate_title, is_title_correct


def rename_user_deck(user: models.User, user_deck: models.UserDeck, deck_title: str) -> models.UserDeck:

    if not is_title_correct(deck_title):
        raise AttributeError('deck title contains incorrect symbols')

    proper_title = generate_title(user.chat_id, deck_title)

    if len(proper_title) > config.MAX_DECK_TITLE_LENGTH:
        raise ValueError('deck title is too long')

    search = models.UserDeck.query.filter_by(title=proper_title).first()

    if search:
        raise errors.NonUniqueTitleError(
            'deck title must be unique inside a user namespace'
        )

    else:
        user_deck.title = proper_title
        models.db.session.add(user_deck)
        models.db.session.commit()
        return user_deck


def is_answer_correct(user_card: models.Card, user_answer: str) -> bool:

    public_card = user_card.public_card

    if public_card.card_type == 1:
        return user_answer in public_card.correct_answers

    elif public_card.card_type == 2:
        return list(user_answer) == list(public_card.correct_answers)

    elif public_card.card_type == 3:
        return sorted(list(user_answer)) == sorted(list(public_card.correct_answers))


def add_attempt(card: models.Card, user_answer: str) -> bool:

    success = is_answer_correct(card, user_answer)
    timestamp = int(time())
    attempt = generate_attempt(success, timestamp)
    card.attempts_number += 1
    attempts = card.attempts_list
    attempts.append(attempt)
    card.attempts_list = attempts

    models.db.session.add(card)
    models.db.session.commit()

    return success


def inc_attempt(card: models.Card) -> models.Card:
    card.attempts_number += 1

    models.db.session.add(card)
    models.db.session.commit()

    return card


def set_knowledge(card: models.Card, knowledge: int) -> typing.Union[models.Card, int]:
    if knowledge in range(1, config.KNOWLEDGE_RANGE + 1):
        card.knowledge = knowledge
        models.db.session.add(card)
        models.db.session.commit()
        return card
    else:
        return knowledge


def set_inline_keyboard(user: models.User, inline_keyboard_id: int) -> None:
    user.inline_keyboard_id = inline_keyboard_id
    models.db.session.add(user)
    models.db.session.commit()
