import os
import pathlib
from logging.config import dictConfig

import yaml


BOT_SECRET_URL = os.getenv('BOT_SECRET_URL')
TOKEN = os.getenv('BOT_TOKEN')
DB_USER = os.getenv('DATABASE_USER')
DB_PASS = os.getenv('DATABASE_PASS', '')
DB_HOST = os.getenv('DATABASE_HOST', 'localhost')
DB_NAME = os.getenv('DATABASE_NAME')
SECRET_KEY = os.getenv('SECRET_KEY')
WEBSITE = os.getenv('WEBSITE')

SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost/ankibot'
SQLALCHEMY_TRACK_MODIFICATIONS = False

LOGGING_CONFIG_PATH = os.getenv(
    'LOGGING_CONFIG_PATH', f"{(pathlib.Path().absolute())}/logging-config.yaml"
)

try:
    with open(LOGGING_CONFIG_PATH, 'r') as file:
        log_cfg = yaml.safe_load(file.read())
        dictConfig(log_cfg)
except FileNotFoundError:
    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {
            'default': {
                'format': (
                    '%(asctime)s %(levelname)s '
                    'in %(module)s.%(funcName)s [%(lineno)d]: %(message)s'
                )
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'default',
                'filename': 'memento.log',
                'maxBytes': 1024,
                'backupCount': 3,
            },
        },
        'loggers': {
            'app': {
                'level': 'DEBUG',
                'handlers': ['console', 'file'],
                'propagate': False,
            }
        },
        'root': {'level': 'DEBUG', 'handlers': ['console']},
    }
    dictConfig(LOGGING_CONFIG)
