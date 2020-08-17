from dataclasses import dataclass
from typing import Any, Optional

from flask_babel import _

from app.settings import BotCommands


MARKDOWN = 'Markdown'


@dataclass
class Reply:
    text: str
    parse_mode: Optional[str] = None

    def format(self, *args: Any, **kwargs: Any) -> 'Reply':
        instance = Reply(self.text.format(*args, **kwargs), self.parse_mode)
        return instance

    def __str__(self) -> str:
        return self.text


START = Reply(
    text=_(
        "Hi, *{}*!\n"
        "I am gonna help you learn everything you've always wanted,\n"
        "no matter how hard it is!"
    ),
    parse_mode=MARKDOWN,
)

START_AGAIN = Reply(text=_("Welcome back, *{}*!"), parse_mode=MARKDOWN,)

HELP = Reply(
    text=_(
        "%(menu_command)s - use this command to navigate\n",
        menu_command=BotCommands.menu_commands[-1],
    ),
)

UNKNOWN_COMMAND = Reply(text=_("Sorry, I don't understand this command"),)

DECK_CREATED = Reply(
    text=_("Deck *{title}* was successfully created!"), parse_mode=MARKDOWN,
)

CARD_DELETED = Reply(text=_("The card was successfully deleted!"),)

CARD_ALREADY_DELETED = Reply(text=_("The card is already deleted"))

DECK_DELETED = Reply(
    text=_("Deck *{deck_title}* was successfully deleted!"), parse_mode=MARKDOWN,
)

DECK_RENAMED = Reply(
    text=_("Deck *{previous_deck_title}* was renamed to *{new_deck_title}*."),
    parse_mode=MARKDOWN,
)

DECK_NOT_FOUND = Reply(text=_("Sorry, but I can't find this deck.\n"),)

CHOOSE_DECK = Reply(text=_("Your decks:"),)

RATE_KNOWLEDGE = Reply(text=_("Please, estimate your knowledge level:"),)

MAIN_MENU = Reply(text=_("It's a start menu."),)

ADD_DECK = Reply(text=_("Do you want to create a new deck or add an existing one?"),)

CREATE_NEW_DECK = Reply(
    text=_("Send me a name to your deck.\n" "P.S. Remember that it should be unique.")
)

TOO_LONG_DECK_TITLE = Reply(text=_("Deck title is too long. Try to make it shorter."))

INCORRECT_CHARACTERS_IN_DECK_TITLE = Reply(
    text=_(
        "Deck title contains incorrect characters. Only latin letters, numbers "
        "and dash are allowed."
    )
)

DECK_TITLE_ALREADY_EXISTS = Reply(
    text=_("Deck with title *{title}* already exists. Come up with another name.")
)

DECK_MENU = Reply(text=_("Deck *{title}*"), parse_mode=MARKDOWN,)

DECK_IS_EMPTY = Reply(text=_("Deck *{title}* is empty"),)

CHOOSE_CARD_TYPE = Reply(
    text=_(
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
    text=_(
        'You chose card type *{}*.\n\nSend me a *question*, that should be on a card.'
    ),
    parse_mode=MARKDOWN,
)

NOTE_GAPS_FOR_TYPE_2 = Reply(
    text=_('\n\n' 'Remember that the question should contain gaps "*_*".'),
    parse_mode=MARKDOWN,
)

SEND_FACT = Reply(
    text=_('Send me the *fact*, that should be on this card.'), parse_mode=MARKDOWN,
)

FACT_CREATED = Reply(text=_('Your new card:\n\n' '{fact}'),)

SEND_EXACT_NUMBER_CORRECT_ANSWERS = Reply(
    text=_(
        'Send me {number} comma-separated correct answers to this question:\n\n'
        '{question}'
    )
)

SEND_CORRECT_ANSWERS = Reply(
    text=_('Send me comma-separated correct answers to this question:\n\n' '{question}')
)

SEND_WRONG_ANSWERS = Reply(
    text=_('Send me comma-separated wrong answers to this question:\n\n' '{question}')
)

SEND_CORRECT_ANSWER = Reply(
    text=_('Send me the correct answer to this question:\n\n' '{question}'),
)

THERE_ARE_NO_CORRECT_ANSWERS = Reply(text=_("There are no correct answers."),)

THERE_ARE_NO_WRONG_ANSWERS = Reply(text=_("There are no wrong answers."),)

INADEQUATE_CORRECT_ANSWER_SENT = Reply(
    text=_(
        'You are confusing me!\n\n'
        'Send me the correct answer to this question:\n\n'
        '{question}'
    ),
)

INADEQUATE_CORRECT_ANSWERS_SENT = Reply(
    text=_(
        'You are confusing me!\n\n'
        'Send me comma-separated correct answers to this question:\n\n'
        '{question}'
    ),
)

INADEQUATE_WRONG_ANSWERS_SENT = Reply(
    text=_(
        'You are confusing me!\n\n'
        'Send me comma-separated wrong answers to this question:\n\n'
        '{question}'
    ),
)

EDIT_CARD = Reply(
    text=_('What do you want to change in this card?\n\n' '{question}\n\n' '{answers}'),
)

EDIT_FACT = Reply(text=_("Do you want to change in this fact?\n\n" "{question}"))

EDIT_DECK = Reply(
    text=_("What do you want to change in the deck *{deck_title}*?"),
    parse_mode=MARKDOWN,
)

RENAME_DECK = Reply(
    text=_('Send me the name to the deck *{deck_title}*.'), parse_mode=MARKDOWN,
)

DELETE_DECK = Reply(
    text=_('Are you sure you want to delete deck *{title}*?'), parse_mode=MARKDOWN,
)

CORRECT_ANSWER_IS = Reply(text=_('Correct answer: '),)

CORRECT_ANSWERS_ARE = Reply(text=_('Correct answers: '),)

WRONG_ANSWERS_ARE = Reply(text=_('Wrong answers: '),)

USER_CHOSEN = Reply(text=_('Your choice:'),)

CORRECT_REPLIES = [
    Reply(text=_('Correct!')),
    Reply(text=_('Absolutely correct!')),
    Reply(text=_('Perfect!')),
    Reply(text=_('Well done!')),
    Reply(text=_('Excellent!')),
]

WRONG_REPLIES = [
    Reply(text=_('Wrong!')),
    Reply(text=_('Bad news, wrong!')),
    Reply(text=_('Sorry, incorrect!')),
]

QUESTION_TOO_LONG = Reply(
    text=_("Your question is too long.\n" "Try to make it shorter.")
)

CARD_CREATED = Reply(
    text=_(
        "The card of type {type} was successfully created:\n\n"
        "{question}\n\n"
        "Correct answers: {correct_answers}"
    )
)

CARD_WITH_CHOICE_CREATED = Reply(
    _(
        "The card of type {type} was successfully created:\n\n"
        "{question}\n\n"
        "Correct: {correct_answers}\n\n"
        "Wrong: {wrong_answers}"
    )
)

NO_GAPS_IN_TYPE_2 = Reply(
    text=_('Sorry, but a card of type *2* should contain gaps "*_*"')
)

INCORRECT_GAPS_NUMBER_IN_ANSWER = Reply(
    text=_("Sorry, but I need {expected} answers, whereas you gave me {actual}.")
)

CHANGE_LANGUAGE = Reply(text=_("Choose the language you want to set"))

LANGUAGE_WAS_CHANGED = Reply(text=_("The language was successfully changed!"))

TIP = Reply(text=_("Tip: "))

NO_TIPS = Reply(
    text=_(
        "Unfortunately, there are no tips for this question...\n"
        "I can show you the answer though"
    )
)

CONTEXT_FORGOTTEN = Reply(
    text=_("Unfortunately, the context of our dialogue is already forgotten...")
)

WTF_MESSAGES = [
    Reply(text=_('What do you mean?')),
    Reply(text=_('Please type /help and get the available commands')),
    Reply(text=_("Sorry, I can't understand")),
    Reply(text=_("Sorry, but I can't reply...\nBut I can help you learn something!")),
]
