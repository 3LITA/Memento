import random
import urllib.parse

from flask import Flask, request

from tests import conftest

from . import utils

tgstub = Flask('test_app')
logging = tgstub.logger


def return_message(args: dict) -> dict:
    return {
        "ok": True,
        "result": {
            "message_id": random.randint(100, 10000),
            "from": {
                "id": random.randint(100, 10000),
                "is_bot": True,
                "first_name": utils.random_string(),
                "username": utils.random_string()
            },
            "chat": {
                "id": args['chat_id'],
                "first_name": utils.random_string(),
                "last_name": utils.random_string(),
                "username": utils.random_string(),
                "type": "private"
            },
            "date": 1597495958,
            "text": args['text'],
            "parse_mode": args.get("parse_mode"),
        }
    }


def parse_args(raw_url: str) -> dict:
    arg_line = raw_url.split('?')[1]
    clean_url = urllib.parse.unquote_plus(arg_line)
    args = urllib.parse.parse_qs(clean_url)
    return args


@tgstub.route(f'/{conftest.BOT_TOKEN}/sendMessage', methods=['POST'])
def get_new_message() -> dict:
    args = parse_args(request.url)
    utils.queue.append(args)
    logging.info("Message was delivered!")
    return return_message(args)


@tgstub.route(f'/{conftest.BOT_TOKEN}/deleteMessage', methods=['POST'])
def delete_message() -> dict:
    args = parse_args(request.url)
    utils.queue.append(args)
    logging.info("Message was deleted!")
    return {"ok": True, "result": True}


@tgstub.route(f'/{conftest.BOT_TOKEN}/editMessageText', methods=['POST'])
def edit_message() -> dict:
    args = parse_args(request.url)
    utils.queue.append(args)
    logging.info("Message was edited!")
    return return_message(args)
