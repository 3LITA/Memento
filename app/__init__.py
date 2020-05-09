import importlib
import json
import typing

import telebot
from flask import Flask, request
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy

from app import settings


server = Flask(__name__)
server.config.from_object(settings)
db = SQLAlchemy(server)
babel = Babel(server)


@babel.localeselector
def get_locale() -> typing.Optional[str]:
    if request.path == f'/{settings.BOT_SECRET_URL}':
        json_string = request.get_data().decode('utf-8')
        info = json.loads(json_string)
        try:
            lang = info['callback_query']['from']['language_code']
        except KeyError:
            lang = info['message']['from']['language_code']
        return lang if lang in settings.LANGUAGES else settings.DEFAULT_LOCALE
    else:
        return request.accept_languages.best_match(settings.LANGUAGES)


@server.route('/', methods=['GET'])
def index() -> str:
    return '<h1>Bot welcomes you!</h1>'


@server.route(f'/{settings.BOT_SECRET_URL}', methods=['POST'])
def webhook() -> str:
    importlib.import_module('bot.contextual_handlers')
    importlib.import_module('bot.markup_handlers')
    from app.bot.main import bot

    server.logger.info('Got new bot request')
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return ''


if __name__ == '__main__':
    server.run(debug=False)
