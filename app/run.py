import importlib
import logging

import telebot
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from app import settings

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)

server = Flask(__name__)
server.config.from_object(settings)
db = SQLAlchemy(server)


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
