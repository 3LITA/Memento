import json
import re
from copy import copy

import mock
import pytest
from flask_babel import _

from tests import conftest
from tests.test_bot import markups
from tests.testutils import request_generator, setup, mocks, utils

setup.setup_servers()


@pytest.mark.parametrize(
    'deck_title',
    [
        'correct-deck-title',
        'incorrect*title',
        'incorrect_title',
        utils.random_string(128),
    ],
    ids=[
        'correct title',
        'incorrect characters',
        'incorrect characters 2',
        'too long deck title',
    ]
)
def test_create_deck(chat_id, question_text, deck_title):
    import app.bot.contexts
    from app.models.Deck import Deck

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.CREATE_NEW_DECK
    )
    app.bot.contexts.expectations = {
        chat_id: copy(expectations)
    }

    expected_markup = markups.creating_deck_markup()

    if len(deck_title) > 127:
        expected_reply = _("Deck title is too long. Try to make it shorter.")
    elif not re.compile(r'^[A-Za-z0-9-]*$').search(deck_title):
        expected_reply = _(
            "Deck title contains incorrect characters. Only latin letters, numbers "
            "and dash are allowed."
        )
    else:
        expectations = None
        expected_reply = _("Deck *{title}* was successfully created!").format(
            title=deck_title.upper()
        )
        expected_markup = markups.main_menu_with_decks()

    data = request_generator.generate_message(
        text=deck_title,
        chat_id=chat_id,
    )

    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    assert req['text'][0] == expected_reply
    utils.expectations_match(app.bot.contexts.expectations.get(chat_id), expectations)

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_create_deck_with_non_unique_title(chat_id, deck_id, question_text):
    import app.bot.contexts
    from app.models.Deck import Deck

    deck_title = 'NotUniqueDeckTitle'

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.CREATE_NEW_DECK)
    expected_markup = markups.creating_deck_markup()

    app.bot.contexts.expectations = {chat_id: copy(expectations)}

    data = request_generator.generate_message(
        text=deck_title,
        chat_id=chat_id,
    )

    existing_deck = mocks.deck_get_by_id(deck_id, deck_title)
    with mock.patch.object(
            Deck, 'search_by_title', lambda user, title: existing_deck
    ):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    assert req['text'][0] == _(
        "Deck with title *{title}* already exists. Come up with another name."
    ).format(title=deck_title.upper())
    utils.expectations_match(app.bot.contexts.expectations.get(chat_id), expectations)

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


@pytest.mark.parametrize(
    'deck_title',
    [
        'correct-deck-title',
        'incorrect*title',
        'incorrect_title',
        utils.random_string(128),
    ],
    ids=[
        'correct title',
        'incorrect characters',
        'incorrect characters 2',
        'too long deck title',
    ]
)
def test_rename_deck(chat_id, deck_id, question_text, deck_title):
    import app.bot.contexts
    from app.models.Deck import Deck

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.RENAME_USER_DECK,
        deck_id=deck_id,
    )
    app.bot.contexts.expectations = {
        chat_id: copy(expectations)
    }

    expected_markup = markups.cancel_to_deck_menu(deck_id)
    if len(deck_title) > 127:
        expected_reply = _("Deck title is too long. Try to make it shorter.")
    elif not re.compile(r'^[A-Za-z0-9-]*$').search(deck_title):
        expected_reply = _(
            "Deck title contains incorrect characters. Only latin letters, numbers "
            "and dash are allowed."
        )
    else:
        expectations = None
        expected_reply = _(
            "Deck *{previous_deck_title}* was renamed to *{new_deck_title}*."
        ).format(
            previous_deck_title=f"deck{deck_id}".upper(),
            new_deck_title=deck_title.upper()
        )
        expected_markup = markups.deck_menu_without_cards(deck_id)

    data = request_generator.generate_message(
        text=deck_title,
        chat_id=chat_id,
    )

    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    assert req['text'][0] == expected_reply
    utils.expectations_match(app.bot.contexts.expectations.get(chat_id), expectations)

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_rename_deck_with_non_unique_title(chat_id, deck_id, question_text):
    import app.bot.contexts
    from app.models.Deck import Deck

    deck_title = 'NotUniqueDeckTitle'
    old_title = 'OldTitle'

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.RENAME_USER_DECK,
        deck_id=deck_id,
    )
    app.bot.contexts.expectations = {chat_id: copy(expectations)}

    data = request_generator.generate_message(
        text=deck_title,
        chat_id=chat_id,
    )

    existing_deck = mocks.deck_get_by_id(deck_id + 1, deck_title)
    deck_to_rename = mocks.deck_get_by_id(deck_id, old_title)
    with mock.patch.object(
            Deck, 'search_by_title', lambda user, title: existing_deck
    ):
        with mock.patch.object(Deck, 'get', lambda *args: deck_to_rename):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    assert req['text'][0] == _(
        "Deck with title *{title}* already exists. Come up with another name."
    ).format(title=deck_title.upper())
    utils.expectations_match(app.bot.contexts.expectations.get(chat_id), expectations)

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == markups.cancel_to_deck_menu(deck_id)


@pytest.mark.parametrize(
    'fact',
    (f"{utils.random_string()}?", f"{utils.random_string(255)}?"),
    ids=('OK', 'Too long question'),
)
def test_send_fact(deck_id, chat_id, fact, card_id):
    import app.bot.contexts
    from app.models.Card import Card
    from app.models.Deck import Deck
    from app.models import CardType

    card_type = CardType.FACT

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.SEND_FACT,
        deck_id=deck_id,
        card_type=card_type,
    )
    app.bot.contexts.expectations = {chat_id: copy(expectations)}

    if len(fact) > 255:
        expected_reply = _("Your question is too long.\n" "Try to make it shorter.")
        expected_markup = markups.cancel_to_deck_menu(deck_id)
    else:
        expectations = None
        expected_reply = _('Your new card:\n\n' '{fact}').format(fact=fact)
        expected_markup = markups.card_created_markup(card_id, deck_id)

    data = request_generator.generate_message(
        text=fact,
        chat_id=chat_id,
    )

    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        with mock.patch.object(Card, 'id', card_id):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    assert req['text'][0] == expected_reply
    utils.expectations_match(app.bot.contexts.expectations.get(chat_id), expectations)

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_send_too_long_question(deck_id, chat_id):
    import app.bot.contexts
    from app.models.Deck import Deck
    from app.models import CardType

    card_type = CardType.SIMPLE
    question = utils.random_string(256)

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.SEND_QUESTION,
        deck_id=deck_id,
        card_type=card_type,
    )

    app.bot.contexts.expectations = {
        chat_id: copy(expectations)
    }

    data = request_generator.generate_message(
        text=question,
        chat_id=chat_id,
    )

    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    assert req['text'][0] == _("Your question is too long.\nTry to make it shorter.")
    utils.expectations_match(
        app.bot.contexts.expectations.get(chat_id),
        app.bot.contexts.Context(
            app.bot.contexts.ExpectedCommands.SEND_QUESTION,
            deck_id=deck_id,
            card_type=card_type,
        )
    )

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == markups.cancel_to_deck_menu(deck_id)


@pytest.mark.parametrize(
    'card_type',
    [i for i in range(1, 5)],
    ids=('Simple', 'With gaps', 'Multiple choice', 'RadioButton')
)
def test_send_question(deck_id, chat_id, question_text, card_type):
    import app.bot.contexts
    from app.models.Deck import Deck
    from app.models import CardType

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.SEND_QUESTION,
        deck_id=deck_id,
        card_type=card_type,
    )
    app.bot.contexts.expectations = {chat_id: copy(expectations)}

    expected_markup = markups.cancel_to_deck_menu(deck_id)
    if card_type == CardType.GAPS:
        expected_reply = _('Sorry, but a card of type *2* should contain gaps "*_*"')
    else:
        command = (
            app.bot.contexts.ExpectedCommands.SEND_CORRECT_ANSWERS_ONLY
            if card_type == CardType.SIMPLE
            else app.bot.contexts.ExpectedCommands.SEND_CORRECT_ANSWERS
        )

        expectations = app.bot.contexts.Context(
            command,
            deck_id=deck_id,
            card_type=card_type,
            question=question_text,
        )
        if card_type == CardType.RADIOBUTTON:
            expected_reply = _(
                'Send me the correct answer to this question:\n\n{question}'
            ).format(question=question_text)
        else:
            expected_reply = _(
                'Send me comma-separated correct answers to this question:\n\n'
                '{question}'
            ).format(question=question_text)
            if card_type == CardType.MULTIPLE_CHOICE:
                expected_markup['inline_keyboard'].insert(0, [
                    {
                        'callback_data': {'command': 'no_correct_answers'},
                        'text': 'No correct answers'
                    }
                ])

    data = request_generator.generate_message(
        text=question_text,
        chat_id=chat_id,
    )

    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    assert req['text'][0] == expected_reply
    utils.expectations_match(app.bot.contexts.expectations.get(chat_id), expectations)

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_send_question_with_gaps(deck_id, chat_id, question_with_gaps):
    import app.bot.contexts
    from app.models.Deck import Deck
    from app.models import CardType

    card_type = CardType.GAPS

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.SEND_QUESTION,
        deck_id=deck_id,
        card_type=card_type,
    )

    app.bot.contexts.expectations = {
        chat_id: copy(expectations)
    }

    data = request_generator.generate_message(
        text=question_with_gaps,
        chat_id=chat_id,
    )

    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    gaps_number = len(question_with_gaps.split('_')) - 1

    assert req['text'][0] == _(
        'Send me {number} comma-separated correct answers to this question:\n\n'
        '{question}'
    ).format(number=gaps_number, question=question_with_gaps)

    expectations.command = app.bot.contexts.ExpectedCommands.SEND_CORRECT_ANSWERS_ONLY
    expectations.question = question_with_gaps
    expectations.gaps = gaps_number
    utils.expectations_match(app.bot.contexts.expectations.get(chat_id), expectations)

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == markups.cancel_to_deck_menu(deck_id)


def test_send_wrong_gaps_number(deck_id, chat_id, question_with_gaps):
    import app.bot.contexts
    from app.models.Deck import Deck
    from app.models import CardType

    gaps_number = len(question_with_gaps.split('_')) - 1

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.SEND_CORRECT_ANSWERS_ONLY,
        deck_id=deck_id,
        card_type=CardType.GAPS,
        question=question_with_gaps,
        gaps=gaps_number,
    )
    app.bot.contexts.expectations = {chat_id: copy(expectations)}

    expected_markup = markups.cancel_to_deck_menu(deck_id)

    data = request_generator.generate_message(
        text=', '.join([utils.random_string() for i in range(gaps_number + 1)]),
        chat_id=chat_id,
    )

    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    assert req['text'][0] == _(
        "Sorry, but I need {expected} answers, whereas you gave me {actual}."
    ).format(expected=gaps_number, actual=gaps_number + 1)
    utils.expectations_match(app.bot.contexts.expectations.get(chat_id), expectations)

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


@pytest.mark.parametrize(
    'card_type', (1, 3, 4), ids=("Simple", "Multiple Choice", "RadioButton")
)
def test_send_correct_answers_none(deck_id, chat_id, question_text, card_type):
    import app.bot.contexts
    from app.models.Deck import Deck
    from app.models import CardType

    command = (
        app.bot.contexts.ExpectedCommands.SEND_CORRECT_ANSWERS_ONLY
        if card_type == CardType.SIMPLE
        else app.bot.contexts.ExpectedCommands.SEND_CORRECT_ANSWERS
    )
    if card_type == CardType.RADIOBUTTON:
        expected_reply = _(
            'You are confusing me!\n\n'
            'Send me the correct answer to this question:\n\n'
            '{question}'
        ).format(question=question_text)
    else:
        expected_reply = _(
            'You are confusing me!\n\n'
            'Send me comma-separated correct answers to this question:\n\n'
            '{question}'
        ).format(question=question_text)

    expectations = app.bot.contexts.Context(
        command,
        deck_id=deck_id,
        card_type=card_type,
        question=question_text,
    )
    app.bot.contexts.expectations = {chat_id: copy(expectations)}

    expected_markup = markups.cancel_to_deck_menu(deck_id)

    data = request_generator.generate_message(
        text=',',
        chat_id=chat_id,
    )

    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    assert req['text'][0] == expected_reply
    utils.expectations_match(app.bot.contexts.expectations.get(chat_id), expectations)

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_radio_send_many_correct_answers(
        deck_id, chat_id, question_text, correct_answers
):
    import app.bot.contexts
    from app.models.Deck import Deck
    from app.models import CardType

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.SEND_CORRECT_ANSWERS,
        deck_id=deck_id,
        card_type=CardType.RADIOBUTTON,
        question=question_text,
    )
    app.bot.contexts.expectations = {chat_id: copy(expectations)}

    expected_markup = markups.cancel_to_deck_menu(deck_id)

    data = request_generator.generate_message(
        text=', '.join(correct_answers),
        chat_id=chat_id,
    )

    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    assert req['text'][0] == _(
        'You are confusing me!\n\n'
        'Send me the correct answer to this question:\n\n'
        '{question}'
    ).format(question=question_text)
    utils.expectations_match(app.bot.contexts.expectations.get(chat_id), expectations)

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


@pytest.mark.parametrize(
    'card_type', (1, 3, 4), ids=("Simple", "Multiple Choice", "RadioButton")
)
def test_send_correct_answers(
        deck_id, card_id, chat_id, question_text, correct_answers, card_type
):
    import app.bot.contexts
    from app.models.Card import Card
    from app.models.Deck import Deck
    from app.models import CardType

    command = (
        app.bot.contexts.ExpectedCommands.SEND_CORRECT_ANSWERS_ONLY
        if card_type == CardType.SIMPLE
        else app.bot.contexts.ExpectedCommands.SEND_CORRECT_ANSWERS
    )

    expectations = app.bot.contexts.Context(
        command,
        deck_id=deck_id,
        card_type=card_type,
        question=question_text,
    )
    app.bot.contexts.expectations = {chat_id: copy(expectations)}

    if card_type == CardType.SIMPLE:
        expectations = None
        expected_markup = markups.card_created_markup(card_id, deck_id)
        expected_reply = _(
            "The card of type {type} was successfully created:\n\n"
            "{question}\n\n"
            "Correct answers: {correct_answers}"
        ).format(
            type=card_type,
            question=question_text,
            correct_answers=', '.join([ans.lower() for ans in correct_answers])
        )
    else:
        expected_reply = _(
            'Send me comma-separated wrong answers to this question:\n\n' '{question}'
        ).format(question=question_text)
        expected_markup = markups.cancel_to_deck_menu(deck_id)
        if card_type == CardType.MULTIPLE_CHOICE:
            expected_markup['inline_keyboard'].insert(
                0, [
                    {
                        'callback_data': {'command': 'no_wrong_answers'},
                        'text': 'No wrong answers'
                    }
                ]
            )
        else:
            correct_answers = correct_answers[:1]
        expectations.correct_answers = [ans.lower() for ans in correct_answers]
        expectations.command = app.bot.contexts.ExpectedCommands.SEND_WRONG_ANSWERS

    data = request_generator.generate_message(
        text=', '.join(correct_answers),
        chat_id=chat_id,
    )

    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        with mock.patch.object(Card, 'id', card_id):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    assert req['text'][0] == expected_reply
    utils.expectations_match(app.bot.contexts.expectations.get(chat_id), expectations)

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


def test_send_correct_answers_gaps(
        deck_id, card_id, chat_id, question_with_gaps
):
    import app.bot.contexts
    from app.models.Card import Card
    from app.models.Deck import Deck
    from app.models import CardType

    gaps_number = len(question_with_gaps.split('_')) - 1
    correct_answers = [utils.random_string() for i in range(gaps_number)]

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.SEND_CORRECT_ANSWERS_ONLY,
        deck_id=deck_id,
        card_type=CardType.GAPS,
        question=question_with_gaps,
        gaps=gaps_number,
    )
    app.bot.contexts.expectations = {chat_id: copy(expectations)}

    expected_markup = markups.card_created_markup(card_id, deck_id)
    expected_reply = _(
        "The card of type {type} was successfully created:\n\n"
        "{question}\n\n"
        "Correct answers: {correct_answers}"
    ).format(
        type=CardType.GAPS,
        question=question_with_gaps,
        correct_answers=', '.join([ans.lower() for ans in correct_answers])
    )

    data = request_generator.generate_message(
        text=', '.join(correct_answers),
        chat_id=chat_id,
    )

    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        with mock.patch.object(Card, 'id', card_id):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    assert req['text'][0] == expected_reply
    assert not app.bot.contexts.expectations.get(chat_id)

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


@pytest.mark.parametrize('card_type', (3, 4), ids=("Multiple Choice", "RadioButton"))
def test_send_wrong_answers_none(card_id, deck_id, chat_id, question_text, card_type):
    import app.bot.contexts
    from app.models.Deck import Deck

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.SEND_WRONG_ANSWERS,
        deck_id=deck_id,
        card_type=card_type,
        question=question_text,
        correct_answers=[utils.random_string().lower()],
    )
    app.bot.contexts.expectations = {chat_id: copy(expectations)}

    expected_markup = markups.cancel_to_deck_menu(deck_id)

    data = request_generator.generate_message(
        text=',',
        chat_id=chat_id,
    )

    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    assert req['text'][0] == _(
        'You are confusing me!\n\n'
        'Send me comma-separated wrong answers to this question:\n\n'
        '{question}'
    ).format(question=question_text)
    utils.expectations_match(app.bot.contexts.expectations.get(chat_id), expectations)

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == expected_markup


@pytest.mark.parametrize('card_type', (3, 4), ids=("Multiple Choice", "RadioButton"))
def test_send_wrong_answers(
        card_id, deck_id, chat_id, question_text, wrong_answers, card_type
):
    import app.bot.contexts
    from app.models.Card import Card
    from app.models.Deck import Deck

    correct_answers = [utils.random_string().lower()]

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.SEND_WRONG_ANSWERS,
        deck_id=deck_id,
        card_type=card_type,
        question=question_text,
        correct_answers=correct_answers,
    )
    app.bot.contexts.expectations = {chat_id: copy(expectations)}

    data = request_generator.generate_message(
        text=','.join(wrong_answers),
        chat_id=chat_id,
    )

    with mock.patch.object(Deck, 'get', mocks.deck_get_by_id):
        with mock.patch.object(Card, 'id', card_id):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200
    assert len(queue) > 0

    req = queue[-1]

    assert req['text'][0] == _(
        "The card of type {type} was successfully created:\n\n"
        "{question}\n\n"
        "Correct: {correct_answers}\n\n"
        "Wrong: {wrong_answers}"
    ).format(
        type=card_type,
        question=question_text,
        correct_answers=', '.join([ans.lower() for ans in correct_answers]),
        wrong_answers=', '.join([ans.lower() for ans in wrong_answers]),
    )
    assert not app.bot.contexts.expectations.get(chat_id)

    actual_markup = json.loads(req['reply_markup'][0])

    assert actual_markup == markups.card_created_markup(card_id, deck_id)
