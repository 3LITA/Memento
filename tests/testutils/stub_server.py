import logging
import random
import urllib.parse
from typing import Tuple

import json
from flask import Flask, request

from tests import conftest

from . import telebot_requests, utils

tgstub = Flask('test_app')


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


def parse_args(action: str, raw_url: str) -> Tuple[telebot_requests.Request, dict]:
    arg_line = raw_url.split('?')[1]
    clean_url = urllib.parse.unquote_plus(arg_line)
    args = urllib.parse.parse_qs(clean_url)

    reply_markup = args.get('reply_markup', [None])[0]
    if reply_markup:
        reply_markup = json.loads(reply_markup)
        for row in reply_markup['inline_keyboard']:
            for btn in row:
                if callback_data := btn.pop('callback_data', None):
                    btn['callback_data'] = json.loads(callback_data)

    return telebot_requests.Request(
        action=action,
        chat_id=int(args['chat_id'][0]),
        text=args.get('text', [None])[0],
        reply_markup=reply_markup,
        parse_mode=args.get('parse_mode', [None])[0],
    ), args


@tgstub.route(f'/{conftest.BOT_TOKEN}/sendMessage', methods=['POST'])
def get_new_message() -> dict:
    r, args = parse_args(telebot_requests.SEND_MESSAGE, request.url)
    utils.queue.append(r)
    logging.info("Message was delivered!")
    return return_message(args)


@tgstub.route(f'/{conftest.BOT_TOKEN}/deleteMessage', methods=['POST'])
def delete_message() -> dict:
    r, _ = parse_args(telebot_requests.DELETE_MESSAGE, request.url)
    utils.queue.append(r)
    logging.info("Message was deleted!")
    return {"ok": True, "result": True}


@tgstub.route(f'/{conftest.BOT_TOKEN}/editMessageText', methods=['POST'])
def edit_message() -> dict:
    r, args = parse_args(telebot_requests.EDIT_MESSAGE, request.url)
    utils.queue.append(r)
    logging.info("Message was edited!")
    return return_message(args)
