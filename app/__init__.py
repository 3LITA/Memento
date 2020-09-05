import json
import logging
from typing import Optional

from flask import request
from flask_babel import Babel


babel = Babel()


@babel.localeselector
def get_locale() -> str:
    from app import settings
    from app.models.User import User

    logging.info('Selecting locale')
    if request.path == f'/{settings.BOT_SECRET_URL}':

        json_string = request.get_data().decode('utf-8')
        js = json.loads(json_string)
        try:
            info = js['callback_query']
        except KeyError:
            info = js['message']
        chat_id = info['from']['id']
        user: Optional[User] = User.get_by(_chat_id=chat_id)
        lang = info['from']['language_code']
        lang = lang if lang in settings.LANGUAGES else None

        if user:
            if user.preferred_language:
                lang = user.preferred_language
        return lang or settings.DEFAULT_LOCALE
    else:
        return (
            request.accept_languages.best_match(settings.LANGUAGES)
            or settings.DEFAULT_LOCALE
        )


__all__ = ['babel', 'support_bot']
