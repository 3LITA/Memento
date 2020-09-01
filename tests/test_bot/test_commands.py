import mock
from flask_babel import gettext as _

from tests.test_bot import markups
from tests.testutils import setup, request_generator, utils, mocks
from tests.testutils.telebot_requests import (
    Request, SEND_MESSAGE, DELETE_MESSAGE, MARKDOWN
)
from tests import conftest

setup.setup_servers()


def test_start_handler(first_name, chat_id):
    from app.settings import BotCommands

    data = request_generator.generate_message(
        text=f'/{BotCommands.start_commands[0]}',
        chat_id=chat_id,
        first_name=first_name,
    )
    r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            action=SEND_MESSAGE,
            chat_id=chat_id,
            text=_(
                "Hi, *{}*!\n"
                "I am gonna help you learn everything you've always wanted, "
                "no matter how hard it is!\n"
                "But first, you must sign up."
            ).format(first_name),
            reply_markup=markups.sign_up_markup(chat_id),
            parse_mode=MARKDOWN,
        ),
        Request(
            action=DELETE_MESSAGE,
            chat_id=chat_id,
        ),
    ]


def test_start_again_handler(username, inline_keyboard_id, chat_id):
    from app.settings import BotCommands
    from app.models.User import User

    data = request_generator.generate_message(
        text=f'/{BotCommands.start_commands[0]}',
        chat_id=chat_id,
    )
    with mock.patch.object(User, 'get_by', mocks.get_user_by(
            by_chat_id=True, username=username
    )):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            action=SEND_MESSAGE,
            chat_id=chat_id,
            text=_("Welcome back, *{}*!").format(username),
            parse_mode=MARKDOWN,
            reply_markup=markups.main_menu_without_decks(),
        ),
        Request(
            action=DELETE_MESSAGE,
            chat_id=chat_id,
        ),
    ]


def test_help_handler(chat_id):
    from app.settings import BotCommands
    from app.models.User import User

    data = request_generator.generate_message(
        text=f'/{BotCommands.help_commands[0]}',
        chat_id=chat_id,
    )
    with mock.patch.object(User, 'get_by', mocks.get_user_by(by_chat_id=True)):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            action=SEND_MESSAGE,
            chat_id=chat_id,
            text=_(
                "%(menu_command)s - use this command to navigate\n",
                menu_command=BotCommands.menu_commands[-1],
            )
        ),
        Request(
            action=DELETE_MESSAGE,
            chat_id=chat_id,
        )
    ]


def test_menu_command_with_no_decks(chat_id):
    from app.settings import BotCommands
    from app.models.User import User

    data = request_generator.generate_message(
        text=f'/{BotCommands.menu_commands[0]}',
        chat_id=chat_id
    )
    with mock.patch.object(User, 'get_by', mocks.get_user_by(by_chat_id=True)):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            SEND_MESSAGE,
            chat_id=chat_id,
            text=_("It's a start menu."),
            reply_markup=markups.main_menu_without_decks(),
        ),
        Request(
            DELETE_MESSAGE,
            chat_id=chat_id,
        )
    ]


def test_menu_command_having_decks(chat_id):
    from app.settings import BotCommands
    from app.models.User import User

    data = request_generator.generate_message(
        text=f'/{BotCommands.menu_commands[0]}',
        chat_id=chat_id,
    )

    with mock.patch.object(
            User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            SEND_MESSAGE,
            chat_id=chat_id,
            text=_("It's a start menu."),
            reply_markup=markups.main_menu_with_decks(),
        ),
        Request(
            DELETE_MESSAGE,
            chat_id=chat_id,
        )
    ]


def test_unknown_command(chat_id):
    from app.models.User import User

    data = request_generator.generate_message(
        text=f'/{utils.random_string(10)}',
        chat_id=chat_id,
    )
    with mock.patch.object(
            User, 'get_by', mocks.get_user_by(by_chat_id=True)
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            SEND_MESSAGE,
            chat_id=chat_id,
            text=_("Sorry, I don't understand this command"),
        ),
        Request(
            DELETE_MESSAGE,
            chat_id=chat_id,
        )
    ]
