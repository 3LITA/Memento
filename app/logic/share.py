from .. import errors
from ..models import models
from .create import create_card_with_question
from .delete import remove_user_card
from .utils import generate_title


def get_rights(user: models.User, public_deck: models.PublicDeck):

    rights = None
    for admin in public_deck.admins:
        if admin.user == user:
            rights = admin.rights
    return rights


def share_user_deck(
    user: models.User, user_deck: models.UserDeck, slug: str, password=None
):
    """
        Creates a PublicDeck from a UserDeck
        :param user: User that wants to share a deck
        :param user_deck: UserDeck that is to be shared
        :param slug: unique slug of the new PublicDeck
        :param password: # TODO: later
        :return: slug if it is already in use
                 PublicDeck if successfully shared
        """

    slug = slug.lower()
    if models.PublicDeck.query.filter_by(slug=slug).first():
        raise errors.NonUniqueSlugError

    new_public_deck = models.PublicDeck(slug=slug, password=password)
    models.db.session.add(new_public_deck)

    user_deck.public_deck = new_public_deck
    user_deck.version = new_public_deck.version
    models.db.session.add(user_deck)

    admin = models.Admin(user=user, public_deck=new_public_deck, rights=2)
    models.db.session.add(admin)

    for card in user_deck.cards:
        public_card = card.public_card
        if public_card.public_deck is None:
            public_card.public_deck = new_public_deck
            models.db.session.add(public_card)
        else:
            new_public_card = models.Question(
                card_type=public_card.card_type,
                question=public_card.question,
                correct_answers=public_card.correct_answers,
                wrong_answers=public_card.wrong_answers,
                public_deck=new_public_deck,
            )
            models.db.session.add(new_public_card)
    models.db.session.commit()
    return new_public_deck


def join_deck(
    user: models.User, public_deck: models.PublicDeck, title: str, password=None
):
    """
    Creates UserDeck that is connected to the PublicDeck and fills it with [UserCard]
    :param user: User that wants to add a deck
    :param public_deck: PublicDeck user wants to add
    :param title: title to be set for a UserDeck
    :param password: password of PublicDeck
    :raises: PasswordsNotMatchError if password does not match
             NonUniqueTitleError if UserDeck with this title already exists
    :return: None if user has already added it
             UserDeck if successful
    """

    if public_deck.password != password:
        raise errors.PasswordsNotMatchError(password)

    proper_title = generate_title(user.chat_id, title)
    if models.UserDeck.query.filter_by(title=proper_title).first():
        raise errors.NonUniqueTitleError('UserDeck with this title already exist')

    if models.UserDeck.query.filter_by(user=user, public_deck=public_deck).first():
        return

    user_deck = models.UserDeck(
        title=proper_title,
        public_deck=public_deck,
        version=public_deck.version,
        user=user,
    )
    models.db.session.add(user_deck)

    cards = public_deck.questions

    if cards:
        for public_card in cards:
            user_card = models.Card(user_deck=user_deck, public_card=public_card)
            models.db.session.add(user_card)

    models.db.session.commit()
    return user_deck


def update_user_deck(user_deck: models.UserDeck, delete=True):
    """
    Makes UserDeck.cards similar to its public instance if version of public_instance is newer;
    saves public_deck
    :param user_deck: UserDeck that is to be updated
    :param delete: should [UserCard] that have no public instance (anymore / have been created by user) be removed
    :raises: NoPublicDeckError if user_deck has no public instance;
    :return: None if already up-to-date;
             UserDeck if successfully updated.
    """

    public_deck = user_deck.public_deck

    if not public_deck:
        raise errors.NoPublicDeckError('Deck has no public instance')

    if user_deck.version == public_deck.version:
        return

    if delete:
        for user_card in user_deck.cards:
            if user_card.public_card not in public_deck.cards:
                remove_user_card(user_card)

    user_cards_public = [user_card.public_card for user_card in user_deck.cards]
    public_cards = set(public_deck.cards)
    cards_to_add = list(public_cards - set(user_cards_public))

    for public_card in cards_to_add:
        create_card_with_question(user_deck, public_card, need_commit=False)

    user_deck.version = public_deck.version
    models.db.session.add(user_deck)
    models.db.session.commit()

    return user_deck


def merge_user_deck_with_public(user: models.User, user_deck: models.UserDeck):
    """
    Merges UserDeck with its public instance;
    removes [PublicCard] that were deleted as [UserCard] in UserDeck;
    :param user: User whose UserDeck is to be merged
    :param user_deck: UserDeck that is to be merged
    :raises: NoPublicDeckError if user_deck has no public instance,
             RightsError if user is neither admin nor creator,
    :return: None if no changes were made - versions of user_deck and public_deck are equal
             PublicDeck if successfully merged
    """

    public_deck = user_deck.public_deck

    if public_deck is None:
        raise errors.NoPublicDeckError('Deck has no public instance')

    is_admin = get_rights(user, public_deck)

    if not is_admin:
        raise errors.RightsError('User does not have rights for merging')

    if user_deck.version == public_deck.version:
        return

    cards = [user_card.public_card for user_card in user_deck.cards]

    public_deck.cards = cards
    public_deck.version += 1
    user_deck.version = public_deck.version

    models.db.session.add(public_deck)
    models.db.session.add(user_deck)
    models.db.session.commit()
    return public_deck


def become_admin(user: models.User, public_deck: models.PublicDeck):

    if get_rights(user, public_deck):
        raise errors.AdminError('User is already admin')
    else:
        admin = models.Admin(user=user, public_deck=public_deck, rights=1)
    return admin


def add_admin(
    recruiter: models.User, newbie_username: str, public_deck: models.PublicDeck
):
    """
    Adds an admin to the PublicDeck
    :param recruiter: User that has to be creator of the deck
    :param public_deck: PublicDeck of the recruiter
    :param newbie_username: nickname of User that is to become an admin
    :raises: DoesNotExistError if newbie does not exist
             CreatorError if recruiter is not creator
             AdminError if newbie is already admin
    :return: Admin if newbie became admin;
    """

    newbie = models.User.query.filter_by(username=newbie_username).first()
    if newbie is None:
        raise errors.DoesNotExistError('There is no user with such username')

    if get_rights(recruiter, public_deck) != 2:
        raise errors.CreatorError('Recruiter has to be creator')

    admin = become_admin(newbie, public_deck)
    models.db.session.add(admin)
    models.db.session.commit()
    return admin


def kick_admin(
    recruiter: models.User, kicked_username: str, public_deck: models.PublicDeck
):

    kicked = models.User.query.filter_by(username=kicked_username).first()
    if kicked is None:
        raise errors.DoesNotExistError('There is no user with such username')

    if get_rights(recruiter, public_deck) != 2:
        raise errors.CreatorError('Recruiter has to be creator')

    admin = models.Admin.query.filter_by(user=kicked, public_deck=public_deck).first()
    if admin is None:
        raise errors.AdminError('User is not an admin')

    models.db.session.delete(admin)
    models.db.session.commit()
    return admin
