import re
from typing import Any, Union

from app.app import db, logging


class ActiveRecordMixin:
    def save(self) -> None:
        logging.debug("Save %s", self)
        if self not in db.session:
            logging.debug("Created %s with args %s", self.__class__, self.__dict__)
            db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        logging.debug("Delete %s", self)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, id_: Union[str, int]) -> Any:
        logging.debug("Getting %s from database", cls.__name__)
        deck = cls.query.filter_by(id=id_).first()  # type: ignore
        if not deck:
            logging.critical("%s with id %s not found in database", cls.__name__, id_)
            raise AttributeError(f'{cls.__name__} not found')
        return deck

    @classmethod
    def get_by(cls, **kw: Any) -> Any:
        logging.debug("Querying %s with args %s", cls.__name__, kw)
        res = cls.query.filter_by(**kw).first()  # type: ignore
        if not res:
            logging.warning("%s with args %s not found in database", cls.__name__, kw)
        return res


def is_title_correct(title: str) -> bool:
    return bool(re.compile(r'^[A-Za-z0-9-]*$').search(title))


def generate_title(user_id: int, title: str) -> str:
    return f'{user_id}:{title.lower()}'


def humanize_title(title: str) -> str:
    return ''.join(title.split(':')[1:])
