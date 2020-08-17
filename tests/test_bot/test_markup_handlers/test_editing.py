import json
from functools import partial
from typing import List

import mock
import pytest
from flask_babel import _

from tests import conftest
from tests.test_bot import markups
from tests.testutils import setup, request_generator, utils, mocks

setup.setup_servers()


def test_edit_fact(question_text, card_id, deck_id):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models import CardType

    data = request_generator.generate_callback_query(
        callback_data=cd.edit_card(card_id),
    )
    with mock.patch.object(
            Card, 'get', mocks.card_get_by_id(
                card_type=CardType.FACT, question=question_text, deck_id=deck_id
            )
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    expected_reply = _("Do you want to change in this fact?\n\n{question}").format(
        question=question_text)
    assert req['text'][0] == expected_reply

    expected_markup = markups.edit_fact_markup(card_id, deck_id)
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


@pytest.mark.parametrize(
    "card_type",
    [i for i in range(1, 5)],
    ids=("SIMPLE", "WITH_GAPS", "MULTICHOICE", "RADIOBUTTON"),
)
def test_edit_card(
        card_id: int,
        deck_id: int,
        question_text: str,
        question_with_gaps: str,
        correct_answers: List[str],
        card_type: int,
):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models import CardType

    question = question_with_gaps if card_type == CardType.GAPS else question_text

    data = request_generator.generate_callback_query(
        callback_data=cd.edit_card(card_id),
    )
    with mock.patch.object(
            Card, 'get', mocks.card_get_by_id(
                card_type=card_type,
                question=question,
                correct_answers=correct_answers,
                deck_id=deck_id)
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    answers = f"{_('Correct answers: ')}{', '.join(correct_answers)}"
    if card_type in (CardType.MULTIPLE_CHOICE, CardType.RADIOBUTTON):
        answers = f"{answers}\n\n{_('No wrong answers')}"

    expected_reply = _(
        'What do you want to change in this card?\n\n{question}\n\n{answers}').format(
        question=question, answers=answers
    )
    print(f"Expected reply:\n\n{expected_reply}")
    assert req['text'][0] == expected_reply

    expected_markup = markups.edit_simple_card_markup(card_id, deck_id)
    if card_type in (CardType.MULTIPLE_CHOICE, CardType.RADIOBUTTON):
        expected_markup = markups.edit_complex_card_markup(card_id, deck_id)
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


@pytest.mark.parametrize('card_type', (3, 4), ids=("MULTICHOICE", "RADIOBUTTON"))
def test_edit_card_with_wrong_answers(card_type, card_id, question_text,
                                      correct_answers, wrong_answers, deck_id):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models import CardType

    if card_type == CardType.RADIOBUTTON:
        correct_answers = correct_answers[:1]

    data = request_generator.generate_callback_query(
        callback_data=cd.edit_card(card_id),
    )
    with mock.patch.object(
            Card, 'get', mocks.card_get_by_id(
                card_type=card_type,
                question=question_text,
                correct_answers=correct_answers,
                wrong_answers=wrong_answers,
                deck_id=deck_id,
            )
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    answers = f"{_('Correct answers: ')}{', '.join(correct_answers)}"

    answers = f"{answers}\n\n{_('Wrong answers: ')}{', '.join(wrong_answers)}"

    expected_reply = _(
        'What do you want to change in this card?\n\n' '{question}\n\n' '{answers}'
    ).format(question=question_text, answers=answers)

    assert req['text'][0] == expected_reply

    expected_markup = markups.edit_complex_card_markup(card_id, deck_id)
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_edit_multiple_choice_card_with_no_correct_answers(card_id, deck_id,
                                                           question_text,
                                                           wrong_answers):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models import CardType

    data = request_generator.generate_callback_query(
        callback_data=cd.edit_card(card_id),
    )
    with mock.patch.object(
            Card, 'get', mocks.card_get_by_id(
                card_type=CardType.MULTIPLE_CHOICE,
                question=question_text,
                wrong_answers=wrong_answers,
                deck_id=deck_id,
            )
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    answers = (
        f"{_('No correct answers')}\n\n{_('Wrong answers: ')}{', '.join(wrong_answers)}"
    )

    expected_reply = (
        "What do you want to change in this card?\n\n{question}\n\n{answers}".format(
            question=question_text, answers=answers
        )
    )

    assert req['text'][0] == expected_reply

    expected_markup = markups.edit_complex_card_markup(card_id, deck_id)
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_rename_deck(deck_id, chat_id):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck
    from app.bot.contexts import expectations, Context, ExpectedCommands

    data = request_generator.generate_callback_query(
        callback_data=cd.rename_user_deck(deck_id),
        chat_id=chat_id,
    )
    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    expected_reply = _('Send me the name to the deck *{deck_title}*.').format(
        deck_title=f'deck{deck_id}'.upper())
    assert req['text'][0] == expected_reply

    utils.expectations_match(expectations[chat_id], Context(
        ExpectedCommands.RENAME_USER_DECK,
        deck_id=deck_id
    ))

    expected_markup = {
        'inline_keyboard': [
            [
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


def test_delete_deck(deck_id):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck

    data = request_generator.generate_callback_query(
        callback_data=cd.delete_user_deck(deck_id),
    )
    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    expected_reply = _('Are you sure you want to delete deck *{title}*?').format(
        title=f'deck{deck_id}'.upper())
    assert req['text'][0] == expected_reply

    expected_markup = {
        'inline_keyboard': [
            [
                {
                    'callback_data': {
                        'command': 'sure_delete_user_deck',
                        'deck_id': deck_id,
                    },
                    'text': 'Delete'
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


def test_confirm_deck_deletion(deck_id):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck

    data = request_generator.generate_callback_query(
        callback_data=cd.sure_delete_user_deck(deck_id),
    )
    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    expected_reply = _("Deck *{deck_title}* was successfully deleted!").format(
        deck_title=f'deck{deck_id}'.upper())
    assert req['text'][0] == expected_reply

    expected_markup = markups.main_menu_without_decks()
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_confirm_deck_deletion_not_found(deck_id):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck

    data = request_generator.generate_callback_query(
        callback_data=cd.sure_delete_user_deck(deck_id),
    )
    with mock.patch.object(Deck, 'get', mocks.raise_attribute_error):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    expected_reply = _("Sorry, but I can't find this deck.\n")
    assert req['text'][0] == expected_reply

    expected_markup = markups.main_menu_without_decks()
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_delete_card(card_id, question_text, deck_id, correct_answers):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models import CardType

    data = request_generator.generate_callback_query(
        callback_data=cd.delete_user_card(card_id),
    )
    with mock.patch.object(
            Card, 'get', mocks.card_get_by_id(
                card_type=CardType.SIMPLE,
                question=question_text,
                correct_answers=correct_answers,
                deck_id=deck_id,
            )
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    expected_reply = (
        f"{_('The card was successfully deleted!')}\n\n"
        f"{_('Deck *{title}*').format(title=f'deck{deck_id}'.upper())}"
    )
    assert req['text'][0] == expected_reply

    expected_markup = markups.deck_menu_having_cards(deck_id)
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_delete_card_not_found(card_id, question_text, deck_id, correct_answers):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.delete_user_card(card_id),
    )
    with mock.patch.object(Card, 'get', mocks.raise_attribute_error):
        with mock.patch.object(User, 'has_decks', mocks.true_func):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    expected_reply = (
        f"{_('The card is already deleted')}"
    )
    assert req['text'][0] == expected_reply

    expected_markup = markups.main_menu_with_decks()
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup
