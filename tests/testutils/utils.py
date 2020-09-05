import string
import time
from functools import partial
from random import choice
from typing import Any, List, Optional, Tuple

import requests

from tests import conftest

from .telebot_requests import Request

queue = list()


def await_queue(await_time: Optional[float] = None) -> List[Request]:
    if not await_time:
        await_time = conftest.MAX_AWAIT_TIME

    await_end = time.time() + await_time
    while time.time() < await_end:
        if len(queue) > 0:
            time.sleep(0.1)
            q = queue.copy()
            queue.clear()
            return q
    raise AssertionError("queue is empty")


def _make_request(
        method: str,
        relative_url: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        wait: Optional[float] = None,
        **kwargs: Any,
) -> Tuple[requests.Response, List[Request]]:
    url = f'{conftest.MAIN_SERVER_ROOT}/{relative_url.lstrip("/")}'
    if method == 'get':
        r = requests.get(url, params=params, data=data, json=json, **kwargs)
    elif method == 'post':
        r = requests.post(url, data=data, json=json, **kwargs)
    else:
        raise NotImplementedError
    return r, await_queue(wait)


post = partial(_make_request, 'post')
get = partial(_make_request, 'get')


def expectations_match(actual, expected) -> bool:
    if not expected:
        assert not actual
    else:
        assert actual.__dict__ == expected.__dict__
    return True


def random_string(letters: int = 10) -> str:
    return ''.join([choice(string.ascii_letters) for _ in range(letters)])


def set_expectations(user_id: int, command: str, metadata: dict):
    from app.bot import contexts
    data = {'command': command}
    data.update(metadata)
    contexts.expectations[user_id] = data
