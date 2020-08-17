import json
from functools import partial
from typing import List

import mock
import pytest
from flask_babel import _

from tests import conftest
from tests.testutils import setup, request_generator, utils, mocks
from tests.test_bot import markups

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


def test_learn_deck_with_no_cards(deck_id):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck

    data = request_generator.generate_callback_query(
        callback_data=cd.learn_user_deck(deck_id),
    )
    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        with mock.patch.object(Deck, 'pull_card', mocks.raise_value_error):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    expected_reply = _("Deck *{title}* is empty").format(title=f"deck{deck_id}".upper())
    assert req['text'][0] == expected_reply

    expected_markup = markups.deck_menu_without_cards(deck_id)
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_learn_fact(deck_id, card_id, question_text):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck
    from app.models import CardType

    data = request_generator.generate_callback_query(
        callback_data=cd.learn_user_deck(deck_id),
    )
    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        with mock.patch.object(
                Deck, 'pull_card', lambda f: mocks._card_get_by_id(
                    card_id=card_id,
                    question=question_text,
                    card_type=CardType.FACT,
                    deck_id=deck_id,
                )
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    expected_reply = (
        f"{question_text}\n\n"
        f"{_('Please, estimate your knowledge level:')}"
    )
    assert req['text'][0] == expected_reply

    expected_markup = markups.rate_knowledge_markup(card_id)
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


@pytest.mark.parametrize('card_type', (1, 2), ids=('SIMPLE', 'WITH_GAPS'))
def test_learn_card(deck_id, card_id, question_text, question_with_gaps,
                    correct_answers, chat_id, card_type):
    from app.bot.keyboard import cd
    from app.bot.contexts import expectations, Context, ExpectedCommands
    from app.models.Deck import Deck
    from app.models import CardType

    question = question_with_gaps if card_type == CardType.GAPS else question_text

    data = request_generator.generate_callback_query(
        callback_data=cd.learn_user_deck(deck_id),
        chat_id=chat_id,
    )
    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        with mock.patch.object(
                Deck, 'pull_card', lambda f: mocks._card_get_by_id(
                    card_id=card_id,
                    question=question,
                    card_type=card_type,
                    correct_answers=correct_answers,
                    deck_id=deck_id
                )
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == question

    utils.expectations_match(expectations[chat_id], Context(
        ExpectedCommands.LEARN,
        card_id=card_id,
    ))

    expected_markup = {
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
    }
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


@pytest.mark.parametrize('card_type', (3, 4), ids=("MULTICHOICE", "RADIOBUTTON"))
def test_learn_complex_cards(deck_id, card_id, question_text, correct_answers,
                             wrong_answers, chat_id, card_type):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck
    from app.models import CardType

    if card_type == CardType.RADIOBUTTON:
        correct_answers = correct_answers[:1]

    data = request_generator.generate_callback_query(
        callback_data=cd.learn_user_deck(deck_id),
    )
    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
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
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    expected_reply = (
        f"{question_text}\n\n{_('Your choice:')}"
        if card_type == CardType.MULTIPLE_CHOICE
        else question_text
    )
    assert req['text'][0] == expected_reply

    actual_markup = json.loads(req['reply_markup'][0])
    all_answers = correct_answers + wrong_answers

    if card_type == CardType.MULTIPLE_CHOICE:
        assert multiple_choice_answer_sheet_built_correctly(actual_markup, card_id,
                                                            deck_id, all_answers)
    else:
        assert radiobutton_answer_sheet_built_correctly(
            actual_markup, card_id, deck_id, all_answers, correct_answers
        )


@pytest.mark.parametrize('knowledge', (1, 2, 3))
def test_set_knowledge(deck_id, card_id, question_text, knowledge):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models.Deck import Deck
    from app.models import CardType

    rate_card_id = 19

    data = request_generator.generate_callback_query(
        callback_data=cd.rate_knowledge(rate_card_id, knowledge),
    )
    with mock.patch.object(
            Card, 'get', mocks.card_get_by_id(
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
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == question_text

    expected_markup = markups.learn_card_markup(card_id, deck_id)
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_get_tip(question_text, card_id, deck_id):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models import CardType

    tips = ['tip1']

    prev_markup = markups.multiple_choice_answer_sheet(card_id, deck_id)
    data = request_generator.generate_callback_query(
        callback_data=cd.tip(card_id),
        text=question_text,
        reply_markup=prev_markup,
    )
    with mock.patch.object(
            Card, 'get', mocks.card_get_by_id(
                question=question_text,
                card_type=CardType.SIMPLE,
                tips=tips,
                deck_id=deck_id,
            )
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == f"{question_text}\n\n{_('Tip: ')}{tips[0]}"

    expected_markup = prev_markup
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
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_get_no_tips(question_text, card_id, deck_id):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models import CardType

    prev_markup = markups.multiple_choice_answer_sheet(card_id + 1, deck_id)
    data = request_generator.generate_callback_query(
        callback_data=cd.tip(card_id),
        text=question_text,
        reply_markup=prev_markup,
    )
    with mock.patch.object(
            Card, 'get', mocks.card_get_by_id(
                question=question_text, card_type=CardType.SIMPLE
            )
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == _(
        f"{question_text}\n\n"
        "Unfortunately, there are no tips for this question...\n"
        "I can show you the answer though"
    )

    expected_markup = prev_markup
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
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


@pytest.mark.parametrize('correct_answers_cnt', [2, 1, 0])
def test_show_answers(card_id, deck_id, question_text, correct_answers,
                      correct_answers_cnt):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models import CardType

    correct_answers = correct_answers[:correct_answers_cnt]

    prev_markup = markups.multiple_choice_answer_sheet_after_tip(card_id, deck_id)
    data = request_generator.generate_callback_query(
        callback_data=cd.show_answer(card_id),
        text=question_text,
        reply_markup=prev_markup,
    )
    with mock.patch.object(
            Card, 'get', mocks.card_get_by_id(
                question=question_text,
                card_type=CardType.MULTIPLE_CHOICE,
                correct_answers=correct_answers,
            )
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    if correct_answers_cnt == 0:
        text = _("There are no correct answers.")
    elif correct_answers_cnt == 1:
        text = _('Correct answer: ')
    else:
        text = _('Correct answers: ')
    expected_reply = f"{question_text}\n\n{text}{', '.join(correct_answers)}"

    req = queue[-1]
    assert req['text'][0] == expected_reply

    expected_markup = prev_markup
    expected_markup['inline_keyboard'].pop()
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


@pytest.mark.parametrize('is_correct', [True, False], ids=('Correct', 'Wrong'))
def test_answer_radiobutton(card_id, deck_id, question_text, correct_answers,
                            wrong_answers, is_correct):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models import CardType

    mark = 'T' if is_correct else 'F'

    data = request_generator.generate_callback_query(
        callback_data=cd.radio_answer(card_id, mark),
    )
    with mock.patch.object(
            Card, 'get', mocks.card_get_by_id(
                question=question_text,
                card_type=CardType.RADIOBUTTON,
                correct_answers=correct_answers[:1],
                wrong_answers=wrong_answers,
                deck_id=deck_id
            )
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    expected_replies = CORRECT_REPLIES if is_correct else [f"{question_text}\n\n{reply}"
                                                           for reply in WRONG_REPLIES]
    assert req['text'][0] in expected_replies

    actual_markup = json.loads(req['reply_markup'][0])

    if is_correct:
        expected_markup = markups.rate_knowledge_markup(card_id)
        assert actual_markup == expected_markup
    else:
        all_answers = correct_answers[:1] + wrong_answers
        assert radiobutton_answer_sheet_built_correctly(
            actual_markup, card_id, deck_id, all_answers, correct_answers
        )


@pytest.mark.parametrize('prev_answers', [[], [1, 3], [1, 2]],
                         ids=('activate first', 'activate more', 'deactivate'))
def test_pick_answer(card_id, deck_id, question_text, correct_answers, wrong_answers,
                     prev_answers):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models import CardType

    chosen_answer = 2

    answers = correct_answers + wrong_answers

    default_text = f"{question_text}\n\n{_('Your choice:')}"
    prev_text = (
        f"{default_text} {', '.join(str(ans) for ans in prev_answers)}"
        if prev_answers
        else default_text
    )

    prev_markup = markups.multiple_choice_answer_sheet(card_id, deck_id, answers)
    data = request_generator.generate_callback_query(
        callback_data=cd.pick_answer(chosen_answer),
        text=prev_text,
        reply_markup=prev_markup,
    )
    with mock.patch.object(
            Card, 'get', mocks.card_get_by_id(
                question=question_text,
                card_type=CardType.MULTIPLE_CHOICE,
                correct_answers=correct_answers,
                wrong_answers=wrong_answers,
            )
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    if chosen_answer in prev_answers:
        prev_answers.remove(chosen_answer)
    else:
        prev_answers.append(chosen_answer)
        prev_answers.sort()
    expected_reply = f"{default_text} {', '.join([str(ans) for ans in prev_answers])}"
    assert req['text'][0] == expected_reply

    actual_markup = json.loads(req['reply_markup'][0])
    assert actual_markup == prev_markup


@pytest.mark.parametrize(
    argnames='submitted_nums,correct_cnt',
    argvalues=[(['1', '2'], 2), (['1'], 2), (['1', '2'], 0), ([], 2), ([], 0)],
    ids=("Both correct", "One less", "Two extra", "Two less", "None correct")
)
def test_submit_answers(card_id, deck_id, question_text, wrong_answers, submitted_nums,
                        correct_cnt, correct_answers):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models import CardType

    correct_answers = correct_answers[:correct_cnt]

    answers = correct_answers + wrong_answers
    correct_nums = [str(i + 1) for i, answer in enumerate(answers) if
                    answer in correct_answers]
    is_correct = correct_nums == submitted_nums

    final_text = f"{question_text}\n\n{_('Your choice:')} {', '.join(submitted_nums)}"

    prev_markup = markups.multiple_choice_answer_sheet(card_id, deck_id, answers)
    data = request_generator.generate_callback_query(
        callback_data=cd.submit(card_id),
        text=final_text,
        reply_markup=prev_markup,
    )
    with mock.patch.object(
            Card, 'get', mocks.card_get_by_id(
                question=question_text,
                card_type=CardType.MULTIPLE_CHOICE,
                correct_answers=correct_answers,
                wrong_answers=wrong_answers,
                deck_id=deck_id,
            )
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    expected_replies = (
        CORRECT_REPLIES
        if is_correct
        else [f"{question_text}\n\n{reply}" for reply in WRONG_REPLIES]
    )
    assert req['text'][0] in expected_replies

    actual_markup = json.loads(req['reply_markup'][0])

    if is_correct:
        assert actual_markup == markups.rate_knowledge_markup(card_id)
    else:
        assert multiple_choice_answer_sheet_built_correctly(actual_markup, card_id,
                                                            deck_id, answers)


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
