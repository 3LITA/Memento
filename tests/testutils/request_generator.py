import random
from typing import Optional

from tests.testutils.utils import random_string

_message = {
    "update_id": 120399271,
    "message": {
        "message_id": 2915,
        "from": {
            "id": 309531723,
            "is_bot": False,
            "first_name": "Albert",
            "last_name": "Shaidullin",
            "username": "albertshady",
            "language_code": "en"
        },
        "chat": {
            "id": 309531723,
            "first_name": "Albert",
            "last_name": "Shaidullin",
            "username": "albertshady",
            "type": "private"
        },
        "date": 1592672666,
        "text": "/start",
        "entities": [
            {
                "offset": 0,
                "length": 6,
                "type": "bot_command"
            }
        ]
    }
}

_callback = {
    'update_id': 120399355,
    'callback_query': {
        'id': '1329428628799200028',
        'from': {
            'id': 309531723,
            'is_bot': False,
            'first_name': 'Albert',
            'last_name': 'Shaidullin',
            'username': 'albertshady',
            'language_code': 'en'
        },
        'message': {
            'message_id': 2938,
            'from': {
                'id': 898816147,
                'is_bot': True,
                'first_name': 'Anki',
                'username': 'Jankibot'
            },
            'chat': {
                'id': 309531723,
                'first_name': 'Albert',
                'last_name': 'Shaidullin',
                'username': 'albertshady',
                'type': 'private'
            },
            'date': 1592839363,
            'edit_date': 1592862799,
            'text': 'Создать новую колоду или добавить существующую?',
            'reply_markup': {
                'inline_keyboard': [
                    [{
                        'text': 'Создать',
                        'callback_data': 'new_deck'
                    }],
                    [{
                        'text': 'Назад',
                        'callback_data': 'main_menu'
                    }]
                ]}
        },
        'chat_instance': '70867223178320818',
        'data': 'main_menu'
    }
}


def _generate_message(chat_id: int, first_name: str, last_name: str, username: str, text: str) -> dict:
    _message['message']['from']['id'] = chat_id
    _message['message']['chat']['id'] = chat_id

    _message['message']['from']['first_name'] = first_name
    _message['message']['chat']['first_name'] = first_name

    _message['message']['from']['last_name'] = last_name
    _message['message']['chat']['last_name'] = last_name

    _message['message']['from']['username'] = username
    _message['message']['chat']['username'] = username

    _message['message']['text'] = text

    return _message


def generate_message(
        text: str,
        chat_id: Optional[int] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
) -> dict:
    chat_id = random.randint(0, 1000) if not chat_id else chat_id
    first_name = random_string() if not first_name else first_name
    last_name = random_string() if not last_name else last_name
    username = random_string() if not username else username
    return _generate_message(chat_id, first_name, last_name, username, text)


def _generate_callback_query(
        chat_id: int,
        first_name: str,
        last_name: str,
        username: str,
        text: str,
        callback_data: str,
        reply_markup: Optional[dict] = None,
) -> dict:
    _callback['callback_query']['from']['id'] = chat_id
    _callback['callback_query']['message']['chat']['id'] = chat_id

    _callback['callback_query']['from']['first_name'] = first_name
    _callback['callback_query']['message']['chat']['first_name'] = first_name

    _callback['callback_query']['from']['last_name'] = last_name
    _callback['callback_query']['message']['chat']['last_name'] = last_name

    _callback['callback_query']['from']['username'] = username
    _callback['callback_query']['message']['chat']['username'] = username

    _callback['callback_query']['message']['text'] = text

    _callback['callback_query']['data'] = callback_data

    if reply_markup:
        _callback['callback_query']['message']['reply_markup'] = reply_markup

    return _callback


def generate_callback_query(
        callback_data: str,
        chat_id: Optional[int] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
        text: Optional[str] = None,
        reply_markup: Optional[dict] = None,
) -> dict:
    chat_id = random.randint(0, 1000) if not chat_id else chat_id
    first_name = random_string() if not first_name else first_name
    last_name = random_string() if not last_name else last_name
    username = random_string() if not username else username
    text = random_string() if not text else text
    return _generate_callback_query(chat_id, first_name, last_name, username, text, callback_data, reply_markup)
