from copy import copy

import mock
import pytest
from flask_babel import gettext as _

from tests import conftest
from tests.test_bot import markups
from tests.testutils import request_generator, setup, mocks, utils
from tests.testutils.telebot_requests import (
    Request, SEND_MESSAGE, DELETE_MESSAGE, MARKDOWN
)

setup.setup_servers()

CORRECT_REPLIES = (
    _('Correct!'),
    _('Absolutely correct!'),
    _('Perfect!'),
    _('Well done!'),
    _('Excellent!'),
)
WRONG_REPLIES = (
    _('Wrong!'),
    _('Bad news, wrong!'),
    _('Sorry, incorrect!'),
)


@pytest.mark.parametrize('card_type', (1, 2), ids=("Simple", "With Gaps"))
def test_answer_correct(
        chat_id, card_id, correct_answers, question_text, question_with_gaps, card_type
):
    import app.bot.contexts
    from app.models import CardType
    from app.models.Card import Card
    from app.models.User import User

    correct_answers = [ans.lower() for ans in correct_answers]

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.LEARN,
        card_id=card_id,
    )
    app.bot.contexts.expectations = {
        chat_id: copy(expectations)
    }

    answer, text = (
        (correct_answers[0].upper(), question_text)
        if card_type == CardType.SIMPLE
        else (', '.join([ans.title() for ans in correct_answers]), question_with_gaps)
    )

    data = request_generator.generate_message(
        text=answer,
        chat_id=chat_id,
    )

    with mock.patch.object(User, 'get_by', mocks.get_user_by(by_chat_id=True)):
        with mock.patch.object(
                Card, 'get', mocks.get_card(
                    question=text,
                    card_type=card_type,
                    correct_answers=correct_answers,
                )
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue[1] == Request(DELETE_MESSAGE, chat_id=chat_id)

    send_request: Request = queue[0]
    assert send_request.action == SEND_MESSAGE
    assert send_request.chat_id == chat_id
    assert send_request.text in [
        f"{reply}\n\n{_('Please, estimate your knowledge level:')}"
        for reply in CORRECT_REPLIES
    ]
    assert not send_request.parse_mode
    assert send_request.reply_markup == markups.rate_knowledge_markup(card_id)

    assert utils.expectations_match(
        app.bot.contexts.expectations.get(chat_id), expectations
    )


@pytest.mark.parametrize('card_type', (1, 2), ids=("Simple", "With Gaps"))
def test_answer_wrong(
        chat_id,
        card_id,
        deck_id,
        correct_answers,
        question_text,
        question_with_gaps,
        card_type,
):
    import app.bot.contexts
    from app.models import CardType
    from app.models.Card import Card
    from app.models.User import User

    correct_answers = [ans.lower() for ans in correct_answers]

    expectations = app.bot.contexts.Context(
        app.bot.contexts.ExpectedCommands.LEARN,
        card_id=card_id,
    )
    app.bot.contexts.expectations = {
        chat_id: copy(expectations)
    }

    answer, question = (
        (utils.random_string(), question_text)
        if card_type == CardType.SIMPLE
        else (
            ', '.join(utils.random_string() for i in range(len(correct_answers))),
            question_with_gaps
        )
    )

    data = request_generator.generate_message(
        text=answer,
        chat_id=chat_id,
    )

    with mock.patch.object(User, 'get_by', mocks.get_user_by(by_chat_id=True)):
        with mock.patch.object(
                Card, 'get', mocks.get_card(
                    card_type=card_type,
                    question=question,
                    correct_answers=correct_answers,
                    deck_id=deck_id,
                ),
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue[1] == Request(DELETE_MESSAGE, chat_id=chat_id)

    send_request: Request = queue[0]
    assert send_request.action == SEND_MESSAGE
    assert send_request.chat_id == chat_id
    assert send_request.text in [
        f"{reply}\n\n{question}"
        for reply in WRONG_REPLIES
    ]
    assert not send_request.parse_mode
    assert send_request.reply_markup == markups.learn_card_markup(card_id, deck_id)

    assert utils.expectations_match(
        app.bot.contexts.expectations.get(chat_id), expectations
    )
