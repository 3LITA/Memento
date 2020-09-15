import json
import logging
from dataclasses import dataclass
from typing import List, Optional, Union

from redis import Redis
from telebot.types import CallbackQuery, Message

from app import settings
from app.models.User import User


rdb = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class ContextNotFound(Exception):
    pass


class ExpectedCommands:
    CREATE_NEW_DECK = "create_new_deck"

    RENAME_USER_DECK = "rename_user_deck"

    SEND_FACT = "send_fact"

    SEND_QUESTION = "send_question"

    SEND_CORRECT_ANSWERS_ONLY = "correct_answers_only"

    SEND_CORRECT_ANSWERS = "correct_answers"

    SEND_WRONG_ANSWERS = "wrong_answers"

    LEARN = "learn"

    SEND_ISSUE = "send_issue"


@dataclass
class Context:
    command: str
    deck_id: int = None
    card_id: int = None
    card_type: int = None
    question: str = None
    correct_answers: List[str] = None
    gaps: int = None

    def serialize(self) -> str:
        return json.dumps({k: v for k, v in self.__dict__.items()})

    @classmethod
    def parse(cls, raw_context: str) -> 'Context':
        return cls(**json.loads(raw_context))


def forget_context(user: User) -> Optional[Context]:
    return rdb.delete(user.chat_id)


def set_context(user: User, command: str, **kwargs: Union[int, str, List[str]]) -> None:
    if not user.chat_id:
        raise AttributeError("User %s has no chat_id", user.id)
    rdb.set(
        user.chat_id,
        Context(command=command, **kwargs).serialize(),
        ex=settings.REDIS_EXPIRATION_SECONDS,
    )


def command_expected(message: Message, command: str) -> bool:
    try:
        return get_context(message).command == command
    except AttributeError:
        return False
    except ContextNotFound:
        return False
    except Exception as e:
        logging.error(e)
    return True


def get_context(message: Union[Message, CallbackQuery]) -> Context:
    context = rdb.get(message.from_user.id)
    if not context:
        raise ContextNotFound("Context for user %s not found", message.from_user.id)
    return Context.parse(context)
