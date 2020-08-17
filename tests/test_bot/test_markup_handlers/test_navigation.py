import json

import mock
from flask_babel import _

from tests import conftest
from tests.testutils import setup, request_generator, utils, mocks
from tests.test_bot import markups

setup.setup_servers()


def test_open_main_menu_with_no_decks():
    from app.bot.keyboard import cd

    data = request_generator.generate_callback_query(
        callback_data=cd.main_menu(),
    )
    r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == _("It's a start menu.")

    expected_markup = markups.main_menu_without_decks()
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_open_main_menu_having_decks():
    from app.bot.keyboard import cd
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.main_menu(),
    )
    with mock.patch.object(User, 'has_decks', mocks.true_func):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == _("It's a start menu.")

    expected_markup = markups.main_menu_with_decks()
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_open_add_deck_menu():
    from app.bot.keyboard import cd

    data = request_generator.generate_callback_query(
        callback_data=cd.add_deck(),
    )
    r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == _(
        "Do you want to create a new deck or add an existing one?")

    expected_markup = {
        'inline_keyboard': [
            [
                {
                    'callback_data': {'command': 'new_deck'},
                    'text': 'Create'
                }
            ],
            [
                {
                    'callback_data': {'command': 'main_menu'},
                    'text': 'Back'
                }
            ]
        ]
    }
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_open_my_decks_menu():
    from app.bot.keyboard import cd
    from app.models.User import User

    deck_id_1 = 1
    deck_id_2 = 2

    data = request_generator.generate_callback_query(
        callback_data=cd.my_decks(),
    )
    with mock.patch.object(User, 'decks', mocks.get_decks(deck_id_1, deck_id_2)):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == _("Your decks:")

    expected_markup = {
        'inline_keyboard': [
            [
                {
                    'callback_data': {
                        'command': 'deck_menu',
                        'deck_id': deck_id_1,
                    },
                    'text': 'DECK1',
                }
            ],
            [
                {
                    'callback_data': {
                        'command': 'deck_menu',
                        'deck_id': deck_id_2,
                    },
                    'text': 'DECK2',
                }
            ],
            [
                {
                    'callback_data': {'command': 'main_menu'},
                    'text': 'Back',
                }
            ]
        ]
    }
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_open_deck_menu_with_no_cards(deck_id):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck

    data = request_generator.generate_callback_query(
        callback_data=cd.deck_menu(deck_id),
    )
    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == _("Deck *{title}*").format(title=f'deck{deck_id}'.upper())

    expected_markup = markups.deck_menu_without_cards(deck_id)
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_open_deck_menu_having_cards(deck_id):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck

    data = request_generator.generate_callback_query(
        callback_data=cd.deck_menu(deck_id),
    )
    with mock.patch.object(Deck, 'has_cards', mocks.true_func):
        with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
            with mock.patch.object(Deck, 'id', deck_id):
                r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == _("Deck *{title}*").format(title=f'deck{deck_id}'.upper())

    expected_markup = markups.deck_menu_having_cards(deck_id)
    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup
