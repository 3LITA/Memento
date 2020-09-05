from copy import copy

import mock
from flask_babel import gettext as _

from tests import conftest
from tests.test_bot import markups
from tests.testutils import request_generator, setup, mocks, utils
from tests.testutils.telebot_requests import (
    Request, SEND_MESSAGE, DELETE_MESSAGE, MARKDOWN
)

setup.setup_servers()


def test_send_issue(chat_id, username):
    import app.bot.contexts
    from app.models.User import User

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.SEND_ISSUE
    )
    app.bot.contexts.expectations = {
        chat_id: copy(expectations)
    }

    issue = "I am just testing the handler"

    data = request_generator.generate_message(
        text=issue,
        chat_id=chat_id,
    )

    with mock.patch.object(
            User, 'get_by', mocks.get_user_by(by_chat_id=True, username=username)
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            SEND_MESSAGE,
            chat_id=chat_id,
            text=_(
                "Fine, *{username}*, your issue was sent to the support assistant:\n\n"
                "{issue_text}"
            ).format(username=username, issue_text=issue),
            parse_mode=MARKDOWN,
            reply_markup=markups.main_menu_without_decks(),
        ),
        Request(
            DELETE_MESSAGE,
            chat_id=chat_id,
        ),
    ]

    assert not app.bot.contexts.expectations.get(chat_id)
