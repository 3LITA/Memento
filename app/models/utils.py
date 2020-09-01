import logging
import re
from typing import Any, Optional, Union

from werkzeug.security import generate_password_hash

from app import exceptions

from . import db


class ActiveRecordMixin:
    def save(self) -> None:
        logging.debug("Save %s", self)
        if self not in db.session:
            logging.debug(
                "Created %s with args %s", self.__class__, _hide_pii(self.__dict__)
            )
            db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        logging.debug("Delete %s", self)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, id_: Union[str, int]) -> Any:
        logging.debug("Getting %s from database", cls.__name__)
        res = cls.query.get(id_)  # type: ignore
        logging.debug("Get result: %s", res)
        if not res:
            logging.critical("%s with id %s not found in database", cls.__name__, id_)
            raise AttributeError(f'{cls.__name__} not found')
        return res

    @classmethod
    def get_by(cls, **kw: Any) -> Optional[Any]:
        logging.debug("Querying %s with args %s", cls.__name__, _hide_pii(kw))
        res = cls.query.filter_by(**kw).first()  # type: ignore
        logging.debug("Query result: %s", res)
        if not res:
            logging.warning(
                "%s with args %s not found in database", cls.__name__, _hide_pii(kw)
            )
        return res


def generate_hash(raw_string: str) -> str:
    return generate_password_hash(raw_string)


def _validate_password(raw_password: str) -> None:
    if len(raw_password) < 8:
        raise exceptions.TooShortPassword("Password must contain at least 8 characters")
    elif re.search('[0-9]', raw_password) is None:
        raise exceptions.NoNumber("Password must contain a numeric digit")
    elif re.search('[A-Z]', raw_password) is None:
        raise exceptions.NoCapitalLetter("Password must contain an uppercase letter")
    elif re.search('[A-Z]', raw_password) is None:
        raise exceptions.NoLowercaseLetter("Password must contain a lowercase letter")


def hash_password(raw_password: str) -> str:
    _validate_password(raw_password)
    return generate_hash(raw_password)


def is_title_correct(title: str) -> bool:
    return bool(re.compile(r'^[A-Za-z0-9-]*$').search(title))


def generate_title(user_id: int, title: str) -> str:
    return f'{user_id}:{title.lower()}'


def humanize_title(title: str) -> str:
    return ''.join(title.split(':')[1:])


def _hide_pii(raw_data: dict) -> dict:
    private_fields = ('_email', '_username')
    return {
        k: generate_hash(raw_data[k]) if k in private_fields else raw_data[k]
        for k in raw_data
    }
