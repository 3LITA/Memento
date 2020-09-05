import mock
import requests
from flask_babel import gettext as _

from tests import conftest
from tests.test_bot import markups
from tests.testutils import setup, mocks, utils
from tests.testutils.telebot_requests import Request, SEND_MESSAGE, MARKDOWN

setup.setup_servers()


def test_login():
    from app.settings import URLS

    url = f"{conftest.MAIN_SERVER_ROOT}{URLS.LOGIN}"
    r = requests.get(url, cookies={})

    assert r.status_code == 200
    assert r.url == url
    assert not r.cookies


def test_login_with_chat_id(chat_id):
    from app.settings import URLS

    url = f"{conftest.MAIN_SERVER_ROOT}{URLS.LOGIN}?chat_id={chat_id}"
    r = requests.get(url, cookies={})

    assert r.status_code == 200
    assert r.url == url
    assert r.cookies.get('chat_id') == str(chat_id)


def test_successful_sign_up(username):
    from app.settings import URLS

    url = f"{conftest.MAIN_SERVER_ROOT}{URLS.SIGN_UP}"
    r = requests.post(
        url, data=dict(email="hello@com", password1="Qwerty123", username=username),
    )

    assert r.status_code == 200
    assert r.url == f"{conftest.MAIN_SERVER_ROOT}{URLS.LOGIN}"
    assert _("Well done! Now you can sign in using your credentials") in r.text


def test_successful_sign_up_with_chat_id(chat_id, username):
    from app.settings import URLS

    r, queue = utils.post(
        URLS.SIGN_UP,
        data=dict(email="hello@com", password1="Qwerty123", username=username),
        cookies=dict(chat_id=str(chat_id)),
    )

    assert r.status_code == 200
    assert r.url == f"{conftest.MAIN_SERVER_ROOT}{URLS.LOGIN}"
    assert _("Well done! Now you can sign in using your credentials") in r.text
    assert queue == [
        Request(
            SEND_MESSAGE,
            chat_id=chat_id,
            text=_(
                "Excellent, *{username}*!\n"
                "Since you have signed up, you can create new decks!"
            ).format(username=username),
            parse_mode=MARKDOWN,
            reply_markup=markups.main_menu_without_decks(),
        )
    ]


def test_sign_up_email_in_use(chat_id, email, username):
    from app.settings import URLS
    from app.models.User import User

    url = f"{conftest.MAIN_SERVER_ROOT}{URLS.SIGN_UP}"

    with mock.patch.object(User, 'get_by', mocks.get_user_by(by_email=True)):
        r = requests.post(
            url, data=dict(email=email, password1="Qwerty123", username=username)
        )

    assert r.status_code == 200
    assert r.url == f"{conftest.MAIN_SERVER_ROOT}{URLS.LOGIN}"
    assert _("The email {email} is already in use").format(email=email) in r.text


def test_sign_up_incorrect_chars_in_username(chat_id, email, username):
    from app.settings import URLS

    url = f"{conftest.MAIN_SERVER_ROOT}{URLS.SIGN_UP}"

    username = f"{username}%$"

    r = requests.post(
        url, data=dict(email=email, password1="Qwerty123", username=username)
    )

    assert r.status_code == 200
    assert r.url == f"{conftest.MAIN_SERVER_ROOT}{URLS.LOGIN}"
    assert _(
        "The username {username} contains incorrect characters, "
        "only latin letters and numbers are allowed"
    ).format(username=username) in r.text


def test_sign_up_username_in_use(chat_id, email, username):
    from app.settings import URLS
    from app.models.User import User

    url = f"{conftest.MAIN_SERVER_ROOT}{URLS.SIGN_UP}"

    with mock.patch.object(User, 'get_by', mocks.get_user_by(by_username=True)):
        r = requests.post(
            url, data=dict(email=email, password1="Qwerty123", username=username)
        )

    assert r.status_code == 200
    assert r.url == f"{conftest.MAIN_SERVER_ROOT}{URLS.LOGIN}"
    assert _("The username {username} is already in use").format(
        username=username
    ) in r.text


def test_sign_up_insecure_password(chat_id, email, username):
    from app.settings import URLS

    url = f"{conftest.MAIN_SERVER_ROOT}{URLS.SIGN_UP}"

    r = requests.post(
        url, data=dict(email=email, password1="hi", username=username)
    )

    assert r.status_code == 200
    assert r.url == f"{conftest.MAIN_SERVER_ROOT}{URLS.LOGIN}"
    assert _(
        "Password must be at least 8 characters long, "
        "contain at least one digit, "
        "one uppercase and one lowercase latin letter"
    ) in r.text
