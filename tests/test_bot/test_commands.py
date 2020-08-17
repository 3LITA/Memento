import json

import mock
from flask_babel import _

from tests.testutils import setup, request_generator, utils, mocks
from tests import conftest

setup.setup_servers()


def test_start_handler(first_name):
    from app.settings import BotCommands

    data = request_generator.generate_message(
        text=f'/{BotCommands.start_commands[0]}',
        first_name=first_name,
    )
    r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == _(
        "Hi, *{}*!\n"
        "I am gonna help you learn everything you've always wanted,\n"
        "no matter how hard it is!"
    ).format(first_name)


def test_start_again_handler(first_name, inline_keyboard_id):
    from app.settings import BotCommands
    from app.models.User import User

    data = request_generator.generate_message(
        text=f'/{BotCommands.start_commands[0]}',
        first_name=first_name,
    )
    with mock.patch.object(User, 'inline_keyboard_id', inline_keyboard_id):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == _("Welcome back, *{}*!").format(first_name)


def test_help_handler():
    from app.settings import BotCommands

    data = request_generator.generate_message(
        text=f'/{BotCommands.help_commands[0]}',
    )
    r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == _(
        "%(menu_command)s - use this command to navigate\n",
        menu_command=BotCommands.menu_commands[-1],
    )


def test_menu_command_with_no_decks():
    from app.settings import BotCommands
    from app.bot.keyboard import button_texts, cd

    data = request_generator.generate_message(
        text=f'/{BotCommands.menu_commands[0]}',
    )
    r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == _("It's a start menu.")

    expected_markup = {
        'inline_keyboard': [[
            {'text': button_texts.ADD_DECK, 'callback_data': cd.add_deck()},
            {'text': button_texts.LANGUAGE, 'callback_data': cd.language()},
         ]]
    }
    actual_markup = json.loads(req['reply_markup'][0])
    assert actual_markup == expected_markup


def test_menu_command_having_decks():
    from app.settings import BotCommands
    from app.bot.keyboard import button_texts, cd
    from app.models.User import User

    with mock.patch.object(User, 'has_decks', new=mocks.true_func):

        data = request_generator.generate_message(
            text=f'/{BotCommands.menu_commands[0]}',
        )
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

        assert r.status_code == 200
        assert len(queue) > 0

        req = queue[-1]
        assert req['text'][0] == _("It's a start menu.")

        expected_markup = {
            'inline_keyboard': [[
                {'text': button_texts.MY_DECKS, 'callback_data': cd.my_decks()},
                {'text': button_texts.ADD_DECK, 'callback_data': cd.add_deck()},
                {'text': button_texts.LANGUAGE, 'callback_data': cd.language()},
             ]]
        }
        actual_markup = json.loads(req['reply_markup'][0])
        assert actual_markup == expected_markup


def test_unknown_command():
    data = request_generator.generate_message(
        text=f'/{utils.random_string(10)}',
    )
    r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]
    assert req['text'][0] == _("Sorry, I don't understand this command")
