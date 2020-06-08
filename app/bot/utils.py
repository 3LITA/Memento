import re
from typing import Optional, List, Tuple, Sequence, Dict, Any, Union

from telebot.types import CallbackQuery, InlineKeyboardMarkup, Message

from . import replies
from .keyboard import buttons, markups
from app.models import utils
from app.models.Card import Card
from app.models.User import User

expectations: Dict[
    int, Dict[str, Any]
] = dict()  # chat_id: {key: value}


def get_user(message: Union[CallbackQuery, Message]) -> User:
    return User.get_or_create(message.from_user.id, message.from_user.username)


def button_pressed(message, callback_data: str) -> bool:
    return message.data.startswith(callback_data)


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
) -> Tuple[str, InlineKeyboardMarkup]:
    text = card.question.text
    if card.question.card_type == 0:
        text += '\n\n' + replies.SET_KNOWLEDGE_REPLY
        keyboard = markups.rate_knowledge_markup(card)
    elif card.question.card_type == 3:
        text += '\n\n' + replies.USER_CHOSEN_REPLY
        keyboard = markups.multiple_choice_markup(
            card.id,
            card.user_deck.id,
            card.question.correct_answers,
            card.question.wrong_answers,
        )
    elif card.question.card_type == 4:
        keyboard = markups.radiobutton_markup(
            card.id,
            card.user_deck.id,
            card.question.correct_answers[0],
            card.question.wrong_answers,
        )
    else:
        keyboard = markups.basic_learn_markup(card.id, card.user_deck.id)
        metadata = {'card_id': card.id}
        set_context(user, 'learn', metadata)
    return text, keyboard


def repeat_keyboard(
        data: dict, exclude: Sequence = (), delete_card_id: int = None
) -> InlineKeyboardMarkup:
    prev_keyboard = get_prev_keyboard(data)
    if not prev_keyboard:
        raise ValueError

    add_btns = [buttons.DeleteUserCardButton(delete_card_id)] if delete_card_id else []
    return markups.repeat_keyboard(prev_keyboard, exclude, *add_btns)


def get_prev_keyboard(data: dict) -> dict:
    return data.get('reply_markup', {}).get('inline_keyboard')


def forget_context(user: User) -> Optional[Dict[str, Any]]:
    return expectations.pop(user.chat_id, None)


def set_context(user: User, command: str, metadata: dict = None) -> None:
    data = {'command': command}
    if metadata:
        data.update(metadata)
    expectations[user.chat_id] = data


def get_expected(message: Message) -> Optional[str]:
    data = expectations.get(message.from_user.id)
    if data:
        return data.get('command')
    return None


def get_context(message: Union[Message, CallbackQuery]) -> Dict[str, Any]:
    data = expectations[message.from_user.id]
    return data


def build_chosen_answers_reply(card: Card) -> str:
    return card.question.text + '\n\n' + replies.USER_CHOSEN_REPLY + ' '


def parse_chosen_nums(js: dict) -> List[str]:
    text = js['text'].split(replies.USER_CHOSEN_REPLY)
    chosen_nums = sorted([num.strip() for num in text[-1].split(',')])

    return chosen_nums


def convert_chosen_to_answers(js: dict, chosen: List[int]) -> List[str]:
    inline_keyboard = js.get('reply_markup', {}).get('inline_keyboard')
    answers = []
    for num in chosen:
        num_part_length = len(f'{num - 1}) ')
        answer = inline_keyboard[num - 1][0]['text'][num_part_length:]
        answers.append(answer)
    return answers
