from flask_babel import _

from app.settings import COMMANDS


START_REPLY = _(
    "Hi, *{}*!\n"
    "I am gonna help you learn everything you've always wanted,\n"
    "no matter how hard it is!"
)

START_AGAIN = _("Welcome back, *{}*!")

HELP_REPLY = _(
    "%(menu_command)s - use this command to navigate\n",
    menu_command=COMMANDS['menu_commands'][-1],
)

UNKNOWN_COMMAND_REPLY = _("Sorry, I don't understand this command")

USER_DECK_CREATED_REPLY = _("Deck *{title}* was successfully created!")

CARD_DELETED_REPLY = _("The card was successfully deleted!")

USER_DECK_DELETED_REPLY = _("Deck *{deck_title}* was successfully deleted!")

USER_DECK_RENAMED_REPLY = _("Deck *{ex_deck_title}* was renamed to *{new_deck_title}*.")

USER_DECK_NOT_FOUND_REPLY = _("Sorry, but I can't find this deck.\n")

CHOOSE_DECK_REPLY = _("Your decks:")

SET_KNOWLEDGE_REPLY = _("Please, estimate your knowledge level:")

MENU_REPLY = _("It's a start menu.")

ADD_DECK_REPLY = _("Do you want to create a new deck or add an existing one?")

CREATE_NEW_DECK_REPLY = _(
    "Send me a name to your deck.\n" "P.S. Remember that it should be unique."
)

DECK_MENU_REPLY = _("Deck *{}*")

CHOOSE_CARD_TYPE_REPLY = _(
    'Choose type of a card that you want to add to "*{}*".\n\n'
    '0: a card with no answer, just some fact;\n'
    '1: a question-answer card;\n'
    '2: a card with gaps \\_ that you need to fill;\n'
    '3: a card with multiple choice;\n'
    '4: a card with only one correct answer.'
)

SEND_QUESTION_REPLY = _(
    'You chose card type *{}*.\n\n' 'Send me a *question*, that should be on a card.'
)

NOTE_GAPS_FOR_TYPE_2_REPLY = _(
    '\n\n' 'Remember that the question should contain gaps "*_*".'
)

SEND_FACT_REPLY = _('Send me the *fact*, that should be on this card.')

FACT_CREATED_REPLY = _('Your new card:\n\n' '{}')

SEND_ANSWERS_TYPE_1_REPLY = _('Send me possible answers to this question.\n\n' '{}')

ALL_POSSIBLE = "all possible"

CORRECT_ANSWERS = "correct answers"

WRONG_ANSWERS = "wrong answers"

SEND_ANSWERS_REPLY = _('Send me {}comma-separated {} to this question:\n\n' '{}')

SEND_CORRECT_ANSWER_REPLY = _('Send me the correct answer to this question:\n\n' '{}')

THERE_ARE_NO_REPLY = _("There are no {}.")

INCORRECT_NUMBER_OF_REPLY = _(
    'You are confusing me!\n\n' 'Send me comma-separated {} to this question:\n\n' '{}'
)

EDIT_CARD_REPLY = _('What do you want to change in this card?\n\n' '{}\n\n' '{}')

EDIT_USER_DECK_REPLY = _("What do you want to change in the deck *{deck_title}*?")

RENAME_USER_DECK_REPLY = _('Send me the name to the deck *{deck_title}*.')

DELETE_USER_DECK_REPLY = _('Are you sure you want to delete deck *{}*?')

CORRECT_ANSWER_IS_REPLY = _('Correct answer: ')

CORRECT_ANSWERS_ARE_REPLY = _('Correct answers: ')

WRONG_ANSWERS_ARE_REPLY = _('Wrong answers: ')

USER_CHOSEN_REPLY = _('Your choice:')

CORRECT_REPLIES = [
    _('Correct!'),
    _('Absolutely correct!'),
    _('Perfect!'),
    _('Well done!'),
    _('Excellent!'),
]

WRONG_REPLIES = [
    _('Wrong!'),
    _('Bad news, wrong!'),
    _('Sorry, incorrect!'),
]

CARD_QUESTION_TOO_LONG_REPLY = _(
    "Your question is too long.\n" "Try to make it shorter."
)

CARD_CREATED_REPLY = _(
    "The card of type {type} was successfully created:\n\n"
    "{question}\n\n"
    "{correct_answers}"
)

CARD_WITH_CHOICE_CREATED_REPLY = _(
    "The card of type {type} was successfully created:\n\n"
    "{question}\n\n"
    "Correct: {correct_answers}\n\n"
    "Wrong: {wrong_answers}"
)

NO_GAPS_IN_TYPE_2_REPLY = _('Sorry, but a card of type *2* should contain gaps "*_*"')

INCORRECT_GAPS_NUMBER_IN_ANSWER_REPLY = _(
    "Sorry, but I need {expected} answers, whereas you gave me {actual}."
)

WTF_MESSAGES = [
    _('What do you mean?'),
    _('Please type /help and get the available commands'),
    _("Sorry, I can't understand"),
    _("Sorry, but I can't reply...\n" 'But I can help you learn something!'),
]
