import os
from gettext import translation

from app.models.User import User


localedir = os.path.abspath(os.path.dirname(__file__))
ru_translate = translation('messages', localedir, ['ru'])
en_translate = translation('messages', localedir, ['en'])


def gettext(text: str) -> str:
    language = os.getenv('LANGUAGE', 'en')
    if language == 'ru':
        return ru_translate.gettext(text)
    else:
        return en_translate.gettext(text)


def set_language(user: User) -> None:
    os.environ['LANGUAGE'] = user.preferred_language or 'en'
