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
    print('selecting locale')
    if request.path == f'/{settings.BOT_SECRET_URL}':
        from app.models.User import User

        json_string = request.get_data().decode('utf-8')
        js = json.loads(json_string)
        try:
            info = js['callback_query']
        except KeyError:
            info = js['message']
        chat_id = info['from']['id']
        user = User.get_or_create(chat_id)
        if user.preferred_language:
            lang = user.preferred_language
        else:
            lang = info['from']['language_code']
            if lang not in settings.LANGUAGES:
                lang = settings.DEFAULT_LOCALE
        user.set_preferred_language(lang)
        return lang
    else:
        return request.accept_languages.best_match(settings.LANGUAGES)


@server.route('/', methods=['GET'])
def index() -> str:
    return '<h1>Bot welcomes you!</h1>'


@server.route(f'/{settings.BOT_SECRET_URL}', methods=['POST'])
def bot_message() -> str:
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
