import logging
import os
import pathlib
from logging.config import dictConfig

import yaml


SECRET_KEY = os.getenv('SECRET_KEY')
WEBSITE = os.getenv('WEBSITE')

ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
BOT_SECRET_URL = os.getenv('BOT_SECRET_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')
SUPPORT_BOT_TOKEN = os.getenv('SUPPORT_BOT_TOKEN')

DB_USER = os.getenv('DATABASE_USER')
DB_PASS = os.getenv('DATABASE_PASS', '')
DB_HOST = os.getenv('DATABASE_HOST', 'localhost')
DB_NAME = os.getenv('DATABASE_NAME')

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_PASS = os.getenv('REDIS_PASS', '')

SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

LOGGING_CONFIG_PATH = os.getenv(
    'LOGGING_CONFIG_PATH', f"{(pathlib.Path().absolute())}/logging-config.yaml"
)

with open(LOGGING_CONFIG_PATH, 'r') as file:
    log_cfg = yaml.safe_load(file.read())
    dictConfig(log_cfg)
    logging.info("Successfully loaded logging config")
