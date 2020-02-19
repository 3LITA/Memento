import re

from ..models import models


def generate_title(chat_id, title):
    return str(chat_id) + ':' + title.lower()


def humanize_title(chat_id, title):
    return title[1 + len(str(chat_id)) :]


def is_title_correct(title):
    return re.match(r'^[A-Za-z0-9_-]*$', title)


def generate_attempt(success, timestamp):
    return 'T:' + str(timestamp) if success else 'F:' + str(timestamp)


def get_or_create(chat_id, username):

    if username:
        named_user = models.User.query.filter_by(username=username).first()
        if named_user:
            if named_user.chat_id == chat_id:
                # no fields have changed
                return named_user
            else:
                # another user used to have this username
                named_user.username = None
                models.db.session.add(named_user)

    unnamed_user = models.User.query.filter_by(chat_id=chat_id).first()

    if not unnamed_user:
        # user is new
        unnamed_user = models.User(chat_id=chat_id, username=username)
        models.db.session.add(unnamed_user)

    elif unnamed_user.username != username:
        unnamed_user.username = username

    models.db.session.commit()
    return unnamed_user
