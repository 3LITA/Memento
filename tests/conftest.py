import os
import random

import pytest

from tests.testutils.utils import random_string

BOT_SECRET_URL = random_string()
BOT_TOKEN = 'BOT'
LOGGING_CONFIG = (
    f"{os.path.dirname(os.path.abspath(__file__))}/test-logging-config.yaml"
)
DB_USER = 'postgres'
DB_NAME = 'ankibot'

AWAIT_TIME = .1

MAIN_SERVER_HOST = 'http://localhost'
MAIN_SERVER_PORT = '5000'

STUB_SERVER_HOST = 'http://localhost'
STUB_SERVER_PORT = '5001'

MAIN_SERVER_ROOT = f'{MAIN_SERVER_HOST}:{MAIN_SERVER_PORT}'
STUB_SERVER_ROOT = f'{STUB_SERVER_HOST}:{STUB_SERVER_PORT}'


@pytest.fixture()
def first_name():
    return random_string()


@pytest.fixture()
def inline_keyboard_id():
    return random.randint(0, 100000)


@pytest.fixture()
def chat_id():
    return random.randint(0, 100000)


@pytest.fixture()
def deck_id():
    return random.randint(0, 1000)


@pytest.fixture()
def card_id():
    return random.randint(0, 1000)


@pytest.fixture()
def question_text():
    return f"{random_string()}?"


@pytest.fixture()
def question_with_gaps():
    return f"{random_string()}_{random_string()}_{random_string()}?"


@pytest.fixture()
def correct_answers():
    return [random_string(), random_string()]


@pytest.fixture()
def wrong_answers():
    return [random_string(), random_string(), random_string()]
