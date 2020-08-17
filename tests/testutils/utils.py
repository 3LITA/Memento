import string
import time
from functools import partial
from random import choice
from typing import List, Optional, Tuple

import requests

from tests import conftest

queue = list()


def _make_request(
        method: str,
        relative_url: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        wait: Optional[int] = None,
) -> Tuple[requests.Response, List[dict]]:
    if not wait:
        wait = conftest.AWAIT_TIME
    url = f'{conftest.MAIN_SERVER_ROOT}/{relative_url}'
    if method == 'get':
        r = requests.get(url, params=params, data=data, json=json)
    elif method == 'post':
        r = requests.post(url, data=data, json=json)
    else:
        raise NotImplementedError
    time.sleep(wait)
    return r, queue


post = partial(_make_request, 'post')
get = partial(_make_request, 'get')


def expectations_match(actual, expected):
    if not expected:
        assert not actual
    else:
        assert actual.__dict__ == expected.__dict__


def random_string(letters: int = 10) -> str:
    return ''.join([choice(string.ascii_letters) for _ in range(letters)])


def set_expectations(user_id: int, command: str, metadata: dict):
    from app.bot import contexts
    data = {'command': command}
    data.update(metadata)
    contexts.expectations[user_id] = data
