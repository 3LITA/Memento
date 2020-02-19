from ..models import models

from .utils import generate_title


def remove_user_deck(user: models.User, deck_title: str):

    title = generate_title(user.chat_id, deck_title)
    deck = models.UserDeck.query.filter_by(title=title).first()

    if deck:
        return delete_user_deck(deck)


def delete_user_deck(deck: models.UserDeck):
    models.db.session.delete(deck)
    models.db.session.commit()
    return True


def remove_user_card(user_card: models.Card):
    # while training user decides to delete the current card
    public_card = user_card.public_card
    if len(public_card.user_cards) == 1:
        models.db.session.delete(user_card)
        models.db.session.delete(public_card)
    else:
        models.db.session.delete(user_card)
    models.db.session.commit()
    return user_card


def remove_public_deck(public_deck: models.PublicDeck):
    models.db.session.delete(public_deck)
    models.db.session.commit()


def forget_keyboard(user):
    user.inline_keyboard_id = None
    models.db.session.add(user)
    models.db.session.commit()