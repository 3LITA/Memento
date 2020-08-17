import importlib
import json
import typing

import telebot
from flask import Flask, request
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy

from app import settings


server = Flask('app')
server.config.from_object(settings)
db = SQLAlchemy(server)
babel = Babel(server)

logging = server.logger


@babel.localeselector
def get_locale() -> typing.Optional[str]:
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
        user = User.get_or_create_by_chat_id(chat_id)
        if not user.preferred_language:
            lang = info['from']['language_code']
            if lang not in settings.LANGUAGES:
                lang = settings.DEFAULT_LOCALE
            user.set_inline_keyboard_id(lang)
        return user.preferred_language
    else:
        return request.accept_languages.best_match(settings.LANGUAGES)


@server.route('/', methods=['GET'])
def index() -> str:
    logging.info('Got new request')
    return '<h1>Bot welcomes you!</h1>'


@server.route(f'/{settings.BOT_SECRET_URL}', methods=['POST'])
def bot_message() -> str:
    importlib.import_module('app.bot.contextual_handlers')
    importlib.import_module('app.bot.markup_handlers')
    from app.bot.main import bot

    logging.info('Got new bot request')
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return ''
