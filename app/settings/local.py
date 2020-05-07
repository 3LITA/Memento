import os

BOT_SECRET_URL = os.getenv('BOT_PATH')
TOKEN = os.getenv('TOKEN')
# TOKEN = '1152242930:AAFI9hBDihuwE1bhp4GewXrjkIa_JZk2maY'
DB_USER = os.getenv('DATABASE_USER')
DB_PASS = os.getenv('DATABASE_PASS', '')
DB_HOST = os.getenv('DATABASE_HOST', 'localhost')
DB_NAME = os.getenv('DATABASE_NAME')
SECRET_KEY = os.getenv('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
