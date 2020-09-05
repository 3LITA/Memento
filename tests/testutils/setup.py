import os
import threading
import time

import telebot.apihelper

from tests import conftest

telebot.apihelper.API_URL = 'http://localhost:5001/{}/{}'

os.environ['ADMIN_CHAT_ID'] = str(conftest.ADMIN_CHAT_ID)
os.environ['BOT_TOKEN'] = conftest.BOT_TOKEN
os.environ['SUPPORT_BOT_TOKEN'] = conftest.SUPPORT_BOT_TOKEN
os.environ['BOT_SECRET_URL'] = conftest.BOT_SECRET_URL
os.environ['LOGGING_CONFIG_PATH'] = conftest.LOGGING_CONFIG
os.environ['DATABASE_USER'] = conftest.DB_USER
os.environ['DATABASE_NAME'] = conftest.DB_NAME
os.environ['WEBSITE'] = conftest.WEBSITE
os.environ['SECRET_KEY'] = conftest.SECRET_KEY


def _run_stub_server():
    from .stub_server import tgstub
    tgstub.run(host='localhost', port=5001, debug=False)


def run_main_server():
    from app.server import web
    web.run(host='localhost', port=5000, debug=False)


def setup_servers():
    stub_server = threading.Thread(
        target=_run_stub_server, name='Stub Server', daemon=True
    )
    main_server = threading.Thread(
        target=run_main_server, name='Main Server', daemon=True
    )

    stub_server.start()
    main_server.start()

    time.sleep(1)
