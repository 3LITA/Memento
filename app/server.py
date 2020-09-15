import importlib
import logging
import os
from typing import Any, Callable

from flask import Flask, request
from flask_login import LoginManager

from app import bot, settings, support_bot
from app.models import db

from . import babel


web = Flask(__name__)
web.secret_key = os.urandom(24)
web.config.from_object(settings)
db.init_app(web)
db.create_all(app=web)
babel.init_app(web)
login_manager = LoginManager(web)


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
            support_bot.notify_critical_error(e)
        else:
            return res

    return wrapper


@web.route(f'/{settings.BOT_SECRET_URL}', methods=['POST'])
@catch_errors
def bot_message() -> str:
    logging.info('Got new bot request')
    json_string = request.get_data().decode('utf-8')
    bot.process_update(json_string)
    logging.info('Update is proceeded')
    return ''


importlib.import_module("app.views.auth")
importlib.import_module("app.views.main")
