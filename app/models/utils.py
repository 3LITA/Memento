import re
import typing

from sqlalchemy.ext.mutable import Mutable


class MutableList(Mutable, list):
    def append(self, value: typing.Any) -> None:
        list.append(self, value)
        self.changed()
        return None

    @classmethod
    def coerce(
        cls: typing.Any, key: typing.Any, value: typing.Any
    ) -> typing.Optional[typing.Union['MutableList', typing.Any]]:
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value


def is_title_correct(title: str) -> typing.Optional[typing.Match]:
    return re.match(r'^[A-Za-z0-9_-]*$', title)


def generate_title(chat_id: int, title: str) -> str:
    return str(chat_id) + ':' + title.lower()


def humanize_title(chat_id: int, title: str) -> str:
    return title[1 + len(str(chat_id)) :]


def generate_attempt(success: bool, timestamp: int) -> str:
    return 'T:' + str(timestamp) if success else 'F:' + str(timestamp)
