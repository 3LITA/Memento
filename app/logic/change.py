from time import time

from .. import config
from .. import errors
from ..models import models

from .utils import generate_title, generate_attempt, is_title_correct


def rename_user_deck(user: models.User, user_deck: models.UserDeck, deck_title: str):

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


def is_answer_correct(user_card: models.Card, user_answer):

    public_card = user_card.public_card

    if public_card.card_type == 1:
        return user_answer in public_card.correct_answers

    elif public_card.card_type == 2:
        return list(user_answer) == list(public_card.correct_answers)

    elif public_card.card_type == 3:
        return sorted(list(user_answer)) == sorted(list(public_card.correct_answers))


def add_attempt(card: models.Card, user_answer):

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


def inc_attempt(card: models.Card):
    card.attempts_number += 1

    models.db.session.add(card)
    models.db.session.commit()

    return card


def set_knowledge(card: models.Card, knowledge: int):
    if knowledge in range(1, config.KNOWLEDGE_RANGE + 1):
        card.knowledge = knowledge
        models.db.session.add(card)
        models.db.session.commit()
        return card
    else:
        return knowledge


def set_inline_keyboard(user, inline_keyboard_id):
    user.inline_keyboard_id = inline_keyboard_id
    models.db.session.add(user)
    models.db.session.commit()


# def rename_public_deck(user: User, public_deck: PublicDeck, title: str):
#     """
#     Strictly renames public deck
#     :param user: User that send rename request
#     :param public_deck: PublicDeck that is to be renamed
#     :param title: title that is to be set
#     :return: PublicDeck if renamed;
#              None if User has no rights
#     """
#
#     for user_deck in user.decks:
#         if user_deck.public == public_deck:
#             if user_deck.rights == 1 or user_deck.rights == 2:
#                 public_deck.title = title
#                 public_deck.save()
#                 return public_deck
#
#
# def set_slug(user: User, public_deck: PublicDeck, slug: str):
#     """
#         Sets a slug for a public deck
#         :param user: User that send rename request
#         :param public_deck: PublicDeck that is to be renamed
#         :param slug: slug that is to be set
#         :return: PublicDeck if successful;
#                  slug if this slug already in use
#                  None if User has no rights
#         """
#
#     for user_deck in user.decks:
#         if user_deck.public == public_deck:
#             if user_deck.rights == 2:
#                 try:
#                     PublicDeck.objects.get(slug=slug)
#                     return slug
#                 except DoesNotExist:
#                     public_deck.slug = slug
#                     public_deck.save()
#                     return public_deck
#
#
# def set_password(user: User, public_deck: PublicDeck, new_password: str, old_password=None):
#     """
#         Sets a slug for a public deck
#         :param user: User that send rename request
#         :param public_deck: PublicDeck that is to be renamed
#         :param new_password: password that is to be set
#         :param old_password: current password
#         :return: PublicDeck if renamed;
#                  old_password if it does not match the real password
#                  None if User has no rights
#         """
#
#     for user_deck in user.decks:
#         if user_deck.public == public_deck:
#             if user_deck.rights == 2:
#                 if public_deck.password == old_password:
#                     public_deck.password = new_password
#                     public_deck.save()
#                     return public_deck
#                 else:
#                     return old_password
