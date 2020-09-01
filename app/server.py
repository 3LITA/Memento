import importlib
import json
import logging
from typing import Any, Callable, Optional

import telebot
from flask import Flask, request
from flask_babel import Babel
from flask_login import LoginManager

from app import settings
from app.bot.main import bot
from app.models import db


web = Flask(__name__)
web.config.from_object(settings)
db.init_app(web)
login_manager = LoginManager(web)
babel = Babel(web)


importlib.import_module("app.views.auth")
importlib.import_module("app.views.main")


def catch_errors(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            logging.critical(
                "An unexpected error happened in route %s.%s: %s",
                func.__module__,
                func.__name__,
                e,
            )
        else:
            return res

    return wrapper


@babel.localeselector
def get_locale() -> Optional[str]:
    logging.info('Selecting locale')
    if request.path == f'/{settings.BOT_SECRET_URL}':
        from app.models.User import User

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
        return request.accept_languages.best_match(settings.LANGUAGES)


@web.route(f'/{settings.BOT_SECRET_URL}', methods=['POST'])
@catch_errors
def bot_message() -> str:
    importlib.import_module('app.bot.contextual_handlers')
    importlib.import_module('app.bot.markup_handlers')

    logging.info('Got new bot request')
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return ''
