import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, Message

from app import settings
from app.app import logging
from app.models import CardType, utils
from app.models.Card import Card
from app.models.Deck import Deck
from app.models.User import User

from . import contexts, replies
from .keyboard import buttons, markups


handler_return = Tuple[Optional[InlineKeyboardMarkup], replies.Reply]


def log_message(func: Callable) -> Callable:
    from app.bot.main import bot

    def wrapped(message: Message) -> None:
        logging.info(
            "[%s.%s] %s: %s",
            func.__module__,
            func.__name__,
            message.chat.id,
            message.text,
        )
        user = get_user(message)
        keyboard, reply = None, None
        try:
            keyboard, reply = func(message=message, user=user)
        except contexts.ContextNotFound as e:
            logging.warning(e)
            reply = replies.CONTEXT_FORGOTTEN
            keyboard = markups.main_menu_markup(user.has_decks())
        except Exception as e:
            logging.critical(e)
        finally:
            if reply:
                if user.inline_keyboard_id:
                    delete_message(bot, message.from_user.id, user.inline_keyboard_id)
                message_id = bot.send_message(
                    chat_id=user.chat_id,
                    text=reply.text,
                    reply_markup=keyboard,
                    parse_mode=reply.parse_mode,
                ).message_id
                user.set_inline_keyboard_id(message_id)

                logging.info(
                    "[%s.%s] bot: %s", func.__module__, func.__name__, reply.text,
                )

    return wrapped


def log_pressed_button(func: Callable) -> Callable:
    from app.bot.main import bot

    def wrapper(callback: CallbackQuery) -> None:
        logging.info(
            "%s.%s - %s pressed the button %s",
            func.__module__,
            func.__name__,
            callback.from_user.id,
            callback.data.get('command'),
        )
        user = get_user(callback)
        kwargs = callback.data
        keyboard, reply = None, None
        try:
            keyboard, reply = func(callback=callback, user=user, **kwargs)
        except contexts.ContextNotFound as e:
            logging.warning(e)
            reply = replies.CONTEXT_FORGOTTEN
            keyboard = markups.main_menu_markup(user.has_decks())
        except Exception as e:
            logging.critical(e)
        finally:
            if reply:
                bot.edit_message_text(
                    text=reply.text,
                    chat_id=user.chat_id,
                    message_id=user.inline_keyboard_id,
                    reply_markup=keyboard,
                    parse_mode=reply.parse_mode,
                )
                logging.info(
                    "[%s.%s] bot: %s", func.__module__, func.__name__, reply.text,
                )

    return wrapper


def get_user(message: Union[CallbackQuery, Message]) -> User:
    return User.get_or_create_by_chat_id(message.from_user.id)


def button_pressed(callback: CallbackQuery, command: Dict[str, Any]) -> bool:
    return callback.data.get('command') == command.get('command')


def humanize_title(title: str) -> str:
    return utils.humanize_title(title)


def get_args(message: Message) -> Optional[List[str]]:
    pattern = r'(^/\w+)(\s(.*))?'
    search = re.search(pattern, message.text)
    args = None
    if search:
        args = search.group(3)
        if args and args.strip() != '':
            args = args.strip()
    return args


def count_gaps(question: str) -> int:
    pattern = r'(_)'
    count = len(re.findall(pattern, question))
    return count


def build_learn_text_and_keyboard(
    user: User, card: Card
) -> Tuple[replies.Reply, InlineKeyboardMarkup]:
    reply = replies.Reply(text=card.question)
    if card.type == CardType.FACT:
        reply = replies.Reply(
            text=f"{reply}\n\n{replies.RATE_KNOWLEDGE}",
            parse_mode=replies.RATE_KNOWLEDGE.parse_mode,
        )
        keyboard = markups.rate_knowledge_markup(card.id)
    elif card.type == CardType.MULTIPLE_CHOICE:
        reply = replies.Reply(
            text=f"{reply}\n\n{replies.USER_CHOSEN}",
            parse_mode=replies.USER_CHOSEN.parse_mode,
        )
        keyboard = markups.multiple_choice_markup(
            card.id, card.deck_id, card.correct_answers, card.wrong_answers,
        )
    elif card.type == CardType.RADIOBUTTON:
        keyboard = markups.radiobutton_markup(
            card.id, card.deck_id, card.correct_answers[0], card.wrong_answers,
        )
    else:
        keyboard = markups.basic_learn_markup(card.id, card.deck.id)
        contexts.set_context(user, contexts.ExpectedCommands.LEARN, card_id=card.id)
    return reply, keyboard


def repeat_keyboard(
    callback: CallbackQuery, exclude: Sequence[str] = (), delete_card_id: int = None
) -> InlineKeyboardMarkup:
    data = callback.message.json
    prev_keyboard = get_previous_keyboard(data)
    if not prev_keyboard:
        raise ValueError

    add_btns = [buttons.DeleteUserCardButton(delete_card_id)] if delete_card_id else []
    return markups.repeat_keyboard(prev_keyboard, exclude, *add_btns)


def get_previous_keyboard(data: dict) -> dict:
    return data.get('reply_markup', {}).get('inline_keyboard')


def delete_message(
    bot: TeleBot, chat_id: Union[int, str], message_id: Union[int, str]
) -> None:
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        logging.error(
            "Failed to delete message %s in chat %s, reason: %s", message_id, chat_id, e
        )


def parse_chosen_nums(callback: CallbackQuery) -> List[int]:
    js = callback.message.json
    text = js['text'].split(replies.USER_CHOSEN.text)
    return sorted([int(num.strip()) for num in text[-1].split(',')])


def parse_question(text: str) -> str:
    question = text.split(replies.USER_CHOSEN.text)
    return ''.join(question[:-1])


def convert_chosen_to_answers(callback: CallbackQuery, chosen: List[int]) -> List[str]:
    js = callback.message.json
    inline_keyboard = js.get('reply_markup', {}).get('inline_keyboard')
    answers = []
    for num in chosen:
        num_part_length = len(f'{num - 1}) ')
        answer = inline_keyboard[num - 1][0]['text'][num_part_length:]
        answers.append(answer)
    return answers


def check_deck_title_is_correct(user: User, title: str) -> Optional[replies.Reply]:
    if len(title) > settings.MAX_DECK_TITLE_LENGTH:
        return replies.TOO_LONG_DECK_TITLE
    if not utils.is_title_correct(title):
        return replies.INCORRECT_CHARACTERS_IN_DECK_TITLE
    if Deck.search_by_title(user, utils.generate_title(user.id, title)):
        return replies.DECK_TITLE_ALREADY_EXISTS.format(title=title.upper())
    return None
