from copy import deepcopy
from typing import List

import mock
import pytest
import json
from flask_babel import gettext as _

from tests import conftest
from tests.test_bot import markups
from tests.testutils import setup, request_generator, utils, mocks
from tests.testutils.telebot_requests import EDIT_MESSAGE, MARKDOWN, Request

setup.setup_servers()

CORRECT_REPLIES = [
    _('Correct!'),
    _('Absolutely correct!'),
    _('Perfect!'),
    _('Well done!'),
    _('Excellent!'),
]

WRONG_REPLIES = [
    _('Wrong!'),
    _('Bad news, wrong!'),
    _('Sorry, incorrect!'),
]


def test_learn_deck_with_no_cards(chat_id, deck_id):
    from app.bot.keyboard import cd
    from app import exceptions
    from app.models.Deck import Deck
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.learn_deck(deck_id),
        chat_id=chat_id,
    )
    with mock.patch.object(Deck, 'pull_card', mocks.raise_error(exceptions.EmptyDeck)):
        with mock.patch.object(Deck, 'get', mocks.get_deck):
            with mock.patch.object(
                    User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
            ):
                r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=_("Deck *{title}* is empty").format(title=f"deck{deck_id}".upper()),
            parse_mode=MARKDOWN,
            reply_markup=markups.deck_menu_without_cards(deck_id),
        )
    ]


def test_learn_fact(chat_id, deck_id, card_id, question_text):
    from app.bot.keyboard import cd
    from app.models import CardType
    from app.models.Deck import Deck
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.learn_deck(deck_id),
        chat_id=chat_id,
    )
    with mock.patch.object(Deck, 'get', mocks.get_deck):
        with mock.patch.object(
                Deck, 'pull_card', lambda f: mocks._card_get_by_id(
                    card_id=card_id,
                    question=question_text,
                    card_type=CardType.FACT,
                    deck_id=deck_id,
                )
        ):
            with mock.patch.object(
                    User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
            ):
                r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=f"{question_text}\n\n{_('Please, estimate your knowledge level:')}",
            reply_markup=markups.rate_knowledge_markup(card_id),
        )
    ]


@pytest.mark.parametrize('card_type', (1, 2), ids=('SIMPLE', 'WITH_GAPS'))
def test_learn_card(
        deck_id,
        card_id,
        question_text,
        question_with_gaps,
        correct_answers,
        chat_id,
        card_type,
):
    from app.bot.keyboard import cd
    from app.bot.contexts import expectations, Context, ExpectedCommands
    from app.models import CardType
    from app.models.Deck import Deck
    from app.models.User import User

    question = question_with_gaps if card_type == CardType.GAPS else question_text

    data = request_generator.generate_callback_query(
        callback_data=cd.learn_deck(deck_id),
        chat_id=chat_id,
    )
    with mock.patch.object(Deck, 'get', mocks.get_deck):
        with mock.patch.object(
                Deck, 'pull_card', lambda f: mocks._card_get_by_id(
                    card_id=card_id,
                    question=question,
                    card_type=card_type,
                    correct_answers=correct_answers,
                    deck_id=deck_id
                )
        ):
            with mock.patch.object(
                    User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
            ):
                r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=question,
            reply_markup={
                'inline_keyboard': [
                    [
                        {
                            'callback_data': {
                                'command': 'tip',
                                'card_id': card_id,
                            },
                            'text': 'Tip'
                        },
                        {
                            'callback_data': {
                                'command': 'deck_menu',
                                'deck_id': deck_id,
                            },
                            'text': 'Cancel'
                        }
                    ]
                ]
            },
        )
    ]

    utils.expectations_match(expectations[chat_id], Context(
        ExpectedCommands.LEARN,
        card_id=card_id,
    ))


@pytest.mark.parametrize('card_type', (3, 4), ids=("MULTICHOICE", "RADIOBUTTON"))
def test_learn_complex_cards(
        deck_id,
        card_id,
        question_text,
        correct_answers,
        wrong_answers,
        chat_id,
        card_type,
):
    from app.bot.keyboard import cd
    from app.models import CardType
    from app.models.Deck import Deck
    from app.models.User import User

    if card_type == CardType.RADIOBUTTON:
        correct_answers = correct_answers[:1]

    data = request_generator.generate_callback_query(
        callback_data=cd.learn_deck(deck_id),
        chat_id=chat_id,
    )
    with mock.patch.object(Deck, 'get', mocks.get_deck):
        with mock.patch.object(
                Deck, 'pull_card', lambda f: mocks._card_get_by_id(
                    card_id=card_id,
                    question=question_text,
                    card_type=card_type,
                    correct_answers=correct_answers,
                    wrong_answers=wrong_answers,
                    deck_id=deck_id,
                )
        ):
            with mock.patch.object(
                    User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
            ):
                r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) == 1

    req: Request = queue[0]
    assert req.action == EDIT_MESSAGE
    assert req.chat_id == chat_id
    assert req.text == (
        f"{question_text}\n\n{_('Your choice:')}"
        if card_type == CardType.MULTIPLE_CHOICE
        else question_text
    )
    assert not req.parse_mode

    all_answers = correct_answers + wrong_answers

    if card_type == CardType.MULTIPLE_CHOICE:
        assert multiple_choice_answer_sheet_built_correctly(
            req.reply_markup, card_id, deck_id, all_answers
        )
    else:
        assert radiobutton_answer_sheet_built_correctly(
            req.reply_markup, card_id, deck_id, all_answers, correct_answers
        )


@pytest.mark.parametrize('knowledge', (1, 2, 3))
def test_set_knowledge(chat_id, deck_id, card_id, question_text, knowledge):
    from app.bot.keyboard import cd
    from app.models import CardType
    from app.models.Card import Card
    from app.models.Deck import Deck
    from app.models.User import User

    rate_card_id = 19

    data = request_generator.generate_callback_query(
        callback_data=cd.rate_knowledge(rate_card_id, knowledge),
        chat_id=chat_id,
    )
    with mock.patch.object(
            Card, 'get', mocks.get_card(
                question='Old question',
                card_type=CardType.SIMPLE,
                deck_id=deck_id,
            )
    ):
        with mock.patch.object(
                Deck, 'pull_card', lambda f: mocks._card_get_by_id(
                    card_id=card_id,
                    question=question_text,
                    card_type=CardType.SIMPLE,
                    deck_id=deck_id,
                )
        ):
            with mock.patch.object(
                    User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
            ):
                r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=question_text,
            reply_markup=markups.learn_card_markup(card_id, deck_id),
        )
    ]


def test_get_tip(chat_id, question_text, card_id, deck_id):
    from app.bot.keyboard import cd
    from app.models import CardType
    from app.models.Card import Card
    from app.models.User import User

    tips = ['tip1']

    prev_markup = markups.multiple_choice_answer_sheet(card_id, deck_id)
    expected_markup = deepcopy(prev_markup)

    serialize_callback_data(prev_markup)

    data = request_generator.generate_callback_query(
        callback_data=cd.tip(card_id),
        text=question_text,
        reply_markup=prev_markup,
        chat_id=chat_id,
    )
    with mock.patch.object(
            Card, 'get', mocks.get_card(
                question=question_text,
                card_type=CardType.SIMPLE,
                tips=tips,
                deck_id=deck_id,
            )
    ):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    expected_markup['inline_keyboard'].pop(-2)
    expected_markup['inline_keyboard'].append(
        [
            {
                'callback_data': {
                    'command': 'show_answer',
                    'card_id': card_id,
                },
                'text': 'Show answer'
            }
        ]
    )
    expected_queue = [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=f"{question_text}\n\n{_('Tip: ')}{tips[0]}",
            reply_markup=expected_markup,
        )
    ]
    assert queue == expected_queue


def test_get_no_tips(chat_id, question_text, card_id, deck_id):
    from app.bot.keyboard import cd
    from app.models import CardType
    from app.models.Card import Card
    from app.models.User import User

    prev_markup = markups.multiple_choice_answer_sheet(card_id + 1, deck_id)
    expected_markup = deepcopy(prev_markup)

    serialize_callback_data(prev_markup)

    data = request_generator.generate_callback_query(
        callback_data=cd.tip(card_id),
        text=question_text,
        reply_markup=prev_markup,
        chat_id=chat_id,
    )
    with mock.patch.object(
            Card, 'get', mocks.get_card(
                question=question_text, card_type=CardType.SIMPLE
            )
    ):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    expected_markup['inline_keyboard'].pop(-2)
    expected_markup['inline_keyboard'].append(
        [
            {
                'callback_data': {
                    'command': 'show_answer',
                    'card_id': card_id,
                },
                'text': 'Show answer'
            }
        ]
    )
    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=_(
                f"{question_text}\n\n"
                "Unfortunately, there are no tips for this question...\n"
                "I can show you the answer though"
            ),
            reply_markup=expected_markup,
        )
    ]


@pytest.mark.parametrize('correct_answers_cnt', [2, 1, 0])
def test_show_answers(
        chat_id, card_id, deck_id, question_text, correct_answers, correct_answers_cnt
):
    from app.bot.keyboard import cd
    from app.models import CardType
    from app.models.Card import Card
    from app.models.User import User

    correct_answers = correct_answers[:correct_answers_cnt]

    prev_markup = markups.multiple_choice_answer_sheet_after_tip(card_id, deck_id)
    expected_markup = deepcopy(prev_markup)

    serialize_callback_data(prev_markup)

    data = request_generator.generate_callback_query(
        callback_data=cd.show_answer(card_id),
        text=question_text,
        reply_markup=prev_markup,
        chat_id=chat_id,
    )
    with mock.patch.object(
            Card, 'get', mocks.get_card(
                question=question_text,
                card_type=CardType.MULTIPLE_CHOICE,
                correct_answers=correct_answers,
            )
    ):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    if correct_answers_cnt == 0:
        text = _("There are no correct answers.")
    elif correct_answers_cnt == 1:
        text = _('Correct answer: ')
    else:
        text = _('Correct answers: ')
    expected_reply = f"{question_text}\n\n{text}{', '.join(correct_answers)}"

    expected_markup['inline_keyboard'].pop()

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=expected_reply,
            reply_markup=expected_markup,
        )
    ]


@pytest.mark.parametrize('is_correct', [True, False], ids=('Correct', 'Wrong'))
def test_answer_radiobutton(
        chat_id,
        card_id,
        deck_id,
        question_text,
        correct_answers,
        wrong_answers,
        is_correct,
):
    from app.bot.keyboard import cd
    from app.models import CardType
    from app.models.Card import Card
    from app.models.User import User

    mark = 'T' if is_correct else 'F'

    data = request_generator.generate_callback_query(
        callback_data=cd.radio_answer(card_id, mark),
        chat_id=chat_id,
    )
    with mock.patch.object(
            Card, 'get', mocks.get_card(
                question=question_text,
                card_type=CardType.RADIOBUTTON,
                correct_answers=correct_answers[:1],
                wrong_answers=wrong_answers,
                deck_id=deck_id
            )
    ):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) == 1

    req: Request = queue[0]
    assert req.action == EDIT_MESSAGE
    assert req.chat_id == chat_id
    assert not req.parse_mode

    expected_replies = (
        CORRECT_REPLIES
        if is_correct
        else [f"{question_text}\n\n{reply}" for reply in WRONG_REPLIES]
    )
    assert req.text in expected_replies

    if is_correct:
        expected_markup = markups.rate_knowledge_markup(card_id)
        assert req.reply_markup == expected_markup
    else:
        all_answers = correct_answers[:1] + wrong_answers
        assert radiobutton_answer_sheet_built_correctly(
            req.reply_markup, card_id, deck_id, all_answers, correct_answers
        )


@pytest.mark.parametrize('prev_answers', [[], [1, 3], [1, 2]],
                         ids=('activate first', 'activate more', 'deactivate'))
def test_pick_answer(
        chat_id,
        card_id,
        deck_id,
        question_text,
        correct_answers,
        wrong_answers,
        prev_answers,
):
    from app.bot.keyboard import cd
    from app.models import CardType
    from app.models.Card import Card
    from app.models.User import User

    chosen_answer = 2

    answers = correct_answers + wrong_answers

    default_text = f"{question_text}\n\n{_('Your choice:')}"
    prev_text = (
        f"{default_text} {', '.join(str(ans) for ans in prev_answers)}"
        if prev_answers
        else default_text
    )

    prev_markup = markups.multiple_choice_answer_sheet(card_id, deck_id, answers)
    expected_markup = deepcopy(prev_markup)

    serialize_callback_data(prev_markup)

    data = request_generator.generate_callback_query(
        callback_data=cd.pick_answer(chosen_answer),
        text=prev_text,
        reply_markup=prev_markup,
        chat_id=chat_id,
    )
    with mock.patch.object(
            Card, 'get', mocks.get_card(
                question=question_text,
                card_type=CardType.MULTIPLE_CHOICE,
                correct_answers=correct_answers,
                wrong_answers=wrong_answers,
            )
    ):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    if chosen_answer in prev_answers:
        prev_answers.remove(chosen_answer)
    else:
        prev_answers.append(chosen_answer)
        prev_answers.sort()

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=f"{default_text} {', '.join([str(ans) for ans in prev_answers])}",
            reply_markup=expected_markup,
        )
    ]


@pytest.mark.parametrize(
    argnames='submitted_nums,correct_cnt',
    argvalues=[(['1', '2'], 2), (['1'], 2), (['1', '2'], 0), ([], 2), ([], 0)],
    ids=("Both correct", "One less", "Two extra", "Two less", "None correct")
)
def test_submit_answers(
        chat_id,
        card_id,
        deck_id,
        question_text,
        wrong_answers,
        submitted_nums,
        correct_cnt,
        correct_answers,
):
    from app.bot.keyboard import cd
    from app.models import CardType
    from app.models.Card import Card
    from app.models.User import User

    correct_answers = correct_answers[:correct_cnt]

    answers = correct_answers + wrong_answers
    correct_nums = [
        str(i + 1) for i, answer in enumerate(answers) if answer in correct_answers
    ]
    is_correct = correct_nums == submitted_nums

    final_text = f"{question_text}\n\n{_('Your choice:')} {', '.join(submitted_nums)}"

    prev_markup = markups.multiple_choice_answer_sheet(card_id, deck_id, answers)
    serialize_callback_data(prev_markup)

    data = request_generator.generate_callback_query(
        callback_data=cd.submit(card_id),
        text=final_text,
        reply_markup=prev_markup,
        chat_id=chat_id,
    )
    with mock.patch.object(
            Card, 'get', mocks.get_card(
                question=question_text,
                card_type=CardType.MULTIPLE_CHOICE,
                correct_answers=correct_answers,
                wrong_answers=wrong_answers,
                deck_id=deck_id,
            )
    ):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) == 1

    req: Request = queue[0]

    assert req.action == EDIT_MESSAGE
    assert req.chat_id == chat_id, "Chat ids are different"
    assert req.text in (
        CORRECT_REPLIES
        if is_correct
        else [f"{question_text}\n\n{reply}" for reply in WRONG_REPLIES]
    )
    assert not req.parse_mode

    if is_correct:
        assert req.reply_markup == markups.rate_knowledge_markup(card_id)
    else:
        assert multiple_choice_answer_sheet_built_correctly(
            req.reply_markup, card_id, deck_id, answers
        )


def multiple_choice_answer_sheet_built_correctly(
        actual_markup: dict, card_id: int, deck_id: int, all_answers: List[str]
) -> bool:
    actual_rows = actual_markup['inline_keyboard']
    expected_static_rows = markups.multiple_choice_static_rows(card_id, deck_id)
    assert len(actual_rows) == len(expected_static_rows) + len(all_answers)

    for i, row in enumerate(actual_rows[:len(all_answers)]):
        assert len(row) == 1, f"Row length is more than one: {row}"
        answer = row[0]['text'][3:]
        assert row[0]['text'][:3] == f'{i + 1}: '
        assert row[0]['callback_data'] == {
            'command': 'pick_answer',
            'option': i + 1,
        }
        assert answer in all_answers

    for button_row in expected_static_rows:
        assert button_row in actual_markup['inline_keyboard']

    return True


def radiobutton_answer_sheet_built_correctly(
        actual_markup: dict, card_id: int, deck_id: int, all_answers: List[str],
        correct_answers: List[str]
) -> bool:
    actual_rows = actual_markup['inline_keyboard']
    expected_static_rows = markups.radiobutton_static_rows(card_id, deck_id)
    assert len(actual_rows) == len(expected_static_rows) + len(all_answers)

    for row in actual_rows[:len(all_answers)]:
        assert len(row) == 1, f"Row length is more than one: {row}"
        answer = row[0]['text']
        mark = 'T' if answer in correct_answers else 'F'
        assert row[0]['callback_data'] == {
            'command': 'radio_answer',
            'card_id': card_id,
            'mark': mark,
        }
        assert answer in all_answers

    for button_row in expected_static_rows:
        assert button_row in actual_markup['inline_keyboard']

    return True


def serialize_callback_data(markup: dict) -> None:
    for row in markup['inline_keyboard']:
        for btn in row:
            if callback_data := btn.pop('callback_data', None):
                btn['callback_data'] = json.dumps(callback_data)
