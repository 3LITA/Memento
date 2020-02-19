from .. import errors
from .. import config
from ..models import models

from .utils import generate_title, is_title_correct


def create_new_user_deck(user: models.User, deck_title: str):
    """

    :param user:
    :param deck_title:
    :raises errors.NonUniqueTitleError: if deck_title is already in use,
            ValueError: if title contains incorrect symbols
    :return: UserDeck if it has been created;
    """

    proper_title = generate_title(user.chat_id, deck_title)

    search = models.UserDeck.query.filter_by(title=proper_title).first()

    if search:
        raise errors.NonUniqueTitleError('this title is already in use')
    if not is_title_correct(deck_title):
        raise AttributeError('deck title contains incorrect symbols')
    if len(generate_title(user.chat_id, deck_title)) > config.MAX_DECK_TITLE_LENGTH:
        raise ValueError('deck title is too long')
    else:
        deck = models.UserDeck(title=proper_title, user=user)
        models.db.session.add(deck)
        models.db.session.commit()
        return deck


def create_card_with_question(
    deck: models.UserDeck, question: models.Question, need_commit=True
):
    user_card = models.Card(question=question, user_deck=deck)
    models.db.session.add(user_card)
    if need_commit:
        models.db.session.commit()
    return user_card


def create_new_card(
    user_deck: models.UserDeck,
    card_type,
    question_string,
    correct_answers: list = None,
    wrong_answers: list = None,
):
    """
    Creates a new UserCard;
    :param user_deck: UserDeck that is to store the UserCard
    :param card_type: see more info in models.models
    :param question_string: any string
    :param correct_answers: list
    :param wrong_answers: list
    :raises: ValueError: if len(question_string) > allowed question length
             errors.RangeError: if card_type is out of available range
             AttributeError: if card has incorrect number of answers
    :return: UserCard if a Card was created;
    """

    if card_type not in range(config.CARD_TYPES_RANGE):
        raise errors.RangeError('card_type is out of available range')
    if len(question_string) > config.MAX_QUESTION_LENGTH:
        raise ValueError('question is too long')
    else:
        user_deck.version = -1
        models.db.session.add(user_deck)

        if (
            card_type == 3
            and (not correct_answers or len(correct_answers) == 0)
            and (not correct_answers or len(correct_answers) == 0)
        ):
            raise AttributeError(
                'card with type 3 must have at least one answer in total'
            )

        elif card_type in (1, 2, 4) and (
            not correct_answers or len(correct_answers) == 0
        ):
            raise AttributeError('card with this type must have correct_answers')

        elif card_type == 4 and len(correct_answers) != 1:
            raise AttributeError(
                'card with type 4 must have exactly one correct answer'
            )

        question = models.Question(
            card_type=card_type,
            question=question_string.lower(),
            correct_answers=correct_answers,
            wrong_answers=wrong_answers,
        )
        models.db.session.add(question)
        return create_card_with_question(deck=user_deck, question=question)
