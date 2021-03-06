import logging
import os
import pathlib
from logging.config import dictConfig

import yaml


ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
BOT_SECRET_URL = os.getenv('BOT_SECRET_URL')
SUPPORT_BOT_TOKEN = os.getenv('SUPPORT_BOT_TOKEN')
TOKEN = os.getenv('BOT_TOKEN')
DB_USER = os.getenv('DATABASE_USER')
DB_PASS = os.getenv('DATABASE_PASS', '')
DB_HOST = os.getenv('DATABASE_HOST', 'localhost')
DB_NAME = os.getenv('DATABASE_NAME')
SECRET_KEY = os.getenv('SECRET_KEY')
WEBSITE = os.getenv('WEBSITE')

SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

LOGGING_CONFIG_PATH = os.getenv(
    'LOGGING_CONFIG_PATH', f"{(pathlib.Path().absolute())}/logging-config.yaml"
)

with open(LOGGING_CONFIG_PATH, 'r') as file:
    log_cfg = yaml.safe_load(file.read())
    dictConfig(log_cfg)
    logging.info("Successfully loaded logging config")
