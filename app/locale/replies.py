from app.settings import COMMANDS

START_REPLY = (
    "Hi, *{}*!\n"
    "I am gonna help you learn everything you've always wanted,\n"
    "no matter how hard it is!"
)

START_AGAIN = "Welcome back, *{}*!"

HELP_REPLY = (
    f"{COMMANDS['menu_commands'][-1]} - use this command to navigate\n"
)

UNKNOWN_COMMAND_REPLY = "Sorry, I don't understand this command"

NO_DECKS_REPLY = (
    "You don't have any decks yet!\n"
    "Maybe it's time to create one?"
)

DECKS_REPLY = 'Your decks:\n'

TOO_LONG_DECK_TITLE_REPLY = (
    'Sorry, this title is too long. \n' 'Try to choose a shorter one.'
)

USER_DECK_TITLE_NOT_UNIQUE_REPLY = (
    'Oops, you already have a deck called *{title}*. \n'
    'Please, choose another name or rename the existing deck.'
)

USER_DECK_CREATED_REPLY = 'Deck *{title}* was successfully created!'

NOTHING_TO_DELETE_MESSAGE = "Sorry, but there's nothing to delete."

CARD_DELETED_REPLY = "The card was successfully deleted!"

USER_DECK_DELETED_REPLY = "Deck *{deck_title}* was successfully deleted!"

USER_DECK_RENAMED_REPLY = (
    "Deck *{ex_deck_title}* was renamed to *{new_deck_title}*."
)

USER_DECK_WRONG_TITLE_FORMATTING_REPLY = (
    "A deck title can only contain these symbols:\n"
    "Uppercase or lowercase letters, digits, -, _."
)

DELETE_DECK_NONE_MESSAGE = (
    "Sorry, but you have no decks."
)

DELETE_DECK_NOT_FOUND_MESSAGE = (
    "Sorry, but I can't find this deck.\n"
    "Type /decks to see your decks"
)

USER_DECK_NOT_FOUND_REPLY = (
    "Sorry, but I can't find this deck.\n"
    'Type /decks to see your decks'
)

CARD_NO_TITLE_MESSAGE = 'Please, use this format:\n' '/card DECK_NAME'

CARD_TYPES_MESSAGE = (
    'Do it this way:\n'
    'CARD_TYPE. QUESTION\n\n'
    'Card types:\n'
    '0: a card with no answer, just some fact;\n'
    '1: a question-answer card;\n'
    '2: a card with gaps _ that you need to fill;\n'
    '3: a card with multiple choice.\n\n'
    "P.S. If it's a type 1 card you don't need to write a CARD_TYPE, just a QUESTION."
)

EMPTY_DECK_REPLY = (
    "Sorry, but there aren't any cards in this deck so far.\n" "Maybe it's time to add one?"
)

LEARN_NO_TITLE_MESSAGE = (
    'Please, use this format::\n' '/learn DECK_NAME'
)

NOTHING_TO_SHOW_MESSAGE = 'Sorry, I have nothing to show.'

CANCEL_MESSAGE = 'You last command was cancelled.'

NOTHING_TO_CANCEL_MESSAGE = 'Sorry, nothing to cancel.'

# NO_CORRECT_ANSWERS_MESSAGE = 'No correct answers to this question.\n' \
#                              'In this case you need to set type 0.'

UNEXPECTED_ERROR_REPLY = 'Something went wrong.\n' 'Try again.'

SHARE_MESSAGE = 'Well, now send me a deck name, it can contain letters of any case.'

PERMISSION_DENIED_MESSAGE = 'Sorry, permission denied.'

NO_PUBLIC_DECK_INSTANCE_MESSAGE = 'This deck cannot be updated.'

DECK_UPDATED_MESSAGE = 'The deck was successfully updated!'

DECK_UP_TO_DATE_MESSAGE = 'The deck is up to date.'

PUBLIC_DECK_NOT_FOUND_MESSAGE = 'Sorry, deck not found.'

ASK_PASSWORD_MESSAGE = (
    'This deck has a password. Type it to add this deck.'
)

JOIN_SET_TITLE_MESSAGE = (
    'OK. Please give this deck a name.\n'
    'Remember that it should be unique!'
)

PUBLIC_DECK_DELETED_MESSAGE = (
    'Sorry, but this deck no longer exists.'
)

HIRE_MESSAGE = (
    'OK, now send me a username that you want to give admin rights, for example,\n'
    '@durov'
)

FIRE_MESSAGE = (
    'OK, now send me a username that you want to disrank, for example,\n'
    '@durov'
)

CHOOSE_DECK_REPLY = 'Your decks:'

SET_KNOWLEDGE_REPLY = 'Please, estimate your knowledge level:'

CHOOSE_MANY_REPLY = (
    'Choose correct answers (if there are any) and press *Submit*:\n\n' 'Your answers:'
)

CHOOSE_ONE_REPLY = 'Choose one answer'

LEARN_REPLY = '/show - show correct answer\n' '/cancel - stop learning'

TOO_LATE_TO_SET_KNOWLEDGE_REPLY = "It's too late to set knowledge level."

TOO_LATE_TO_EDIT_REPLY = "It's too late to edit the card."

TOO_LATE_TO_ANSWER_REPLY = "It's too late to answer this question."

MENU_REPLY = "It's a start menu."

ADD_DECK_REPLY = 'Do you want to create a new deck or add an existing one?'

CREATE_NEW_DECK_REPLY = (
    'Send me a name to your deck.\n'
    'P.S. Remember that it should be unique.'
)

DECK_MENU_REPLY = "Deck *{}*"

CHOOSE_CARD_TYPE_REPLY = (
    'Choose type of a card that you want to add to "*{}*".\n\n'
    '0: a card with no answer, just some fact;\n'
    '1: a question-answer card;\n'
    '2: a card with gaps \\_ that you need to fill;\n'
    '3: a card with multiple choice;\n'
    '4: a card with only one correct answer.'
)

SEND_QUESTION_REPLY = (
    'You chose card type *{}*.\n\n'
    'Send me a *question*, that should be on a card.'
)

SEND_QUESTION_TYPE_2_REPLY = (
    'You chose card type *2*.\n\n'
    'Send me a *question*, that should be on a card.\n\n'
    'Remember that the question should contain gaps "*_*".'
)

SEND_FACT_REPLY = 'Send me the *fact*, that should be on this card.'

FACT_CREATED_REPLY = 'Your new card:\n\n' '{}'

SEND_ANSWERS_TYPE_1_REPLY = (
    'Send me possible answers to this question.\n\n' '{}'
)

SEND_ANSWERS_TYPE_2_REPLY = (
    'Send me {} comma-separated answers to this question.\n\n'
    '{}'
)

SEND_CORRECT_ANSWERS_REPLY = (
    'Send me comma-separated correct answers to this question:\n\n' '{}'
)

SEND_CORRECT_ANSWER_REPLY = 'Send me the correct answer to this question:\n\n' '{}'

SEND_WRONG_ANSWERS_REPLY = (
    'Send me comma-separated incorrect answers to this question:\n\n' '{}'
)

NO_CORRECT_ANSWERS_REPLY = 'There are no correct answers.'

NO_WRONG_ANSWERS_REPLY = 'There are no incorrect answers.'

INCORRECT_WRONG_ANSWERS_REPLY = (
    'You are confusing me!\n\n'
    'Send me comma-separated incorrect answers to this question:\n\n'
    '{}'
)

INCORRECT_CORRECT_ANSWERS_REPLY = (
    'You are confusing me!\n\n'
    'Send me comma-separated correct answers to this question:\n\n'
    '{}'
)

EDIT_CARD_REPLY = 'What do you want to change in this card?\n\n' '{}\n\n' '{}'

EDIT_USER_DECK_REPLY = 'What do you want to change in this deck *{deck_title}*?'

RENAME_USER_DECK_REPLY = (
    'Send me the name to the deck *{deck_title}*.'
)

DELETE_USER_DECK_REPLY = 'Are you sure you want to delete deck *{}*?'

CARD_REPLY = '{}\n\n' '{}'

CORRECT_ANSWER_IS_REPLY = 'Correct answer: '

CORRECT_ANSWERS_ARE_REPLY = 'Correct answers: '

USER_CHOSEN_REPLY = 'Your choice:'

CORRECT_REPLIES = [
    'Correct!',
    'Absolutely correct!',
    'Perfect!',
    'Well done!',
    'Excellent!',
]

WRONG_REPLIES = ['Wrong!', 'Bad news, wrong!', 'Sorry, incorrect!']

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

CARD_QUESTION_TOO_LONG_MESSAGE = (
    'Your question is too long.\n' 'Try to make it shorter.'
)

CARD_QUESTION_TYPE_0 = 'Well done! Here is your card:\n\n' 'QUESTION:\n' '{}'

CARD_QUESTION_TYPE_1 = (
    'Perfect, please send me semicolon-separated answers to this question.'
)

CARD_QUESTION_TYPE_2_NO_GAPS = (
    'On no!\n'
    'You chose a gap text question, so there have to be gaps _\n'
    "P.S. it's an underscore."
)

CARD_QUESTION_TYPE_2 = (
    'OK, I got it, now please send me {} answers separated with semicolon.'
)

CARD_QUESTION_TYPE_3 = (
    'Great, now please give me correct and wrong answers as follows:\n'
    '[correct_answer_1; correct_answer_2] [wrong_answer_1]\n'
    'P.S. You can leave one of the lists empty. But only one!'
)

CARD_QUESTION_NO_TYPE = 'Err, what? Please type /card_types if you need help in card editing.'

CARD_CREATED_REPLY = 'The card of type {type} was successfully created:\n\n' '{question}\n\n' '{correct_answers}'

CARD_WITH_CHOICE_CREATED_REPLY = (
    'The card of type {0} was successfully created:\n\n'
    '{1}\n\n'
    'Correct: {2}\n\n'
    'Wrong: {3}'
)

INCORRECT_GAPS_NUMBER_IN_QUESTION_REPLY = (
    'Sorry, but a card of type *2* should contain gaps "*_*"'
)

INCORRECT_GAPS_NUMBER_IN_ANSWER_REPLY = (
    'Sorry, but I need {} answers, whereas you gave me {}.'
)

CARD_TYPE_3_BRACKETS_NOT_MATCH_MESSAGE = (
    'Looks like your message has mistakes in "[" and "]" brackets.\n'
    'Please correct it and send your answers again.'
)

CARD_TYPE_3_NO_ANSWERS_MESSAGE = (
    "Sorry, but I couldn't get a single answer.\n"
    'Please check once more and send your answers again.'
)

ANSWER_INCORRECT_MESSAGE = (
    'Wrong\n' 'Try again, or type /show, to see the correct answer'
)

ANSWER_CORRECT_MESSAGES = ['Well done!', 'Correct!', 'Perfect!', 'Excellent!']

NO_SUCH_OPTION_MESSAGE = (
    "Sorry, either this variant doesn't exist or I didn't understand it.\n"
    "Send correct answers separated with semicolon, or 0 if there aren't any."
)

UNKNOWN_CARD_TYPE_MESSAGE = (
    "I don't know how to check a card of this type."
)

SET_KNOWLEDGE_MESSAGE = (
    'Now rate you knowledge level, send me a number:\n'
    "1 - I don't know\n"
    '2 - I know a little\n'
    '3 - I know it.\n\n'
    'Then I will give you the next card.'
)

INCORRECT_KNOWLEDGE_MESSAGE = (
    'Just give me the number:\n' "1 - I don't know\n" '2 - I know a little\n' '3 - I know it.'
)

KNOWLEDGE_OUT_OF_RANGE_MESSAGE = 'You can rate your knowledge level from 1 to 3.'

TOO_LONG_SLUG_MESSAGE = "This line is too long."

SLUG_NON_UNIQUE_MESSAGE = "This line is already used, try again."

PUBLIC_DECK_CREATED_MESSAGE = (
    'Great! Type this command to allow others to add this deck:\n'
    '/join {}'
)

USER_NOT_FOUND_MESSAGE = (
    'Sorry, but I cannot find this user.\n'
    'Are you sure they are registered?'
)

USERNAME_NOT_PARSED_MESSAGE = (
    'Check the spelling of a username, it should start with @.'
)

HIRED_IS_ADMIN_ALREADY_MESSAGE = 'This user is already an admin.'

HIRED_NOTIFY_MESSAGE = 'Congratulations! You were set as an admin of deck {}!'

USER_HIRED_MESSAGE = 'User @{} was set as an admin of deck {}.'

FIRED_IS_NOT_ADMIN_MESSAGE = 'This user is not an admin.'

FIRED_NOTIFY_MESSAGE = 'Sorry, but you were resigned from deck {}.'

USER_FIRED_MESSAGE = 'User @{} was resigned from deck {}.'

SELF_USERNAME_MESSAGE = "You can't perform this operation with yourself!"

WRONG_PASSWORD_MESSAGE = 'Wrong password, try again.'

PASSWORD_CHANGED_MESSAGE = (
    'Sorry, but the password was updated, do it again.'
)

ALREADY_JOINED_MESSAGE = 'You have already added this deck.'

JOIN_MESSAGE = 'You successfully added a deck {}.'

WTF_MESSAGES = [
    'What do you mean?',
    'Please type /help and get the available commands',
    "Sorry, I can't understand",
    "Sorry, but I can't reply...\n" 'But I can help you learn something!',
]
