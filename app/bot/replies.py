from dataclasses import dataclass
from typing import Any, Optional

from app.i18n import gettext
from app.settings import BotCommands


MARKDOWN = 'Markdown'


@dataclass
class Reply:
    _text: str
    parse_mode: Optional[str] = None

    def __init__(self, text: str, parse_mode: Optional[str] = None) -> None:
        self._text = text
        self.parse_mode = parse_mode

    def text(self, *args: Any, **kwargs: Any) -> str:
        return gettext(self._text).format(*args, **kwargs)

    def format(self, *args: Any, **kwargs: Any) -> 'Reply':
        instance = Reply(self.text(*args, **kwargs), self.parse_mode)
        return instance

    def __str__(self) -> str:
        return self._text


START = Reply(
    text=(
        "Hi, *{first_name}*!\n"
        "I am gonna help you learn everything you've always wanted, "
        "no matter how hard it is!\n"
        "But first, you must sign up."
    ),
    parse_mode=MARKDOWN,
)

AFTER_SIGN_UP = Reply(
    text=(
        "Excellent, *{username}*!\n"
        "Since you have signed up, you can create new decks!"
    ),
    parse_mode=MARKDOWN,
)

START_AGAIN = Reply(text="Welcome back, *{username}*!", parse_mode=MARKDOWN)

SUPPORT = Reply(
    text=(
        "Okay, *{username}*, please describe your issue, "
        "it will be forwarded to our support assistant"
    ),
    parse_mode=MARKDOWN,
)

ISSUE_SENT = Reply(
    text=(
        "Fine, *{username}*, your issue was sent to the support assistant:\n\n"
        "{issue_text}"
    ),
    parse_mode=MARKDOWN,
)

HELP = Reply(text=f"{BotCommands.menu_commands[-1]} - use this command to navigate\n")

UNKNOWN_COMMAND = Reply(text="Sorry, I don't understand this command")

DECK_CREATED = Reply(
    text="Deck *{title}* was successfully created!", parse_mode=MARKDOWN
)

CARD_DELETED = Reply(text="The card was successfully deleted!")

CARD_ALREADY_DELETED = Reply(text="The card is already deleted")

DECK_DELETED = Reply(
    text="Deck *{deck_title}* was successfully deleted!", parse_mode=MARKDOWN
)

DECK_RENAMED = Reply(
    text="Deck *{previous_deck_title}* was renamed to *{new_deck_title}*.",
    parse_mode=MARKDOWN,
)

DECK_NOT_FOUND = Reply(text="Sorry, but I can't find this deck.\n")

CHOOSE_DECK = Reply(text="Your decks:")

RATE_KNOWLEDGE = Reply(text="Please, estimate your knowledge level:")

MAIN_MENU = Reply(text="It's a start menu.")

ADD_DECK = Reply(text="Do you want to create a new deck or add an existing one?")

CREATE_NEW_DECK = Reply(
    text="Send me a name to your deck.\n" "P.S. Remember that it should be unique."
)

TOO_LONG_DECK_TITLE = Reply(text="Deck title is too long. Try to make it shorter.")

INCORRECT_CHARACTERS_IN_DECK_TITLE = Reply(
    text=(
        "Deck title contains incorrect characters. Only latin letters, numbers "
        "and dash are allowed."
    ),
)

DECK_TITLE_ALREADY_EXISTS = Reply(
    text="Deck with title *{title}* already exists. Come up with another name.",
    parse_mode=MARKDOWN,
)

DECK_MENU = Reply(text="Deck *{title}*", parse_mode=MARKDOWN)

DECK_IS_EMPTY = Reply(text="Deck *{title}* is empty", parse_mode=MARKDOWN)

CHOOSE_CARD_TYPE = Reply(
    text=(
        'Choose type of a card that you want to add to "*{}*".\n\n'
        '0: a card with no answer, just some fact\n'
        '1: a question-answer card\n'
        '2: a card with gaps \\_ that you need to fill\n'
        '3: a card with multiple choice\n'
        '4: a card with only one correct answer.'
    ),
    parse_mode=MARKDOWN,
)

SEND_QUESTION = Reply(
    text='You chose card type *{}*.\n\nSend me a *question*, that should be on a card.',
    parse_mode=MARKDOWN,
)

NOTE_GAPS_FOR_TYPE_2 = Reply(
    text='\n\nRemember that the question should contain gaps "*_*".',
    parse_mode=MARKDOWN,
)

SEND_FACT = Reply(
    text='Send me the *fact*, that should be on this card.', parse_mode=MARKDOWN
)

FACT_CREATED = Reply(text='Your new card:\n\n' '{fact}')

SEND_EXACT_NUMBER_CORRECT_ANSWERS = Reply(
    text=(
        'Send me {number} comma-separated correct answers to this question:\n\n'
        '{question}'
    )
)

SEND_CORRECT_ANSWERS = Reply(
    text='Send me comma-separated correct answers to this question:\n\n{question}',
)

SEND_WRONG_ANSWERS = Reply(
    text='Send me comma-separated wrong answers to this question:\n\n{question}',
)

SEND_CORRECT_ANSWER = Reply(
    text='Send me the correct answer to this question:\n\n{question}',
)

THERE_ARE_NO_CORRECT_ANSWERS = Reply(text="There are no correct answers.")

THERE_ARE_NO_WRONG_ANSWERS = Reply(text="There are no wrong answers.")

INADEQUATE_CORRECT_ANSWER_SENT = Reply(
    text=(
        'You are confusing me!\n\n'
        'Send me the correct answer to this question:\n\n'
        '{question}'
    ),
)

INADEQUATE_CORRECT_ANSWERS_SENT = Reply(
    text=(
        'You are confusing me!\n\n'
        'Send me comma-separated correct answers to this question:\n\n'
        '{question}'
    ),
)

INADEQUATE_WRONG_ANSWERS_SENT = Reply(
    text=(
        'You are confusing me!\n\n'
        'Send me comma-separated wrong answers to this question:\n\n'
        '{question}'
    ),
)

EDIT_CARD = Reply(
    text='What do you want to change in this card?\n\n{question}\n\n{answers}',
)

EDIT_FACT = Reply(text="Do you want to change in this fact?\n\n{question}")

EDIT_DECK = Reply(
    text="What do you want to change in the deck *{deck_title}*?", parse_mode=MARKDOWN
)

RENAME_DECK = Reply(
    text='Send me the name to the deck *{deck_title}*.', parse_mode=MARKDOWN
)

DELETE_DECK = Reply(
    text='Are you sure you want to delete deck *{title}*?', parse_mode=MARKDOWN
)

CORRECT_ANSWER_IS = Reply(text='Correct answer: ')

CORRECT_ANSWERS_ARE = Reply(text='Correct answers: ')

WRONG_ANSWERS_ARE = Reply(text='Wrong answers: ')

USER_CHOSEN = Reply(text='Your choice:')

CORRECT_REPLIES = [
    Reply(text='Correct!'),
    Reply(text='Absolutely correct!'),
    Reply(text='Perfect!'),
    Reply(text='Well done!'),
    Reply(text='Excellent!'),
]

WRONG_REPLIES = [
    Reply(text='Wrong!'),
    Reply(text='Bad news, wrong!'),
    Reply(text='Sorry, incorrect!'),
]

QUESTION_TOO_LONG = Reply(text="Your question is too long.\nTry to make it shorter.")

CARD_CREATED = Reply(
    text=(
        "The card of type {type} was successfully created:\n\n"
        "{question}\n\n"
        "Correct answers: {correct_answers}"
    ),
)

CARD_WITH_CHOICE_CREATED = Reply(
    text=(
        "The card of type {type} was successfully created:\n\n"
        "{question}\n\n"
        "Correct: {correct_answers}\n\n"
        "Wrong: {wrong_answers}"
    ),
)

NO_GAPS_IN_TYPE_2 = Reply(
    text='Sorry, but a card of type *2* should contain gaps "*_*"',
)

INCORRECT_GAPS_NUMBER_IN_ANSWER = Reply(
    text="Sorry, but I need {expected} answers, whereas you gave me {actual}.",
)

CHANGE_LANGUAGE = Reply(text="Choose the language you want to set")

LANGUAGE_WAS_CHANGED = Reply(text="The language was successfully changed!")

TIP = Reply(text="Tip: ")

NO_TIPS = Reply(
    text=(
        "Unfortunately, there are no tips for this question...\n"
        "I can show you the answer though"
    ),
)

CONTEXT_FORGOTTEN = Reply(
    text="Unfortunately, the context of our dialogue is already forgotten...",
)

WTF_MESSAGES = [
    Reply(text="What do you mean?"),
    Reply(text="Please type /help and get the available commands"),
    Reply(text="Sorry, I can't understand"),
    Reply(text="Sorry, but I can't reply...\nBut I can help you learn something!"),
]
