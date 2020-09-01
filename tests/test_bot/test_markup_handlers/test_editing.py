from typing import List

import mock
import pytest
from flask_babel import gettext as _

from tests import conftest
from tests.test_bot import markups
from tests.testutils import setup, request_generator, utils, mocks
from tests.testutils.telebot_requests import EDIT_MESSAGE, MARKDOWN, Request

setup.setup_servers()


def test_edit_fact(question_text, card_id, deck_id, chat_id):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models.User import User
    from app.models import CardType

    data = request_generator.generate_callback_query(
        callback_data=cd.edit_card(card_id),
        chat_id=chat_id,
    )
    with mock.patch.object(
            Card, 'get', mocks.get_card(
                card_type=CardType.FACT, question=question_text, deck_id=deck_id
            )
    ):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    expected_reply = _("Do you want to change in this fact?\n\n{question}").format(
        question=question_text)
    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=expected_reply,
            reply_markup=markups.edit_fact_markup(card_id, deck_id),
        )
    ]


@pytest.mark.parametrize(
    "card_type",
    [i for i in range(1, 5)],
    ids=("SIMPLE", "WITH_GAPS", "MULTICHOICE", "RADIOBUTTON"),
)
def test_edit_card(
        card_id: int,
        deck_id: int,
        question_text: str,
        question_with_gaps: str,
        correct_answers: List[str],
        card_type: int,
        chat_id: int,
):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models.User import User
    from app.models import CardType

    question = question_with_gaps if card_type == CardType.GAPS else question_text

    data = request_generator.generate_callback_query(
        callback_data=cd.edit_card(card_id),
        chat_id=chat_id,
    )
    with mock.patch.object(
            Card, 'get', mocks.get_card(
                card_type=card_type,
                question=question,
                correct_answers=correct_answers,
                deck_id=deck_id)
    ):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    answers = f"{_('Correct answers: ')}{', '.join(correct_answers)}"
    if card_type in (CardType.MULTIPLE_CHOICE, CardType.RADIOBUTTON):
        answers = f"{answers}\n\n{_('No wrong answers')}"

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=_(
                'What do you want to change in this card?\n\n{question}\n\n{answers}'
            ).format(question=question, answers=answers),
            reply_markup=(
                markups.edit_complex_card_markup(card_id, deck_id)
                if card_type in (CardType.MULTIPLE_CHOICE, CardType.RADIOBUTTON)
                else markups.edit_simple_card_markup(card_id, deck_id)
            ),
        )
    ]


@pytest.mark.parametrize('card_type', (3, 4), ids=("MULTICHOICE", "RADIOBUTTON"))
def test_edit_card_with_wrong_answers(
        card_type,
        card_id,
        question_text,
        correct_answers,
        wrong_answers,
        deck_id,
        chat_id,
):
    from app.bot.keyboard import cd
    from app.models import CardType
    from app.models.Card import Card
    from app.models.User import User

    if card_type == CardType.RADIOBUTTON:
        correct_answers = correct_answers[:1]

    data = request_generator.generate_callback_query(
        callback_data=cd.edit_card(card_id),
        chat_id=chat_id,
    )
    with mock.patch.object(
            Card, 'get', mocks.get_card(
                card_type=card_type,
                question=question_text,
                correct_answers=correct_answers,
                wrong_answers=wrong_answers,
                deck_id=deck_id,
            )
    ):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    answers = f"{_('Correct answers: ')}{', '.join(correct_answers)}"
    answers = f"{answers}\n\n{_('Wrong answers: ')}{', '.join(wrong_answers)}"

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=_(
                'What do you want to change in this card?\n\n{question}\n\n{answers}'
            ).format(question=question_text, answers=answers),
            reply_markup=markups.edit_complex_card_markup(card_id, deck_id),
        )
    ]


def test_edit_multiple_choice_card_with_no_correct_answers(
        chat_id, card_id, deck_id, question_text, wrong_answers
):
    from app.bot.keyboard import cd
    from app.models import CardType
    from app.models.Card import Card
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.edit_card(card_id),
        chat_id=chat_id,
    )
    with mock.patch.object(
            Card, 'get', mocks.get_card(
                card_type=CardType.MULTIPLE_CHOICE,
                question=question_text,
                wrong_answers=wrong_answers,
                deck_id=deck_id,
            )
    ):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    answers = (
        f"{_('No correct answers')}\n\n{_('Wrong answers: ')}{', '.join(wrong_answers)}"
    )

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=(
                "What do you want to change in this card?\n\n{question}\n\n"
                "{answers}".format(question=question_text, answers=answers)
            ),
            reply_markup=markups.edit_complex_card_markup(card_id, deck_id),
        )
    ]


def test_rename_deck(deck_id, chat_id):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck
    from app.models.User import User
    from app.bot.contexts import expectations, Context, ExpectedCommands

    data = request_generator.generate_callback_query(
        callback_data=cd.rename_deck(deck_id),
        chat_id=chat_id,
    )
    with mock.patch.object(Deck, 'get', mocks.get_deck):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    utils.expectations_match(expectations[chat_id], Context(
        ExpectedCommands.RENAME_USER_DECK,
        deck_id=deck_id
    ))

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=_('Send me the name to the deck *{deck_title}*.').format(
                deck_title=f'deck{deck_id}'.upper()
            ),
            parse_mode=MARKDOWN,
            reply_markup=markups.cancel_to_deck_menu(deck_id),
        )
    ]


def test_delete_deck(chat_id, deck_id):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.delete_deck(deck_id),
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
            text=_('Are you sure you want to delete deck *{title}*?').format(
                title=f'deck{deck_id}'.upper()
            ),
            parse_mode=MARKDOWN,
            reply_markup=markups.confirm_deck_deletion(deck_id),
        )
    ]


def test_confirm_deck_deletion(chat_id, deck_id):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.sure_delete_deck(deck_id),
        chat_id=chat_id,
    )
    with mock.patch.object(Deck, 'get', mocks.get_deck):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=False)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=_("Deck *{deck_title}* was successfully deleted!").format(
                deck_title=f'deck{deck_id}'.upper()
            ),
            reply_markup=markups.main_menu_without_decks(),
            parse_mode=MARKDOWN,
        )
    ]


def test_confirm_deck_deletion_not_found(chat_id, deck_id):
    from app.bot.keyboard import cd
    from app.models.Deck import Deck
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.sure_delete_deck(deck_id),
        chat_id=chat_id,
    )
    with mock.patch.object(Deck, 'get', mocks.raise_attribute_error):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=False)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=_("Sorry, but I can't find this deck.\n"),
            reply_markup=markups.main_menu_without_decks(),
        )
    ]


def test_delete_card(chat_id, card_id, question_text, deck_id, correct_answers):
    from app.bot.keyboard import cd
    from app.models import CardType
    from app.models.Card import Card
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.delete_card(card_id),
        chat_id=chat_id,
    )
    with mock.patch.object(
            Card, 'get', mocks.get_card(
                card_type=CardType.SIMPLE,
                question=question_text,
                correct_answers=correct_answers,
                deck_id=deck_id,
            )
    ):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=(
                f"{_('The card was successfully deleted!')}\n\n"
                f"{_('Deck *{title}*').format(title=f'deck{deck_id}'.upper())}"
            ),
            parse_mode=MARKDOWN,
            reply_markup=markups.deck_menu_having_cards(deck_id),
        )
    ]


def test_delete_card_not_found(
        chat_id, card_id, question_text, deck_id, correct_answers
):
    from app.bot.keyboard import cd
    from app.models.Card import Card
    from app.models.User import User

    data = request_generator.generate_callback_query(
        callback_data=cd.delete_card(card_id),
        chat_id=chat_id,
    )
    with mock.patch.object(Card, 'get', mocks.raise_attribute_error):
        with mock.patch.object(
                User, 'get_by', mocks.get_user_by(by_chat_id=True, has_decks=True)
        ):
            r, queue = utils.post(conftest.BOT_SECRET_URL, json=data)

    assert r.status_code == 200

    assert queue == [
        Request(
            EDIT_MESSAGE,
            chat_id=chat_id,
            text=f"{_('The card is already deleted')}",
            reply_markup=markups.main_menu_with_decks(),
        )
    ]
