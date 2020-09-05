from typing import List

from app.i18n import gettext as _


def sign_up() -> str:
    return _('Sign up')


def my_decks() -> str:
    return _('My decks')


def add_deck() -> str:
    return _('Add deck')


def question() -> str:
    return _('Question')


def correct() -> str:
    return _('Correct')


def wrong() -> str:
    return _('Wrong')


def delete() -> str:
    return _('Delete')


def cancel() -> str:
    return _('Cancel')


def rename() -> str:
    return _('Rename')


def back() -> str:
    return _('Back')


def add_card() -> str:
    return _('Add card')


def learn() -> str:
    return _('Learn')


def edit() -> str:
    return _('Edit')


def tip() -> str:
    return _('Tip')


def show_answer() -> str:
    return _('Show answer')


def submit() -> str:
    return _('Submit')


def language() -> str:
    return _('Change language')


def support() -> str:
    return _('Support')


def knowledge_rates() -> List[str]:
    return [_('👎'), _('🖕'), _('👍')]


def create_new_deck() -> str:
    return _('Create')


def add_existing_deck() -> str:
    return _('Add')


def no_correct_answers() -> str:
    return _('No correct answers')


def no_wrong_answers() -> str:
    return _('No wrong answers')
