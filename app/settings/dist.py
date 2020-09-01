MAX_QUESTION_LENGTH = 255
MAX_DECK_TITLE_LENGTH = 127
MAX_SLUG_LENGTH = 127
MAX_ANSWER_LENGTH = 63
MAX_TIP_LENGTH = 63
CARD_TYPES_RANGE = 5  # 0 - 4
KNOWLEDGE_RANGE = 3

DEFAULT_LOCALE = 'en'
LANGUAGES = {'en': '🇬🇧', 'ru': '🇷🇺'}
BABEL_TRANSLATION_DIRECTORIES = 'i18n'


class URLS:
    INDEX = '/'
    PROFILE = '/profile'

    SIGN_IN = '/signin'
    SIGN_UP = '/signup'

    LOGIN = '/login'
    LOGOUT = '/logout'


class BotCommands:
    start_commands = ['start']
    help_commands = ['help']
    expectations_commands = ['expectations']
    menu_commands = ['menu']
