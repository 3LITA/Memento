import json

import mock
from flask_babel import gettext as _

from tests import conftest
from tests.test_bot import markups
from tests.testutils import setup, request_generator, utils, mocks
from tests.testutils.telebot_requests import EDIT_MESSAGE, MARKDOWN, Request

setup.setup_servers()


def test_open_main_menu_with_no_decks(chat_id):
    from app.bot.keyboard import cd
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.main_menu(),
        chat_id=chat_id,
    )
    with mock.patch.object(
            User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=False)
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=_("It's a start menu."),
            reply_markup=markups.main_menu_without_decks(),
        )
    ]


def test_open_main_menu_having_decks(chat_id):
    from app.bot.keyboard import cd
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.main_menu(),
        chat_id=chat_id
    )
    with mock.patch.object(
            User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=_("It's a start menu."),
            reply_markup=markups.main_menu_with_decks(),
        )
    ]


def test_open_add_deck_menu(chat_id):
    from app.bot.keyboard import cd
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.add_deck(),
        chat_id=chat_id,
    )
    with mock.patch.object(
            User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=_("Do you want to create a new deck or add an existing one?"),
            reply_markup={
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
        )
    ]


def test_open_my_decks_menu(chat_id):
    from app.bot.keyboard import cd
    from app.models.User import User

    deck_id_1 = 1
    deck_id_2 = 2

    data = request_generator.generate_callback_query(
        callback_data=cd.my_decks(),
        chat_id=chat_id,
    )
    with mock.patch.object(
            User,
            'get_by',
            mocks.get_user_by(by_chat_id=True, deck_ids=(deck_id_1, deck_id_2)),
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=_("Your decks:"),
            reply_markup={
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
        )
    ]


def test_open_deck_menu_with_no_cards(chat_id, deck_id):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.deck_menu(deck_id),
        chat_id=chat_id,
    )
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
            text=_("Deck *{title}*").format(title=f'deck{deck_id}'.upper()),
            parse_mode=MARKDOWN,
            reply_markup=markups.deck_menu_without_cards(deck_id),
        )
    ]


def test_open_deck_menu_having_cards(chat_id, deck_id):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.deck_menu(deck_id),
        chat_id=chat_id,
    )
    with mock.patch.object(Deck, 'has_cards', mocks.true_func):
        with mock.patch.object(Deck, 'get', mocks.get_deck):
            with mock.patch.object(Deck, 'id', deck_id):
                with mock.patch.object(
                        User, 'get_by',
                        mocks.get_user_by(by_chat_id=True, has_decks=True)
                ):
                    r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=_("Deck *{title}*").format(title=f'deck{deck_id}'.upper()),
            parse_mode=MARKDOWN,
            reply_markup=markups.deck_menu_having_cards(deck_id),
        )
    ]
