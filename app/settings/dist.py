URL = 'https://api.telegram.org/bot'

MAX_QUESTION_LENGTH = 255
MAX_DECK_TITLE_LENGTH = 127
MAX_SLUG_LENGTH = 127
MAX_ANSWER_LENGTH = 63
CARD_TYPES_RANGE = 5  # 0 - 4
KNOWLEDGE_RANGE = 3

DEFAULT_LOCALE = 'en'
LANGUAGES = {'en': '🇬🇧', 'ru': '🇷🇺'}
BABEL_TRANSLATION_DIRECTORIES = 'localization/i18n'

COMMANDS = {
    'start_commands': ['start'],
    'help_commands': ['help'],
    'decks_commands': ['decks'],
    'deck_create_commands': ['create', 'deck', 'new'],
    'delete_commands': ['delete', 'del'],
    'delete_public_commands': ['delete_public', 'del_pub'],
    'card_create_commands': ['card'],
    'card_types_commands': ['card_types'],
    'cancel_commands': ['cancel'],
    'learn_commands': ['learn'],
    'show_commands': ['show'],
    'get_me_commands': ['getme'],
    'expectations_commands': ['expectations'],
    'share_commands': ['share'],
    'join_commands': ['join'],
    'merge_commands': ['merge'],
    'update_commands': ['update'],
    'hire_commands': ['hire'],
    'fire_commands': ['fire'],
    'menu_commands': ['menu'],
}
