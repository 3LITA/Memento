from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import telebot

server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost/ankibot'
db = SQLAlchemy(server)


@server.route('/', methods=['GET'])
def index():
    return '<h1>Bot welcomes you!</h1>'


@server.route('/secret', methods=['POST'])
def webhook():
    print('got here')
    from app.bot.handlers import bot

    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return ''


if __name__ == '__main__':
    server.run(debug=True)
