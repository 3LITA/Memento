import importlib

import telebot
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from app.settings import local


server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = local.POSTGRES_URI
db = SQLAlchemy(server)  # type: ignore


@server.route('/', methods=['GET'])
def index() -> str:
    return '<h1>Bot welcomes you!</h1>'


@server.route(f'/{local.BOT_SECRET_URL}', methods=['POST'])
def webhook() -> str:
    print('Got new bot request')
    importlib.import_module('bot.contextual_handlers')
    importlib.import_module('bot.markup_handlers')
    from app.bot.main import bot

    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return ''


if __name__ == '__main__':
    server.run(debug=False)
