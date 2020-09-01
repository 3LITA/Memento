import mock
import pytest
from flask_babel import gettext as _

from tests import conftest
from tests.test_bot import markups
from tests.testutils import setup, request_generator, utils, mocks
from tests.testutils.telebot_requests import Request, EDIT_MESSAGE, MARKDOWN

setup.setup_servers()


def test_add_card(deck_id, chat_id):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.add_card(deck_id),
        chat_id=chat_id,
    )
    with mock.patch.object(Deck, 'get', mocks.get_deck):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=_(
                'Choose type of a card that you want to add to "*{}*".\n\n'
                '0: a card with no answer, just some fact\n'
                '1: a question-answer card\n'
                '2: a card with gaps \\_ that you need to fill\n'
                '3: a card with multiple choice\n'
                '4: a card with only one correct answer.'
            ).format(f'deck{deck_id}'.upper()),
            parse_mode=MARKDOWN,
            reply_markup={
                'inline_keyboard': [
                    [
                        {
                            'callback_data': {
                                'command': 'card_type',
                                'deck_id': deck_id,
                                'card_type': i,
                            },
                            'text': str(i)
                        }
                        for i in range(5)
                    ],
                    [
                        {
                            'callback_data': {
                                'command': 'deck_menu',
                                'deck_id': deck_id,
                            },
                            'text': 'Back'
                        }
                    ]
                ]
            }
        )
    ]


@pytest.mark.parametrize(
    'deck_id,card_type',
    [(10 + i, i) for i in range(5)],
    ids=[f'type {i}' for i in range(5)]
)
def test_choose_card_type(deck_id, card_type, chat_id):
    from app.bot.keyboard import cd
    from app.bot.contexts import expectations, Context, ExpectedCommands
    from app.models import CardType
    from app.models.Deck import Deck
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.card_type(deck_id, card_type),
        chat_id=chat_id,
    )
    with mock.patch.object(Deck, 'get', mocks.get_deck):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    if card_type == 0:
        expected_reply = _('Send me the *fact*, that should be on this card.')
    else:
        expected_reply = _(
            'You chose card type *{}*.\n\n'
            'Send me a *question*, that should be on a card.'
        ).format(card_type)
        if card_type == 2:
            text = _('Remember that the question should contain gaps "*_*".')
            expected_reply = f"{expected_reply}\n\n{text}"
    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=expected_reply,
            parse_mode=MARKDOWN,
            reply_markup={
                'inline_keyboard': [
                    [
                        {
                            'callback_data': {
                                'command': 'add_card',
                                'deck_id': deck_id,
                            },
                            'text': 'Back'
                        }
                    ]
                ]
            }
        )
    ]

    utils.expectations_match(
        expectations.get(chat_id), Context(
            command=(
                ExpectedCommands.SEND_FACT
                if card_type == CardType.FACT
                else ExpectedCommands.SEND_QUESTION
            ),
            card_type=card_type,
            deck_id=deck_id,
        )
    )


def test_no_correct_answers(chat_id, deck_id, question_text):
    import app.bot.contexts
    from app.bot.keyboard import cd
    from app.models.Deck import Deck
    from app.models.User import User
    from app.models import CardType

    card_type = CardType.MULTIPLE_CHOICE
    app.bot.contexts.expectations = {
        chat_id: app.bot.contexts.Context(
            app.bot.contexts.ExpectedCommands.SEND_QUESTION,
            deck_id=deck_id,
            question=question_text,
            card_type=card_type,
        )
    }

    data = request_generator.generate_callback_query(
        callback_data=cd.no_correct_answers(),
        chat_id=chat_id,
    )

    with mock.patch.object(Deck, 'get', mocks.get_deck):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    text = _(
        'Send me comma-separated wrong answers to this question:\n\n{question}'
    ).format(question=question_text)
    expected_reply = f"{_('There are no correct answers.')}\n{text}"

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=expected_reply,
            reply_markup=markups.cancel_to_deck_menu(deck_id),
        )
    ]
    utils.expectations_match(
        app.bot.contexts.expectations.get(chat_id),
        app.bot.contexts.Context(
            app.bot.contexts.ExpectedCommands.SEND_WRONG_ANSWERS,
            deck_id=deck_id,
            question=question_text,
            correct_answers=[],
            card_type=card_type,
        )
    )


def test_no_wrong_answers(chat_id, deck_id, card_id, question_text, correct_answers):
    import app.bot.contexts
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models.Deck import Deck
    from app.models.User import User
    from app.models import CardType

    card_type = CardType.MULTIPLE_CHOICE

    app.bot.contexts.expectations = {
        chat_id: app.bot.contexts.Context(
            app.bot.contexts.ExpectedCommands.SEND_QUESTION,
            deck_id=deck_id,
            question=question_text,
            card_type=card_type,
            correct_answers=correct_answers,
        )
    }

    data = request_generator.generate_callback_query(
        chat_id=chat_id,
        first_name=utils.random_string(),
        last_name=utils.random_string(),
        username=utils.random_string(),
        text=utils.random_string(),
        callback_data=cd.no_wrong_answers(),
    )
    with mock.patch.object(Deck, 'get', mocks.get_deck):
        with mock.patch.object(Card, 'id', card_id):
            with mock.patch.object(
                    User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
            ):
                r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    expected_reply = _(
        "The card of type {type} was successfully created:\n\n"
        "{question}\n\n"
        "Correct: {correct_answers}\n\n"
        "Wrong: {wrong_answers}"
    ).format(
        type=card_type,
        question=question_text,
        correct_answers=correct_answers,
        wrong_answers=_("There are no wrong answers."),
    )
    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=expected_reply,
            reply_markup=markups.card_created_markup(card_id, deck_id)
        )
    ]
    assert not app.bot.contexts.expectations.get(chat_id)
