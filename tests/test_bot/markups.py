from typing import List, Optional, Union

from tests.conftest import WEBSITE
from tests.testutils.utils import random_string


def sign_up_markup(chat_id: int) -> dict:
    return {
        "inline_keyboard": [
            [
                {
                    "text": "Sign up",
                    "url": f"{WEBSITE}/login?chat_id={chat_id}",
                    "callback_data": {"command": "delete_message"},
                }
            ]
        ]
    }


def back_to_main_menu() -> dict:
    return {
        'inline_keyboard': [
            [
                {
                    'callback_data': {'command': 'main_menu'},
                    'text': 'Back'
                },
            ]
        ]
    }


def main_menu_without_decks() -> dict:
    return {
        'inline_keyboard': [
            [
                {
                    'callback_data': {'command': 'add_deck'},
                    'text': 'Add deck'
                },
                {
                    'callback_data': {'command': 'choose_language'},
                    'text': 'Change language'
                }
            ],
            [
                {
                    'callback_data': {'command': 'support'},
                    'text': 'Support'
                }
            ]
        ]
    }


def main_menu_with_decks() -> dict:
    keyboard = main_menu_without_decks()
    keyboard['inline_keyboard'][0].insert(0, {
        'callback_data': {
            'command': 'decks_list',
        },
        'text': 'My decks'
    })
    return keyboard


def deck_menu_without_cards(deck_id: Union[int, str]) -> dict:
    return {
        'inline_keyboard': [
            [
                {
                    'callback_data': {
                        'command': 'add_card',
                        'deck_id': deck_id,
                    },
                    'text': 'Add card'
                },
                {
                    'callback_data': {
                        'command': 'edit_deck',
                        'deck_id': deck_id,
                    },
                    'text': 'Edit'
                }
            ],
            [
                {
                    'callback_data': {
                        'command': 'decks_list',
                    },
                    'text': 'Back'
                }
            ]
        ]
    }


def deck_menu_having_cards(deck_id: Union[int, str]) -> dict:
    return {
        'inline_keyboard': [
            [
                {
                    'callback_data': {
                        'command': 'add_card',
                        'deck_id': deck_id,
                    },
                    'text': 'Add card'
                },
                {
                    'callback_data': {
                        'command': 'learn',
                        'deck_id': deck_id,
                    },
                    'text': 'Learn'
                },
                {
                    'callback_data': {
                        'command': 'edit_deck',
                        'deck_id': deck_id,
                    },
                    'text': 'Edit'
                }
            ],
            [
                {
                    'callback_data': {
                        'command': 'decks_list',
                    },
                    'text': 'Back'
                }
            ]
        ]
    }


def creating_deck_markup() -> dict:
    return {
        'inline_keyboard': [
            [
                {
                    'callback_data': {'command': 'add_deck'},
                    'text': 'Back'
                }
            ]
        ]
    }


def cancel_to_deck_menu(deck_id: Union[int, str]) -> dict:
    return {
        'inline_keyboard': [
            [
                {
                    'callback_data': {
                        'command': 'deck_menu',
                        'deck_id': deck_id,
                    },
                    'text': 'Cancel'
                }
            ]
        ]
    }


def card_created_markup(card_id: Union[int, str], deck_id: Union[int, str]) -> dict:
    return {
        'inline_keyboard': [
            [
                {
                    'callback_data': {
                        'card_id': card_id,
                        'command': 'edit_card'
                    },
                    'text': 'Edit'
                },
                {
                    'callback_data': {
                        'command': 'add_card',
                        'deck_id': deck_id
                    },
                    'text': 'Add card'
                }
            ],
            [
                {
                    'callback_data': {
                        'command': 'deck_menu',
                        'deck_id': deck_id
                    },
                    'text': 'Cancel'
                }
            ]
        ]
    }


def edit_fact_markup(card_id: Union[int, str], deck_id: Union[int, str]) -> dict:
    return {
        'inline_keyboard': [
            [
                {
                    'callback_data': {
                        'command': 'change_card_question',
                        'card_id': card_id,
                    },
                    'text': 'Question'
                },
            ],
            [
                {
                    'callback_data': {
                        'command': 'delete_card',
                        'card_id': card_id,
                    },
                    'text': 'Delete'
                },
                {
                    'callback_data': {
                        'command': 'deck_menu',
                        'deck_id': deck_id,
                    },
                    'text': 'Cancel'
                }
            ]
        ]
    }


def edit_simple_card_markup(card_id: Union[int, str], deck_id: Union[int, str]) -> dict:
    keyboard = edit_fact_markup(card_id, deck_id)
    keyboard['inline_keyboard'][0].append({
        'callback_data': {
            'command': 'change_card_correct_answers',
            'card_id': card_id,
        },
        'text': 'Correct'
    })
    return keyboard


def edit_complex_card_markup(card_id: Union[int, str],
                             deck_id: Union[int, str]) -> dict:
    keyboard = edit_simple_card_markup(card_id, deck_id)
    keyboard['inline_keyboard'][0].append({
        'callback_data': {
            'command': 'change_card_wrong_answers',
            'card_id': card_id,
        },
        'text': 'Wrong'
    })
    return keyboard


def rate_knowledge_markup(card_id: Union[int, str]) -> dict:
    return {
        'inline_keyboard': [
            [
                {
                    'callback_data': {
                        'command': 'rate_knowledge',
                        'card_id': card_id,
                        'knowledge': 0,
                    },
                    'text': '👎'
                },
                {
                    'callback_data': {
                        'command': 'rate_knowledge',
                        'card_id': card_id,
                        'knowledge': 1,
                    },
                    'text': '🖕'
                },
                {
                    'callback_data': {
                        'command': 'rate_knowledge',
                        'card_id': card_id,
                        'knowledge': 2,
                    },
                    'text': '👍'
                }
            ],
            [
                {
                    'callback_data': {
                        'command': 'edit_card',
                        'card_id': card_id,
                    },
                    'text': 'Edit'
                }
            ]
        ]
    }


def learn_card_markup(card_id: Union[int, str], deck_id: Union[int, str]) -> dict:
    return {
        'inline_keyboard': [
            [
                {
                    'callback_data': {
                        'command': 'tip',
                        'card_id': card_id,
                    },
                    'text': 'Tip'
                },
                {
                    'callback_data': {
                        'command': 'deck_menu',
                        'deck_id': deck_id,
                    },
                    'text': 'Cancel'
                }
            ]
        ]
    }


def multiple_choice_answer_sheet_after_tip(
        card_id: Union[int, str], deck_id: Union[int, str],
        answers: Optional[List[str]] = None
) -> dict:
    keyboard = multiple_choice_answer_sheet(card_id, deck_id, answers)
    keyboard['inline_keyboard'].pop(-2)
    keyboard['inline_keyboard'].append(
        [

            {
                'callback_data': {
                    'command': 'show_answer',
                    'card_id': card_id,
                },
                'text': 'Show answer'
            }
        ]
    )
    return keyboard


def multiple_choice_answer_sheet(
        card_id: Union[int, str], deck_id: Union[int, str],
        answers: Optional[List[str]] = None
) -> dict:
    if not answers:
        answers = [random_string() for _ in range(4)]

    return {
        'inline_keyboard': [
            *[
                [
                    {
                        'callback_data': {
                            'command': 'pick_answer',
                            'option': i + 1,
                        },
                        'text': f'{i + 1}: {answer}',
                    }
                ]
                for i, answer in enumerate(answers)
            ],
            [
                {
                    'callback_data': {
                        'command': 'submit',
                        'card_id': card_id,
                    },
                    'text': 'Submit'
                }
            ],
            [
                {
                    'callback_data': {
                        'command': 'tip',
                        'card_id': card_id,
                    },
                    'text': 'Tip'
                }
            ],
            [
                {
                    'callback_data': {
                        'command': 'tip',
                        'deck_id': deck_id,
                    },
                    'text': 'Cancel'
                }
            ]
        ]
    }


def radiobutton_answer_sheet(card_id: Union[int, str],
                             deck_id: Union[int, str]) -> dict:
    return {
        'inline_keyboard': [
            [
                {
                    'callback_data': {
                        'command': 'radio_answer',
                        'card_id': card_id,
                        'mark': 'F'
                    },
                    'text': random_string()
                }
            ],
            [
                {
                    'callback_data': {
                        'command': 'radio_answer',
                        'card_id': card_id,
                        'mark': 'F'
                    },
                    'text': random_string()
                }
            ],
            [
                {
                    'callback_data': {
                        'command': 'radio_answer',
                        'card_id': card_id,
                        'mark': 'T'
                    },
                    'text': random_string()
                }
            ],
            [
                {
                    'callback_data': {
                        'command': 'tip',
                        'card_id': card_id,
                    },
                    'text': 'Tip'
                }
            ],
            [
                {
                    'callback_data': {
                        'command': 'deck_menu',
                        'deck_id': deck_id,
                    },
                    'text': 'Cancel'
                }
            ]
        ]
    }


def radiobutton_static_rows(card_id: Union[int, str], deck_id: Union[int, str]) -> list:
    return [
        [
            {
                'callback_data': {
                    'command': 'tip',
                    'card_id': card_id,
                },
                'text': 'Tip'
            }
        ],
        [
            {
                'callback_data': {
                    'command': 'deck_menu',
                    'deck_id': deck_id,
                },
                'text': 'Cancel'
            }
        ]
    ]


def multiple_choice_static_rows(card_id: Union[int, str],
                                deck_id: Union[int, str]) -> list:
    return radiobutton_static_rows(card_id, deck_id) + [
        [
            {
                'callback_data': {
                    'command': 'submit',
                    'card_id': card_id,
                },
                'text': 'Submit'
            }
        ]
    ]


def confirm_deck_deletion(deck_id: int) -> dict:
    return {
        'inline_keyboard': [
            [
                {
                    'callback_data': {
                        'command': 'sure_delete_deck',
                        'deck_id': deck_id,
                    },
                    'text': 'Delete'
                },
                {
                    'callback_data': {
                        'command': 'deck_menu',
                        'deck_id': deck_id,
                    },
                    'text': 'Cancel'
                }
            ]
        ]
    }
