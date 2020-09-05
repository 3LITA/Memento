import importlib
import logging
import os
from typing import Any, Callable

import telebot
from flask import Flask, request
from flask_login import LoginManager

from app import settings
from app.bot.main import bot
from app.models import db

from . import babel, support_bot


web = Flask(__name__)
web.secret_key = os.urandom(24)
web.config.from_object(settings)
db.init_app(web)
babel.init_app(web)
login_manager = LoginManager(web)


importlib.import_module("app.views.auth")
importlib.import_module("app.views.main")


def catch_errors(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            support_bot.notify_critical_error(e)
            logging.critical(
                "An unexpected error happened in route %s.%s: %s",
                func.__module__,
                func.__name__,
                e,
            )
        else:
            return res

    return wrapper


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
