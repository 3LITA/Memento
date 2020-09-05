import logging
from typing import Dict, List, Optional, Union

from telebot.types import CallbackQuery, Message

from app.models.User import User


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


class Context:
    command: str
    deck_id: int
    card_id: int
    card_type: int
    question: str
    correct_answers: List[str]
    gaps: int

    def __init__(self, command: str, **kwargs: Union[int, str, List[str]]) -> None:
        self.command = command
        for item in kwargs:
            self.__setattr__(item, kwargs[item])


expectations: Dict[int, Context] = dict()  # chat_id: {key: value}


def forget_context(user: User) -> Optional[Context]:
    return expectations.pop(user.chat_id, None) if user.chat_id else None


def set_context(user: User, command: str, **kwargs: Union[int, str, List[str]]) -> None:
    if not user.chat_id:
        raise AttributeError("User %s has no chat_id", user.id)
    expectations[user.chat_id] = Context(command=command, **kwargs)


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
    context = expectations.get(message.from_user.id)
    if not context:
        raise ContextNotFound("Context for user %s not found", message.from_user.id)
    return context
